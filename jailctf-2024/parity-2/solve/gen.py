#!/usr/bin/env python3

import builtins
import string
from itertools import pairwise


# checks if all characters in the given string alternate parity
def parity_alternates(s):
    parities = [v % 2 for v in s.encode()]
    return all(a != b for a, b in pairwise(parities))


def find_valid_attribs(dirresult):
    for name in dirresult:
        if parity_alternates(name.replace('_', '')):
            print(name)


odd, even = [], []

for i in range(128):
    if chr(i) not in string.printable:
        continue
    if i % 2:
        odd.append(chr(i))
    else:
        even.append(chr(i))

odd = ''.join(odd)
even = ''.join(even)

print(f'{even=}')
print(f'{odd=}')
print()

print('valid builtins:')
print()

print()
print('valid dunder methods on f:')
print()

f = lambda: None
find_valid_attribs(dir(f))

print()
print('valid dunder methods on f.__globals__:')
print()

find_valid_attribs(dir(f.__globals__))

print()
print('builtins:')
print()

find_valid_attribs(dir(builtins))

print()
print('open():')
print()

fp = open('flag.txt')

find_valid_attribs(dir(fp))
