# Hazard was proudly coded by Rdimo (https://github.com/Rdimo).
# Hazard Nuker under the GNU General Public Liscense v2 (1991).
#GCSpammer created by (https://github.com/RithDev).

import requests
import json
import Hazard
from colorama import Fore

from util.plugins.common import print_slow, getheaders

def GcSpammer(token, recipients):
    json = {
        "recipients": recipients
    }
    for i in range(10): # you change if you want but ratelimits are strict
        try:
            r = requests.post(f'https://discordapp.com/api/v9/users/@me/channels',
            headers=getheaders(token), json=json)
            print(f"{Fore.RED}Created GC"+Fore.RESET)
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")
    print_slow(f"{Fore.RED}Spammed recipients with groupchats ")
    print("Enter anything to continue. . . ", end="")
    input()
    Hazard.main()