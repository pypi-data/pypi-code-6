"""
A library for Stack Overflow question notifications.
"""
__author__ = 'Matt Deacalion Stevens'
__version__ = '0.2.1'

import re
import time
import urllib.parse
import json
import requests


class RulesMixin:
    """
    A mixin that can provides validation 'rules' to a Question. These rules are
    properties and if they all return True the question is considered valid.
    """
    @property
    def is_not_answered(self):
        """
        Return True if this question has no answers.
        """
        return not self.answered

    @property
    def is_new(self):
        """
        Return True if the question is less than 6 hours old.
        """
        return self.creation_date > time.time() - (60 * 60 * 6)

    @property
    def is_including_positive_tags(self):
        """
        Question is tagged with at least one of our `positive` tags.
        """
        return any(tag in self.tags for tag in self.get_positive_tags())

    @property
    def is_excluding_negative_tags(self):
        """
        Question does not contain a single `negative` tag.
        """
        negative_tags = self.get_negative_tags()

        if not negative_tags:
            return True

        return not any(tag in self.tags for tag in negative_tags)


class QuestionMetaClass(type):
    """
    Find all the methods within the `Question` class beginning with `is_` and
    adds them to the `rules` attribute. This is so all of the `rules` can be
    dynamically run at once.
    """
    def __new__(cls, name, bases, attrs):
        attrs['rules'] = cls.get_rules(bases[0].__dict__) if bases else {}
        attrs['rules'].update(cls.get_rules(attrs))

        return type.__new__(cls, name, bases, attrs)

    def get_rules(attrs):
        return {k: v for k, v in attrs.items() if k.startswith('is_')}


class Question(metaclass=QuestionMetaClass):
    """
    An entity to contain a single question from any Stack Exchange web site.
    Also has methods of validating and classifying itself.
    """
    positive_tags = []
    negative_tags = []

    def __init__(self, *args, **kwargs):
        # first lets grab the tags for this question
        self.tags = kwargs.pop('tags', [])

        # …then we grab everything else
        question_attributes = [
            'question_id',
            'title',
            'link',
            'score',
            'answered',
            'view_count',
            'creation_date',
            'text',
            'owner_id',
            'owner_display_name',
            'owner_link',
            'owner_reputation',
            'owner_accept_rate',
        ]

        for attribute in question_attributes:
            setattr(self, attribute, kwargs.get(attribute))

    def __getitem__(self, attribute):
        """
        Allow attributes to be accessible in the same way as a dict.
        """
        return getattr(self, attribute)

    @classmethod
    def from_dict(cls, question_dict):
        """
        Takes a dict and returns a `Question` instance. Maps the attributes
        used in Stack Exchange JSON responses to the attributes in `Question`.
        """
        owner = question_dict.pop('owner')

        question_dict['owner_id'] = owner.get('user_id', 0)
        question_dict['owner_display_name'] = owner.get('display_name', '')
        question_dict['owner_link'] = owner.get('link', '')
        question_dict['owner_reputation'] = owner.get('reputation', 0)
        question_dict['owner_accept_rate'] = owner.get('accept_rate', 0)
        question_dict['answered'] = question_dict.get('is_answered')

        return cls(**question_dict)

    @classmethod
    def from_list(cls, question_list):
        """
        Takes a list of dicts and returns a list of `Question` instances.
        """
        return [cls.from_dict(question) for question in question_list]

    @property
    def adheres_to_rules(self):
        """
        Return True if all properties whose name begins with `is_` return True.
        """
        return all([getattr(self, prop) for prop in self.rules])

    def get_short_link(self):
        """
        Returns the StackExchange URL without the text.
        """
        short_link = re.match('http://([^/]+/){2}\d+/', self.link)

        if short_link:
            return short_link.group()

        return self.link

    def get_short_title(self, length=50):
        """
        Returns the question title truncated to `length`.
        """
        if len(self.title) > length:
            return self.title[:length] + '…'

        return self.title

    def get_positive_tags(self):
        """
        Returns a list of tags that we consider `positive`, that is tags that
        we are interested in.
        """
        return self.positive_tags

    def get_negative_tags(self):
        """
        Returns a list of tags that we consider `negative`, that is tags that
        we are not interested in and want to filter out.
        """
        return self.negative_tags


class Retriever:
    """
    Responsible for retrieving the questions from a Stack Exchange web site
    and creating `Question` instances with the results.
    """
    api_version = '2.2'
    base_url = 'http://api.stackexchange.com/{}/questions'
    base_params = {'order': 'desc', 'sort': 'creation'}

    def __init__(
        self,
        interval=60,
        tag=None,
        site='stackoverflow',
        question_cls=Question,
        bookmark=None,
    ):
        self.params = dict(site=site, **self.get_base_params())

        if tag:
            self.params['tagged'] = tag

        self.interval = interval
        self.last_retrieved = 0
        self.question_cls = question_cls
        self.bookmark = bookmark
        self._active = True

    @property
    def feed_url(self):
        """
        Builds and returns the StackExchange API URL with the querystring.
        """
        return '?'.join([
            self.get_base_url(),
            urllib.parse.urlencode(self.params),
        ])

    @property
    def delay_is_active(self):
        """
        Returns True if we are currently in the delay 'window'.
        """
        return self.last_retrieved > time.time() - self.interval

    def get_base_params(self):
        """
        Returns a list of the default parameters to use in the API URL.
        """
        return self.base_params

    def get_base_url(self):
        """
        Returns the base URL to use in constructing the API URL.
        """
        return self.base_url.format(self.get_api_version())

    def get_api_version(self):
        """
        Returns the Stack Exchange API version to use as a string.
        """
        return self.api_version

    def _get_feed(self):
        """
        Retrieves the question feed and saves the time it happened.
        """
        self.last_retrieved = time.time()
        return requests.get(self.get_base_url(), params=self.params)

    def _parse_response(self, response):
        """
        Takes a HTTP requests response object, extracts the questions from it
        and returns a list of question dicts.
        """
        return json.loads(response.content.decode())['items']

    def _get_questions_from_feed(self):
        """
        Returns an array of `Question` instances that have been created from
        the feed response.
        """
        response = self._get_feed()
        return self.question_cls.from_list(self._parse_response(response))

    def _filter_new_questions(self, questions):
        """
        Takes a list of Question objects and returns only the new ones.
        """
        if not questions:
            return []

        new_questions = []

        for question in questions:
            if question['question_id'] == self.bookmark:
                break

            new_questions.append(question)

        self.bookmark = questions[0]['question_id']

        return new_questions

    def disable_retriever(self):
        """
        Disables the `Question` generator from retrieving anymore questions.
        """
        self._active = False

    def enable_retriever(self):
        """
        Enables the `Question` generator, on by default.
        """
        self._active = True

    def questions(self):
        """
        Generator that returns `Question` objects.
        """
        while self._active:
            while self.delay_is_active:
                time.sleep(1)

            questions = self._get_questions_from_feed()
            new_questions = self._filter_new_questions(questions)

            for new_question in new_questions:
                yield new_question


class Notifier:
    """
    Contains methods of notifying the user about certain types of question.
    """
    pass
