#!/usr/bin/env python

import pickle
import sys
from typing import List

if len(sys.argv) != 2:
    print('Usage: ./dump.py <file name>')
    sys.exit(1)

with open(sys.argv[1], 'rb') as fd:
    raw: bytes = fd.read()

o: List[bytes] = pickle.loads(raw)
assert(len(o) == 1)
print(o[0].decode())