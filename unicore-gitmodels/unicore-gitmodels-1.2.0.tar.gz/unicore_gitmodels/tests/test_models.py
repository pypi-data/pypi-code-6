import os
import unittest
import shutil
import pygit2

from gitmodel.workspace import Workspace

from unicore_gitmodels import models


def get_workspace(repo):
    try:
        ws = Workspace(repo.path, repo.head.name)
    except pygit2.GitError:
        ws = Workspace(repo.path)
    return ws


class ModelsTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ModelsTestCase, self).__init__(*args, **kwargs)
        self.repo_path = os.path.join(os.getcwd(), '.test_repo/')

    def delete_repo(self):
        try:
            shutil.rmtree(self.repo_path)
        except:
            pass

    def create_repo(self):
        try:
            self.repo = pygit2.Repository(self.repo_path)
        except:
            self.repo = pygit2.init_repository(self.repo_path, False)

    def get_repo_models(self):
        ws = get_workspace(self.repo)
        ws.register_model(models.GitPageModel)
        ws.register_model(models.GitCategoryModel)
        return ws.import_models(models)

    def setUp(self):
        self.delete_repo()
        self.create_repo()

    def tearDown(self):
        self.delete_repo()

    def test_category_language_filter(self):
        models = self.get_repo_models()

        cat = models.GitCategoryModel(
            title='Diarrhoea', slug='diarrhoea', language='eng-UK'
        )
        cat.save(True, message='added diarrhoea Category')

        cat2 = models.GitCategoryModel(
            title='Diarrhoea', slug='diarrhoea', language='eng-US', source=cat
        )
        cat.save(True, message='added diarrhoea Category')

        self.assertEquals(
            len(models.GitCategoryModel.filter(language='eng-UK')), 1)
        self.assertEquals(cat2.source.uuid, cat.uuid)

    def test_page_language_filter(self):
        models = self.get_repo_models()

        p = models.GitPageModel(
            title='Test Page 1', content='this is sample content for pg 1',
            language='eng-UK'
        )
        p.save(True, message='added diarrhoea Category')

        p2 = models.GitPageModel(
            title='Test Page 1', content='this is sample content for pg 1',
            language='eng-US', source=p
        )
        p2.save(True, message='added diarrhoea Category')

        self.assertEquals(
            len(models.GitPageModel.filter(language='eng-UK')), 1)
        self.assertEquals(p2.source.uuid, p.uuid)
