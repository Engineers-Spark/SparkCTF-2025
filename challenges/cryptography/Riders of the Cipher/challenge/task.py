from Crypto.Util.number import *
from secret import flag

def gen_key():
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    e = 65537
    return n , e

def encrypt(message, e, n):
    return [pow(ord(c) , e , n) for c in message]


def main():
    n , e = gen_key()
    encrypted = encrypt(flag , e , n)
    encrypted = "\n".join([str(c) for c in encrypted])

    with open("output.txt", 'w+') as f:
        f.write(encrypted)
        
if __name__ == "__main__":
    main()
