import unittest
import os
import sys
import re
from typing import Tuple, List, Mapping
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

from dbeurive.imap.client import Client

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class TestClient(unittest.TestCase):

    @staticmethod
    def get_lst_raws() -> Mapping[str, str]:
        files = {}
        r = re.compile('^(.+)\-lst-fix\.raw$')
        for entry in os.listdir(data_path):
            p = os.path.join(data_path, entry)
            if not os.path.isfile(p):
                continue
            m = r.match(entry)
            # noinspection PyUnusedLocal
            isp_name: str = None
            if m is not None:
                isp_name = m.group(1)
                files[isp_name] = p
        return files

    # [b'(\\HasNoChildren) "/" "Chats"',
    #  b'(\\HasNoChildren) "/" "Contacts"',
    #  b'(\\HasNoChildren) "/" "Drafts"',
    #  b'(\\HasNoChildren) "/" "Emailed Contacts"',
    #  b'(\\HasNoChildren) "/" "INBOX"',
    #  b'(\\NoInferiors) "/" "Junk"',
    #  b'(\\HasNoChildren) "/" "Sent"',
    #  b'(\\HasNoChildren) "/" "Trash"']

    def test_list_mailboxes(self):

        expected = {
            'net-c.com': [
                ['/', 'inbox'],
                ['/', 'sent'],
                ['/', 'trash'],
                ['/', 'draftbox'],
                ['/', 'unsolbox'],
                ['/', 'newsletter'],
                ['/', 'social'],
                ['/', 'register'],
                ['/', 'ecard']
            ],
            'laposte.net': [
                ["/", "Chats"],
                ["/", "Contacts"],
                ["/", "Drafts"],
                ["/", "Emailed Contacts"],
                ["/", "INBOX"],
                ["/", "Junk"],
                ["/", "Sent"],
                ["/", "Trash"]
            ],
            'mail.com' : [
                ['/', 'Drafts'],
                ['/', 'INBOX'],
                ['/', 'OUTBOX'],
                ['/', 'Sent'],
                ['/', 'Spam'],
                ['/', 'Trash']
            ],
            'vivaldi.net': [
                ['.', 'Trash'],
                ['.', 'Junk'],
                ['.', 'Sent'],
                ['.', 'Drafts'],
                ['.', 'INBOX']
            ],
            'yandex.ru': [
                ['|', 'Drafts'],
                ['|', 'INBOX'],
                ['|', 'Outbox'],
                ['|', 'Sent'],
                ['|', 'Spam'],
                ['|', 'Trash']
            ]
        }

        test_set = __class__.get_lst_raws()

        for isp in test_set.items():
            name = isp[0]
            path_input = isp[1]
            with open(os.path.join(data_path, path_input), 'rb') as fd:
                mailboxes_bin = fd.read()
            list_object: List[bytes] = pickle.loads(mailboxes_bin)
            mailboxes = Client._list(list_object)
            expected_list = expected[name]
            self.assertEqual(expected_list, mailboxes)

    def test_list_mailboxes_empty(self):
        self.assertEqual([], Client._list([None]))

