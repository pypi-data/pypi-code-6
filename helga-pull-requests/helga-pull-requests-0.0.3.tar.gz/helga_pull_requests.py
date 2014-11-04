from helga import settings
from helga.plugins import match


@match(r'(([\w\-\.]+?)/)?([\w\-\.]+?)-pr([\d]+)')
def pull_requests(client, channel, nick, message, matches):
    prs = []
    for _, org, repo, pr in matches:
        org = org or getattr(settings, 'PULL_REQUESTS_DEFAULT_ACCOUNT', '')

        if not org:
            continue

        prs.append(u'https://github.com/{org}/{repo}/pull/{pr}'.format(org=org, repo=repo, pr=pr))

    if not prs:
        return None

    return u'{0} might be talking about pull request: {1}'.format(nick, ', '.join(prs))
