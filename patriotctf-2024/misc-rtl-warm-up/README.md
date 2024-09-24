# RTL Warm up

## Description

Let's Warm up.
Spartan's wanted to create their own ASIC, to secure doors.
One of the spy was able to extract the simulation file,
can you find the password to the door?

Note: The spaces are _

Author: [Databuoy](https://databuoy.com/)

## Files

* [flag.vcd](flag.vcd)

## Solution

* [solve.py](solve.py)

Judging from the initial lines in `flag.vcd`, we can infer that `"` and `#` correspond to `dout` and `din`, respectively. Elsewhere, we see many 8-bit binary values apparently being read or written to them:

```
b01010000 "
b01010000 #
```

We can collect all of the output values (or all of the inputs), convert them to decimal, then convert those to ASCII to get the flag.

## Flag

`PCTF{RTL_i$_D@D_0F_H@rdw@r3}`
