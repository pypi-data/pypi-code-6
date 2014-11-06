import unittest

from ZODB import MappingStorage, DB
import transaction


from twsfolders.rootfolders import RootFolders

from twsfolders.rootfolders import ValidatorRefusedError, RootAlreadyExistError

from twsfolders.item import Item
from twsfolders.folder import Folder


from application import Application
from application import application_folders_validator, IApplication, IApplicationService


class FoldersTestCase(unittest.TestCase):

    def setUp(self):
        # setup data ZODB Storage connection
        storage = MappingStorage.MappingStorage('folders')
        db = DB(storage)
        self.connection = db.open()

    def get_folders(self, validator=None):
        return RootFolders(self.connection, validator=validator)

    def test_folders_validator_callable(self):
        application_folders = self.get_folders(validator=application_folders_validator)
        app = Application(name='app')

        application_folders.add_item(app)

        self.assertIn('app', application_folders)

        folder = Folder(name='folder')

        self.assertRaises(ValidatorRefusedError, application_folders.add_item, folder)

    def test_folders_validator_interface(self):
        application_folders = self.get_folders(validator=IApplication)
        app = Application(name='app')

        application_folders.add_item(app)

        self.assertIn('app', application_folders)

        folder = Folder(name='folder')
        self.assertRaises(ValidatorRefusedError, application_folders.add_item, folder)

    def test_folders_add_non_folder(self):
        application_folders = self.get_folders()
        item = Item(name='item')

        self.assertRaises(TypeError, application_folders.add_item, item)

    def test_folders_item_with_parent(self):
        """add Folders item with parents"""
        application_folders = self.get_folders()
        folder = Folder(name='item')
        folder_folder = Folder(parent=folder, name='folder2')

        self.assertRaises(AttributeError, application_folders.add_item, folder_folder)

    def test_folders_add_existing_item(self):
        """add existing item name"""
        folders = self.get_folders()
        folder = Folder(name='folder')
        folders.add_item(folder)

        folder2 = Folder(name='folder')

        self.assertRaises(RootAlreadyExistError, folders.add_item, folder2)

    def test_folders_items(self):
        """working with items"""

        folders = self.get_folders()

        self.assertFalse(folders.has_items())

        folder = Folder(name='folder')
        folders.add_item(folder)

        self.assertIn(folder.name, folders)

        self.assertTrue(folders.has_items())

        folder2 = Folder(name='folder2')
        folders.add_item(folder2)

        # rename item ouside rootfolders
        folder2.name = 'folders2_renamed_in_side'
        self.assertIn('folder2', folders.check_names())

        folders.repair_names()

        self.assertNotIn('folder2', folders.check_names())

        self.assertIn(folder2.name, folders)

        names = folders.list_items()
        for name in names:
            self.assertIn(name, folders)

        for item in folders:
            self.assertIn(item.name, folders)

        folder_ = folders.get_item('folder')
        self.assertEqual(folder, folder_)

        folder2_ = folders.get_item('folder2')
        self.assertEqual(folder2, folder2_)

        folders.delete_item('folder2')
        self.assertNotIn('folder2', folders)

        folders.rename_item('folder', 'folder_renamed')

        self.assertIn('folder_renamed', folders)
        self.assertEqual('folder_renamed', folder.name)

        folder_renamed = folders.get_item('folder_renamed')
        self.assertEqual(folder, folder_renamed)

    def test_folders_url(self):
        """
        test working with url
        """
        folders = self.get_folders()
        root_folder = Folder(name='root')
        folders.add_item(root_folder)
        folder = Folder(root_folder, name='folder')
        folder2 = Folder(folder, name='folder2')

        #from folders
        url_item = folders.get_url_item('root')
        self.assertEqual(url_item, root_folder)

        url_item = folders.get_url_item('root/folder')
        self.assertEqual(url_item, folder)

        url_item = folders.get_url_item('root/folder/')
        self.assertEqual(url_item, folder)

        url_item = folders.get_url_item('root/folder/folder2')
        self.assertEqual(url_item, folder2)

        url_item = folders.get_url_item('root/folder/folder2/')
        self.assertEqual(url_item, folder2)

        # from root_folder
        self.assertEqual(folder2.url(), '/folder/folder2')
        self.assertEqual(root_folder.get_url_item('/folder/folder2'), folder2)
        self.assertEqual(root_folder.get_url_item('/folder/folder2/'), folder2)

        self.assertEqual(folder.url(), '/folder')
        self.assertEqual(root_folder.get_url_item('/folder'), folder)
        self.assertEqual(root_folder.get_url_item('/folder/'), folder)

    def tearDown(self):
        transaction.commit()
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
