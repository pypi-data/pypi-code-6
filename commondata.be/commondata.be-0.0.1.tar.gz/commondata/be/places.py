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
from __future__ import print_function

from commondata.utils import Place, PlaceGenerator


class PlaceInBelgium(Place):
    def __unicode__(self):
        return self.fr

class Country(PlaceInBelgium):
    value = 0

class Region(PlaceInBelgium):
    value = 1

class Province(PlaceInBelgium):
    value = 2

class City(PlaceInBelgium):
    value = 3

class Village(City):
    value = 4

class Township(City):  # "Section" d'une commune,  "Stadtteil"
    value = 4


def root():

    pg = PlaceGenerator()
    pg.install(Country, Region, Province, City, Village, Township)
    pg.set_args('fr nl de en')

    belgium = pg.country("Belgique", "België", "Belgien", "Belgium")

    pg.region("Bruxelles", "Brussel", "Brüssel", "Brussels")
    from .brussels import populate ; populate(pg)
    
    pg.set_args('fr nl de en')
    pg.region(
        "Région flamande", "Vlaams Gewest", "Flandern", "Flemish Region")
    from .antwerpen import populate ; populate(pg)
    from .luxembourg import populate ; populate(pg)
    from .oostvlaanderen import populate ; populate(pg)
    from .westvlaanderen import populate ; populate(pg)
    from .vlaamsbrabant import populate ; populate(pg)

    pg.set_args('fr nl de en')
    pg.region(
        "Région wallonne", "Wallonië", "Wallonische Region", "Wallonia")
    from .namur import populate ; populate(pg)
    from .liege import populate ; populate(pg)
    from .hainaut import populate ; populate(pg)
    from .limburg import populate ; populate(pg)
    from .brabantwallon import populate ; populate(pg)
    
    return belgium
