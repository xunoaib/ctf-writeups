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

Judging from the initial lines in `flag.vcd`, we see that `"` and `#` correspond to `dout` and `din`. Elsewhere, we see many 8-bit binary values being passed between them:

```
b01010000 "
b01010000 #
```

By converting each of the 8-bit binary output values to the corresponding ASCII character, we can reconstruct the flag.

## Flag

`PCTF{RTL_i$_D@D_0F_H@rdw@r3}`
