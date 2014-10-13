from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .common_data import (
    MEMBERS_TOPIC_SLUGS,
    PUBLIC_TOPIC_SLUGS,
    STAFF_TOPIC_SLUGS,
    )


STAFF_TOPIC_SLUG = 'staff-and-members-topic'
STAFF_QUESTION_SLUGS = ['members-question-2', 'staff-question-2']
STAFF_QUESTION_SLUG = 'staff-question-2'
MEMBERS_QUESTION_SLUGS = ['members-question-2']
MEMBERS_QUESTION_SLUG = 'members-question-2'
MEMBERS_TOPIC_SLUG = 'staff-and-members-topic'
PUBLIC_QUESTION_SLUGS = ['public-question-1', 'public-question-2']
PUBLIC_QUESTION_SLUG = 'public-question-2'
PUBLIC_TOPIC_SLUG = 'public-topic'


class StaffUserTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def setUp(self):
        self.user = User.objects.create_user(
            'staffuser',
            'staff@example.com',
            'password',
            )
        self.user.save()
        self.user.is_staff = True
        self.user.save()
        self.client = Client()
        self.client.login(username='staffuser', password='password')

    def test_staff_topiclist(self):
        response = self.client.get(reverse('qanda.views.topiclist'))
        self.assertEqual(response.context['user'].is_staff, True)

        self.assertEqual(response.status_code, 200)
        got_topics = response.context['object_list']
        got_slugs = [t.slug for t in got_topics]
        try:
            self.assertItemsEqual(STAFF_TOPIC_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(STAFF_TOPIC_SLUGS), sorted(got_slugs))

    def test_staff_topicdetail(self):
        response = self.client.get(reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': 'staff-and-members-topic'}
            ))
        self.assertEqual(response.status_code, 200)
        got_questions = response.context['question_list']
        got_slugs = [q.slug for q in got_questions]
        try:
            self.assertItemsEqual(STAFF_QUESTION_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(STAFF_QUESTION_SLUGS), sorted(got_slugs))

    def test_staff_questiondetail(self):
        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': STAFF_TOPIC_SLUG,
                'question_slug': STAFF_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']
        self.assertEqual(obj.slug, STAFF_QUESTION_SLUG)
        self.assertEqual(obj.topic.slug, STAFF_TOPIC_SLUG)


class MemberUserTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def setUp(self):
        self.user = User.objects.create_user(
            'memberuser',
            'member@example.com',
            'password',
            )
        self.user.save()
        self.client = Client()
        self.client.login(username='memberuser', password='password')

    def test_member_topiclist(self):
        response = self.client.get(reverse('qanda.views.topiclist'))
        self.assertFalse(response.context['user'].is_staff)
        self.assertTrue(response.context['user'].is_authenticated())

        self.assertEqual(response.status_code, 200)
        got_topics = response.context['object_list']
        got_slugs = [t.slug for t in got_topics]
        try:
            self.assertItemsEqual(MEMBERS_TOPIC_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(MEMBERS_TOPIC_SLUGS), sorted(got_slugs))

    def test_member_topicdetail(self):
        response = self.client.get(reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': 'staff-and-members-topic'}
            ))

        self.assertEqual(response.status_code, 200)
        got_questions = response.context['question_list']
        got_slugs = [q.slug for q in got_questions]
        try:
            self.assertItemsEqual(MEMBERS_QUESTION_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(MEMBERS_QUESTION_SLUGS), sorted(got_slugs))

    def test_member_topicdetail_noaccess(self):
        response = self.client.get(reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': 'staff-topic'}
            ))
        self.assertEqual(response.status_code, 404)

    def test_member_questiondetail(self):
        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': MEMBERS_TOPIC_SLUG,
                'question_slug': MEMBERS_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']
        self.assertEqual(obj.slug, MEMBERS_QUESTION_SLUG)
        self.assertEqual(obj.topic.slug, MEMBERS_TOPIC_SLUG)

    def test_member_questiondetail_noaccess(self):
        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': STAFF_TOPIC_SLUG,
                'question_slug': STAFF_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 404)


class AnonymousUserTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def setUp(self):
        self.client = Client()

    def test_anonymous_topiclist(self):
        response = self.client.get(reverse('qanda.views.topiclist'))
        self.assertFalse(response.context['user'].is_authenticated())

        self.assertEqual(response.status_code, 200)
        got_topics = response.context['object_list']
        got_slugs = [t.slug for t in got_topics]
        try:
            self.assertItemsEqual(PUBLIC_TOPIC_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(PUBLIC_TOPIC_SLUGS), sorted(got_slugs))

    def test_anonymous_topicdetail(self):
        response = self.client.get(reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': 'public-topic'}
            ))
        self.assertEqual(response.status_code, 200)
        got_questions = response.context['question_list']
        got_slugs = [q.slug for q in got_questions]
        try:
            self.assertItemsEqual(PUBLIC_QUESTION_SLUGS, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(PUBLIC_QUESTION_SLUGS), sorted(got_slugs))

    def test_anonymous_topicdetail_noaccess(self):
        response = self.client.get(reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': 'staff-and-members-topic'}
            ))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_questiondetail(self):
        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': PUBLIC_TOPIC_SLUG,
                'question_slug': PUBLIC_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 200)
        obj = response.context['object']
        self.assertEqual(obj.slug, PUBLIC_QUESTION_SLUG)
        self.assertEqual(obj.topic.slug, PUBLIC_TOPIC_SLUG)

    def test_anonymous_questiondetail_noaccess(self):
        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': STAFF_TOPIC_SLUG,
                'question_slug': STAFF_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': MEMBERS_TOPIC_SLUG,
                'question_slug': MEMBERS_QUESTION_SLUG
                }
            ))
        self.assertEqual(response.status_code, 404)
