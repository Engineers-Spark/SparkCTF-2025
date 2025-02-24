from pwn import *
from randcrack import RandCrack

host , port = "192.168.212.128" , 7000
io = remote(host,port)  # Connect to the server

rc = RandCrack()

print(io.recv().decode())

for i in range(624):
    io.sendline(b'1')
    io.recvuntil(b'number: ')
    number = io.recvline().strip().decode()
    print(number)
    rc.submit(int(number))

print(io.recv().decode())

for i in range(100):
    io.sendline(b'2')
    io.recv()
    next_number = rc.predict_randint(0,6969)
    print(next_number)
    io.sendline(str(next_number))
    print(io.recv().decode())
