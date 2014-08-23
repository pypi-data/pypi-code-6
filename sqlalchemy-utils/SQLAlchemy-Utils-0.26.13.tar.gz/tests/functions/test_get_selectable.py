import sqlalchemy as sa
from sqlalchemy_utils.functions.orm import get_selectable

from tests import TestCase


class TestGetSelectable(TestCase):
    def create_models(self):
        class TextItem(self.Base):
            __tablename__ = 'text_item'
            id = sa.Column(sa.Integer, primary_key=True)

            type = sa.Column(sa.Unicode(255))

            __mapper_args__ = {
                'polymorphic_on': type,
            }

        class Article(TextItem):
            __tablename__ = 'article'
            id = sa.Column(
                sa.Integer, sa.ForeignKey(TextItem.id), primary_key=True
            )
            category = sa.Column(sa.Unicode(255))
            __mapper_args__ = {
                'polymorphic_identity': u'article'
            }

        class BlogPost(TextItem):
            __tablename__ = 'blog_post'
            id = sa.Column(
                sa.Integer, sa.ForeignKey(TextItem.id), primary_key=True
            )
            __mapper_args__ = {
                'polymorphic_identity': u'blog_post'
            }

        self.TextItem = TextItem
        self.Article = Article
        self.BlogPost = BlogPost

    def test_mapper(self):
        mapper = sa.inspect(self.TextItem)
        assert get_selectable(mapper) == mapper

    # def test_entity(self):
    #     assert get_selectable(self.TextItem) == self.TextItem

    # def test_instrumented_attribute(self):
    #     assert get_selectable(self.TextItem.id) == self.TextItem

    # def test_column(self):
    #     query = self.session.query(self.TextItem.__table__.c.id)
    #     assert list(get_query_entities(query)) == [self.TextItem.__table__]

    # def test_aliased_selectable(self):
    #     selectable = sa.orm.with_polymorphic(self.TextItem, [self.BlogPost])
    #     query = self.session.query(selectable)
    #     assert list(get_query_entities(query)) == [selectable]

    # def test_joined_entity(self):
    #     query = self.session.query(self.TextItem).join(
    #         self.BlogPost, self.BlogPost.id == self.TextItem.id
    #     )
    #     assert list(get_query_entities(query)) == [
    #         self.TextItem, sa.inspect(self.BlogPost)
    #     ]

    # def test_joined_aliased_entity(self):
    #     alias = sa.orm.aliased(self.BlogPost)

    #     query = self.session.query(self.TextItem).join(
    #         alias, alias.id == self.TextItem.id
    #     )
    #     assert list(get_query_entities(query)) == [
    #         self.TextItem, sa.inspect(alias)
    #     ]

    # def test_column_entity_with_label(self):
    #     query = self.session.query(self.Article.id.label('id'))
    #     assert list(get_query_entities(query)) == [sa.inspect(self.Article)]

    # def test_with_subquery(self):
    #     number_of_articles = (
    #         sa.select(
    #             [sa.func.count(self.Article.id)],
    #         )
    #         .select_from(
    #             self.Article.__table__
    #         )
    #     ).label('number_of_articles')

    #     query = self.session.query(self.Article, number_of_articles)
    #     assert list(get_query_entities(query)) == [self.Article, number_of_articles]

    # def test_aliased_entity(self):
    #     alias = sa.orm.aliased(self.Article)
    #     query = self.session.query(alias)
    #     assert list(get_query_entities(query)) == [alias]
