from datetime import datetime, timedelta
from django import test
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils import six
from admintimestamps.base import TimestampedChangelist
from testproject.admin import TimestampedAdmin
from testproject.models import (
    AlternativeTimestampedItem, FakeTimestampedItem,
    SingleTimestampedItem, DateStampedItem, NullTimestampedItem)


class TestAdmin(test.TestCase):
    def setUp(self):
        self.admin = TimestampedAdmin(FakeTimestampedItem, None)

    def test_get_changelist(self):
        self.assertTrue(issubclass(
            self.admin.get_changelist(None), TimestampedChangelist),
            'Expected changelist to be a subclass of TimestampedChangelist')

    def test_has_timestamp_fields(self):
        self.assertTrue(hasattr(self.admin, 'timestamp_fields'),
                        'Expected timestamp_fields on ModelAdmin')


class TestChangeList(test.TestCase):
    def setUp(self):
        FakeTimestampedItem(
            title='just now', created=datetime.now() - timedelta(minutes=1),
            modified=datetime.now() - timedelta(minutes=2)).save()
        FakeTimestampedItem(
            title='some time ago', created=datetime(2010, 1, 15, 21, 19),
            modified=datetime(2011, 5, 28, 9, 59)).save()
        AlternativeTimestampedItem(title='alternative').save()
        SingleTimestampedItem(title='single timestamp').save()
        DateStampedItem(title='datestamp').save()
        NullTimestampedItem(title='null timestamp').save()
        user = User.objects.create_user('test', 'test@example.com', 'test')
        user.is_staff = user.is_superuser = True
        user.save()
        self.client.login(username='test', password='test')

    def test_header_row(self):
        response = self.client.get('/admin/testproject/faketimestampeditem/')
        content = force_text(response.content)
        six.assertRegex(self, content, r'Created\s*</a></div>')
        six.assertRegex(self, content, r'Modified\s*</a></div>')

    def test_recent_cell_values(self):
        response = self.client.get('/admin/testproject/faketimestampeditem/')
        content = force_text(response.content)
        self.assertContains(response, 'a minute ago</td>', count=1)
        six.assertRegex(self, content, r'2\W+minutes\W+ago</td>')

    def test_some_time_ago_values(self):
        response = self.client.get('/admin/testproject/faketimestampeditem/')
        self.assertContains(response, '01/15/2010 9:19 p.m.</td>', count=1)
        self.assertContains(response, '05/28/2011 9:59 a.m.</td>', count=1)

    def test_alternative_header_row(self):
        response = self.client.get(
            '/admin/testproject/alternativetimestampeditem/')
        content = force_text(response.content)
        six.assertRegex(self, content, r'Created at\s*</a></div>')
        six.assertRegex(self, content, r'Modified at\s*</a></div>')

    def test_single_header_row(self):
        response = self.client.get('/admin/testproject/singletimestampeditem/')
        content = force_text(response.content)
        six.assertRegex(self, content, r'Modified\s*</a></div>')

    def test_datestamp_header_row(self):
        response = self.client.get('/admin/testproject/datestampeditem/')
        content = force_text(response.content)
        six.assertRegex(self, content, r'Created\s*</a></div>')
        six.assertRegex(self, content, r'Modified\s*</a></div>')

    def test_null_timestamp_header_row(self):
        response = self.client.get('/admin/testproject/nulltimestampeditem/')
        content = force_text(response.content)
        six.assertRegex(self, content, r'Created\s*</a></div>')
        six.assertRegex(self, content, r'Modified\s*</a></div>')

    def test_null_timestamp_cell_values(self):
        response = self.client.get('/admin/testproject/nulltimestampeditem/')
        self.assertContains(response, '&nbsp;</td>', count=2)
