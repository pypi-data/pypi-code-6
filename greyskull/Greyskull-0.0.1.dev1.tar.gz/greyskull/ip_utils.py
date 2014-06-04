# -*- coding: utf-8 -*-
"""
Various utilities for dealing with ip addresses (v4 AND v6)
"""

import ipaddress


def encode_host_and_port(ip: str, port: str or int) -> str:
    ip = ipaddress.ip_address(ip)
    if isinstance(ip, ipaddress.IPv4Address):
        return ":".join([str(ip), str(port)])
    elif isinstance(ip, ipaddress.IPv6Address):
        return ":".join(["[" + str(ip) + "]", str(port)])