import os
import sys
import pickle
from typing import List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from dbeurive.imap.config import Config
from dbeurive.imap.client import Client

data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
config_path_clear: str = os.path.join(data_path, 'isp.yaml')
config = Config.get_conf_from_file(config_path_clear)

def dump_emails_ids(emails_ids: Tuple[str, List[bytes]], dir_path: str, file_name: str) -> bool:
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, mode='wb') as fd:
        pickle.dump(emails_ids, fd)

isp: str
for isp in config.get_isps():
    hostname = config.get_hostname(isp)
    port = config.get_port(isp)
    username = config.get_user_login(isp)
    password = config.get_user_password(isp)

    print(f'Get emails list IDs from "{isp}":\n\t"{hostname}:{port}\n\t{username}/{password}"')

    client = Client(hostname, port, username, password)
    if not client.connect():
        print(f'{isp}: cannot connect to {hostname}:{port}: {client.get_last_error()}')
        continue
    if not client.login():
        print(f'{isp}: cannot login with {username}:{password}: {client.get_last_error()}')
        continue

    try:
        client.select_mailbox()
        emails_ids = client.get_raw_emails_ids()
    # noinspection PyBroadException
    except Exception as e:
        print(f"ERROR {isp} ! {e}")
        continue

    p = f'{isp}-ids.raw'
    print(f'Save the list into the file "{p}"')

    dump_emails_ids(emails_ids, data_path, p)
