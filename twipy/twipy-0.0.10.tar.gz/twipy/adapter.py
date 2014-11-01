# -*- coding: utf-8 -*-

import models
import json


class Adapter():

    def __init__(self):
        self._user_obj = None
        self._status_obj = None
        self._dm_obj = None

    def _get_status_object(self, dict_status):
        self._status_obj = models.Status(
            id_str=dict_status['id_str'],
            text=dict_status['text'],
            in_reply_to_status_id=dict_status['in_reply_to_status_id'],
            in_reply_to_user_id=dict_status['in_reply_to_user_id'],
            user=self._get_user_object(dict_status['user']),
            retweet_count=dict_status['retweet_count'],
            is_favorite=dict_status['favorited'],
            is_retweet=dict_status['retweeted'],
            created_at=dict_status['created_at']
        )

        return self._status_obj

    def _get_user_object(self, dict_user):
        self._user_obj = models.User(
            id_str=dict_user['id_str'],
            name=dict_user['name'],
            screen_name=dict_user['screen_name'],
            description=dict_user['description'],
            url=dict_user['url'],
            created_at=dict_user['created_at'],
            friends_count=dict_user['friends_count'],
            followers_count=dict_user['followers_count'],
            favourites_count=dict_user['favourites_count']
        )

        return self._user_obj

    def _get_dm_object(self, dict_dm):
        self._dm_obj = models.DirectMessage(
            id_str=dict_dm['id_str'],
            created_at=dict_dm['created_at'],
            sender_screen_name=dict_dm['sender_screen_name'],
            recipient_screen_name=dict_dm['recipient_screen_name'],
            text=dict_dm['text']
        )

        return self._dm_obj

    def create_dm_timeline_object(self, dict_content):
        timeline = models.Timeline()
        json_content = json.loads(dict_content)

        for content in json_content:
            direct_message = self._get_dm_object(content)
            timeline.add(direct_message)

        return timeline

    def create_timeline_object(self, dict_content):
        timeline = models.Timeline()
        json_content = json.loads(dict_content)

        for content in json_content:
            status = self._get_status_object(content)
            timeline.add(status)

        return timeline


class CliAdapter():

    def __init__(self, timeline):
        self._timeline = timeline

    def _print_status(self, status):
        print '(%s) %s: %s' % (status.c_id, status.user.screen_name, status.text)  # pragma: no cover

    def _print_dm(self, dm):
        print '(%s) %s: %s' % (dm.c_id, dm.sender_screen_name, dm.text)  # pragma: no cover

    def get_statuses(self):
        for status in self._timeline.statuses:  # pragma: no cover
            self._print_status(status)  # pragma: no cover

    def get_status_from_id(self, c_id):
        return self._timeline.statuses[c_id]

    def get_direct_messages(self):
        for dm in self._timeline.statuses:  # pragma: no cover
            self._print_dm(dm)  # pragma: no cover
