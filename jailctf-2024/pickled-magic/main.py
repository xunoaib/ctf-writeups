#!/usr/local/bin/python3
# modified from https://github.com/splitline/My-CTF-Challenges/blob/master/hitcon-quals/2022/misc/Picklection/release/share/chal.py
import io
import pickle
from pickle import _getattribute

import numpy


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        print((module, name))
        if module == 'numpy' and '__' not in name:
            return _getattribute(numpy, name)[0]
        raise pickle.UnpicklingError('bad')


data = bytes.fromhex(input("(hex)> "))
print(RestrictedUnpickler(io.BytesIO(data)).load())


