
__author__ = 'Ninad'

from addonpy.IAddonInfo import IAddonInfo


class ClickMeAddon(IAddonInfo):
    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def execute(self):
        raise NotImplemented

    @staticmethod
    def __addon__():
        return 'ClickMeAddon'


    def test(self):
        raise NotImplemented

    def  test1(self):
        raise NotImplemented