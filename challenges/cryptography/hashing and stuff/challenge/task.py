from Crypto.Util.number import *
from Crypto.Hash import MD5
from secret import FLAG
import base64

text = """ 
 ▄████▄   ▒█████   ██▓     ██▓     ██▓  ██████  ██▓ ▒█████   ███▄    █         
▒██▀ ▀█  ▒██▒  ██▒▓██▒    ▓██▒    ▓██▒▒██    ▒ ▓██▒▒██▒  ██▒ ██ ▀█   █         
▒▓█    ▄ ▒██░  ██▒▒██░    ▒██░    ▒██▒░ ▓██▄   ▒██▒▒██░  ██▒▓██  ▀█ ██▒        
▒▓▓▄ ▄██▒▒██   ██░▒██░    ▒██░    ░██░  ▒   ██▒░██░▒██   ██░▓██▒  ▐▌██▒        
▒ ▓███▀ ░░ ████▓▒░░██████▒░██████▒░██░▒██████▒▒░██░░ ████▓▒░▒██░   ▓██░        
░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░▓  ░░ ▒░▓  ░░▓  ▒ ▒▓▒ ▒ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒         
  ░  ▒     ░ ▒ ▒░ ░ ░ ▒  ░░ ░ ▒  ░ ▒ ░░ ░▒  ░ ░ ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░        
░        ░ ░ ░ ▒    ░ ░     ░ ░    ▒ ░░  ░  ░   ▒ ░░ ░ ░ ▒     ░   ░ ░         
░ ░          ░ ░      ░  ░    ░  ░ ░        ░   ░      ░ ░           ░         
░                                                                              
  █████▒▒█████   ██▀███     ▄▄▄█████▓ ██░ ██ ▓█████     █     █░ ██▓ ███▄    █ 
▓██   ▒▒██▒  ██▒▓██ ▒ ██▒   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀    ▓█░ █ ░█░▓██▒ ██ ▀█   █ 
▒████ ░▒██░  ██▒▓██ ░▄█ ▒   ▒ ▓██░ ▒░▒██▀▀██░▒███      ▒█░ █ ░█ ▒██▒▓██  ▀█ ██▒
░▓█▒  ░▒██   ██░▒██▀▀█▄     ░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄    ░█░ █ ░█ ░██░▓██▒  ▐▌██▒
░▒█░   ░ ████▓▒░░██▓ ▒██▒     ▒██▒ ░ ░▓█▒░██▓░▒████▒   ░░██▒██▓ ░██░▒██░   ▓██░
 ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░     ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░   ░ ▓░▒ ▒  ░▓  ░ ▒░   ▒ ▒ 
 ░       ░ ▒ ▒░   ░▒ ░ ▒░       ░     ▒ ░▒░ ░ ░ ░  ░     ▒ ░ ░   ▒ ░░ ░░   ░ ▒░
 ░ ░   ░ ░ ░ ▒    ░░   ░      ░       ░  ░░ ░   ░        ░   ░   ▒ ░   ░   ░ ░ 
           ░ ░     ░                  ░  ░  ░   ░  ░       ░     ░           ░ 
"""

def banner():
    for i in text.split("\n"):
        print(i)

def get_flag(ms1 , msg2):
    if MD5.new(ms1).hexdigest() == MD5.new(msg2).hexdigest():
        print("[-] You are not allowed to get the flag")
        print(FLAG.decode())
        exit(1)
    else:
        print('[!] hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm try again')

def choices():
    print('1. add msg')
    print('2. get the flag')
    print('3. exit')



def main():
    banner()
    while True:
        choices()
        c = int(input("Enter your choice: "))
        if c == 1:
            msg1 = base64.b64decode(input("Enter your msg: "))
            msg2 = base64.b64decode(input("Enter your msg: "))
            if msg1 == msg2:
                print('[-] msg1 == msg2')
                print('[-] try again')
                continue
        elif c == 2:
            get_flag(msg1 , msg2)
        elif c == 3:
            exit(1)
        else:
            print("[+] Invalid choice")

if __name__ == '__main__':
    main()


