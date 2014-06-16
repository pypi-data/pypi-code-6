import sqlalchemy as sa
from sqlalchemy_continuum import version_class
from sqlalchemy_continuum.plugins import PropertyModTrackerPlugin
from tests import TestCase


class TestPropertyModificationsTracking(TestCase):
    plugins = [PropertyModTrackerPlugin()]

    def create_models(self):
        class User(self.Model):
            __tablename__ = 'text_item'
            __versioned__ = {
                'base_classes': (self.Model, )
            }
            id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

            name = sa.Column(sa.Unicode(255))

            age = sa.Column(sa.Integer)

        self.User = User

    def test_each_column_generates_additional_mod_column(self):
        UserVersion = version_class(self.User)
        assert 'name_mod' in UserVersion.__table__.c
        column = UserVersion.__table__.c['name_mod']
        assert not column.nullable
        assert isinstance(column.type, sa.Boolean)

    def test_primary_keys_not_included(self):
        UserVersion = version_class(self.User)
        assert 'id_mod' not in UserVersion.__table__.c

    def test_mod_properties_get_updated(self):
        user = self.User(name=u'John')
        self.session.add(user)
        self.session.commit()

        assert user.versions[-1].name_mod


class TestChangeSetWithPropertyModPlugin(TestCase):
    plugins = [PropertyModTrackerPlugin()]

    def test_changeset_for_insert(self):
        article = self.Article()
        article.name = u'Some article'
        article.content = u'Some content'
        self.session.add(article)
        self.session.commit()
        assert article.versions[0].changeset == {
            'content': [None, u'Some content'],
            'name': [None, u'Some article'],
            'id': [None, 1]
        }

    def test_changeset_for_update(self):
        article = self.Article()
        article.name = u'Some article'
        article.content = u'Some content'
        self.session.add(article)
        self.session.commit()

        article.name = u'Updated name'
        article.content = u'Updated content'
        self.session.commit()

        assert article.versions[1].changeset == {
            'content': [u'Some content', u'Updated content'],
            'name': [u'Some article', u'Updated name']
        }


class TestWithAssociationTables(TestCase):
    plugins = [PropertyModTrackerPlugin()]

    def create_models(self):
        class Article(self.Model):
            __tablename__ = 'article'
            __versioned__ = {
                'base_classes': (self.Model, )
            }

            id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
            name = sa.Column(sa.Unicode(255))

        article_tag = sa.Table(
            'article_tag',
            self.Model.metadata,
            sa.Column(
                'article_id',
                sa.Integer,
                sa.ForeignKey('article.id'),
                primary_key=True,
            ),
            sa.Column(
                'tag_id',
                sa.Integer,
                sa.ForeignKey('tag.id'),
                primary_key=True
            )
        )

        class Tag(self.Model):
            __tablename__ = 'tag'
            __versioned__ = {
                'base_classes': (self.Model, )
            }

            id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
            name = sa.Column(sa.Unicode(255))

        Tag.articles = sa.orm.relationship(
            Article,
            secondary=article_tag,
            backref='tags'
        )

        self.Article = Article
        self.Tag = Tag

    def test_each_column_generates_additional_mod_column(self):
        ArticleVersion = version_class(self.Article)
        assert 'name_mod' in ArticleVersion.__table__.c
        column = ArticleVersion.__table__.c['name_mod']
        assert not column.nullable
        assert isinstance(column.type, sa.Boolean)
