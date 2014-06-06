import requests.exceptions


class IAS3HTTPError(requests.exceptions.HTTPError):

    def __init__(self, requests_exception, item, key, request):
        super(IAS3HTTPError, self).__init__()
        self.requests_exception = requests_exception
        self.response = requests_exception.response
        self.item = item
        self.request = request

    def __str__(self):
        error_msg = str(self.requests_exception)

        # 400 Bad request.
        if self.response.status_code == 400:
            error_msg += (' - Check your metadata and header values for '
                          'newline charchters (i.e. "\\n").')
            if any('\n' in str(v) for (k, v) in self.request.headers.items()):
                error_msg += (' - Check your metadata and header values for '
                              'newline charchters (i.e. "\\n").')

        # 403 Forbidden.
        if self.response.status_code == 403:
            if (not self.item.session.access_key) and (not self.item.session.secret_key):
                error_msg += (' - IAS3 Authentication failed. Please set your IAS3 '
                              'access key and secret key via the environment '
                              'variables `IAS3_ACCESS_KEY` and `IAS3_SECRET_KEY`, '
                              'or run `ia configure` to add your IAS3 keys to your '
                              'ia config file. You can obtain your IAS3 keys at the '
                              'following URL: https://archive.org/account/s3.php')
            else:
                error_msg += (' - IAS3 Authentication failed. It appears the keyset '
                              '"{0}:{1}" \ndoes not have permission to upload '
                              'to the given item or '
                              'collection.\n\n'.format(self.item.session.access_key,
                                                       self.item.session.secret_key))
        return error_msg
