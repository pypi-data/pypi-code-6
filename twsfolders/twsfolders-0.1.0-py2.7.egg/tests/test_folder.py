
import unittest

from twsfolders import Folder
from twsfolders.item import Item

from application import Application
from application import ApplicationService


class FolderTestCase(unittest.TestCase):

    def get_folders_three(self):
        application = Application(name='application')
        service1 = ApplicationService(application, name='service1')
        folder11 = Folder(service1, name='folder11')
        folder12 = Folder(folder11, name='folder11')
        Item(folder12, name='item13')

        service2 = ApplicationService(application, name='service2')
        folder21 = Folder(service2, name='folder21')
        folder22 = Folder(folder21, name='folder21')

        Item(folder22, name='item23')

        return application

    def test_url(self):
        # todo
        application = self.get_folders_three()

        print application.list_items()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

