#!/usr/bin/env python3

for line in open('flag.vcd'):
    if line.startswith('b') and '"' in line:
        b = line.split(' ')[0][1:]
        print(chr(int(b, 2)), end='')
print()
