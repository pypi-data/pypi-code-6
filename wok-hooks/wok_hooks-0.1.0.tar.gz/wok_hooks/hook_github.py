import logging
from wok_hooks.misc import Configuration as _Configuration

DEFAULTS = {'user': ''}

from activitystreams import Activity, PostActivity, Object as ActivityObject
from activitystreams.atom import make_activities_from_feed
import urllib2
import xml.etree.ElementTree
import re
from bs4 import BeautifulSoup, NavigableString, Tag
from wok_hooks.timeline import Post as TimelineUpdate

GITHUB_PREFIX = "{http://github.dummy/activitystream/}"
GITHUB_PUSH = GITHUB_PREFIX + 'push'
GITHUB_PULL_REQUEST = GITHUB_PREFIX + 'pull-request'
GITHUB_FORK = GITHUB_PREFIX + 'fork'
GITHUB_CREATE = GITHUB_PREFIX + 'create'
ATOM_GITHUB_PUSH = re.compile('tag:github.com,2008:PushEvent/')
ATOM_GITHUB_PULL_REQUEST = re.compile('tag:github.com,2008:PullRequestEvent/')
ATOM_GITHUB_FORK = re.compile('tag:github.com,2008:ForkEvent/')
ATOM_GITHUB_CREATE = re.compile('tag:github.com,2008:CreateEvent/')
ATOM_GITHUB_WATCH = re.compile('tag:github.com,2008:WatchEvent/')
ATOM_GITHUB_ISSUES = re.compile('tag:github.com,2008:IssuesEvent/')
ATOM_GITHUB_ISSUE_COMMENT = re.compile('tag:github.com,2008:IssueCommentEvent/')


class Configuration(_Configuration):
    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class PushObject(ActivityObject):
    def __init__(self, base_object):
        ActivityObject.__init__(self, id=base_object.id, url=base_object.url)
        self.project = None
        self.branch = None
        self.commits = []

        soup = BeautifulSoup(base_object.content)
        title_soup = soup.find('div', {'class': 'title'})
        for index, segment in enumerate(title_soup.contents):
            if isinstance(segment, NavigableString) and segment.strip() == 'to':
                self.branch = title_soup.contents[index + 1].text
            if isinstance(segment, NavigableString) and segment.strip() == 'at':
                self.owner, self.project = title_soup.contents[index + 1].text.split('/')
                self.repository_url = 'https://github.com/%s/%s' % (self.owner, self.project)
        push_user = title_soup.contents[1].text
        detail_soup = soup.find('div', {'class': 'details'})
        items = detail_soup.find('ul')
        if items:
            for item in items:
                if isinstance(item, Tag):
                    commit = item.find('a')['href']
                    message = item.find('div', {'class': 'message'})
                    if not message:
                        logging.info('commit without message')
                    elif item.contents[1]['title'] != push_user:
                        logging.info('ignore foreign commit')
                    else:
                        message = message.text.strip()
                        self.commits.append(('http://github.com%s' % commit, message))


class PullRequestObject(ActivityObject):
    def __init__(self, base_object):
        ActivityObject.__init__(self,
                                id=base_object.id,
                                url=base_object.url)
        self.owner, self.project, self.issue = None, None, None

        soup = BeautifulSoup(base_object.content)
        title_soup = soup.find('div', {'class': 'title'})
        for index, segment in enumerate(title_soup.contents):
            if isinstance(segment, NavigableString) and segment.strip() == 'pull request':
                self.owner, self.project = title_soup.contents[index + 1].text.split('/')
                self.project, self.issue = self.project.split('#')
                self.repository_url = 'https://github.com/%s/%s' % (self.owner, self.project)


class ForkObject(ActivityObject):
    def __init__(self, base_object):
        ActivityObject.__init__(self, id=base_object.id, url=base_object.url)
        self.owner, self.project = None, None

        soup = BeautifulSoup(base_object.content)
        title_soup = soup.find('div', {'class': 'title'})
        for index, segment in enumerate(title_soup.contents):
            if isinstance(segment, NavigableString) and segment.strip() == 'to':
                self.owner, self.project = title_soup.contents[index - 1].text.split('/')
                self.repository_url = 'https://github.com/%s/%s' % (self.owner, self.project)


class CreateObject(ActivityObject):
    def __init__(self, base_object):
        ActivityObject.__init__(self, id=base_object.id, url=base_object.url)
        self.owner, self.project = None, None

        soup = BeautifulSoup(base_object.content)
        title_soup = soup.find('div', {'class': 'title'})
        for index, segment in enumerate(title_soup.contents):
            if isinstance(segment, NavigableString) and segment.strip() == 'branch':
                self.owner, self.project = title_soup.contents[index + 3].text.split('/')
                self.branch_name = title_soup.contents[index + 1].text
                self.object_url = 'https://github.com%s' % title_soup.contents[index + 1]['href']
                self.repository_url = 'https://github.com/%s/%s' % (self.owner, self.project)
                self.project = '/'.join([self.project, self.branch_name])
                self.object_type = segment.strip()
            if isinstance(segment, NavigableString) and segment.strip() == 'repository':
                self.owner, self.project = title_soup.contents[index + 1]['title'].split('/')
                self.object_url = 'https://github.com%s' % title_soup.contents[index + 1]['href']
                self.repository_url = self.object_url
                self.object_type = segment.strip()


