import unittest
import os
import sys
import re
from typing import Tuple, List, Mapping
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

from dbeurive.imap.client import Client

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
mailboxes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'mailboxes')
emails_ids_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'emails-ids')

class TestClient(unittest.TestCase):

    @staticmethod
    def get_mailboxes_lst_raw_files() -> Mapping[str, str]:
        files = {}
        r = re.compile('^(.+)\-lst\.raw$')
        for entry in os.listdir(mailboxes_path):
            p = os.path.join(mailboxes_path, entry)
            if not os.path.isfile(p):
                continue
            m = r.match(entry)
            # noinspection PyUnusedLocal
            isp_name: str = None
            if m is not None:
                isp_name = m.group(1)
                files[isp_name] = p
        return files

    @staticmethod
    def get_emails_ids_raw_files() -> Mapping[str, str]:
        files = {}
        r = re.compile('^(.+)\-ids\.raw$')
        for entry in os.listdir(emails_ids_path):
            p = os.path.join(emails_ids_path, entry)
            if not os.path.isfile(p):
                continue
            m = r.match(entry)
            # noinspection PyUnusedLocal
            isp_name: str = None
            if m is not None:
                isp_name = m.group(1)
                files[isp_name] = p
        return files

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
        test_set = __class__.get_mailboxes_lst_raw_files()
        for isp in test_set.items():
            name: str = isp[0]
            path_input: str = isp[1]
            with open(os.path.join(mailboxes_path, path_input), 'rb') as fd:
                mailboxes_bin = fd.read()
            list_object: List[bytes] = pickle.loads(mailboxes_bin)
            mailboxes = Client._list(list_object)
            expected_list = expected[name]
            self.assertEqual(expected_list, mailboxes)

    def test_list_mailboxes_empty(self):
        self.assertEqual([], Client._list([None]))

    def test_list_emails_ids(self):
        expected = {
            'laposte.net': ['1'],
            'mail.com': ['1', '2', '3', '4', '5', '6', '7', '8'],
            'net-c.com': ['1', '2'],
            'vivaldi.net': ['1'],
            'yandex.ru': ['1', '2', '3']
        }

        test_set = __class__.get_emails_ids_raw_files()

        for isp in test_set.items():
            name: str = isp[0]
            path_input: str = isp[1]
            with open(os.path.join(emails_ids_path, path_input), 'rb') as fd:
                emails_ids_bin = fd.read()
            list_object: List[bytes] = pickle.loads(emails_ids_bin)
            emails = Client._search(list_object)
            self.assertEqual(expected[name], emails)

