# Intro > No Leak

## Description

every crypto always has leaks...

## Files

* [main.py](main.py)

## Solution

* [solve.py](solve.py)

We're given the ciphertext, the length of a randomly generated (and unknown) key, and the XOR algorithm used to generate the ciphertext. The weakness comes from it reusing the same parts of the key to encode multiple characters in the flag. We also have some known plaintext (the flag format: `CodeVinciCTF{...}`) which we can use to reverse some parts of the key.

I used z3 to encode the constraints and some educated guessing to narrow down the final characters.

```python
from z3 import And, BitVec, Or, Solver, sat

# Convert ciphertext to bytes, and specify key length
ciphertext = bytes.fromhex(
    'b3f0716f4a94ef6a6d6ce2b908d52d53c64696af67477dcade387770829324f23852fe78aff3266b5780'
)
key_length = 18

flag_length = len(ciphertext)

# Create symbolic variables for the key and flag
key = [BitVec(f'k{i}', 8) for i in range(key_length)]
flag = [BitVec(f'f{i}', 8) for i in range(flag_length)]

solver = Solver()

# Add XOR relationships to knowledge base (flag ^ key = ciphertext)
for i in range(flag_length):
    solver.add(flag[i] ^ key[i % key_length] == ciphertext[i])

# Add known plaintext relationships
# ie: Flag is in the form: CodeVinciCTF{...}
prefix = 'CodeVinciCTF{'
for i, ch in enumerate(prefix):
    solver.add(flag[i] == ord(ch))
solver.add(flag[-1] == ord('}'))

# Add alphanumeric constraints to inner portion of flag
for c in flag[len(prefix):-1]:
    solver.add(
        Or(
            And(c >= ord('a'), c <= ord('z')),
            And(c >= ord('A'), c <= ord('Z')),
            And(c >= ord('0'), c <= ord('9')),
            And(c >= ord('_'), c <= ord('_')),
        ))

# The above constraints reveal with certainty some but not all flag characters:
#
#   CodeVinciCTF{?????f0rMa7_1s_4lW?????_l3aK}
#
# The '?'s are still ambiguous, meaning there are many different possible
# satisfying values for them. However, only one is the "expected" flag.

# We can make educated guesses about what the remaining characters might be.
# based on what we did find: "_____format is alw_____ leak",
# "4lW..." could be be "always":

solver.add(Or(flag[31] == ord('4'), flag[31] == ord('a'), flag[31] == ord('A')))
solver.add(Or(flag[32] == ord('y'), flag[32] == ord('Y')))
solver.add(Or(flag[33] == ord('s'), flag[33] == ord('S'), flag[33] == ord('5')))

# This constrains an earlier portion of the flag to: "fl...format", which
# might be "flag format":

solver.add(Or(flag[13] == ord('F'), flag[13] == ord('f')))
solver.add(Or(flag[14] == ord('l'), flag[14] == ord('l')))
solver.add(Or(flag[15] == ord('a'), flag[15] == ord('A'), flag[15] == ord('4')))
solver.add(Or(flag[16] == ord('g'), flag[16] == ord('G')))
solver.add(Or(flag[17] == ord('_'), flag[17] == ord('_')))

# This leaves us with two possible flags, the first of which is correct:

# CodeVinciCTF{Fl4g_f0rMa7_1s_4lWay5_a_l3aK}
# CodeVinciCTF{fl4g_f0rMa7_1s_4lWAy5_a_l3aK}

# Find all satisfying models
while solver.check() == sat:
    model = solver.model()
    recovered_flag = ''.join(chr(model[f].as_long()) for f in flag)
    print(recovered_flag)

    # Block the current solution
    solver.add(Or([f != model[f].as_long() for f in flag]))
```

## Flag

`CodeVinciCTF{Fl4g_f0rMa7_1s_4lWay5_a_l3aK}`
