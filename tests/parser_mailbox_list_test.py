import unittest
import os
import sys
from typing import Tuple, List, Union

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
from dbeurive.imap.parser import ListMailbox

class TestParser(unittest.TestCase):

    # ------------------------------------------------------------------
    # Testing the low level methods that extracts tokens from the
    # beginning of a text.
    # ------------------------------------------------------------------

    def test_empty_cme(self):
        test_set = (
            ('() ...',    ('', len('()'))),
            ('"/" ...',   None),
        )
        for test in test_set:
            r = ListMailbox._get_empty_cme(test[0])
            self.assertEqual(test[1], r)

    def test_get_cme_list(self):
        test_set = (
            ('(\\A \\B \\C) ...',       ('\\A \\B \\C', len('(\\A \\B \\C)'))),
            ('(\\HasNoChildren) ...',   ('\\HasNoChildren', len('(\\HasNoChildren)'))),
            ('(\\NoInferiors) ...',     ('\\NoInferiors', len('(\\NoInferiors)'))),
            ('\\NoInferiors ...',       None),
            ('"/" ...',                 None),
        )
        for test in test_set:
            r = ListMailbox._get_cme_list(test[0])
            self.assertEqual(test[1], r)

    def test_get_path1(self):
        test_set = (
            ('"/" ...',                 ('/', len('"/"'))),
            ('"|" ...',                 ('|', len('"|"'))),
            ('"INBOX" ...',             ('INBOX', len('"INBOX"'))),
            ('"My Mailbox" ...',        ('My Mailbox', len('"My Mailbox"'))),
            ('"My \\"Mailbox\\"" ...',  ('My \\"Mailbox\\"', len('"My \\"Mailbox\\""'))),
            ('(\\NoInferiors) ...',     None),
        )
        for test in test_set:
            r = ListMailbox._get_path1(test[0])
            self.assertEqual(test[1], r)

    def test_get_path2(self):
        test_set = (
            ('/ ...',                 ('/', len('/'))),
            ('| ...',                 ('|', len('|'))),
            ('INBOX ...',             ('INBOX', len('INBOX'))),
            ('(\\NoInferiors) ...',   None),
        )
        for test in test_set:
            r = ListMailbox._get_path2(test[0])
            self.assertEqual(test[1], r)

    # ------------------------------------------------------------------
    # Testing the (high level) method that extracts tokens from the
    # beginning of a text.
    # ------------------------------------------------------------------

    def test_get_token(self):
        test_set = [
            ('"/" ...',                 (ListMailbox.TYPE_PATH, ('/', len('"/"')))),
            ('/ ...',                   (ListMailbox.TYPE_PATH, ('/', len('/')))),
            ('"|" ...',                 (ListMailbox.TYPE_PATH, ('|', len('"|"')))),
            ('| ...',                   (ListMailbox.TYPE_PATH, ('|', len('|')))),
            ('"INBOX" ...',             (ListMailbox.TYPE_PATH, ('INBOX', len('"INBOX"')))),
            ('INBOX ...',               (ListMailbox.TYPE_PATH, ('INBOX', len('INBOX')))),
            ('"My Mailbox" ...',        (ListMailbox.TYPE_PATH, ('My Mailbox', len('"My Mailbox"')))),
            ('"My \\"Mailbox\\"" ...',  (ListMailbox.TYPE_PATH, ('My \\"Mailbox\\"', len('"My \\"Mailbox\\""')))),
            ('(\\NoInferiors) ...',     (ListMailbox._TYPE_CME_LIST, ('\\NoInferiors', len('(\\NoInferiors)')))),
            ('\\NoInferiors ...',       (ListMailbox._TYPE_UNKNOWN, None)),
            ('NoInferiors ...',         (ListMailbox.TYPE_PATH, ('NoInferiors', len('NoInferiors')))),
            ('"NoInferiors ...',        (ListMailbox._TYPE_UNKNOWN, None)),
            ('(\\A \\B \\C) ...',       (ListMailbox._TYPE_CME_LIST, ('\\A \\B \\C', len('(\\A \\B \\C)')))),
            ('() ...',                  (ListMailbox._TYPE_EMPTY_CME, ('', len('()'))))
        ]
        for test in test_set:
            r = ListMailbox._get_token(test[0])
            self.assertEqual(test[1], r)

    # ------------------------------------------------------------------
    # Test the parsing
    # ------------------------------------------------------------------

    def test_parse(self):
        test_set: List[Tuple[str, Union[List[Tuple[int, str]], List[str]]]] =\
            [
                ('(\\HasNoChildren) "/" "Chats"',
                    [
                        (ListMailbox.TYPE_CME,  '\\HasNoChildren'),
                        (ListMailbox.TYPE_PATH, '/'),
                        (ListMailbox.TYPE_PATH, 'Chats')
                    ],
                    ['\\HasNoChildren', '/', 'Chats']
                ),

                ('"/" "Chats"',
                     [
                         (ListMailbox.TYPE_PATH, '/'),
                         (ListMailbox.TYPE_PATH, 'Chats')
                     ],
                     ['/', 'Chats']
                ),

                ('/ "Chats"',
                     [
                         (ListMailbox.TYPE_PATH, '/'),
                         (ListMailbox.TYPE_PATH, 'Chats')
                     ],
                     ['/', 'Chats']
                ),

                ('() / "Chats"',
                     [
                         (ListMailbox.TYPE_PATH, '/'),
                         (ListMailbox.TYPE_PATH, 'Chats')
                     ],
                     ['/', 'Chats']
                ),

                ('(\\A \\B \\C) / "Chats"',
                     [
                         (ListMailbox.TYPE_CME, '\\A'),
                         (ListMailbox.TYPE_CME, '\\B'),
                         (ListMailbox.TYPE_CME, '\\C'),
                         (ListMailbox.TYPE_PATH, '/'),
                         (ListMailbox.TYPE_PATH, 'Chats')
                     ],
                     ['\\A', '\\B', '\\C', '/', 'Chats']
                )
            ]

        for test in test_set:
            ListMailbox.reset()
            self.assertTrue(ListMailbox.parse(test[0]))
            self.assertEqual(ListMailbox.get_tokens(), test[1])
            self.assertEqual(ListMailbox.get_tokens_values(), test[2])

        test_set: List[str] =\
            [
                '(\\HasNoChildren) "/" Chats'
                '\\HasNoChildren "/" "Chats"'
            ]

        for test in test_set:
            ListMailbox.reset()
            self.assertFalse(ListMailbox.parse(test))

if __name__ == '__main__':
    unittest.main()

