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
                    language=None, source=None, featured=False, position=0):
        models = self.get_repo_models()
        category = models.GitCategoryModel(
            title=title, subtitle=subtitle, language=language, source=source,
            featured_in_navbar=featured, position=position)
        category.save(True)
        return category

    def mk_page(self, title='title', subtitle='subtitle',
                description='description', content='content',
                created_at=None, modified_at=None,
                published=True, primary_category=None,
                featured_in_category=None, language='eng-US',
                source=None, featured=None, linked_pages=None,
                position=0):
        models = self.get_repo_models()
        now = modified_at or datetime.now()
        then = created_at or (now - timedelta(days=1))

        page = models.GitPageModel(
            title=title, subtitle=subtitle, description=description,
            content=content, created_at=then, modified_at=now,
            published=published, primary_category=primary_category,
            featured_in_category=featured_in_category,
            language=language, source=source, featured=featured,
            linked_pages=linked_pages, position=position)
        page.save(True)
        return page

    def test_category_to_dict(self):
        category1 = self.mk_category('category1')
        category2 = self.mk_category(
            'category2', source=category1, featured=True, position=4)
        self.assertEquals(category2.to_dict(), {
            'uuid': category2.uuid,
            'title': u'category2',
            'subtitle': 'subtitle',
            'slug': u'category2',
            'language': '',
            'featured_in_navbar': True,
            'source': category1.to_dict(),
            'position': 4,
        })

    def test_page_to_dict(self):
        category = self.mk_category('category')
        page1 = self.mk_page('page1', primary_category=category, position=1)
        page2 = self.mk_page('page2', primary_category=category, source=page1,
                             featured_in_category=True, featured=True,
                             position=4)

        self.assertEqual(page1.featured, False)
        self.assertEqual(page1.position, 1)
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
            'linked_pages': None,
            'position': 4,
        })

    def test_linked_pages(self):
        page1 = self.mk_page('page1')
        page2 = self.mk_page('page2')
        page3 = self.mk_page('page3', linked_pages=[page1.uuid, page2.uuid])

        data = page3.to_dict()
        self.assertEquals(data['linked_pages'], [page1.uuid, page2.uuid])

        linked_page1, linked_page2 = page3.get_linked_pages()
        self.assertEqual(linked_page1.to_dict(), page1.to_dict())
        self.assertEqual(linked_page2.to_dict(), page2.to_dict())

    def test_order_of_categories(self):
        self.mk_category('category1', position=3)
        self.mk_category('category2', position=4)
        self.mk_category('category3', position=2)
        self.mk_category('category4', position=1)

        models = self.get_repo_models()
        categories = list(models.GitCategoryModel.all())

        self.assertEquals(categories[0].title, 'category4')
        self.assertEquals(categories[1].title, 'category3')
        self.assertEquals(categories[2].title, 'category1')
        self.assertEquals(categories[3].title, 'category2')

    def test_order_of_pages(self):
        self.mk_page('page1', position=3)
        self.mk_page('page2', position=4)
        self.mk_page('page3', position=2)
        self.mk_page('page4', position=1)

        models = self.get_repo_models()
        pages = list(models.GitPageModel.all())

        self.assertEquals(pages[0].title, 'page4')
        self.assertEquals(pages[1].title, 'page3')
        self.assertEquals(pages[2].title, 'page1')
        self.assertEquals(pages[3].title, 'page2')
