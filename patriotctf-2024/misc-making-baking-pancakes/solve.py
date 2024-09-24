#!/usr/bin/env python3
from base64 import b64decode

from pwn import remote

r = remote('chal.pctf.competitivecyber.club', 9001)

for i in range(1000):
    print('Challenge', i)
    r.recvuntil(b'Challenge: ')
    data = r.recvuntil(b'\n')
    dec, n = b64decode(data).split(b'|')
    for _ in range(int(n)):
        dec = b64decode(dec)
    r.sendline(dec + f'|{i}'.encode())

print(r.recvall().decode())
