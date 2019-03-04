import os
import sys
import pickle
from typing import List

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from dbeurive.imap.config import Config
from dbeurive.imap.client import Client

data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
config_path_clear: str = os.path.join(data_path, 'isp.yaml')
config = Config.get_conf_from_file(config_path_clear)

def dump_mailboxes(mailboxes: List[bytes], dir_path: str, file_name: str) -> bool:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, mode='wb') as fd:
        pickle.dump(mailboxes, fd)

isp: str
for isp in config.get_isps():
    hostname = config.get_hostname(isp)
    port = config.get_port(isp)
    username = config.get_user_login(isp)
    password = config.get_user_password(isp)

    print(f'Get mailboxes from "{isp}":\n\t"{hostname}:{port}\n\t{username}/{password}"')

    client = Client(hostname, port, username, password)
    if not client.connect():
        print(f'{isp}: cannot connect to {hostname}:{port}: {client._last_error}')
        continue
    if not client.login():
        print(f'{isp}: cannot login with {username}:{password}: {client._last_error}')
        continue
    mailboxes = client.get_raw_list_mailboxes()
    if mailboxes is None:
        print(f'{isp}: cannot get the list of mailboxes')
        continue
    p = f'{isp}-lst.raw'
    print(f'Save the list into the file "{p}"')
    dump_mailboxes(mailboxes, data_path, p)

