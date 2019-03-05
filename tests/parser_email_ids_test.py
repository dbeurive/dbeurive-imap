import unittest
import os
import sys
from typing import Dict, Tuple, List
from pprint import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
from dbeurive.imap.parser import ListEmailIds

class TestParser(unittest.TestCase):

    def test_parse1(self):

        tests = {
            '1 2 3': {
                'raw': [(ListEmailIds.TYPE_ID, '1'), (ListEmailIds.TYPE_ID, '2'), (ListEmailIds.TYPE_ID, '3')],
                'txt': ['1', '2', '3']
            },
            ' 1 2 3 ': {
                'raw': [(ListEmailIds.TYPE_ID, '1'), (ListEmailIds.TYPE_ID, '2'), (ListEmailIds.TYPE_ID, '3')],
                'txt': ['1', '2', '3']
            }
        }

        # noinspection PyUnusedLocal
        list_of_ids: str
        # noinspection PyUnusedLocal
        expected: Dict[str, List[Tuple[int, str]]]
        for list_of_ids, expected in tests.items():
            ListEmailIds.reset()
            ListEmailIds.parse(list_of_ids)
            self.assertEqual(ListEmailIds.get_tokens(), expected['raw'])
            self.assertEqual(ListEmailIds.get_tokens_values(), expected['txt'])

