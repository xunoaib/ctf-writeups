import os
from collections import Counter

import zbar
from PIL import Image


def detect_background_color(image, border_size=7):
    width, height = image.size
    pixels = image.load()

    # Collect colors from the 7-pixel-wide border
    border_pixels = []
    for x in range(width):
        for y in range(border_size):
            border_pixels.append(pixels[x, y])  # Top border
            border_pixels.append(pixels[x, height - 1 - y])  # Bottom border
    for y in range(height):
        for x in range(border_size):
            border_pixels.append(pixels[x, y])  # Left border
            border_pixels.append(pixels[width - 1 - x, y])  # Right border

    # Find the most common color in the border
    most_common_color = Counter(border_pixels).most_common(1)[0][0]
    return most_common_color


def detect_foreground_color(image, background_color, border_size=7):
    width, height = image.size
    pixels = image.load()

    # Collect colors excluding the border
    inside_pixels = []
    for x in range(border_size, width - border_size):
        for y in range(border_size, height - border_size):
            color = pixels[x, y]
            if color != background_color:  # Ignore the background color
                inside_pixels.append(color)

    # Find the most common color that is not the background
    if inside_pixels:
        most_common_color = Counter(inside_pixels).most_common(1)[0][0]
        return most_common_color
    return None


def binarize_image(image, background_color, foreground_color):
    grayscale = image.convert('L')
    width, height = grayscale.size
    pixels = grayscale.load()

    for x in range(width):
        for y in range(height):
            original_color = image.getpixel((x, y))
            if original_color == background_color:
                pixels[x, y] = 255  # Map background to white
            elif original_color == foreground_color:
                pixels[x, y] = 0  # Map foreground to black
            else:
                # If the color doesn't perfectly match, choose based on proximity
                bg_distance = sum(
                    abs(c1 - c2)
                    for c1, c2 in zip(original_color, background_color))
                fg_distance = sum(
                    abs(c1 - c2)
                    for c1, c2 in zip(original_color, foreground_color))
                pixels[x, y] = 0 if fg_distance < bg_distance else 255

    return grayscale


def decode(image_data):
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    width, height = image_data.size
    raw = image_data.tobytes()
    zbar_image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(zbar_image)
    for symbol in zbar_image:
        if symbol.type == zbar.Symbol.QRCODE:
            return symbol.data
    return None


def process_images(stage1_dir, stage2_dir):
    if not os.path.exists(stage2_dir):
        os.makedirs(stage2_dir)

    for filename in os.listdir(stage1_dir):
        if filename.endswith('.bmp'):
            row_col = filename.replace('subimage_', '').replace('.bmp',
                                                                '').split('_')
            row, col = int(row_col[0]), int(row_col[1])

            img_path = os.path.join(stage1_dir, filename)
            image = Image.open(img_path)

            # Detect background and foreground colors
            background_color = detect_background_color(image)
            foreground_color = detect_foreground_color(image, background_color)

            if foreground_color is not None:
                # Binarize the image based on detected colors
                processed_image = binarize_image(image, background_color,
                                                 foreground_color)

                # Try to decode the QR code
                qr_data = decode(processed_image)

                if qr_data:
                    print(f"{(row, col)}: {qr_data}")
                else:
                    print(f"{(row, col)}")
                    image.save(os.path.join(stage2_dir, filename))
            else:
                print(f"{(row, col)}: Unable to detect foreground color")
                image.save(os.path.join(stage2_dir, filename))


def main():
    stage1_dir = 'stage1'
    stage2_dir = 'stage2'
    process_images(stage1_dir, stage2_dir)


if __name__ == '__main__':
    main()
