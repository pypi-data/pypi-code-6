# -*- coding: utf-8 -*-
"""
Class and function for the voting system.
"""

from operator import attrgetter

from openslides.config.api import config

from .models import Category


class Hoechstzahl(object):
    """
    An object represents one hoechstzahl in the Sainte-Laguë method.
    """
    all_hoechstzahls = []

    def __init__(self, category, rank):
        try:
            self.topic = category.topic_set.order_by('-votes', '-weight')[rank]
        except IndexError:
            return
        else:
            self.__class__.all_hoechstzahls.append(self)
        divisor = rank * 2 + 1
        self.value = float(category.sum_of_votes) / divisor

    @classmethod
    def get_results(cls):
        """
        Generator to get all hoechstzahl objects in the winning order.
        """
        cls.all_hoechstzahls.sort(key=attrgetter('value', 'topic.category.weight'), reverse=True)
        for hoechstzahl in cls.all_hoechstzahls:
            yield hoechstzahl

    @classmethod
    def get_winning_topics(cls):
        """
        Returns a dictionary containing all winning topics and the warning
        flags for the result slide and views.
        """
        results_generator = cls.get_results()
        winning_hoechstzahls = []
        for i in range(config['openslides_topicvoting_posts']):
            try:
                winning_hoechstzahls.append(results_generator.next())
            except StopIteration:
                topic_post_warning = True
                runoff_poll_warning = False
                break
        else:
            topic_post_warning = False
            try:
                first_looser_hoechstzahl = results_generator.next()
            except StopIteration:
                runoff_poll_warning = False
            else:
                # First runoff poll check: Check equal hoechstzahls between the categories.
                if (first_looser_hoechstzahl.value == winning_hoechstzahls[-1].value and
                        first_looser_hoechstzahl.topic.category.weight == winning_hoechstzahls[-1].topic.category.weight):
                    runoff_poll_warning = True
                else:
                    runoff_poll_warning = False
        winning_topics = map(lambda hoechstzahl: hoechstzahl.topic, winning_hoechstzahls)
        return {'winning_topics': winning_topics,
                'topic_post_warning': topic_post_warning,
                'runoff_poll_warning': runoff_poll_warning}

    @classmethod
    def get_result_table_and_info(cls):
        """
        Returns a dictionary with a nested list (table) with all
        hoechstzahls ordered by value. This table has only as many columns
        as there are posts (minimum 3). Returns also some info flags for
        the results view and slide.
        """
        winning_dict = cls.get_winning_topics()
        winning_topics = winning_dict['winning_topics']
        runoff_poll_warning = winning_dict['runoff_poll_warning']

        # Create table
        result_table = []
        all_categories = sorted(Category.objects.all(), key=attrgetter('sum_of_votes', 'weight'), reverse=True)
        for category in all_categories:
            category_hoechstzahls = filter(lambda hoechstzahl: hoechstzahl.topic.category == category, cls.all_hoechstzahls)
            category_hoechstzahls.sort(key=lambda hoechstzahl: hoechstzahl.value, reverse=True)
            runoff_poll_warning = second_runoff_poll_check(runoff_poll_warning, category_hoechstzahls, winning_topics)
            category_hoechstzahls += (max(config['openslides_topicvoting_posts'], 3) - len(category_hoechstzahls)) * [None]
            result_table.append(category_hoechstzahls)

        # Return table and flags as dictionary
        return {'result_table': result_table,
                'winning_topics': winning_topics,
                'runoff_poll_warning': runoff_poll_warning,
                'topic_post_warning': winning_dict['topic_post_warning']}


def feed_hoechstzahls():
    """
    Initialize all hoechstzahls by parsing the first topics of all categories.
    The number of posts indicates how many topics are parsed.
    """
    # Clear existing hoechstzahls
    Hoechstzahl.all_hoechstzahls = []
    # Feed them
    for category in Category.objects.all():
        for rank in range(max(config['openslides_topicvoting_posts'], 3)):
            Hoechstzahl(category=category, rank=rank)


def second_runoff_poll_check(runoff_poll_warning, category_hoechstzahls, winning_topics):
    """
    Second runoff poll check: Check equal votes inside a category.
    """
    if not runoff_poll_warning:
        for number, hoechstzahl in enumerate(category_hoechstzahls):
            if number > 0:
                predecessor = category_hoechstzahls[number-1]
                if (hoechstzahl.topic not in winning_topics and
                        predecessor.topic in winning_topics and
                        hoechstzahl.topic.votes == predecessor.topic.votes and
                        hoechstzahl.topic.weight == predecessor.topic.weight):
                    runoff_poll_warning = True
                    break
    return runoff_poll_warning
