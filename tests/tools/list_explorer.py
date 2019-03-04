# Examples of use:
#
# python list_explorer.py net-c.com
# python list_explorer.py laposte.net
# python list_explorer.py mail.com
# python list_explorer.py vivaldi.net
# python list_explorer.py yandex.ru

import os
import sys
from pprint import pprint, pformat
from typing import List, Tuple
import pickle

if len(sys.argv) != 2:
    print(f'ERROR: invalid number of arguments! ({len(sys.argv)})')
    print('')
    print('Usage: python list_explorer.py <name of the mailbox RAW dump>')
    sys.exit(1)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))
from dbeurive.imap.parser import ListMailbox

data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
isp = sys.argv[1]
raw_mb = os.path.join(data_path, f'{isp}-lst.raw')

with open(raw_mb, 'rb') as fd:
    raw = fd.read()

list_object: Tuple[str, List[bytes]] = pickle.loads(raw)

lst = []
r: bytes
for r in list_object:
    ListMailbox.reset()
    text = r.decode()

    print("================================================")
    print("FULL PARSING:")
    print(f'=> {pformat(r)} => {text}')
    if not ListMailbox.parse(text):
        print("Invalid text!")
        continue
    tokens = ListMailbox.get_tokens()
    pprint(tokens)

    print("\nSTRIPPED PARSING:")
    tokens = ListMailbox.get_tokens(True)
    pprint(tokens)
    lst.append(tokens)

print("\n\n=== END ===\n\n")
pprint(lst)





