#!/usr/bin/env python
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES


def solve():

    def neighbors(path: PathGroup):
        for d in ["E", "N", "NE", "NW", "S", "SE", "SW", "W"]:
            yield move(path, pos_in_dir(path, d))

    q = [starting_path]
    visited = {starting_path}

    while q:
        path = q.pop()
        for n in neighbors(path):
            if check_path(n) and n not in visited:
                q.append(n)
                visited.add(n)


class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(
            enc[AES.block_size:])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs -
                                                      len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class PathGroup:
    tiles = []
    current_cordinates = None
    path_history = []

    def __repr__(self):
        return "[X] {} -- {} \n".format(self.tiles, self.path_history)

    def __hash__(self):
        return hash(repr(self))


grid = [
    [
        "SPHINX",
        "urn",
        "vulture",
        "arch",
        "snake",
        "urn",
        "bug",
        "plant",
        "arch",
        "staff",
        "SPHINX",
    ],
    [
        "plant",
        "foot",
        "bug",
        "plant",
        "vulture",
        "foot",
        "staff",
        "vulture",
        "plant",
        "foot",
        "bug",
    ],
    [
        "arch",
        "staff",
        "urn",
        "Shrine",
        "Shrine",
        "Shrine",
        "plant",
        "bug",
        "staff",
        "urn",
        "arch",
    ],
    [
        "snake",
        "vulture",
        "foot",
        "Shrine",
        "Shrine",
        "Shrine",
        "urn",
        "snake",
        "vulture",
        "foot",
        "vulture",
    ],
    [
        "staff",
        "urn",
        "bug",
        "Shrine",
        "Shrine",
        "Shrine",
        "foot",
        "staff",
        "bug",
        "snake",
        "staff",
    ],
    [
        "snake",
        "plant",
        "bug",
        "urn",
        "foot",
        "vulture",
        "bug",
        "urn",
        "arch",
        "foot",
        "urn",
    ],
    [
        "SPHINX",
        "arch",
        "staff",
        "plant",
        "snake",
        "staff",
        "bug",
        "plant",
        "vulture",
        "snake",
        "SPHINX",
    ],
]


def pos_in_dir(path, choice):
    cur_tile = path.current_cordinates
    match choice:
        case "N":
            next_tile = (cur_tile[0] - 1, cur_tile[1])
        case "S":
            next_tile = (cur_tile[0] + 1, cur_tile[1])
        case "E":
            next_tile = (cur_tile[0], cur_tile[1] + 1)
        case "W":
            next_tile = (cur_tile[0], cur_tile[1] - 1)
        case "NE":
            next_tile = (cur_tile[0] - 1, cur_tile[1] + 1)
        case "NW":
            next_tile = (cur_tile[0] - 1, cur_tile[1] - 1)
        case "SE":
            next_tile = (cur_tile[0] + 1, cur_tile[1] + 1)
        case "SW":
            next_tile = (cur_tile[0] + 1, cur_tile[1] - 1)
        case _:
            print('invalid choice', choice)
            exit(-1)
    return next_tile


def try_get_tile(tile_tuple):
    try:
        return grid[tile_tuple[0]][tile_tuple[1]], (tile_tuple[0],
                                                    tile_tuple[1])
    except Exception as e:
        return None


# This is you at (3,10)!
starting_tile = (3, 10)
starting_path = PathGroup()
starting_path.tiles = ["vulture"]
starting_path.current_cordinates = starting_tile
starting_path.path_history = [starting_tile]


def move(path, tile):
    sub_path = PathGroup()
    sub_path.tiles.append(tile)
    sub_path.current_cordinates = tile
    sub_path.path_history = path.path_history.copy()
    sub_path.path_history.append(tile)
    return sub_path


def check_path(path):

    for tile in path.path_history:
        if tile[1] > 10 or tile[1] < 0:
            return False
        if tile[0] > 6 or tile[0] < 0:
            return False

    if path.current_cordinates == (3, 9):
        return False

    if try_get_tile(path.current_cordinates)[0] == "SPHINX":
        return False

    if len(set(path.path_history)) != len(path.path_history):
        return False

    for tile in path.path_history[:-1]:
        if try_get_tile(path.current_cordinates)[0] == try_get_tile(tile)[0]:
            return False

    if try_get_tile(path.current_cordinates)[0] != "Shrine" and len(
            set([x[1] for x in path.path_history])) != len(
                [x[1] for x in path.path_history]):
        return False

    if try_get_tile(path.current_cordinates)[0] == "Shrine":
        key = "".join([try_get_tile(x)[0] for x in path.path_history])
        enc_flag = b"FFxxg1OK5sykNlpDI+YF2cqF/tDem3LuWEZRR1bKmfVwzHsOkm+0O4wDxaM8MGFxUsiR7QOv/p904UiSBgyVkhD126VNlNqc8zNjSxgoOgs="
        obj = AESCipher(key)
        try:
            dec_flag = obj.decrypt(enc_flag)
            if "pctf" in dec_flag:
                print(dec_flag)
                exit(0)
        except Exception:
            pass

    return True


if __name__ == "__main__":
    solve()
