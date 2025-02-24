from Crypto.Util.number import *
from secret import FLAG



def gen_key():
    p = getPrime(512)
    q = getPrime(512)
    n = p*q
    e = 65537
    phi = (p-1)*(q-1)
    d = inverse(e,phi)
    return n,e,d

def encrypt(m,e,n):
    return pow(m,e,n)


def parse(f):
    return [f[i:i+2] for i in range(0,len(f),2)]


def main():
    n,e,d = gen_key()
    parts = (parse(FLAG))
    enc = [encrypt(bytes_to_long(p),e,n) for p in parts]
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"enc = {enc}")


if __name__ == "__main__":
    main()
