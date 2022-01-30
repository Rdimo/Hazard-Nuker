import requests
from colorama import Fore

from util.plugins.common import getheaders


def validateToken(token):
    # contact discord api and see if you can get a valid response with the given token
    r = requests.get('https://discord.com/api/v9/users/@me', headers=getheaders(token))
    if r.status_code == 200:
        # it is a valid token
        print(f"\n{Fore.RED}Valid token : {token}{Fore.RESET}")
        return True
    else:
        return False


def checkTokens(filename):
    valid = False
    with open(filename, "r") as f:
        lines = f.readlines()
    for i in lines:
        i = i.replace("\n", "")
        if validateToken(i):
            valid = True
    if not valid:
        print(f"{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}No Valid Tokens Found{Fore.RED}")
    input(f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Enter anything to continue . . .  {Fore.RED}')
