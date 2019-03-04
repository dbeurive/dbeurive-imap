import unittest
import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

from dbeurive.imap.config import Config

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
config_path = os.path.join(data_path, 'isp.yaml')

class TestConfig(unittest.TestCase):

    def test_loading_ok(self):
        isps_expected = ['mail.com',
                         'yandex.ru',
                         'laposte.net',
                         'vivaldi.net',
                         'net-c.com']
        isps_expected.sort()

        conf = Config.get_conf_from_file(config_path)
        isps = conf.get_isps()
        isps.sort()
        self.assertEqual(isps_expected, isps)
        self.assertEqual('imap.mail.com', conf.get_hostname('mail.com'))
        self.assertEqual(993, conf.get_port('mail.com'))
        self.assertEqual('/', conf.get_path_set('mail.com'))
        self.assertEqual('thermotest@mail.com', conf.get_user_login('mail.com'))
        self.assertEqual('Orn1th0r1que', conf.get_user_password('mail.com'))

        conf = Config.get_conf_from_string(conf.dump())
        isps = conf.get_isps()
        isps.sort()
        self.assertEqual(isps_expected, isps)
        self.assertEqual('imap.mail.com', conf.get_hostname('mail.com'))
        self.assertEqual(993, conf.get_port('mail.com'))
        self.assertEqual('/', conf.get_path_set('mail.com'))
        self.assertEqual('thermotest@mail.com', conf.get_user_login('mail.com'))
        self.assertEqual('Orn1th0r1que', conf.get_user_password('mail.com'))




    def test_cmp_conf(self):
        conf1 = Config.get_conf_from_file(config_path)
        conf2 = Config.get_conf_from_file(config_path)

        m1 = conf1.get_conf()
        m2 = conf2.get_conf()
        self.assertTrue(Config.cmp_conf(m1, m2))

        m1 = conf1.get_conf()

        m2 = conf2.get_conf()
        m2['mail.com']['net']['hostname'] = 'toto'
        self.assertFalse(Config.cmp_conf(m1, m2))

        m2 = conf2.get_conf()
        m2['mail.com']['net']['port'] = 10
        self.assertFalse(Config.cmp_conf(m1, m2))

        m2 = conf2.get_conf()
        m2['mail.com']['user']['login'] = 'user'
        self.assertFalse(Config.cmp_conf(m1, m2))

        m2 = conf2.get_conf()
        m2['mail.com']['user']['password'] = 'password'
        self.assertFalse(Config.cmp_conf(m1, m2))

    def test_cypher1(self):
        clear_conf = Config.get_conf_from_file(config_path)
        str_cyphered_conf: bytes = Config.cypher(clear_conf.dump())
        str_decrypted_conf: str = Config.decrypt(str_cyphered_conf)
        decrypted_conf = Config.get_conf_from_string(str_decrypted_conf)
        self.assertTrue(Config.cmp_conf(clear_conf.get_conf(), decrypted_conf.get_conf()))

    def test_cypher2(self):
        clear_conf = Config.get_conf_from_file(config_path)
        str_cyphered_conf: bytes = Config.cypher(clear_conf.dump())
        decrypted_conf = Config.get_conf_from_string(str_cyphered_conf, False)
        self.assertTrue(Config.cmp_conf(clear_conf.get_conf(), decrypted_conf.get_conf()))




