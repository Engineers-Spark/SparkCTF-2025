from Crypto.Util.number import *
from Crypto.Hash import MD5
from secret import FLAG , SECRET_KEY
import codecs

assert   (1 <= len(SECRET_KEY) <=69 )


def hash(msg):
    return MD5.new(SECRET_KEY + msg).hexdigest()

def banner():
    print("[+] Welcome to hashing contest")
    print("[+] Prove that you are worthy of the flag")

def choices():
    print("[+] 1. create an account")
    print("[+] 2. login to your account")
    print("[+] 3. exit")

def check(h1, h2):
    return h1 == h2

def main():
    
    banner()
    while True:
        choices()
        c = int(input("Enter your choice: "))
        if c == 1:
            username = input("Enter your username: ")
            if "admin" in username:
                print("[+] Invalid username")
                continue
            h = hash(username.encode())
            print(f"[+] Your hash is {h}")
        elif c == 2:
            username = input("Enter your username:")
            user_hash = input("Enter your account hash:")
            if "admin" in username:
                v_hash = hash(codecs.decode(username, 'unicode_escape').encode('latin1'))
                print(v_hash)
                if check(v_hash, user_hash):
                    print(f"[+] Welcome admin, here is your flag: {FLAG}")
                else:
                    print("[+] Invalid hash")
            else:
                print("[+] Welcome back user")
        elif c == 3:
            print("[+] Goodbye!")
            break
        else:
            print("[+] Invalid choice")

if __name__ == "__main__":
    main()