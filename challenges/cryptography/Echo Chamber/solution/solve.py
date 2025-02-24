from Crypto.Cipher import AES
import os
from Crypto.Util.Padding import pad, unpad
from pwn import *

host , port = "127.0.0.1" , 1337
io = remote(host,port)


def decrypt(ciphertext):
    io.sendline(b"2")
    io.sendlineafter(b"Enter the ciphertext : ", (ciphertext.hex()).encode())
    if  "!" in io.recvline().strip().decode() : 
        return False
    return True

def encrypt_via_padding_oracle(plaintext):
    block_size = AES.block_size
    plaintext = pad(plaintext, block_size)
    blocks = [plaintext[i:i + block_size] for i in range(0, len(plaintext), block_size)]
    encrypted_blocks = []
    prev_cipher_block = bytearray(os.urandom(block_size))
    encrypted_blocks.append(bytes(prev_cipher_block))

    print(f"Initial IV: {prev_cipher_block.hex()}")

    for block in reversed(blocks):
        crafted_block = bytearray(block_size)
        intermediate_bytes = bytearray(block_size)

        for byte_index in range(block_size - 1, -1, -1):
            padding_value = block_size - byte_index
            for guess in range(256):
                crafted_block[byte_index] = guess
                temp_block = crafted_block[:]
                for i in range(byte_index + 1, block_size):
                    temp_block[i] = intermediate_bytes[i] ^ padding_value
                if decrypt(bytes(temp_block) + bytes(prev_cipher_block)):
                    intermediate_bytes[byte_index] = guess ^ padding_value
                    crafted_block[byte_index] = intermediate_bytes[byte_index] ^ block[byte_index]
                    break

        prev_cipher_block = bytes(crafted_block)
        encrypted_blocks.append(prev_cipher_block)
        print(f"Block crafted: {prev_cipher_block.hex()}")

    encrypted_blocks.reverse()
    final_ciphertext = b''.join(encrypted_blocks)
    print(f"Final ciphertext: {final_ciphertext.hex()}")
    return final_ciphertext

def main():
    plaintext = b"Spark is the best"
    ciphertext = encrypt_via_padding_oracle(plaintext)
    io.sendline(b"2")
    io.sendlineafter(b"Enter the ciphertext : ", (ciphertext.hex()).encode())
    io.recvuntil(b"Here is your flag : ")
    print(io.recvline().strip().decode())

if __name__ == "__main__":
    main()
    exit()