class PushActivity(Activity):
    def __init__(self, activity):
        Activity.__init__(self, activity.actor, PushObject(activity.object), activity.target, GITHUB_PUSH,
                          activity.time, activity.generator, activity.icon_url, activity.service_provider,
                          activity.links)


class PullRequestActivity(Activity):
    def __init__(self, activity):
        Activity.__init__(self, activity.actor, PullRequestObject(activity.object), activity.target,
                          GITHUB_PULL_REQUEST, activity.time, activity.generator, activity.icon_url,
                          activity.service_provider, activity.links)


class ForkActivity(Activity):
    def __init__(self, activity):
        Activity.__init__(self, activity.actor, ForkObject(activity.object), activity.target, GITHUB_FORK,
                          activity.time, activity.generator, activity.icon_url, activity.service_provider,
                          activity.links)


class CreateActivity(Activity):
    def __init__(self, activity):
        Activity.__init__(self, activity.actor, CreateObject(activity.object), activity.target, GITHUB_CREATE,
                          activity.time, activity.generator, activity.icon_url, activity.service_provider,
                          activity.links)


def github_id_to_wok_slug(base_object):
    slug = base_object.id.replace('tag:', '').replace('.', '-').replace(',', '-').replace('/', '-').replace(':',
                                                                                                            '-').lower()
    return slug


class PushPost(TimelineUpdate):
    def __init__(self, base_object, time):
        assert isinstance(base_object, PushObject)

        slug = github_id_to_wok_slug(base_object)
        title = 'worked on %s' % base_object.project
        url = base_object.url
        content = 'worked on [%s](%s)\n' % (base_object.project, base_object.repository_url)

        for commit, message in base_object.commits:
            content = '%s\n - %s' % (content, message)

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show changes', url))
        self.actions.append(('show project', base_object.repository_url))


class PullRequestPost(TimelineUpdate):
    def __init__(self, base_object, time):
        assert isinstance(base_object, PullRequestObject)

        slug = github_id_to_wok_slug(base_object)
        title = 'requested to pull %s fork' % base_object.project
        url = base_object.url
        content = '[requested](%s) to pull [%s](%s) fork' % (
            base_object.url, base_object.project, base_object.repository_url)

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show request', url))
        self.actions.append(('show project', base_object.repository_url))


class ForkPost(TimelineUpdate):
    def __init__(self, base_object, time):
        assert isinstance(base_object, ForkObject)

        slug = github_id_to_wok_slug(base_object)
        title = 'forked %s' % base_object.project
        url = base_object.url
        content = 'forked [%s](%s)' % (base_object.project, base_object.repository_url)

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show project', url))


class CreatePost(TimelineUpdate):
    def __init__(self, base_object, time):
        assert isinstance(base_object, CreateObject)

        slug = github_id_to_wok_slug(base_object)
        title = 'created %s' % base_object.project
        url = base_object.url
        content = 'created [%s](%s) %s' % (base_object.project, base_object.object_url, base_object.object_type)
        content = content.strip()

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show project', base_object.repository_url))


def add_github_activities_to_timeline(options, content_dir='./content/timeline/'):
    config = Configuration('github.config')
    assert config['user'], 'user must be set in github.config'
    url = '%s%s.atom' % ('https://github.com/', config['user'])
    # req = urllib2.Request(url, {}, {'Content-Type': 'application/atom+xml'})

    logging.info('read %s', url)
    response = urllib2.urlopen(url)
    contents = response.read()

    #import HTMLParser
    #contents = HTMLParser.HTMLParser().unescape(contents)

    xml_tree = xml.etree.ElementTree.fromstring(contents)
    xml_tree.getroot = lambda: xml_tree
    activities = make_activities_from_feed(xml_tree)
    for activity in activities:
        try:
            if isinstance(activity, PostActivity):

                if activity.object.content is None:
                    logging.debug('empty git activity %s', activity.object)
                    continue

                if activity.object and ATOM_GITHUB_PUSH.search(activity.object.id):
                    activity = PushActivity(activity)
                    post = PushPost(activity.object, activity.time)
                    post.save(content_dir)
                elif activity.object and ATOM_GITHUB_PULL_REQUEST.search(activity.object.id):
                    activity = PullRequestActivity(activity)
                    post = PullRequestPost(activity.object, activity.time)
                    post.save(content_dir)
                elif activity.object and ATOM_GITHUB_FORK.search(activity.object.id):
                    activity = ForkActivity(activity)
                    post = ForkPost(activity.object, activity.time)
                    post.save(content_dir)
                elif activity.object and ATOM_GITHUB_CREATE.search(activity.object.id):
                    activity = CreateActivity(activity)
                    post = CreatePost(activity.object, activity.time)
                    post.save(content_dir)
                elif activity.object and ATOM_GITHUB_WATCH.search(activity.object.id):
                    pass  # ingore watch
                elif activity.object and ATOM_GITHUB_ISSUES.search(activity.object.id):
                    pass  # ingore issues
                elif activity.object and ATOM_GITHUB_ISSUE_COMMENT.search(activity.object.id):
                    pass  # ingore issues
                else:
                    logging.debug('unexpected post object')
            else:
                logging.debug('unknwon github activity verb %s' % activity.verb)
        except IOError as ex:
            print ex


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    # import os
    #os.chdir('..')
    add_github_activities_to_timeline({}, '/tmp/')
