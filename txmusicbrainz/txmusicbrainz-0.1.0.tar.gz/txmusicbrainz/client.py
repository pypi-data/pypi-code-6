from treq import json_content, request
from twisted.web.http_headers import Headers

from txmusicbrainz._entities import entity_retriever


class APIError(Exception):
    """
    A request to the API resulted in an error.

    """


class MusicBrainz(object):
    """
    A MusicBrainz client.

    Typical usage:

        >>> import my_cool_app
        >>> MusicBrainz(
        ...     app_name=my_cool_app.__name__,
        ...     app_version=my_cool_app.__version__,
        ...     contact_info="https://github.com/Julian/MyCoolApp",
        ... )

    The first arguments taken by this client are required in order
    to comply with MusicBrainz's request to be able to reach out to
    application developers whose applications exceed `rate limiting
    requirements <https://musicbrainz.org/doc/XML_Web_Service/Rate_Limiting>`
    \ .

        :argument str app_name: the name of the application which will
            communicate with MusicBrainz
        :argument str app_version: the version of the application which
            will communicate with MusicBrainz
        :argument str contact_info: an email or URL suitable for contact
            purposes by MusicBrainz

    Additional arguments:

        :argument IReactor reactor: a Twisted reactor to use
        :argument str root_url: the root API URL

    """

    artists = entity_retriever(
        path="/artist",
        available_includes=frozenset(
            ["recordings", "releases", "release-groups", "works"],
        ),
    )
    labels = entity_retriever(
        path="/label", available_includes=frozenset(["releases"]),
    )
    recordings = entity_retriever(
        path="/recording",
        available_includes=frozenset(["artists", "releases"]),
    )
    releases = entity_retriever(
        path="/release",
        available_includes=frozenset(
            ["artists", "labels", "recordings", "release-groups"],
        ),
    )
    release_groups = entity_retriever(
        path="/release-group", available_includes=["artists", "releases"],
    )
    works = entity_retriever(path="/work")
    areas = entity_retriever(path="/area")
    urls = entity_retriever(path="/url")

    def __init__(
        self,
        app_name,
        app_version,
        contact_info,
        reactor=None,
        root_url="http://musicbrainz.org/ws/2",
    ):
        if reactor is None:
            from twisted.internet import reactor

        self.reactor = reactor
        self.root_url = root_url
        self.user_agent = "{0}/{1} ({2})".format(
            app_name, app_version, contact_info,
        )

    def request(self, path, method="GET", headers=None, **kwargs):
        if headers is None:
            headers = Headers()

        headers.addRawHeader("User-Agent", self.user_agent)
        return request(
            method,
            headers=headers,
            url=self.root_url + path,
            params=[("fmt", "json")],
            reactor=self.reactor,
            **kwargs
        ).addCallback(json_content).addCallback(_check_for_errors)


def _check_for_errors(response):
    error = response.get("error")
    if error is not None:
        raise APIError(error)
    return response
