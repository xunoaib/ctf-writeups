#!/usr/bin/env bash
python stage1.py > codes
python stage2.py >> codes
python stage3.py >> codes
steghide extract -sf ../qr_mosaic.bmp -p ''  --force

cat codes | grep : | python stage4.py
# steghide extract -sf patriotCTF.bmp -p hD72ifj7tE83n --force

zbarimg -q flag_qr_code.bmp
