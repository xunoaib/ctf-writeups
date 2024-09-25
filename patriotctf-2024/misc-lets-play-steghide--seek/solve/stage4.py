#!/usr/bin/env python3
import ast
import subprocess
import sys

d = {}

for line in sys.stdin:
    if ':' in line:
        key, val = line.split(':')
        d[ast.literal_eval(key)] = val.strip()

file_path = 'patriotCTF.bmp'
passphrases = d.values()

for passphrase in passphrases:
    command = [
        'steghide', 'extract', '-sf', file_path, '-p', passphrase, '--force'
    ]

    try:
        result = subprocess.run(command,
                                check=True,
                                capture_output=True,
                                text=True)
        print(f"Success! {passphrase}")
        print(result.stdout + result.stderr)
        exit(0)

    except subprocess.CalledProcessError as e:
        # print(f"Failed with passphrase: {passphrase}")
        # print(e.stderr)
        pass
