from __future__ import unicode_literals

import os
import shutil
import unittest
from doctpl.core import TemplateInfo


class TemplateInfoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # setup TemplateInfo.
        TemplateInfo.CONFIG_DIR = os.path.join(os.getcwd(), '.doctpl')
        TemplateInfo.setup()
        # mkdir testdir.
        cls.testdir = os.path.join(
            TemplateInfo.CONFIG_DIR,
            'testdir',
        )
        os.mkdir(cls.testdir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.testdir)

    def test_avaliable_templates(self):
        self.assertEqual(
            set(TemplateInfo.template_objects),
            {'template_a', 'template_b'},
        )

    def test_copy_for_not_existed_file(self):
        target_not_exist = os.path.join(
            self.testdir,
            'not_exist',
        )
        if os.path.exists(target_not_exist):
            os.remove(target_not_exist)

        template_object = TemplateInfo.template_objects['template_a']
        path = template_object.copy_to('./.doctpl/testdir/not_exist')

        self.assertEqual(path, target_not_exist)
        with open(path, 'r') as f:
            self.assertEqual(
                f.read(),
                "template_a's content.\n",
            )

    def test_copy_for_existed_file(self):
        target_exist = os.path.join(
            self.testdir, 'exist')
        # create empty file.
        open(target_exist, 'w').close()

        template_object = TemplateInfo.template_objects['template_a']
        with self.assertRaises(Exception) as context:
            template_object.copy_to('./.doctpl/testdir/exist')

        self.assertIn(
            'Already Existed',
            ''.join(context.exception.args),
        )


if __name__ == '__main__':
    unittest.main()
