from django.test import TestCase
from qanda.models import Question, Topic

PUBLISHED_PUBLIC_SLUGS = ['public-question-1', 'public-question-2']
PUBLISHED_MEMBER_SLUGS = ['members-question-1', 'members-question-2']
PUBLISHED_STAFF_SLUGS = ['staff-question-1', 'staff-question-2', 'staff-question-4']
TOTAL_QUESTIONS_COUNT = 12

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



PUBLIC_TOPIC_SLUGS = ['public-topic']
MEMBERS_TOPIC_SLUGS = [
    'members-topic',
    'public-topic',
    'staff-and-members-topic',
    ]
STAFF_TOPIC_SLUGS = [
    'members-topic',
    'mixed-topic',
    'public-topic',
    'staff-and-members-topic',
    'staff-topic',
    ]
TOTAL_TOPIC_COUNT = 5


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


