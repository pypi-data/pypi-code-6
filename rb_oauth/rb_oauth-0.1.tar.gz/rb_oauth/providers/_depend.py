from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from reviewboard.hostingsvcs.github import GitHub as GithubService
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import URLRequest, urlopen
