# -*- coding: utf-8 -*-
from typing import Union, List, Tuple
import re



class ListMailbox:
    """This class implements the parser that process the result of the "list" command.

    The parser takes a line of text as input and produces a list of tokens.

    A token is a tuple that contains 2 values:

    * the first value is the type of the token. It can be: TYPE_CME or TYPE_PATH.
    * the second value is the value of the token.
      Examples: "\\HasNoChildren", "INBOX" or "/".
    """

    _TYPE_UNKNOWN   = -1
    _TYPE_CME_LIST  = 0
    _TYPE_EMPTY_CME = 1
    TYPE_CME        = 2
    TYPE_PATH       = 3

    _backslash = re.escape('\\')
    _empty_cme_re = re.compile(f'[(][)]')
    _cme_re = re.compile(f'[(](((%s[a-zA-Z]+)\s+)*(%s[a-zA-Z]+))[)]' %(_backslash, _backslash))
    _path_re1 = re.compile(f'(?<!%s)"(((?<=%s)"|[^"])+)(?<!%s)"' % (_backslash, _backslash, _backslash))
    _path_re2 = re.compile(f'((\/|\|)|([a-z_]+))', re.I)
    _tokens: List[Tuple[int, str]] = []

    @staticmethod
    def parse(text: str) -> bool:
        """Parse a given text.

        Args:
            text (str): the text to parse.

        Returns:
            bool: upon successful completion, the method returns the value True.
                Otherwise, it returns the value False.
        """

        while len(text) > 0:
            token_type, value = __class__._get_token(text)
            if __class__._TYPE_UNKNOWN == token_type:
                return False

            token = value[0]
            total_len = value[1]

            text = text[total_len:]
            text = str.strip(text)

            if __class__._TYPE_EMPTY_CME == token_type:
              continue

            if __class__.TYPE_PATH == token_type:
                __class__._tokens.append((token_type, token))
                continue

            assert __class__._TYPE_CME_LIST == token_type

            for cme in re.split('\s+', token):
                __class__._tokens.append((__class__.TYPE_CME, cme))

        return True

    @staticmethod
    def reset() -> None:
        """Reset the parser internal states.
        """
        __class__._tokens = []

    @staticmethod
    def get_tokens() -> List[Tuple[int, str]]:

        """Return the tokens extracted while parsing the given text.

        Returns:
            List[Tuple[int, str]]: the list of tokens.
        """

        return __class__._tokens

    @staticmethod
    def get_tokens_values() -> List[str]:
        """Return the values of the tokens.

        Returns:
            List[str]: the tokens' values.
        """
        return list(map(lambda x: x[1], __class__._tokens))

    @staticmethod
    def _get_token(text: str) -> Tuple[int, Union[Tuple[str, int], None]]:
        """Search for the first token in a given text.

        Args:
            text (str): text in which to search for tokens.

        Returns:
            Tuple[str, int]: Upon successful completion the method returns a token.
            None: if an error occurs, the method returns the value None.
        """
        r = __class__._get_empty_cme(text)
        if r is not None:
            return __class__._TYPE_EMPTY_CME, r

        r = __class__._get_cme_list(text)
        if r is not None:
            return __class__._TYPE_CME_LIST, r

        r = __class__._get_path1(text)
        if r is not None:
            return __class__.TYPE_PATH, r

        r = __class__._get_path2(text)
        if r is not None:
            return __class__.TYPE_PATH, r

        return __class__._TYPE_UNKNOWN, None

    @staticmethod
    def _get_empty_cme(text: str) -> Union[None, Tuple[str, int]]:
        """Try to extract an empty list of CME from a given text.

        Args:
            text (str): input text.

        Returns:
            Tuple[str, int]: if the given text starts with an empty CME, then the method returns a tuple that contains 2
            values:
                * the first value is the value of the token (in this case, this is an empty string).
                * the second value is the total length of the string that contains the tokens.
            None: if the given text does not start with an empty CME, then the method returns the value None.
        """
        r: re.Match = __class__._empty_cme_re.match(text)
        if r is None:
            return None
        else:
            return '', r.end(0)

    @staticmethod
    def _get_cme_list(text: str) -> Union[None, Tuple[str, int]]:
        """Try to extract a list of CMEs. For example: (\\Drafts \\NoInferiors)

        Args:
            text (str): input text.

        Returns:
            Tuple[str, int]: if the given text starts with a list of CME, then the method returns a tuple that contains 2
            values:
                * the first value is the value of the token (the string that represents the list of CME).
                * the second value is the total length of the string that contains the tokens.
            None: if the given text does not start with a list of CME, then the method returns the value None.
        """
        r: re.Match = __class__._cme_re.match(text)
        if r is None:
            return None
        else:
            return r.group(1), r.end(0)

    @staticmethod
    def _get_path1(text: str) -> Union[None, Tuple[str, int]]:
        """Try to extract a path surrounded by "". For example: "INBOX"

        Args:
            text (str): input text.

        Returns:
            Tuple[str, int]: if the given text starts with a path surrounded by "", then the method returns a tuple that contains 2
            values:
                * the first value is the value of the token (the string that represents the path).
                * the second value is the total length of the string that contains the tokens.
            None: if the given text does not start with a path surrounded by "", then the method returns the value None.
        """
        r: re.Match = __class__._path_re1.match(text)
        if r is None:
            return None
        else:
            return r.group(1), r.end(0)

    @staticmethod
    def _get_path2(text: str) -> Union[None, Tuple[str, int]]:
        """Try to extract a path (without surrounding ""). For example: INBOX

        Args:
            text (str): input text.

        Returns:
            Tuple[str, int]: if the given text starts with a path (without surrounding ""), then the method returns a tuple that contains 2
            values:
                * the first value is the value of the token (the string that represents the path).
                * the second value is the total length of the string that contains the tokens.
            None: if the given text does not start with a path (without surrounding ""), then the method returns the value None.
        """
        r: re.Match = __class__._path_re2.match(text)
        if r is None:
            return None
        else:
            if r.group(2) is None:
                return r.group(3), r.end(0)
            else:
                return r.group(2), r.end(0)



