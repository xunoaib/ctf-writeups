# Phase One

## Description

We had one of our agents infiltrate an adversary's lab and  photograph a gateway device that can get us access to their network. We need to develop an exploit as soon as possible. Attached is a picture of the device. Get us intel on what MCU the device is utilizing so we can continue with our research.

**Flag format: pctf{mcu_vendor_name} (example: pctf{broadcom}**

Author: Dylan (elbee3779)



## Files

* [target_product.jpg](target_product.jpg)

## Solution

Depending on the type of the device, hardware manufacturers in the U.S. must register their products with the FCC and provide detailed information which is also made publicly accessible.

- Perform an FCC product lookup using Google Dorks: `dlink dsl 6300v site:fccid.io`, which leads us to [this page](https://fccid.io/KA2SL6300VA1/User-Manual/User-Manual-1452587).
- Click on [Internal Photos](https://fccid.io/KA2SL6300VA1/Internal-Photos/Internal-Photos-1452582) to view a photo of the circuit board, revealing a large chip with `ikanos` branding.

## Flag

`pctf{ikanos}`
