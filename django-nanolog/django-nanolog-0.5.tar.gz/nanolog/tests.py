from django.test import TestCase
from nanolog.models import Nanolog
from nanolog.utils import nanolog
from django.contrib.auth.models import User


class SimpleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                username='test', email='test@test', password='test')


    def test_nanolog(self):
        logs = Nanolog.objects.all()
        self.assertEquals(logs.count(), 0)

        nanolog('access', 'this_area')
        self.assertEquals(logs.count(), 1)
        self.assertEquals(logs[0].user, None)
        self.assertEquals(logs[0].log_type, 'access')
        self.assertEquals(logs[0].details, 'this_area')
        self.assertEquals(logs[0].note, None)
        self.assertEquals(logs[0].ip, None)
        self.assertEquals(logs[0].content_object, None)

        nanolog('access', '')
        self.assertEquals(logs.count(), 1)

        nanolog('', 'this_area')
        self.assertEquals(logs.count(), 1)

        nanolog('', '')
        self.assertEquals(logs.count(), 1)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter')
        self.assertEquals(logs.count(), 2)
        self.assertEquals(logs[0].user, None)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, None)
        self.assertEquals(logs[0].content_object, None)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter', self.user)
        self.assertEquals(logs.count(), 3)
        self.assertEquals(logs[0].user, self.user)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, None)
        self.assertEquals(logs[0].content_object, None)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter', self.user, '127.0.0.1')
        self.assertEquals(logs.count(), 4)
        self.assertEquals(logs[0].user, self.user)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, '127.0.0.1')
        self.assertEquals(logs[0].content_object, None)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter', self.user, 'wr.on.g.ip')
        self.assertEquals(logs.count(), 5)
        self.assertEquals(logs[0].user, self.user)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, None)
        self.assertEquals(logs[0].content_object, None)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter', self.user, '127.0.0.1', 'wrong_object')
        self.assertEquals(logs.count(), 6)
        self.assertEquals(logs[0].user, self.user)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, '127.0.0.1')
        self.assertEquals(logs[0].content_object, None)

        nanolog('changed_password', 'from:x|to:y', 'as we sugested in the newsletter', self.user, '127.0.0.1', self.user)
        self.assertEquals(logs.count(), 7)
        self.assertEquals(logs[0].user, self.user)
        self.assertEquals(logs[0].log_type, 'changed_password')
        self.assertEquals(logs[0].details, 'from:x|to:y')
        self.assertEquals(logs[0].note, 'as we sugested in the newsletter')
        self.assertEquals(logs[0].ip, '127.0.0.1')
        self.assertEquals(logs[0].content_object, self.user)
