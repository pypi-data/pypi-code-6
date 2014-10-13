# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)


class CheckmywsError(Exception):

    def __init__(self, response):
        self.status_code = response.status_code
        self.reason = response.reason

        super(CheckmywsError, self).__init__(self.__str__())

    def __repr__(self):
        msg = "CheckmywsError: HTTP {0} - {1}".format(
            self.status_code,
            self.reason
        )

        logger.debug(msg)
        return msg

    def __str__(self):
        return self.__repr__()
