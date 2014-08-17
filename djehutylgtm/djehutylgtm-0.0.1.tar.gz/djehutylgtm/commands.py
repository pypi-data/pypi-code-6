import requests

from djehuty.command import Command


class LGTM(Command):
    '''show random LGTM URL'''

    def take_action(self, parsed_args):
        return requests.get(
            'http://www.lgtm.in/g',
            headers={'accept': 'application/json'}
        ).json().get('imageUrl', 'LGTM URL not found.')
