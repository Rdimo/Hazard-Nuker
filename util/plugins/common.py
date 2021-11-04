# Hazard was proudly coded by Rdimo (https://github.com/Rdimo).
# Hazard Nuker under the GNU General Public Liscense v2 (1991).

import os, sys, platform, ctypes
from time import sleep

THIS_VERSION = "1.3.3"


def clear():
    system = platform.system()
    if system == 'Windows':
        os.system('cls')
    elif system == 'Linux':
        os.system('clear')
    else:
        print('\n')*120
    return


def setTitle(str):
    system = platform.system()
    if system == 'Windows':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{str} | Made By Rdimo#6969")
    else:
        os.system(f"\033]0;{str} | Made By Rdimo#6969\a")


def print_slow(str):
    for letter in str:
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.05)


def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers