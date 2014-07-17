from django.db.models import signals

from feincms.management.checker import check_database_schema

from djapps.blogs.abstract_models import AbstractBlog, AbstractPost, PostManager


class Blog(AbstractBlog):
    pass


class Post(AbstractPost):
    pass


signals.post_syncdb.connect(
    check_database_schema(Post, __name__),
    weak=False
)
