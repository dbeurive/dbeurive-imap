import os
import sys
from pprint import pprint
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from dbeurive.imap.config import Config
from dbeurive.imap.client import Client

data_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
config_path_clear: str = os.path.join(data_path, 'isp.yaml')
config = Config.get_conf_from_file(config_path_clear)

# isp = 'yandex.ru'
# mailbox = '|INBOX'

isp = 'mail.com'
mailbox = '/INBOX'

client = Client(
    config.get_hostname(isp),
    config.get_port(isp),
    config.get_user_login(isp),
    config.get_user_password(isp),
    config.get_path_set(isp)
)

if not client.connect():
    print(f'ERROR! Cannot connect to the IMAP server {client.get_last_error()}')

if not client.login():
    print(f'ERROR! Cannot log to the IMAP server {client.get_last_error()}')

resp = client.select_mailbox()
pprint(resp)

emails = client.list_emails_ids()
pprint(emails)



