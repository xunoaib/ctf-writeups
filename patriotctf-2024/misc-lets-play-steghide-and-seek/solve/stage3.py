import os
from collections import Counter

import zbar
from PIL import Image


def detect_background_color(image, border_size=7):
    width, height = image.size
    pixels = image.load()

    border_pixels = []
    for x in range(width):
        for y in range(border_size):
            border_pixels.append(pixels[x, y])  # Top border
            border_pixels.append(pixels[x, height - 1 - y])  # Bottom border
    for y in range(height):
        for x in range(border_size):
            border_pixels.append(pixels[x, y])  # Left border
            border_pixels.append(pixels[width - 1 - x, y])  # Right border

    most_common_color = Counter(border_pixels).most_common(1)[0][0]
    return most_common_color


def detect_foreground_color(image,
                            background_color,
                            border_size=7,
                            distance_threshold=40):
    width, height = image.size
    pixels = image.load()

    inside_pixels = []
    for x in range(border_size, width - border_size):
        for y in range(border_size, height - border_size):
            color = pixels[x, y]
            if color != background_color:
                bg_distance = sum(
                    abs(c1 - c2) for c1, c2 in zip(color, background_color))
                if bg_distance > distance_threshold:
                    inside_pixels.append(color)

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


def process_images(stage2_dir, stage3_dir):
    if not os.path.exists(stage3_dir):
        os.makedirs(stage3_dir)

    for filename in os.listdir(stage2_dir):
        if filename.endswith('.bmp'):
            row_col = filename.replace('subimage_', '').replace('.bmp',
                                                                '').split('_')
            row, col = int(row_col[0]), int(row_col[1])

            img_path = os.path.join(stage2_dir, filename)
            image = Image.open(img_path)

            background_color = detect_background_color(image)
            foreground_color = detect_foreground_color(image, background_color)

            if foreground_color is not None:
                processed_image = binarize_image(image, background_color,
                                                 foreground_color)

                qr_data = decode(processed_image)

                if qr_data:
                    print(f"{(row, col)}: {qr_data}")
                else:
                    print(rgb_to_hex(foreground_color),
                          rgb_to_hex(background_color))
                    print(f"{(row, col)}: none")
                    processed_image.save(os.path.join(stage3_dir, filename))
            else:
                print(f"{(row, col)}: Unable to detect foreground color")
                image.save(os.path.join(stage3_dir, filename))


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def main():
    stage2_dir = 'stage2'
    stage3_dir = 'stage3'
    process_images(stage2_dir, stage3_dir)


if __name__ == '__main__':
    main()
