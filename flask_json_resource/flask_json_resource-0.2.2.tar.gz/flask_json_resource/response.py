import json
import copy

from flask import Response, request


DEFAULT_HEADERS = {
    'Link': []
}


class ErrorResponse(Response):
    def __init__(self, exception, status_code, **kwargs):
        headers = {
            'Content-Type': "application/json"
        }

        error = {
            'error': exception.message,
            'status': status_code
        }

        super(ErrorResponse, self).__init__(
            json.dumps(error), status_code,
            headers=headers, **kwargs
        )


class OptionsResponse(Response):
    def __init__(self, methods, resource):
        headers = copy.deepcopy(DEFAULT_HEADERS)
        headers['Allow'] = ','.join(methods)

        headers['Link'].append('<%s>; rel=describedby' % resource.schema.url)

        return super(OptionsResponse, self).__init__('', headers=headers)


class ResourceResponse(Response):
    autocorrect_location_header = False

    def __init__(self, resource, status=200, **kwargs):
        headers = copy.deepcopy(DEFAULT_HEADERS)

        headers['Content-Type'] = resource.content_type()

        for link in [
                link for link in resource.links() if link['rel'] != 'self'
        ]:
            headers['Link'].append(
                '<%s>; rel=%s' % (resource.rel(link['rel']), link['rel'])
            )

        if resource.url != request.path:
            headers['Location'] = resource.url

        super(ResourceResponse, self).__init__(
            json.dumps(resource, indent=4), status, headers=headers, **kwargs
        )

        try:
            self.set_etag(resource.etag)
        except KeyError:
            pass

        if 'last-modified' in resource.meta:
            self.last_modified = resource.meta['last-modified']

        self.make_conditional(request)


class DeleteResponse(Response):
    def __init__(self, resource, status=204, **kwargs):
        super(DeleteResponse, self).__init__('', status)


class ResourceCreatedResponse(ResourceResponse):
    def __init__(self, resource, status=201):
        super(ResourceCreatedResponse, self).__init__(resource, status)
    pass
