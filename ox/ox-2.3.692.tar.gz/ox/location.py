# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
import math


def center(lat_sw, lng_sw, lat_ne=None, lng_ne=None):
    if not lat_ne and not lng_ne:
        return min(lat_sw, lng_sw) + abs(lat_sw-lng_sw)/2
    else:
        return (center(lat_sw,lng_sw), center(lat_ne, lng_ne))

def area(lat_sw, lng_sw, lat_ne, lng_ne):
    return (lat_ne - lat_sw) * (lng_ne - lng_sw)

def latlngspan2latlng(lat, lng, latSpan, lngSpan):
    return dict(
        lat_sw = lat - latSpan, lng_sw = lng - lngSpan,
        lat_ne = lat + latSpan, lng_ne = lng + latSpan
    )

def parse_location_string(location_string):
    l = location_string.split('+')
    if len(l) == 1:
        l = location_string.split(';')
    l = [i.strip() for i in l]
    l = filter(lambda x: x, l)
    return l

