import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings

date = datetime.date(year=2012, month=3, day=3)
day = relativedelta(days=1)
month = relativedelta(months=1)
year = relativedelta(years=1)

settings.configure(
    DATABASES={'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }},
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'feincms',
        'blogs',
    ),
    USE_TZ = True,
)

from django.test import TestCase
from django.core.management import call_command
from djapps.blogs.models import Blog, Post
from djapps.blogs.templatetags.blogs import blog_years, blog_months, blog_days
from djapps.blogs.views import PostView, PostListView
from django.test.client import RequestFactory
from feincms.content.richtext.models import RichTextContent

Post.register_templates(
    {'title': 'Page',
     'path': 'page/page.html',
     'regions': (
         ('main', 'Main content area'),
     )},
)
Post.create_content_type(RichTextContent)


call_command('syncdb', interactive=False)


class BlogTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_active(self):
        blog = Blog.objects.create(name="test", slug="test")
        post = blog.posts.create()
        self.assertEqual(list(blog.posts.active()), [post])
        post.published = False
        post.save()
        self.assertEqual(list(blog.posts.active()), [])

    def test_before_after(self):

        blog = Blog.objects.create(name="test", slug="test")

        posts = [
            blog.posts.create(id=1,  title='1',  slug='1',
                              date=date-day, time=None),
            blog.posts.create(id=2,  title='2',  slug='2',
                              date=date-day, time=None),
            blog.posts.create(id=5,  title='5',  slug='5',
                              date=date-day, time=datetime.time(hour=11)),
            blog.posts.create(id=3,  title='3',  slug='3',
                              date=date-day, time=datetime.time(hour=12)),
            blog.posts.create(id=4,  title='4',  slug='4',
                              date=date-day, time=datetime.time(hour=12)),
            blog.posts.create(id=6,  title='6',  slug='6',
                              date=date-day, time=datetime.time(hour=13)),
            blog.posts.create(id=7,  title='7',  slug='7',
                              date=date, time=None),
            blog.posts.create(id=8,  title='8',  slug='8',
                              date=date, time=None),
            blog.posts.create(id=11, title='11', slug='11',
                              date=date, time=datetime.time(hour=11)),
            blog.posts.create(id=9,  title='9',  slug='9',
                              date=date, time=datetime.time(hour=12)),
            blog.posts.create(id=10, title='10', slug='10',
                              date=date, time=datetime.time(hour=12)),
            blog.posts.create(id=12, title='12', slug='12',
                              date=date, time=datetime.time(hour=13)),
        ]

        for i in range(len(posts)):
            post = posts[i]
            if i + 1 < len(posts):
                self.assertEqual(Post.objects.after(post).last(), posts[i+1])
            else:
                self.assertEqual(Post.objects.after(post).last(), None)

        posts.reverse()

        for i in range(len(posts)):
            post = posts[i]
            if i + 1 < len(posts):
                self.assertEqual(Post.objects.before(post).first(), posts[i+1])
            else:
                self.assertEqual(Post.objects.before(post).first(), None)

    def test_next_prev(self):
        date = datetime.date.today()
        blog1 = Blog.objects.create(name="test1", slug="test1")
        blog2 = Blog.objects.create(name="test2", slug="test2")
        posts = [
            blog1.posts.create(id=1,  title='1', slug='1', date=date),
            blog2.posts.create(id=2,  title='2', slug='2', date=date),
            blog1.posts.create(id=3,  title='3', slug='3', date=date),
        ]
        self.assertEqual(posts[0].next(), posts[2])
        self.assertEqual(posts[2].previous(), posts[0])
        self.assertEqual(posts[1].next(), None)
        self.assertEqual(posts[1].previous(), None)

    def test_blog_years(self):
        blog = Blog.objects.create(name="test", slug="test")
        blog.posts.create(slug="1", date=date)
        blog.posts.create(slug="2", date=date+day)
        blog.posts.create(slug="3", date=date+year)
        blog.posts.create(slug="4", date=date-year, published=False)
        blog2 = Blog.objects.create(name="test2", slug="test2")
        posts = [
            blog2.posts.create(slug="1", date=date),
            blog2.posts.create(slug="2", date=date-year-year),
        ]
        self.assertEqual(blog_years(blog),
                         [date.year + 1, date.year])
        self.assertEqual(blog_years(blog, order='ASC'),
                         [date.year, date.year + 1])
        self.assertEqual(blog_years(''), [date.year + 1,
                                          date.year,
                                          date.year - 2])

    def test_blog_months(self):
        blog = Blog.objects.create(name="test", slug="test")
        blog.posts.create(slug="1", date=date)
        blog.posts.create(slug="2", date=date+day)
        blog.posts.create(slug="3", date=date+month)
        blog.posts.create(slug="3", date=date+year)
        blog.posts.create(slug="3", date=date-year)
        blog.posts.create(slug="4", date=date-month, published=False)
        blog2 = Blog.objects.create(name="test2", slug="test2")
        posts = [
            blog2.posts.create(slug="1", date=date),
            blog2.posts.create(slug="2", date=date-month),
        ]
        self.assertEqual(blog_months(blog, date=date),
                         [date.month + 1, date.month])
        self.assertEqual(blog_months(blog, year=date.year),
                         [date.month + 1, date.month])
        self.assertEqual(blog_months(blog, date=date, order='ASC'),
                         [date.month, date.month + 1])
        self.assertEqual(blog_months(blog, year=date.year, order='ASC'),
                         [date.month, date.month + 1])
        self.assertEqual(blog_months('', date=date),
                         [date.month + 1,
                          date.month,
                          date.month - 1])
        self.assertEqual(blog_months(blog, date=''), None)
        self.assertEqual(blog_months('', year=date.year),
                         [date.month + 1,
                          date.month,
                          date.month - 1])
        self.assertEqual(blog_months(blog, year=''), None)

    def test_blog_days(self):
        blog = Blog.objects.create(name="test", slug="test")
        blog.posts.create(slug="1", date=date)
        blog.posts.create(slug="2", date=date)
        blog.posts.create(slug="2", date=date+day)
        blog.posts.create(slug="3", date=date+month)
        blog.posts.create(slug="3", date=date-month)
        blog.posts.create(slug="3", date=date+year)
        blog.posts.create(slug="3", date=date-year)
        blog.posts.create(slug="4", date=date-day, published=False)
        blog2 = Blog.objects.create(name="test2", slug="test2")
        posts = [
            blog2.posts.create(slug="1", date=date),
            blog2.posts.create(slug="2", date=date-month),
            blog2.posts.create(slug="3", date=date - day - day),
        ]
        self.assertEqual(blog_days(blog, year=date.year, month=date.month),
                         [date.day + 1, date.day])
        self.assertEqual(blog_days(blog, date=date),
                         [date.day + 1, date.day])
        self.assertEqual(blog_days(blog, year=date.year,
                                   month=date.month, order='ASC'),
                         [date.day, date.day + 1])
        self.assertEqual(blog_days(blog, date=date, order='ASC'),
                         [date.day, date.day + 1])
        self.assertEqual(blog_days('', date=date),
                         [date.day + 1,
                          date.day,
                          date.day - 2])
        self.assertEqual(blog_days(blog, date=''), None)
        self.assertEqual(blog_days('', year=date.year, month=date.month),
                         [date.day + 1,
                          date.day,
                          date.day - 2])
        self.assertEqual(blog_days(blog, year='', month=date.month), None)
        self.assertEqual(blog_days(blog, year=date.year, month=''), None)
        self.assertEqual(blog_days(blog, year='', month=''), None)

    def test_view_post_variables(self):
        blog = Blog.objects.create(name="test", slug="test")
        post = blog.posts.create(slug="test", date=date)
        request = self.request_factory.get('/')
        PostView().dispatch(
            request,
            blog__slug='test',
            date__year=date.year,
            date__month=date.month,
            date__day=date.day,
            slug='test',
        ).context_data
        self.assertEqual(request._blogs_current_blog, blog)
        self.assertEqual(request._blogs_current_date, post.date)
        self.assertEqual(request._blogs_current_year, post.date.year)
        self.assertEqual(request._blogs_current_month, post.date.month)
        self.assertEqual(request._blogs_current_day, post.date.day)

    def test_view_list_variables(self):
        blog = Blog.objects.create(name="test", slug="test")

        request = self.request_factory.get('/')
        PostListView.as_view()(
            request=request,
            blog__slug='test',
        ).context_data
        self.assertEqual(request._blogs_current_blog, blog)
        self.assertEqual(request._blogs_current_date,
                         datetime.date(year=1, month=1, day=1))
        self.assertEqual(request._blogs_current_year, 0)
        self.assertEqual(request._blogs_current_month, 0)
        self.assertEqual(request._blogs_current_day, 0)

        request = self.request_factory.get('/')
        PostListView.as_view()(
            request=request,
            blog__slug='test',
            date__year=date.year,
        ).context_data
        self.assertEqual(request._blogs_current_blog, blog)
        self.assertEqual(request._blogs_current_date,
                         datetime.date(year=date.year, month=1, day=1))
        self.assertEqual(request._blogs_current_year, date.year)
        self.assertEqual(request._blogs_current_month, 0)
        self.assertEqual(request._blogs_current_day, 0)

        request = self.request_factory.get('/')
        PostListView.as_view()(
            request=request,
            blog__slug='test',
            date__year=date.year,
            date__month=date.month,
        )
        self.assertEqual(
            request._blogs_current_date,
            datetime.date(year=date.year, month=date.month, day=1)
        )
        self.assertEqual(request._blogs_current_year, date.year)
        self.assertEqual(request._blogs_current_month, date.month)
        self.assertEqual(request._blogs_current_day, 0)

        request = self.request_factory.get('/')
        PostListView.as_view()(
            request=request,
            blog__slug='test',
            date__year=date.year,
            date__month=date.month,
            date__day=date.day,
        )
        self.assertEqual(
            request._blogs_current_date,
            datetime.date(year=date.year, month=date.month, day=date.day)
        )
        self.assertEqual(request._blogs_current_year, date.year)
        self.assertEqual(request._blogs_current_month, date.month)
        self.assertEqual(request._blogs_current_day, date.day)
