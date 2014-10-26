from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os
import shutil


class GeneralTarget(object):

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def _prepare_rel_path(self, rel_path):
        target_path = os.path.abspath(rel_path)
        if os.path.exists(target_path):
            raise Exception("{} Already Existed.".format(target_path))
        return target_path

    def copy_to(self, rel_dst_path):
        abs_dst_path = self._prepare_rel_path(rel_dst_path)
        self._make_copy(abs_dst_path)
        return abs_dst_path


class TemplateFile(GeneralTarget):

    def _make_copy(self, abs_dst_path):
        shutil.copyfile(self.path, abs_dst_path)


class TemplateDir(GeneralTarget):

    def _make_copy(self, abs_dst_path):
        shutil.copytree(self.path, abs_dst_path)


class TemplateInfo(object):
    CONFIG_DIR = os.path.expanduser('~/.doctpl')
    template_objects = {}

    @classmethod
    def setup(cls):
        # Init dir for storing tmeplates.
        if not os.path.exists(cls.CONFIG_DIR):
            os.mkdir(cls.CONFIG_DIR)
        # Load information of templates.
        for template_name in os.listdir(cls.CONFIG_DIR):
            template_path = os.path.join(cls.CONFIG_DIR, template_name)

            if os.path.isfile(template_path):
                template_cls = TemplateFile
            elif os.path.isdir(template_path):
                template_cls = TemplateDir

            cls.template_objects[template_name] = template_cls(
                template_name,
                template_path,
            )
