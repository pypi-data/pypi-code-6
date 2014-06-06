__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from xml.etree import ElementTree
from urllib import parse, request

import bs4
from requests.auth import HTTPBasicAuth

from pymal import global_functions
from pymal import decorators
from pymal import exceptions
from pymal import consts
from pymal import AccountAnimes
from pymal import AccountMangas

__all__ = ['Account']


class Account(object, metaclass=decorators.SingletonFactory):
    """
    """
    __all__ = ['animes', 'mangas', 'reload', 'search', 'auth_connect',
               'connect', 'is_user_by_name', 'is_user_by_id', 'is_auth']
    
    __AUTH_CHECKER_URL =\
        request.urljoin(consts.HOST_NAME, r'api/account/verify_credentials.xml')
    __SEARCH_URL = request.urljoin(consts.HOST_NAME, 'api/{0:s}/search.xml')
    __ANIME_SEARCH_URL = __SEARCH_URL.format('anime')
    __MANGA_SEARCH_URL = __SEARCH_URL.format('manga')

    __FRIENDS_URL = request.urljoin(consts.HOST_NAME, 'profile/{0:s}/friends')

    __MY_LOGIN_URL = request.urljoin(consts.HOST_NAME, 'login.php')
    __DATA_FORM = 'username={0:s}&password={1:s}&cookie=1&sublogin=Login'

    def __init__(self, username: str, password: str or None=None):
        """
        """
        self.__username = username
        self.__password = password
        self.connect = global_functions.connect
        self.__user_id = 0
        self.__auth_object = None
        self.__cookies = dict()

        self.__animes = None
        self.__mangas = None
        self.__friends_url = self.__FRIENDS_URL.format(self.username)
        self.__friends = None

        if password is not None:
            self.change_password(password)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def user_id(self) -> int:
        if not self.is_auth:
            raise exceptions.UnauthenticatedAccountError(self.username)
        return self.__user_id

    @property
    def mangas(self) -> AccountMangas.AccountMangas:
        if self.__mangas is None:
            self.__mangas = AccountMangas.AccountMangas(self.username, self)
        return self.__mangas

    @property
    def animes(self) -> AccountAnimes.AccountAnimes:
        if self.__animes is None:
            self.__animes = AccountAnimes.AccountAnimes(self.username, self)
        return self.__animes

    @property
    def friends(self) -> set:
        class FriendsFrozenSet(set):
            def __init__(self, account: Account):
                super().__init__()

                self.account = account
                self.reload()

            def reload(self):
                self.clear()
                div_wrapper = global_functions.get_content_wrapper_div(self.account._Account__friends_url, self.account.connect)
                assert div_wrapper is not None

                list_div_friend = div_wrapper.findAll(name="div", attrs={"class": "friendBlock"})
                for div_friend in list_div_friend:
                    div_pic = div_friend.find(name="div", attrs={'class': 'picSurround'})
                    assert div_pic is not None

                    splited_friend_url = div_pic.a['href'].split('/profile/', 1)
                    assert len(splited_friend_url) == 2

                    self.add(Account(splited_friend_url[1]))

        self.__friends = FriendsFrozenSet(account=self)
        return self.__friends

    def search(self, search_line: str, is_anime: bool=True) -> set:
        """
        """
        params = {'q': search_line}
        if is_anime:
            base_url = self.__ANIME_SEARCH_URL
            from pymal import Anime
            searched_object = Anime.Anime
            account_object_list = self.animes
        else:
            base_url = self.__MANGA_SEARCH_URL
            from pymal import Manga
            searched_object = Manga.Manga
            account_object_list = self.mangas

        url_parts = list(parse.urlparse(base_url))
        query = dict(parse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = parse.urlencode(query)
        search_url = parse.urlunparse(url_parts)

        data = self.auth_connect(search_url)
        entries = bs4.BeautifulSoup(data).body.anime.findAll(
            name='entry', recursive=False)

        def get_object(entry):
            object_id = int(entry.id.text)
            if object_id in account_object_list:
                return list(filter(
                    lambda x: x == object_id,
                    account_object_list
                ))[0]
            return searched_object(object_id)
        return set(map(get_object, entries))

    def change_password(self, password: str) -> bool:
        """
        Checking if the new password is valid
        """
        self.__auth_object = HTTPBasicAuth(self.username, password)
        data = self.auth_connect(self.__AUTH_CHECKER_URL)
        if data == 'Invalid credentials':
            self.__auth_object = None
            self.__password = None
            return False
        xml_user = ElementTree.fromstring(data)

        assert 'user' == xml_user.tag, 'user == {0:s}'.format(xml_user.tag)
        l = list(xml_user)
        xml_username = l[1]
        assert 'username' == xml_username.tag,\
            'username == {0:s}'.format(xml_username.tag)
        assert self.username == xml_username.text.strip(),\
            'username = {0:s}'.format(xml_username.text.strip())

        xml_id = l[0]
        assert 'id' == xml_id.tag, 'id == {0:s}'.format(xml_id.tag)
        self.__user_id = int(xml_id.text)

        self.__password = password

        data_form = self.__DATA_FORM.format(self.username, password).encode('utf-8')
        self.connect(self.__MY_LOGIN_URL, data=data_form)

        return True

    def auth_connect(self, url: str, data: str or None=None,
                     headers: dict or None=None) -> str:
        """
        """
        assert self.is_auth, "Not auth yet!"
        return global_functions._connect(url, data=data, headers=headers,
                                         auth=self.__auth_object).text.strip()

    @property
    def __cookies_string(self) -> str:
        return ";".join(["=".join(item)for item in self.__cookies.items()])

    @property
    def is_auth(self) -> bool:
        """
        """
        return self.__auth_object is not None

    def __repr__(self):
        return "<Account username: {0:s}>".format(self.username)

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.username.encode())
        return int(hash_md5.hexdigest(), 16)
