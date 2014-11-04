import requests
import subprocess

from tenxer_pivotal_git_hooks import utils


def get_api_token():
    api_token = None
    try:
        api_token = utils.execute_cmd('git config pivotal.token')
    except subprocess.CalledProcessError:
        pass

    if not api_token or len(api_token) < 10:
        msg = (
            'Enter your Pivotal Tracker API Token, you can find it by going '
            ' to https://www.pivotaltracker.com/profile: ')
        api_token = utils.get_input(msg)
        if not api_token:
            print "Cannot proceed with out an API token\n"
            return
        api_token = api_token.strip()
        utils.execute_cmd(
            'git config pivotal.token {}'.format(api_token))
        utils.execute_cmd(
            'git config --global pivotal.token {}'.format(api_token))

    return api_token


def request_url(method, path, params=None, data=None):
    base_url = 'https://www.pivotaltracker.com/services/v5/'
    url = base_url + path
    api_token = get_api_token()
    headers = {'X-TrackerToken': api_token}
    response = requests.request(
        method=method, url=url, data=data, headers=headers, params=params,
        verify=True)
    return response