from django.test import TestCase
from qanda.models import Question, Topic
from .common_data import (
        PUBLISHED_PUBLIC_SLUGS,
        PUBLISHED_MEMBER_SLUGS,
        PUBLISHED_STAFF_SLUGS,
        TOTAL_QUESTIONS_COUNT,
        PUBLIC_TOPIC_SLUGS,
        MEMBERS_TOPIC_SLUGS,
        STAFF_TOPIC_SLUGS,
        TOTAL_TOPIC_COUNT
        )

class PublishedQuestionMangerTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def test_total_question_count(self):
        self.assertEqual(Question.objects.count(), TOTAL_QUESTIONS_COUNT)

    def test_questions_visible_to_anonymous(self):
        qs = Question.published.for_anonymous()
        expected_slugs = PUBLISHED_PUBLIC_SLUGS
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))

    def test_questions_visible_to_members(self):
        qs = Question.published.for_members()
        expected_slugs = PUBLISHED_PUBLIC_SLUGS + PUBLISHED_MEMBER_SLUGS
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))

    def test_questions_visible_to_staff(self):
        qs = Question.published.all()
        expected_slugs = (
            PUBLISHED_PUBLIC_SLUGS +
            PUBLISHED_MEMBER_SLUGS +
            PUBLISHED_STAFF_SLUGS
            )
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))


class TopicManagerTestCase(TestCase):

    fixtures = ['qanda_test.json']

    def test_total_topic_count(self):
        self.assertEqual(Topic.objects.count(), TOTAL_TOPIC_COUNT)

    def test_topics_visible_to_anonymous(self):
        qs = Topic.objects.for_anonymous()
        expected_slugs = PUBLIC_TOPIC_SLUGS
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))

    def test_topics_visible_to_members(self):
        qs = Topic.objects.for_members()
        expected_slugs = MEMBERS_TOPIC_SLUGS
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))

    def test_topics_visible_to_staff(self):
        qs = Topic.objects.for_staff()
        expected_slugs = STAFF_TOPIC_SLUGS
        got_slugs = qs.values_list('slug', flat=True)
        try:
            self.assertItemsEqual(expected_slugs, got_slugs)
        except AttributeError:
            self.assertEqual(sorted(expected_slugs), sorted(got_slugs))


