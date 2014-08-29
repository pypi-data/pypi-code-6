#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lolapi
import _keys


def main():
    api = lolapi.LolApi(region=lolapi.regions.NORTH_AMERICA, key=_keys.API_KEY)
    print api.data.get_versions()

if __name__ == '__main__':
    main()