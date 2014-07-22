"""
Asyncrnous tasks to handle dsns requests
"""
import logging

from celery import task

from dsns import DSNS


logger = logging.getLogger(__name__)


@task()
def create_subscriptions(target_drn, protocol,
                         channels=[], endpoint=None, **kwargs):
    """
    Description:
        tast to create subscriptions
    params:
        target_drn: identity of subsriber
        endpoint: endpoint may be http URI or email
        protocol: HTTP/EMAIL etc
        channels: list of channel drns
        kwargs: extra info to be submitted
        like token, username, password
    returns:
        resp_dict True/False against channel drn based on
        HTTP status code
    """
    handler = DSNS()
    data = {
        "target_drn": target_drn,
        "protocol": protocol,
        "endpoint": endpoint}
    data.update(**kwargs)
    resp_dict = dict()
    for each_drn in channels:
        data.update(**{"channel_drn": each_drn})
        res = handler.subscription.subscribe(data)
        if not res.get_status_code() == 200:
            logger.error(
                "Unable to subscribe channel %s,"
                " response from DSNS is %s" % (
                    each_drn, res.response_dict()))
            resp_dict[each_drn] = False
        else:
            resp_dict[each_drn] = True
    return "Client with DRN {drn} subsription results {result}".format(
        drn=target_drn, result=resp_dict)
