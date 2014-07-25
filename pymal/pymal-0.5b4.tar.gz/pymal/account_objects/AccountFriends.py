__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"


from pymal import global_functions
from pymal.types import ReloadedSet
from pymal.decorators import load
from pymal import exceptions


class AccountFriends(ReloadedSet.ReloadedSetSingletonFactory):
    def __init__(self, url: str, account):
        self.account = account
        self.__url = url

        self.__friends = frozenset()
        self.reload()

        self._is_loaded = False

    @property
    @load
    def __friends_list(self):
        return self.__friends

    @property
    def _values(self):
        return self.__friends_list

    def reload(self):
        """
        :exception FailedToParseError
        """
        div_wrapper = global_functions.get_content_wrapper_div(self.__url, self.account.connect)
        if div_wrapper is None:
            raise exceptions.FailedToParseError()

        list_div_friend = div_wrapper.findAll(name="div", attrs={"class": "friendBlock"})
        self.__friends = frozenset(map(self.__parse_friend_div, list_div_friend))

        self._is_loaded = True

    @staticmethod
    def __parse_friend_div(div_friend):
        """

        :param div_friend:
        :type div_friend:

        :exception FailedToParseError

        :return:
        :rtype:
        """
        from pymal import Account

        div_pic = div_friend.find(name="div", attrs={'class': 'picSurround'})
        if div_pic is None:
            raise exceptions.FailedToParseError(div_friend)

        splited_friend_url = div_pic.a['href'].split('/profile/', 1)
        if 2 != len(splited_friend_url):
            raise exceptions.FailedToParseError()

        return Account.Account(splited_friend_url[1])

    def __repr__(self):
        return "<User friends' number is {0:d}>".format(len(self))

    def __hash__(self):
        import hashlib

        hash_md5 = hashlib.md5()
        hash_md5.update(self.account.username.encode())
        hash_md5.update(self.__class__.__name__.encode())
        return int(hash_md5.hexdigest(), 16)