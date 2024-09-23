#!/usr/bin/env python3


def encrypt(din):
    temp = (din & 0x3FF) << 2 ^ 0xA
    dout = (temp >> 2) & 0xFF
    return dout


def find_input_byte(target_dout):
    for din in range(256):
        if encrypt(din) == target_dout:
            return din
    return None


def decode_byte_string(encrypted_bytes):
    decoded_bytes = []
    for dout_byte in encrypted_bytes:
        din = find_input_byte(dout_byte)
        if din is not None:
            decoded_bytes.append(din)
        else:
            print(f"Failed to decode byte: {dout_byte}")
            return None
    return bytes(decoded_bytes)


# hex bytes extracted from the SVG
encrypted_bytes = bytes.fromhex(
    '52415644794a4270665d476c61707b72766b6d6c5d6b715d3163717b')

decoded = decode_byte_string(encrypted_bytes)
print(decoded.decode())
