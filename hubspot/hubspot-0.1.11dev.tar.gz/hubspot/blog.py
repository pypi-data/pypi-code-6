from hubspot.hsapi import HSApi
import requests


class Blog:

    def __init__(self, parent):
        self.cms = CMS(parent)
        self.cos = COS(parent)


class CMS(HSApi):
    URL = "https://api.hubapi.com/blog/v1"

    def get_posts(self, guid):
        url = self.URL + "/{guid}/posts.json".format(guid=guid)

        params = self.add_authentication({})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    def get_blog_list(self):
        url = self.URL + "/list.json"

        params = self.add_authentication({})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()
        else:
            return False

    @staticmethod
    def to_cos(data, target_portal):
        author_id = target_portal.blog.cos.get_author_id(data['authorDisplayName'])
        translated_data = {
            "blog_author_id": author_id,
            "is_draft": data['draft'],
            "meta_description": data['metaDescription'],
            "meta_keywords": data['metaKeywords'],
            "name": data['name'],
            "post_body": data['body'],
            "post_summary": data['summary'],
            "publish_date": data['publishTimestamp'],
        }
        translated_data = dict((k, v) for k, v in translated_data.items() if v)
        return translated_data


class COS(HSApi):
    URL = "https://api.hubapi.com/blog/v2"

    def post(self, data, target_portal):
        url = self.URL + "/blog-posts"

        params = target_portal.add_authentication({})

        r = requests.put(url, params=params, data=data)

        if r.status_code is 200:
            return True
        else:
            return False

    def get_author_id(self, name, target_portal):
        url = self.URL + "/blog-authors"

        params = target_portal.add_authentication({"full_name": name})

        r = requests.get(url, params=params)

        if r.status_code is 200:
            return r.json()['objects'][0]['id']
        else:
            return False