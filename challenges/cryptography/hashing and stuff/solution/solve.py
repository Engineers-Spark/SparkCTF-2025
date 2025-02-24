from pwn import *
import base64

host , port =  '172.27.126.227' , 1337

io = remote(host, port)

with open('fastcoll/msg1.bin', 'rb') as f:
   msg1 = (f.read())

with open('fastcoll/msg2.bin', 'rb') as f:
   msg2 = (f.read())



print(io.recv().decode())
io.sendline(b'1')
print(io.recv().decode())
io.sendline(base64.b64encode(msg1))
print(io.recv().decode())
io.sendline(base64.b64encode(msg1))
print(io.recv().decode())
io.sendline(b'2')
print(io.recv().decode())