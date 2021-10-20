from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from urllib.parse import unquote_plus

driver = webdriver.Chrome()


class Program:
    def __init__(self, server, login, password, tribe, type, zast, zastepca, world):
        self.login = login
        self.type = type
        self.tribe = str(tribe)
        self.password = password
        self.zastepca = str(zastepca)
        self.counter = 0
        self.zast = int(zast)
        self.objs = []
        self.file_spis = "wojsko_spis.txt"
        self.file_spis_obrona = "wojsko_spis_obrona.txt"
        self.command_all = 0
        self.page = driver.get(server)
        self.list = []
        self.id_zastepcy = ""
        self.server = world
        self.dict = {
            0: self.save_to_file_defense,
            1: self.save_to_file_troops
        }
        self.tribe_files = "https://{}.plemiona.pl/map/tribe.txt".format(self.server)
        self.lines = self.download()
        self.zastepca_wywolaj(Ally)
        self.logging()
        self.dict[self.type](Ally)

        driver.quit()

    def zastepca_wywolaj(self, Ally):
        for line in self.lines:
            player = Ally(line)
            if player.name == self.zastepca:
                self.id_zastepcy = player.id
                break
        #print(self.id_zastepcy)

    def logging(self):
        login_box = driver.find_element_by_xpath('//*[@id="user"]')
        login_box.send_keys(self.login)
        password_box = driver.find_element_by_xpath('//*[@id="password"]')
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)
        time.sleep(0.7)
        driver.get("http://plemiona.pl/page/play/{}".format(self.server))
        if self.zast == 1:
            driver.get("https://{}.plemiona.pl/game.php?village=2386&screen=settings&mode=vacation".format(self.server))
            for i in range(2,5):
                print(driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table[3]/tbody/tr["+str(i)+"]/td[1]/a").text)
                if driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table[3]/tbody/tr["+str(i)+"]/td[1]/a").text == self.zastepca:
                    loguj = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[2]/table[3]/tbody/tr["+str(i)+"]/td[2]/a")
                    loguj.send_keys(Keys.RETURN)
                    driver.switch_to.window(driver.window_handles[1])
                    break

    def download(self):
        response = requests.get(self.tribe_files)
        print('fetching from {0} - [{1}]'.format(self.tribe_files, response.status_code))
        return [line for line in response.text.split('\n') if len(line) != 0]

    def save_to_file_troops(self, Ally):
        #f = open("wojsko.txt", "a")
        #f.truncate(0)
        bin = PrintInfo(0, 0, 0, self.file_spis)
        bin.clear()
        for line in self.lines:
            # try:
            instances = Ally(line)
            if str(instances.tag) == str(self.tribe): # poco 1619 nuppki 61 350 poco?.
                if self.zast==1:
                    driver.get("https://{}.plemiona.pl/game.php?screen=ally&mode=members_troops&player_id=".format(self.server) + str(
                        instances.id) + "&t=" + self.id_zastepcy)
                else:
                      driver.get("https://{}.plemiona.pl/game.php?screen=ally&mode=members_troops&player_id=".format(self.server) + instances.id)
                #driver.get("https://pl150.plemiona.pl/game.php?screen=ally&mode=members_troops&player_id=3362925&t=699740757")
              #  driver.get(
                  #  "https://pl150.plemiona.pl/game.php?screen=ally&mode=members_troops&player_id=9037821&t=699740757&village=55776")
                danes = [dane for dane in driver.find_element_by_class_name("table-responsive").text.split('\n') if
                         len(dane) != 0]
                # f.write(instances.name+ ";" )
                # print(" {} - {}".format(self.counter, instances.name, ))

                for dane in danes[2:]:
                   # print(dane)
                    data = Troops(dane)
                    self.list.append(
                        data.coordinates[1:8] + ";" + data.spear + ";" + data.sword + ";"
                        + data.axe + ";" + data.spy + ";" + data.light + ";" + data.heavy
                        + ";" + data.ram + ";" + data.catapult + ";" + data.nobel + ";" + data.command + ";"
                        + data.incoming)
                    if not data.command == '?':
                        self.command_all += int(data.command)
                obj = PrintInfo(instances.name, self.list, self.command_all, self.file_spis)
                obj.to_file()
                obj.to_file2()
                self.command_all = 0
                self.list = []
                # f.write(data.coordinates[1:8] + ";" + data.spear + ";" + data.sword + ";" + data.axe + ";"
                #  + data.spy + ";" + data.light + ";" + data.heavy
                #  + ";" + data.ram + ";" + data.catapult + ";" + data.nobel + ";" + data.command + ";"
                #    + data.incoming + "\n")
                # f.write( str(Print.command_all) + "\n")
        # except Exception:
        # print("{} - {} - No access; \n".format(self.counter, instances.name))
        # pass
        #f.close()

        pass

    def save_to_file_defense(self, Ally):
        bin = PrintInfo(0, 0, 0, self.file_spis_obrona)
        bin.clear()
        for line in self.lines:
            try:
                instances = Ally(line)
                if instances.tag == str(self.tribe):
                    if self.zast == 1:
                        driver.get(
                            "https://{}.plemiona.pl/game.php?screen=ally&mode=members_defense&player_id=".format(self.server) + str(
                                instances.id) + "&t=" + self.id_zastepcy)
                    else:
                        driver.get(
                            "https://.plemiona.pl/game.php?screen=ally&mode=members_defense&player_id=" + instances.id)
                    danes = [dane for dane in driver.find_element_by_class_name("table-responsive").text.split('\n') if
                             len(dane) != 0]
                    i = 0
                   # f.write(instances.name + "\n")
                    print(" {} - {}".format(self.counter, instances.name))
                    self.counter += 1
                    for dane in danes[1:]:
                        if len(dane) < 13:
                            pass
                        if i % 2 == 0:
                            data = UnitsDef(dane)
                            self.list.append(data.coordinates[1:8] + ";" + data.spear + ";" + data.sword + ";" + data.axe + ";"
                                    + data.spy + ";" + data.light + ";" + data.heavy
                                    + ";" + data.ram + ";" + data.catapult + ";" + data.nobel)
                        i += 1
                    obj = PrintInfo(instances.name, self.list, 0, self.file_spis_obrona)
                    obj.to_file()
                    self.list = []
            except Exception:
                print("{} - {} - No access ".format(self.counter, instances.name))
                pass
        self.counter = 0


class PrintInfo:
    def __init__(self, name, list, command_all, file_name_spis):
        self.name = name
        self.troops = []
        self.troops.append(list)
        self.commands = command_all
        self.filename_spis = file_name_spis
        self.filename_command = "wojsko_rozkazy.txt"

#nicki + spis wojsk
    def to_file(self):
        f = open(self.filename_spis, "a", encoding='utf-8')
       # f.write(self.name + "\n")
        for troop in self.troops[0]:
            f.write(self.name + ";" + troop + "\n")
        f.close()

#nicki graczy + ilosc rozkazow
    def to_file2(self):
        f = open(self.filename_command, "a", encoding='utf-8')
        f.write(self.name + ";" + str(self.commands) + "\n")
        f.close()

    def clear(self):
        f = open(self.filename_spis, "a", encoding='utf-8')
        f.truncate(0)
        f.close()
        if self.filename_spis == "wojsko_spis.txt":
            f = open(self.filename_command, "a")
            f.truncate(0)
            f.close()

class Ally:
    def __init__(self, line):
        parts = line.split(',')
        self.id = parts[0]
        self.name = unquote_plus(parts[1])
        self.tag = unquote_plus(parts[2])
        self.villagesCount = parts[3]
        self.points = parts[4]
        self.ranking = parts[5]


class UnitsDef:
    def __init__(self, dane):
        parts = dane.split(' ')
        self.coordinates = parts[-15]
        self.spear = parts[-11]
        self.sword = parts[-10]
        self.axe = parts[-9]
        self.spy = parts[-8]
        self.light = parts[-7]
        self.heavy = parts[-6]
        self.ram = parts[-5]
        self.catapult = parts[-4]
        self.nobel = parts[-3]


class Troops:
    def __init__(self, dane):
        parts = dane.split(' ')
        self.coordinates = parts[-14]
        self.spear = parts[-12]
        self.sword = parts[-11]
        self.axe = parts[-10]
        self.spy = parts[-9]
        self.light = parts[-8]
        self.heavy = parts[-7]
        self.ram = parts[-6]
        self.catapult = parts[-5]
        self.nobel = parts[-4]
        self.command = parts[-2]
        self.incoming = parts[-1]


tribe = {
    "nuppki":"61",
    "poco1":"1619",
    "poco2":"350",
    "sin":"70"
}
page = "http://plemiona.pl"
world = "pl150"
login = "x"
password = "x"
type = 1
zast = 1
zastepca = "bigsmoke."
tribe = "61"
plemie="61"
"""
login = input("Login: \n")
password = input("hasło: \n")
type = int(input("0 - Spis obrony: \n1 - Spis wojska z rozkazami: \n"))
zast = int(input("1 - Spis z zastepstwa\n0- Spis ze swojego konta: \n"))
if (zast ==  0):
    zastepca = ""
else:
    zastepca = input("Zastepca (nick jak w grze): ")
plemie = input("Podaj plemie (nuppki,poco1,poco2,sin): \n")
tribe = tribe[plemie]

"""
# 0: self.save_to_file_defensevvvvvvvvvvvvvvvvvvvvvvvvv,
# 1: self.save_to_file_troops
Run = Program(page, login, password, tribe, type, zast, zastepca, world)
