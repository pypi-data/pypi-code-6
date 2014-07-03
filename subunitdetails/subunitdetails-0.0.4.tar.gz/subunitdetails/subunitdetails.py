#!/usr/bin/env python3
#
#  Copyright (c) 2014, Corey Goldberg (cgoldberg@gmail.com)
#
#  license: GNU GPLv3
#
#  This file is part of: subunitdetails
#  https://github.com/cgoldberg/subunitdetails
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; version 3 of the
#  License


import argparse
import logging
import os
import re

from subunit import ByteStreamToStreamResult
from testtools import StreamToExtendedDecorator, TestResult


logging.basicConfig(level='INFO', format='%(message)s')
logger = logging.getLogger(__name__)


class FileSaveResult(TestResult):
    """A TestResult that saves arbitrary test details to files."""

    def addError(self, test, err=None, details=None):
        super().addError(test, err=err, details=details)
        self.save_file_attachments(test.id(), details)

    def addExpectedFailure(self, test, err=None, details=None):
        super().addExpectedFailure(test, err=err, details=details)
        self.save_file_attachments(test.id(), details)

    def addFailure(self, test, err=None, details=None):
        super().addFailure(test, err=err, details=details)
        self.save_file_attachments(test.id(), details)

    def addSkip(self, test, reason=None, details=None):
        super().addSkip(test, reason=reason, details=details)
        self.save_file_attachments(test.id(), details)

    def addSuccess(self, test, details=None):
        super().addSuccess(test, details=details)
        self.save_file_attachments(test.id(), details)

    def addUnexpectedSuccess(self, test, details=None):
        super().addUnexpectedSuccess(test, details=details)
        self.save_file_attachments(test.id(), details)

    def save_file_attachments(self, test_id, details):
        for key, detail in details.items():
            if detail.iter_bytes() == [b'']:
                continue
            slug = re.sub(r'(?u)[^-\w.]', '', key)
            file_name = '%s-%s' % (test_id, slug)
            with open(file_name, 'wb') as f:
                for chunk in detail.iter_bytes():
                    f.write(chunk)
            file_size = os.path.getsize(file_name)
            logger.info(' test id: %r' % test_id)
            logger.info(' attachment: %r (%s) [%s bytes]' % (
                key,
                detail.content_type,
                file_size,)
            )
            logger.info(' saved as: %r\n' % file_name)


def parse_args():
    parser = argparse.ArgumentParser(description='Subunit Detail Extractor')
    parser.add_argument('subunit_file', action="store")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    logger.info('\nParsing Subunit input: %r [%s bytes]' % (
        args.subunit_file,
        os.path.getsize(args.subunit_file))
    )
    stream = open(args.subunit_file, 'rb')
    suite = ByteStreamToStreamResult(stream)
    logger.info('\nExtracting details...\n')
    result = StreamToExtendedDecorator(FileSaveResult())
    result.startTestRun()
    try:
        suite.run(result)
    finally:
        result.stopTestRun()
    logger.info('\nDone.')


if __name__ == '__main__':
    main()
