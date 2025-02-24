import randfacts
from secret import FLAG , KEY 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os 



def encrypt(plaintext : str):
    iv = os.urandom(AES.block_size)  # Random IV
    cipher = AES.new(KEY, AES.MODE_CBC , iv=iv)
    ciphertext = iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext


def decrypt(ciphertext):
    cipher = AES.new(KEY, AES.MODE_CBC, ciphertext[:16]) 
    try:
        plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
        return plaintext
    except ValueError:
        return "[!] Invalid Padding"
    
def generate_fact():
    return randfacts.getFact()

def banner():
    print("[x] Welcome to the Random Facts Server")
    print("[x] We provide random facts to our users")
    print("[x] We also provide a flag to our users but only if they prove their worth")

def options():
    print("[+] Choose an option :")
    print("[+] 1. Get a random encrypted fact")
    print("[+] 2. decrypt")
    print("[+] 3. Exit")

def main():
    print(banner())
    while True:
        options()
        choice = int(input("Enter your choice : "))
        if choice == 1:
            fact = generate_fact()
            print("Encrypted Fact : ",encrypt(fact).hex())
        elif choice == 2:
            ciphertext = input("Enter the ciphertext : ")
            dec = decrypt(bytes.fromhex(ciphertext))
            print(dec)
            if dec == b"Spark is the best":
                print(f"Here is your flag : {FLAG.decode()}")
        elif choice == 3:
            print("[+] Goodbye")
            exit(1)
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
    exit()