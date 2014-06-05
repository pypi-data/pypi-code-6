from urllib import urlencode

from pyrate.main import Pyrate


class GoogleAnalyticsPyrate(Pyrate):
    # request
    base_url = 'https://www.googleapis.com/analytics/v3/'
    default_header_content = None
    default_body_content = None
    auth_data = {'type': 'MANUAL'}
    send_json = False

    # response
    response_formats = []
    default_response_format = None
    validate_response = True

    connection_check = {'http_method': 'GET', 'target': 'account/info'}

    def __init__(self, token, default_response_format=None):
        super(GoogleAnalyticsPyrate, self).__init__()
        self.auth_data['token'] = token
        self.default_header_content = {
            'Authorization': 'Bearer %s' % token
        }

        if default_response_format or default_response_format == '':
            self.default_response_format = default_response_format

    def get_profiles(self, accountId=None, webPropertyId=None):
        if not accountId:
            accountId = '~all'
        if not webPropertyId:
            webPropertyId = '~all'

        return self.get('management/accounts/%s/webproperties/%s/profiles' % (accountId, webPropertyId))

    def get_data(self, ids, start_date, end_date, metrics, dimensions=None):
        target = 'data/ga?ids=ga:%s&start-date=%s&end-date=%s&metrics=' % (str(ids), start_date, end_date)
        for metric in metrics:
            target += '%s,' % metric
        # remove last trailing comma
        target = target[:-1]

        if dimensions:
            target += '&dimensions='
            for dimension in dimensions:
                target += '%s,' % dimension
            # remove last trailing comma
            target = target[:-1]

        return self.get(target)

'''
    def get_lists(self, modified_since=None):
        # modified_since in ISO-8601 eg: 2014-02-17T08:22:10+00:00
        target = 'lists'
        if modified_since:
            target += '?modified_since=%s' % urlencode(modified_since)

        return self.get(target)

    def get_list_by_id(self, id):
        lists = self.get_lists()
        for list in lists:
            if list['id'] == str(id):
                return list
        return None

    def get_list_by_name(self, name):
        lists = self.get_lists()
        for list in lists:
            if list['name'] == name:
                return list
        return None

    def create_contact(self, email, list_id, action_type):
        # action_type can be either ACTION_BY_OWNER or ACTION_BY_VISITOR
        target = 'contacts?action_by=%s' % action_type
        content = {
            'lists': [{'id': str(list_id)}],
            'email_addresses': [{'email_address': email}]
        }
        r = self.post(
            target=target,
            content=content,
            headers={"Content-Type": "application/json"},
            return_raw=True
        )

        success = False
        if r.status_code == 201:
            success = True
        return success, r.content

'''
