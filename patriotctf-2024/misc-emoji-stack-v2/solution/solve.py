#!/usr/bin/env python3

from PIL import Image


def png_to_2d_list(path):
    with Image.open(path) as img:
        img = img.convert('L')
        pixel_values = list(img.getdata())
        width, height = img.size
        state = [
            pixel_values[i * width:(i + 1) * width] for i in range(height)
        ]
    return state


def emoji_to_decimal(emoji_str):
    emoji_to_value = {
        '🕛': 0,
        '🕐': 1,
        '🕑': 2,
        '🕒': 3,
        '🕓': 4,
        '🕔': 5,
        '🕕': 6,
        '🕖': 7,
        '🕗': 8,
        '🕘': 9,
        '🕙': 10,
        '🕚': 11,
    }

    decimal_value = 0
    base = 12

    for char in emoji_str:
        if char in emoji_to_value:
            decimal_value = decimal_value * base + emoji_to_value[char]
        else:
            raise ValueError(f"Invalid emoji '{char}' in input.")

    return decimal_value


def create_image_from_8bit_values(data, output_filename="flag.png"):
    height = len(data)
    width = len(data[0])
    img = Image.new('L', (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixels[x, y] = data[y][x]
    img.save(output_filename)
    print(f"Image saved as {output_filename}")


def create_lookup_tables(s):
    forward_lookup = {}
    reverse_lookup = {}

    positions_1 = [i for i, char in enumerate(s) if char == '🫸']
    positions_2 = [i for i, char in enumerate(s) if char == '🫷']

    for pos in positions_1:
        next_pos = s.find('🫷', pos + 1)
        if next_pos != -1:
            forward_lookup[pos] = next_pos

    for pos in positions_2:
        prev_pos = s.rfind('🫸', 0, pos)
        if prev_pos != -1:
            reverse_lookup[pos] = prev_pos

    return forward_lookup, reverse_lookup


def execute(i, x, y):
    c = prog[i]
    match c:
        case '👉':
            x += 1
        case '👈':
            x -= 1
        case '👆':
            y -= 1
        case '👇':
            y += 1
        case '🫸':
            if not stack[x][y]:
                i = forward_lookup[i]
        case '🫷':
            if stack[x][y]:
                i = reverse_lookup[i]
        case '👂':
            raise NotImplemented('ear')
        case '👍':
            stack[x][y] = min(stack[x][y] + 1, 255)
        case '👎':
            stack[x][y] = max(stack[x][y] - 1, 0)
        case '💬':
            print(chr(stack[x][y]), end='')
        case '🔁':
            encoded = prog[i + 1:i + 4]
            rep = emoji_to_decimal(encoded)
            if prog[i - 1] in ('🫷', '🫸'):
                raise Exception('bad repeat jump:', i)
            for _ in range(rep):
                _, x, y = execute(i - 1, x, y)
            i += 3
        case _:
            raise Exception(f'not implemented: {(c, i, x, y)}')
    i += 1
    return i, x, y


with open('program.txt') as f:
    prog = f.read()

forward_lookup, reverse_lookup = create_lookup_tables(prog)

stack = png_to_2d_list('initial_state.png')

x = y = 0
i = 0

while i < len(prog):
    i, x, y = execute(i, x, y)

create_image_from_8bit_values(stack)  # CACI{3M0J!==G00D!}
