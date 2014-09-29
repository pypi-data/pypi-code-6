import os
import unittest
import shutil
import pygit2
from datetime import datetime, timedelta

from gitmodel.workspace import Workspace

from unicore_gitmodels import models


def get_workspace(repo):
    try:
        ws = Workspace(repo.path, repo.head.name)
    except pygit2.GitError:
        ws = Workspace(repo.path)
    return ws


class ModelsTestCase(unittest.TestCase):

    maxDiff = None

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

    def mk_category(self, title, subtitle='subtitle',
                    language=None, source=None, featured=False):
        models = self.get_repo_models()
        category = models.GitCategoryModel(
            title=title, subtitle=subtitle, language=language, source=source,
            featured_in_navbar=featured)
        category.save(True)
        return category

    def mk_page(self, title='title', subtitle='subtitle',
                description='description', content='content',
                created_at=None, modified_at=None,
                published=True, primary_category=None,
                featured_in_category=None, language='eng-US',
                source=None, featured=None):
        models = self.get_repo_models()
        now = modified_at or datetime.now()
        then = created_at or (now - timedelta(days=1))

        page = models.GitPageModel(
            title=title, subtitle=subtitle, description=description,
            content=content, created_at=then, modified_at=now,
            published=published, primary_category=primary_category,
            featured_in_category=featured_in_category,
            language=language, source=source, featured=featured)
        page.save(True)
        return page

    def test_category_to_dict(self):
        category1 = self.mk_category('category1')
        category2 = self.mk_category(
            'category2', source=category1, featured=True)
        self.assertEquals(category2.to_dict(), {
            'uuid': category2.uuid,
            'title': u'category2',
            'subtitle': 'subtitle',
            'slug': u'category2',
            'language': '',
            'featured_in_navbar': True,
            'source': category1.to_dict(),
        })

    def test_page_to_dict(self):
        category = self.mk_category('category')
        page1 = self.mk_page('page1', primary_category=category)
        page2 = self.mk_page('page2', primary_category=category, source=page1,
                             featured_in_category=True, featured=True)

        self.assertEqual(page1.featured, False)
        self.assertEqual(page1.featured_in_category, False)

        self.assertEquals(page2.to_dict(), {
            'uuid': page2.uuid,
            'title': u'page2',
            'slug': u'page2',
            'subtitle': u'subtitle',
            'description': u'description',
            'content': u'content',
            'created_at': page2.created_at,
            'modified_at': page2.modified_at,
            'published': True,
            'primary_category': page2.primary_category.to_dict(),
            'source': page1.to_dict(),
            'featured_in_category': True,
            'featured': True,
            'language': 'eng-US',
        })
