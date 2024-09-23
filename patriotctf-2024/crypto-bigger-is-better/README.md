# Bigger is Better

## Description

I heard choosing a small value for e when creating an RSA key pair is a bad idea. So I switched it up!

Author: Dylan (elbee3779)

## Files

* [dist.txt](dist.txt)

## Solution

- We're given `N` and `e` (parameters of an RSA public key), and `c` (the cipher message) as integers.
- Plugging these values into dcode.fr gives us the original plaintext: (https://www.dcode.fr/rsa-cipher)
- Now convert the plaintext from an integer to text:

```python
bytes.fromhex(f'{198573282289942360340715068182867171639965772069914565630203355812652530045:x}')
```
- Flag: `pctf{fun_w1th_l4tt1c3s_f039ab9}`
