from typing import List, Union, Tuple
from imaplib import IMAP4_SSL
from dbeurive.imap.parser import ListMailbox
import re
from pprint import pprint

class Client:
    """This class implements an IMAP client.
    """

    def __init__(self, hostname: str, port: int, username: str, password: str, path_sep: str = '/'):
        """Create a client.

        Args:
            hostname (str): name of the host that runs the IMAP server.
            port (int): TCP port of the host that runs the IMAP server.
            username (str): client username.
            password (str): client password.
            path_sep (str): path separator for mailboxes.
        """
        self._hostname: str = hostname
        self._port: int = port
        self._username: str = username
        self._password: str = password
        self._path_sep: str = path_sep
        self._imap: Union[None, IMAP4_SSL]  = None
        self._last_error: Union[None, str, Exception] = None
        self._authenticated: bool = False
        self._selected_mailbox: Union[None, str] = None

    def is_connected(self) -> bool:
        """Test whether the client is connected to the IMAP server or not.

        Returns:
            bool: is the client is connected to the IMAP server, then the method returns the value True.
                Otherwise, it returns the value False.
        """
        return self._imap is not None

    def is_authenticated(self) -> bool:
        """Test whether the client is authenticated on the IMAP server or not.

        Returns:
            bool: is the client is authenticated to the IMAP server, then the method returns the value True.
                Otherwise, it returns the value False.
        """
        return self._authenticated

    def get_last_error(self) -> Union[None, str, Exception]:
        """Return the last error description.

        Returns:
            Union[str, Exception]: if an error occurred, then the method returns its description.
            None: if no error occurred, then the method returns the value None.
        """
        return self._last_error

    def connect(self) -> bool:
        """Connect to the IMAP server.

        Returns:
            True: the connection is established.
            False: the connection could not be established.
        """
        self._last_error = None
        try:
            self._imap = IMAP4_SSL(self._hostname, self._port)
        except IMAP4_SSL.error as e:
            self._imap = None
            self._last_error = e
            return False
        return True

    def login(self) -> bool:
        """Log to the IMAP server.

        Returns:
            True: the client successfully identified himself to the IMAP server.
            False: the client could not identify himself to the IMAP server.
        """
        self._last_error = None
        try:
            self._imap.login(self._username, self._password)
        except IMAP4_SSL.error as e:
            self._last_error = e
            return False
        self._authenticated = True
        return True

    def list_mailboxes(self, directory: str= '""') -> Union[None, List[List[str]]]:
        """List the mailboxes within a given directory on the server.

        Args:
            directory (str): string that identifies the directory.
                The default value is "".

        Returns:
            List[List[str]]: upon successful completion, the method returns the list of mailboxes.
            None: if the method could not interpret the server response, then it returns the value None.
        """
        mailboxes: List[bytes] = self.get_raw_list_mailboxes(directory)
        return __class__._list(mailboxes)

    def get_raw_list_mailboxes(self, directory: str= '""') -> Union[List[bytes], None]:
        """Get the list of mailboxes within a given directory as a list of raw identifiers.

        Args:
            directory (str): string that identifies the directory.
                The default value is "".

        Returns:
            List[bytes]: upon successful completion, the method returns the list of mailboxes.
            None: if an error occurred, then it returns the value None.
        """
        self._authenticated_or_die()
        # noinspection PyUnusedLocal
        status: str
        status, mailboxes = self._imap.list(directory)
        if 'OK' != status:
            return None
        return mailboxes

    def select_mailbox(self, mailbox: str='INBOX', readonly=False) -> int:
        """Select a mailbox and returns the number of emails within this mailbox.

        Args:
            mailbox (str): the name of the mailbox.
            readonly (bool): specify whether the access to the mailbox is restricted to read only or not.
                True: the mailbox can only be read.
                False: the mailbox can be read and written.

        Returns:
            int: the number of messages within the mailbox.

        Raises:
            Exception: if the client cannot select the mailbox.
        """
        self._authenticated_or_die()
        # noinspection PyUnusedLocal
        status: str
        # noinspection PyUnusedLocal
        data: List[bytes]
        status, data = self._imap.select(mailbox, readonly)
        if 'OK' != status:
            raise Exception(f'Cannot select the mailbox {mailbox}! Status code is {status}')
        if 0 == len(data):
            raise Exception(f'Cannot select the mailbox {mailbox}: the number of messages in the mailbox is not returned!')
        self._selected_mailbox = mailbox
        return int(data[0].decode())

    def list_emails_ids(self, *criteria, mailbox=None) -> List[str]:
        """Get the IDs of the emails stored within a mailbox.

        Please note that the mailbox should have been previously selected.
        However, it is possible to specify a mailbox to select through the use of the parameter "mailbox".

        Args:
            *criteria (List[str]): criteria used to select the emails.
            mailbox (Union[None, str]): optional name of a mailbox.

        Returns:
            List[str]: the IDs of the emails stored within the (previously selected / specified) mailbox.

        Raises:
            Exception: if the client could not get the list of IDs.
        """
        status, ids = self.get_raw_emails_ids(*criteria, mailbox=mailbox)
        if 'OK' != status:
            raise Exception(f'Cannot get the list of email in the mailbox {self._selected_mailbox}! Status code is {status}')
        if 0 == len(ids):
            raise Exception(
                f'Cannot get the list of email in the mailbox {self._selected_mailbox}! No list of IDs is returned!')
        return re.split('\s+', ids[0].decode())

    def get_raw_emails_ids(self, *criteria, mailbox=None) -> Tuple[str, List[bytes]]:
        """Get the IDs of the emails stored within a mailbox, a raw data.

        Args:
            *criteria (List[str]): criteria used to select the emails.
            mailbox (Union[None, str]): optional name of a mailbox.

        Returns:
            Tuple[str, List[bytes]]: the method returns two values:
                * the first value of the operation status.
                * the list of IDs formatted as a list of bytes.
        """
        self._authenticated_or_die()
        if mailbox is not None:
            self.select_mailbox(mailbox)
        if self._selected_mailbox is None:
            raise Exception('In order to get the list of emails in a mailbox, you must select a mailbox first!')
        criteria = ['ALL'] if 0 == len(criteria) else criteria
        return self._imap.search(None, *criteria)

    def get_hostname(self) -> str:
        """Return the IMAP server hostname.

        Returns:
            str: the server hostname.
        """
        return self._password

    def get_port(self) -> int:
        """Return the IMAP server port.

        Returns:
            int: the IMAP server port.
        """
        return self._port

    def get_username(self) -> str:
        """Return the client username.

        Returns:
            str: the client username.
        """
        return self._username

    def get_password(self) -> str:
        """Return the client password.

        Returns:
            str: the client password.
        """
        return self._password

    def get_path_sep(self) -> str:
        """Return the string used to express mailboxes paths.

        Returns:
            str: the string used to express mailboxes paths.
        """
        return self._path_sep

    def get_connector(self) -> IMAP4_SSL:
        """Return the IMAP object.

        Returns:
            IMAP4_SSL: the IMAP object.
        """
        return self._imap

    @staticmethod
    def _list(mailboxes: Union[List[bytes], List[None]]) -> Union[None, List[List[str]]]:
        """Given the raw output of the IMAP "list" function, the method return the mailboxes.

        Args:
            mailboxes (Union[List[bytes], List[None]]): raw output of the IMAP "list" function.

        Returns:
            List[List[str]]: upon successful completion, the method returns the list of mailboxes.
            None: if the method could not interpret the given input, then it returns the value None.
        """

        if mailboxes == [None]:
            return []

        result: List[List[str]] = []
        # noinspection PyUnusedLocal
        mailbox: bytes
        for mailbox in mailboxes:
            ListMailbox.reset()
            if not ListMailbox.parse(mailbox.decode()):
                return None
            tokens = ListMailbox.get_tokens()
            result.append([ t[1] for t in tokens if t[0] == ListMailbox.TYPE_PATH ])
        return result

    def _authenticated_or_die(self):
        """If the client is not authenticated, then raise en exception!

        Raises:
            Exception: if the client is not authenticated.
        """
        if not self._authenticated:
            raise Exception('The client is not authenticated!')

