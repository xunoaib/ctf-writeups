import os

import zbar
from PIL import Image


def split_image(image_path, rows, cols):
    img = Image.open(image_path)
    img_width, img_height = img.size
    subimg_width = img_width // cols
    subimg_height = img_height // rows
    subimages = []
    for row in range(rows):
        for col in range(cols):
            left = col * subimg_width
            upper = row * subimg_height
            right = (col + 1) * subimg_width
            lower = (row + 1) * subimg_height
            subimage = img.crop((left, upper, right, lower))
            subimages.append((row, col, subimage))
    return subimages


def decode_qr_code(subimage):
    grayscale_subimage = subimage.convert('L')
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    width, height = grayscale_subimage.size
    raw = grayscale_subimage.tobytes()
    zbar_image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(zbar_image)
    for symbol in zbar_image:
        if symbol.type == zbar.Symbol.QRCODE:
            return symbol.data
    return None


def process_subimages(subimages):
    if not os.path.exists('stage1'):
        os.makedirs('stage1')

    for row, col, subimg in subimages:
        qr_data = decode_qr_code(subimg)
        if qr_data:
            print(f"{(row, col)}: {qr_data}")
        else:
            print(f"{(row, col)}")
            subimg.save(f'stage1/subimage_{row}_{col}.bmp')


def main():
    image_path = '../qr_mosaic.bmp'
    rows = 25
    cols = 40
    subimages = split_image(image_path, rows, cols)
    process_subimages(subimages)


if __name__ == '__main__':
    main()
