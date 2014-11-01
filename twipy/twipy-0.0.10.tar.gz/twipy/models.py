# -*- coding: utf-8 -*-


class User():

    def __init__(self,
                 id_str,
                 name,
                 screen_name,
                 description,
                 url,
                 created_at,
                 friends_count,
                 followers_count,
                 favourites_count):
        self.id_str = id_str
        self.name = name
        self.screen_name = screen_name
        self.description = description
        self.url = url
        self.created_at = created_at
        self.friends_count = friends_count
        self.followers_count = followers_count
        self.favourites_count = favourites_count

    def __str__(self):
        return str(self.id_str)


class Status():

    def __init__(self,
                 id_str,
                 created_at,
                 user,
                 text,
                 in_reply_to_user_id='',
                 in_reply_to_status_id=None,
                 is_retweet=False,
                 retweet_count=0,
                 is_favorite=False):
        self.c_id = None
        self.id_str = id_str
        self.created_at = created_at
        self.user = user
        self.text = text
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_status_id = in_reply_to_status_id
        self.is_retweet = is_retweet
        self.retweet_count = retweet_count
        self.is_favorite = is_favorite

    def __str__(self):
        return str(self.id_str)


class Timeline():

    def __init__(self):
        self.statuses = []
        self.count = 0

    def add(self, status):
        if not status:
            raise Exception('Status is null')

        status.c_id = self.count
        self.count += 1
        self.statuses.append(status)

    def remove(self, status):
        try:
            self.statuses.remove(status)
        except ValueError as e:
            print 'Error deleting tweet with id ' + status.id_str


class DirectMessage():

    def __init__(self,
                 id_str,
                 created_at,
                 sender_screen_name,
                 recipient_screen_name,
                 text):
        self.id_str = id_str
        self.created_at = created_at
        self.sender_screen_name = sender_screen_name
        self.recipient_screen_name = recipient_screen_name
        self.text = text

    def __str__(self):
        return str(self.id_str)
