__authors__ = ""
__copyright__ = "(c) 2014, pymal"
__license__ = "BSD License"
__contact__ = "Name Of Current Guardian of this file <email@address>"

import hashlib
from xml.etree import ElementTree
from threading import Thread
from urllib import request

from pymal import consts
from pymal import decorators
from pymal import MyAnime

__all__ = ['AccountAnimes']


class AccountAnimes(object, metaclass=decorators.SingletonFactory):
    """
    """
    __all__ = ['watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch',
               'reload']

    __URL = request.urljoin(consts.HOST_NAME, "malappinfo.php?u={0:s}&type=anime")

    def __init__(self, username: str, connection):
        """
        """
        self.__connection = connection
        self.__url = self.__URL.format(username)

        self.__watching = []
        self.__completed = []
        self.__on_hold = []
        self.__dropped = []
        self.__plan_to_watch = []

        self.user_days_spent_watching = None

        self.map_of_lists = {
            1: self.__watching,
            2: self.__completed,
            3: self.__on_hold,
            4: self.__dropped,
            6: self.__plan_to_watch,

            '1': self.__watching,
            '2': self.__completed,
            '3': self.__on_hold,
            '4': self.__dropped,
            '6': self.__plan_to_watch,

            'watching': self.__watching,
            'completed': self.__completed,
            'onhold': self.__on_hold,
            'dropped': self.__dropped,
            'plantowatch': self.__plan_to_watch,
        }

        self._is_loaded = False

    @property
    @decorators.load
    def watching(self) -> list:
        return self.__watching

    @property
    @decorators.load
    def completed(self) -> list:
        return self.__completed

    @property
    @decorators.load
    def on_hold(self) -> list:
        return self.__on_hold

    @property
    @decorators.load
    def dropped(self) -> list:
        return self.__dropped

    @property
    @decorators.load
    def plan_to_watch(self) -> list:
        return self.__plan_to_watch

    def __contains__(self, item: MyAnime.MyAnime) -> bool:
        return any(map(lambda x: item == x, self))

    def __iter__(self):
        class AccountAnimesIterator(object):

            def __init__(self, values):
                self. values = values
                self.location = 0

            def __iter__(self):
                self.location = 0
                return self

            def __next__(self):
                if self.location >= len(self.values):
                    raise StopIteration
                value = self.values[self.location]
                self.location += 1
                return value
        return AccountAnimesIterator(self.watching + self.completed +
                                     self.on_hold + self.dropped +
                                     self.plan_to_watch)

    def __getitem__(self, key: str or int) -> list:
        if isinstance(key, int):
            if key < len(self.watching):
                return self.watching[key]
            key -= len(self.watching)
            if key < len(self.completed):
                return self.completed[key]
            key -= len(self.completed)
            if key < len(self.on_hold):
                return self.on_hold[key]
            key -= len(self.on_hold)
            if key < len(self.dropped):
                return self.dropped[key]
            key -= len(self.dropped)
            if key < len(self.plan_to_watch):
                return self.plan_to_watch[key]
            raise IndexError(
                'list index out of range (the size if {0:d}'.format(len(self)))
        key = str(key)
        for mal_object in self:
            if mal_object.title == key:
                return mal_object
        KeyError("{0:s} doesn't have the anime '{1:s}'".format(
            self.__class__.__name__, key))

    def reload(self):
        resp_data = self.__connection.connect(self.__url)
        xml_tree = ElementTree.fromstring(resp_data)
        assert 'myanimelist' == xml_tree.tag, 'myanimelist == {0:s}'.format(
            xml_tree.tag)
        xml_mal_objects = list(xml_tree)
        xml_general_data = xml_mal_objects[0]
        assert 'myinfo' == xml_general_data.tag, 'myinfo == {0:s}'.format(
            xml_general_data.tag)
        l = list(xml_general_data)
        xml_user_id = l[0]
        assert 'user_id' == xml_user_id.tag, xml_user_id.tag
        assert self.__connection.user_id == int(xml_user_id.text),\
            int(xml_user_id.text)
        xml_user_name = l[1]
        assert 'user_name' == xml_user_name.tag, xml_user_name.tag
        assert self.__connection.username == xml_user_name.text.strip(),\
            xml_user_name.text.strip()
        xml_user_watching = l[2]
        assert 'user_watching' == xml_user_watching.tag, xml_user_watching.tag
        xml_user_completed = l[3]
        assert 'user_completed' == xml_user_completed.tag,\
            xml_user_completed.tag
        xml_user_onhold = l[4]
        assert 'user_onhold' == xml_user_onhold.tag, xml_user_onhold.tag
        xml_user_dropped = l[5]
        assert 'user_dropped' == xml_user_dropped.tag, xml_user_dropped.tag
        xml_user_plantowatch = l[6]
        assert 'user_plantowatch' == xml_user_plantowatch.tag,\
            xml_user_plantowatch.tag
        xml_user_days_spent_watching = l[7]
        assert 'user_days_spent_watching' == xml_user_days_spent_watching.tag,\
            xml_user_days_spent_watching.tag
        self.user_days_spent_watching = float(
            xml_user_days_spent_watching.text.strip())

        xml_mal_objects = xml_mal_objects[1:]

        self.__watching.clear()
        self.__completed.clear()
        self.__on_hold.clear()
        self.__dropped.clear()
        self.__plan_to_watch.clear()

        threads = []
        for xml_mal_object in xml_mal_objects:
            if consts.DEBUG:
                self.__get_my_mal_object(xml_mal_object)
            else:
                thread = Thread(
                    target=self.__get_my_mal_object, args=(xml_mal_object, ))
                thread.start()
                threads.append(thread)

        while threads:
            threads.pop().join()

        self._is_loaded = True

    def __get_my_mal_object(self, xml_mal_object: ElementTree.Element):
        mal_object_id_xml = xml_mal_object.find('series_animedb_id')
        assert mal_object_id_xml is not None
        mal_object_id = int(mal_object_id_xml.text)
        my_mal_object_id_xml = xml_mal_object.find('my_id')
        assert my_mal_object_id_xml is not None
        my_mal_object_id = int(my_mal_object_id_xml.text)
        mal_object = MyAnime.MyAnime(mal_object_id, my_mal_object_id,
                                     self.__connection,
                                     my_mal_xml=xml_mal_object)
        self.map_of_lists[mal_object.my_status].append(mal_object)

    def __len__(self):
        return sum([1 for obj in self])

    def __repr__(self):
        return "<User animes' number is {0:d}>".format(len(self))

    def __hash__(self):
        hash_md5 = hashlib.md5()
        hash_md5.update(self.__connection.username.encode())
        hash_md5.update(self.__class__.__name__.encode())
        return int(hash_md5.hexdigest(), 16)
