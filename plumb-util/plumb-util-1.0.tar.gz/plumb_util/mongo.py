import pymongo
import logging; logger = logging.getLogger(__name__)
from .dns_srv import find_service


def get_mongo_connection(zone=None):
    host_and_ports = find_service('_mongodb._tcp', zone)
    error = None
    for host, port in host_and_ports:
        try:
            # Use the first DB connection we can find.
            connection = pymongo.Connection(host, port)
            return connection
        except pymongo.errors.PyMongoError as e:
            # If there's a failure, complain about it but proceed.
            logger.warn(e)
            error = e
    # If we couldn't connect to any databases, was it because...
    if error is None:
        # there aren't any?
        raise ValueError("find_service found no databases. Bother Jason.")
    else:
        # or because they all failed? If so, raise the error from the
        # last one.
        raise error
