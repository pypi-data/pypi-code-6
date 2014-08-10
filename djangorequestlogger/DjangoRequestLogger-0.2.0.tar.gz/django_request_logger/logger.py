import logging

import middleware


def add_filter_to_all_handlers():
    filter = AddDjangoRequestFilter()
    for handler in logging._handlers.values():
        handler.addFilter(filter)


def get_client_ip(request):
    if request is None:
        return ""

    client_ip = request.META.get('REMOTE_ADDR')
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip += " [%s]" % request.META['HTTP_X_FORWARDED_FOR']
    return client_ip


class AddDjangoRequestFilter(object):
    def filter(self, record):
        # Initialise custom fields to empty, so the formatter doesn't raise an error if there is no request or user
        record.client_ip = ""
        record.username = ""
        record.absolute_url = ""
        record.raw_post_data = ""

        request = middleware.get_request()
        if request is not None:
            record.client_ip = get_client_ip(request)
            record.absolute_url = request.build_absolute_uri()

            try:
                record.raw_post_data = request.body
            except Exception as e:
                 record.raw_post_data = '<ERROR: %s>' % e.message

            if request.user is not None:
                record.username = request.user.username or "_"

            # The "data" dictionary is used by the Sentry log handler.
            if not hasattr(record, 'data'):
                record.data = {}
            record.data['client_ip'] = record.client_ip
            record.data['absolute_url'] = record.absolute_url
            record.data['raw_post_data'] = record.raw_post_data
            record.data['username'] = record.username

        return 1
