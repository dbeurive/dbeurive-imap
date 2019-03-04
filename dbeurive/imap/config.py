from typing import List, Mapping, Tuple, Any, Union
import yaml
import os
from Crypto.Cipher import AES

# isp_name:
#   net:
#     hostname: ...
#     port: ...
#   imap:
#     path_sep: ...
#   user:
#     login: ...
#     password: ...

class Config:

    CYPHER_KEY_NAME = 'CYPHER_KEY'
    CYPHER_IV_NAME = 'CYPHER_IV'

    @staticmethod
    def get_conf_from_string(string: str, clear: bool = True) -> '__class__':
        """Create a configuration object from a (YAML formatted) string.

        Args:
            string (str): the (YAML formatted) string that represents the configuration.
            clear (bool): flag that indicates whether the given string is clear text or not.
               The default value True means that the given string is clear text.

        Returns:
            Config: a configuration object.
        """
        conf: str = string
        if not clear:
            conf = __class__.decrypt(conf)
        return Config(conf)
        pass

    @staticmethod
    def get_conf_from_file(path: str, clear: bool = True) -> '__class__':
        """Create a configuration object from a configuration file.

        Args:
            path (str): path to the configuration file.
            clear (bool): flag that indicates whether the content of the configuration file is cyphered or not.
               The default value True means that the content of the file is clear text.

        Returns:
            Config: a configuration object.
        """
        conf: str = __class__.load_conf(path)
        return __class__.get_conf_from_string(conf, clear)

    def __init__(self, conf: str):
        """Create a configuration object from a given (YAML formatted) string that represents the configuration.

        Args:
            conf (str): the configuration (expressed as a YAML structure).
        """
        self._conf: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]] = yaml.load(conf)
        status, message = __class__.validate_conf(self._conf)
        if not status:
            raise Exception(f'Invalid configuration: {message}')
        self._isp_list: List[str] = __class__._get_isp_names(self._conf)

    def dump(self) -> str:
        """Return the configuration as a YAML formatted string.

        Returns:
            str: a YAML formatted string that represents the configuration.
        """
        return yaml.dump(self._conf)

    def get_conf(self) -> Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]:
        """Return the configuration as a Map.

           Returns:
               Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]: a dictionary that represents the configuration.
        """
        return self._conf

    def get_isps(self) -> List[str]:
        """Return the list of configured ISPs.

           Returns:
               List[str]: a list that contains the names of te ISPs.
        """
        return self._isp_list

    def get_hostname(self, isp_name: str) -> str:
        """Return the hostname of the IMAP server for a given IPS.

           Args:
               isp_name(str): the name of the ISP.

           Returns:
               str: the hostname of the IMAP server.
        """
        if isp_name not in self._conf:
            raise Exception(f'ISP "{isp_name}" is not configured.')
        return self._conf[isp_name]['net']['hostname']

    def get_port(self, isp_name: str) -> int:
        """Return the port number used by the IMAP server.

        Args:
            isp_name (str): the name of the ISP.

        Returns:
            int: the port number.
        """
        if isp_name not in self._conf:
            raise Exception(f'ISP "{isp_name}" is not configured')
        return int(self._conf[isp_name]['net']['port'])

    def get_path_set(self, isp_name: str) -> str:
        """Return the string used to separate path elements within the paths that identify mailboxes.

        Args:
            isp_name (str): he name of the ISP.

        Returns:
            str: the string used to separate path elements within the paths that identify mailboxes.
        """
        if isp_name not in self._conf:
            raise Exception(f'ISP "{isp_name}" is not configured')
        return self._conf[isp_name]['imap']['path_sep']

    def get_user_login(self, isp_name: str) -> str:
        """Return the user name used to authenticate to the IMAP server.

        Args:
            isp_name (str): the name of the ISP.

        Returns:
            str: the user name.
        """
        if isp_name not in self._conf:
            raise Exception(f'ISP "{isp_name}" is not configured')
        return self._conf[isp_name]['user']['login']

    def get_user_password(self, isp_name: str) -> str:
        """Return the user password used to authenticate to the IMAP server.

        Args:
            isp_name (str): the name of the ISP.

        Returns:
            str: the user password.
        """
        if isp_name not in self._conf:
            raise Exception(f'ISP "{isp_name}" is not configured')
        return self._conf[isp_name]['user']['password']

    @staticmethod
    def cypher(conf: str) -> bytes:
        """Cypher the configuration.

        The data used for the cyphering come environment variables.

        * CYPHER_KEY: the cypher key.
        * CYPHER_IV: the cypher IV

        Args:
            conf (str): a YAML formatted string that represents the configuration.

        Returns:
            bytes: the cyphered configuration.
        """
        if __class__.CYPHER_KEY_NAME not in os.environ:
            raise Exception(f'Cannot crypt the configuration: environment variable "{__class__.CYPHER_KEY_NAME}" is not set.')
        if __class__.CYPHER_IV_NAME not in os.environ:
            raise Exception(f'Cannot crypt the configuration: environment variable "{__class__.CYPHER_IV_NAME}" is not set.')
        key: str = os.environ[__class__.CYPHER_KEY_NAME]
        iv: bytes = __class__._iv_to_bytes(os.environ[__class__.CYPHER_IV_NAME])
        cipher = AES.new(key, AES.MODE_CFB, IV=iv)
        return cipher.encrypt(conf)

    @staticmethod
    def decrypt(conf: bytes) -> str:
        """Decrypt a cyphered configuration.

        Args:
            conf (bytes): the cyphered configuration.

        Returns:
            str: the decrypted configuration.
        """
        if __class__.CYPHER_KEY_NAME not in os.environ:
            raise Exception(f'Cannot decrypt the given configuration: environment variable "{__class__.CYPHER_KEY_NAME}" is not set.')
        if __class__.CYPHER_IV_NAME not in os.environ:
            raise Exception(f'Cannot decrypt the given configuration: environment variable "{__class__.CYPHER_IV_NAME}" is not set.')
        key: str = os.environ[__class__.CYPHER_KEY_NAME]
        iv: bytes = __class__._iv_to_bytes(os.environ[__class__.CYPHER_IV_NAME])
        cipher = AES.new(key, AES.MODE_CFB, IV=iv)
        return cipher.decrypt(conf)

    @staticmethod
    def load_conf(path: str) -> str:
        """Load the configuration from a file.

        Args:
            path (str): path to the configuration file to load.

        Returns:
            str: the text that represents the configuration.
        """
        with open(path, 'r') as fd:
            conf: str = fd.read()
        return conf

    @staticmethod
    def validate_conf(conf: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]) -> Tuple[bool, str]:
        """Validate a configuration (expressed as a dictionary).

        Args:
            conf (Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]])): The configuration.

        Returns:
            Tuple[bool, str]: the method returns 2 values.
                The first value represents the status of the operation.
                * True: success.
                * False: failure.
                The second value contains a possible error message.
                If the operation was successful, the error message is an empty string.
        """
        for isp in conf.items():
            name: str = isp[0]
            conf: Mapping[str, Mapping[str, Union[int, str]]] = isp[1]
            if not __class__._check_keys(conf, ['net', 'imap', 'user']):
                return False, f'Invalid configuration for ISP "{name}"'
            if not __class__._check_keys(conf['net'], ['hostname', 'port']):
                return False, f'Invalid configuration for ISP "{name}[net]"'
            if not __class__._check_keys(conf['imap'], ['path_sep']):
                return False, f'Invalid configuration for ISP "{name}[imap]"'
            if not __class__._check_keys(conf['user'], ['login', 'password']):
                return False, f'Invalid configuration for ISP "{name}[password]"'
        return True, ''

    @staticmethod
    def _check_keys(m: Mapping[str, Any], keys: List[str]) -> bool:
        """Check whether a given dictionary has a given list of keys or not.

        Args:
            m (Mapping[str, Any]): the dictionary.
            keys (List[str]): the list of keys.

        Returns:
            bool: if the given dictionary has a given list of keys, then the method returns the value True.
                Otherwise, it returns the value False.
        """
        k: List[str] = list(map(lambda x: x[0], m.items()))
        k.sort()
        keys.sort()
        return k == keys

    @staticmethod
    def _get_isp_names(conf: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]) -> List[str]:
        """Return the names of the ISP from a given configuration.

        Args:
            conf (Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]): the configuration.

        Returns:
            List[str]: the names of ISP.
        """
        return list(conf.keys())

    @staticmethod
    def _iv_to_bytes(iv: str) -> bytes:
        """Convert a string that represents the cypher IV into bytes.

        Args:
            iv (str): the cypher IV.

        Returns:
            bytes: the cypher IV expressed as a succession of bytes.
        """
        ints = [ord(c) for c in iv]
        if len(ints) != 16:
            raise Exception(f'Invalid IV ({iv}) from environment variable "{__class__.CYPHER_IV_NAME}": {iv} is not 16 bytes long.')
        return bytes(bytearray(ints))

    @staticmethod
    def _key_to_bytes(key: str) -> bytes:
        """Convert a string that represents the cypher key into bytes.

        Args:
            iv (str): the cypher key.

        Returns:
            bytes: the cypher key expressed as a succession of bytes.
        """
        ints = [ord(c) for c in key]
        if len(ints) != 16:
            raise Exception(f'Invalid key ({key}) from environment variable "{__class__.CYPHER_KEY_NAME}": {key} is not 16 bytes long.')
        return bytes(bytearray(ints))

    @staticmethod
    def cmp_conf(conf1: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]], conf2: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]) -> bool:
        """Compare 2 configurations.

        Args:
            conf1 (Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]], conf2: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]): first configuration.
            conf2 (Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]], conf2: Mapping[str, Mapping[str, Mapping[str, Union[int, str]]]]): second configuration.

        Returns:
            bool: if the 2 configurations are identical, then the method returns the value True.
                Otherwise, it returns the value False.
        """
        isp1 = __class__._get_isp_names(conf1)
        isp2 = __class__._get_isp_names(conf2)
        isp1.sort()
        isp2.sort()
        if isp1 != isp2:
            return False

        for isp_name in isp1:

            hostname1: str = conf1[isp_name]['net']['hostname']
            hostname2: str = conf2[isp_name]['net']['hostname']
            port1: int = conf1[isp_name]['net']['port']
            port2: int = conf2[isp_name]['net']['port']
            path_sep1: str = conf1[isp_name]['imap']['path_sep']
            path_sep2: str = conf2[isp_name]['imap']['path_sep']

            login1: str = conf1[isp_name]['user']['login']
            login2: str = conf2[isp_name]['user']['login']
            password1: str = conf1[isp_name]['user']['password']
            password2: str = conf2[isp_name]['user']['password']

            if hostname1 != hostname2:
                return False

            if port1 != port2:
                return False

            if path_sep1 != path_sep2:
                return False

            if login1 != login2:
                return False

            if password1 != password2:
                return False

        return True

