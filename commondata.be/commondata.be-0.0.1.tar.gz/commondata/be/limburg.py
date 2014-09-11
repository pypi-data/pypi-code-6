# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the commondata library.
# The commondata library is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
# The commondata library is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with the commondata library; if not, see
# <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals


def populate(pg):

    pg.set_args('fr nl de en')
    pg.province("Limbourg", "Limburg", "Limburg", "Limbourg")
    pg.set_args('zip_code fr nl de en')
    
    pg.village("3800", "Aalst-bij-Sint-Truiden", "", "", "")
