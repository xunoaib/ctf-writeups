#!/usr/bin/env python3

with open('input.txt') as f:
    prog = f.read()


def execute(i, p):
    c = prog[i]
    match c:
        case '👉':
            p += 1
        case '👈':
            p -= 1
        case '👍':
            stack[p] += 1
        case '👎':
            stack[p] -= 1
        case '💬':
            print(chr(stack[p]), end='')
        case '🔁':
            rep = int(prog[i + 1:i + 3], 16)
            for _ in range(rep):
                _, p = execute(i - 1, p)
            i += 2
    i += 1
    return i, p


stack = [0] * 256
p = 0
i = 0

while i < len(prog):
    i, p = execute(i, p)

print()
