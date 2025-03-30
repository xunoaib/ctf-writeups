import string
from hashlib import sha256

with open('output.txt') as f:
    lines = f.read().strip().splitlines()

password = ''

for line in lines:
    for c in string.printable:
        if line == sha256((password + c).encode()).hexdigest():
            password += c
            break

print(password)
