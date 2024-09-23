# patriotCTF 24: `Let's Play [steg]Hide & Seek`
1. I used various image processing techniques to decode all 1000 QR codes from the mosaic. Because it was difficult to decode them all in one go, I used a multi-stage approach to decode as many as possible at a time, passing along any failed images to more customized scripts:
```
❯ python stage1.py > codes
❯ python stage2.py >> codes
❯ python stage3.py >> codes
```
2. Running steghide on the mosaic without a passphrase also revealed a hidden image (`patriotCTF.bmp`):
```
❯ steghide extract -sf qr_mosaic.bmp -p ''
wrote extracted data to "patriotCTF.bmp".
```
3. Try running steghide on `patriotCTF.bmp`, using each of the 1000 decoded QR codes as the passphrase. One of them succeeds:
```
❯ cat codes | grep : | python stage4.py
Success! hD72ifj7tE83n
wrote extracted data to "flag_qr_code.bmp".
```
The underlying command used above:
```
❯ steghide extract -sf patriotCTF.bmp -p hD72ifj7tE83n --force
```
4. Decode the final QR code:
```
❯ zbarimg -q flag_qr_code.bmp
QR-Code:PCTF{QR_M0s41c_St3g0_M4st3r}
```
