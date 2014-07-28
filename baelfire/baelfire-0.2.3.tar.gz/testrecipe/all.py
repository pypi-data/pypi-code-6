import sys

from baelfire.recipe import Recipe
from baelfire.task import Task
from baelfire.dependencies import AlwaysRebuild, FileChanged, ParentFileChanged, FileDoesNotExists
from baelfire.template import TemplateTask


class Something(Task):

    def get_output_file(self):
        return 'my3.log'

    def generate_dependencies(self):
        self.add_dependecy(FileDoesNotExists(self.get_output_file()))

    def make(self):
        self.touch(self.get_output_file())


class Ext(Task):

    help = 'my simple help'

    def get_output_file(self):
        return 'my.log'

    def generate_dependencies(self):
        # self.add_dependecy(AlwaysRebuild())
        self.add_dependecy(FileChanged('test.txt'))

    def make(self):
        # print('elo')
        self.touch('elo.txt')
        self.log.info('MEEE')
        open(self.get_output_file(), 'w').close()


class MyT(Task):

    def get_output_file(self):
        return 'my2.log'

    def generate_dependencies(self):
        # self.add_dependecy(AlwaysRebuild())
        self.add_dependecy(
            ParentFileChanged(self.task('/something')))
        self.add_dependecy(ParentFileChanged(self.task('/ext')))

    def make(self):
        self.recipe.log.info('info this')
        open(self.get_output_file(), 'w').close()


class Hey(TemplateTask):

    def get_output_file(self):
        return 'my4.log'

    def get_template_path(self):
        return 'template.jinja2'

    # def generate_dependencies(self):
    #     self.add_dependecy(AlwaysRebuild())


class NewOne(Task):

    def generate_links(self):
        self.add_link('/myt')

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def make(self):
        print("NewOne")


class TestMe(Recipe):

    def create_settings(self):
        self.settings['eloss'] = '10'

    def gather_recipes(self):
        self.add_task(MyT())
        self.add_task(Ext())
        self.add_task(Hey())
        self.add_task(Something())
        self.add_task(NewOne())
