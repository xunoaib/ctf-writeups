# Let's Play [steg]Hide & Seek

## Description

Not much of a backstory here... there is an embedded flag in here somewhere, your job is to find it.

Author: David Morgan (r0m)

## Files

* [qr_mosaic.bmp](qr_mosaic.bmp)

## Solution

* [Solution](solve/)

1. I first split the image up into smaller tiles, one for each QR code, then used various image processing techniques to decode all 1000 QR codes from the mosaic. I struggled to find a reliable way to decode all of them in one go, so I used a multi-stage approach to decode as many as possible at a time, passing along any failed images to more customized scripts.

```
❯ python stage1.py > codes
❯ python stage2.py >> codes
❯ python stage3.py >> codes
```
2. I also ran steghide on the mosaic to reveal a hidden image: `patriotCTF.bmp`
```
❯ steghide extract -sf qr_mosaic.bmp -p ''
wrote extracted data to "patriotCTF.bmp".
```
3. I then ran steghide multiple times against that image, testing each of the 1000 decoded QR codes as a passphrase. One of them succeeded:
```
❯ cat codes | grep : | python stage4.py
Success! hD72ifj7tE83n
wrote extracted data to "flag_qr_code.bmp".
```
For reference, the underlying command used above was:
```
❯ steghide extract -sf patriotCTF.bmp -p hD72ifj7tE83n --force
```
4. Decode the final QR code:
```
❯ zbarimg -q flag_qr_code.bmp
QR-Code:PCTF{QR_M0s41c_St3g0_M4st3r}
```

## Flag

`PCTF{QR_M0s41c_St3g0_M4st3r}`
