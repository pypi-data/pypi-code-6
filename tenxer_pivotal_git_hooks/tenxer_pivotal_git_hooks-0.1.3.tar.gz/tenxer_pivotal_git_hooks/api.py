import requests
import subprocess

from tenxer_pivotal_git_hooks import utils


def request_url(method, path, params=None, data=None):
    base_url = 'https://www.pivotaltracker.com/services/v5/'
    url = base_url + path
    try:
        api_token = utils.execute_cmd('git config pivotal.token')
    except subprocess.CalledProcessError:
        msg = (
            'Enter your Pivotal Tracker API Token (you can find it by going '
            ' tohttps://www.pivotaltracker.com/profile): ')
        api_token = raw_input(msg)
        if not api_token:
            print "Cannot proceed with out an API token"
            return
        api_token = api_token.strip()
        utils.execute_cmd(
            'git config --global pivotal.token {}'.format(api_token))
    headers = {'X-TrackerToken': api_token}
    response = requests.request(
        method=method, url=url, data=data, headers=headers, params=params,
        verify=True)
    return response