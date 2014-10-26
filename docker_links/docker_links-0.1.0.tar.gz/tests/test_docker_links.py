#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_docker_links
----------------------------------

Tests for `docker_links` module.
"""

import unittest

from docker_links.internals import _docker_link_helper


class TestDocker_links(unittest.TestCase):
    def test_docker_link(self):
        self.assertEqual(
            "protocol://username:password@host:1234/path/",
            _docker_link_helper(
                {
                    "scheme": "http",
                    "netloc": "example.com:80",
                    "path": "/",
                    "params": "",
                    "query": "",
                    "fragment": "",
                    "username": None,
                    "password": None,
                    "hostname": "example.com",
                    "port": 80,
                },
                overrides={
                    "scheme": "protocol",
                    "hostname": "host",
                    "port": 1234,
                    "username": "username",
                    "password": "password",
                    "path": "/path/",
                }
            )
        )


if __name__ == '__main__':
    unittest.main()
