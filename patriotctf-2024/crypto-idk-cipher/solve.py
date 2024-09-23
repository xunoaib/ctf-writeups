#!/usr/bin/env python3

import base64

key = 'secretkey'
ciphertext_base64 = 'QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I='
ciphertext = ''.join([chr(b) for b in base64.b64decode(ciphertext_base64)])

flag1 = ''
flag2 = ''

for i in range(len(ciphertext) // 2):
    enc_p1 = ciphertext[2 * i]
    enc_p2 = ciphertext[2 * i + 1]

    flag1 += chr(ord(enc_p1) ^ ord(key[i % len(key)]))
    flag2 += chr(ord(enc_p2) ^ ord(key[i % len(key)]))

flag = ''.join(flag1 + flag2[::-1])
print("pctf{%s}" % flag)
