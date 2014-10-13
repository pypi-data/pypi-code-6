#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from models import artist_db_example as db

# Eksemplel på liste


@bottle.route('/artister')
@bottle.view('artistliste')
def artistliste():
    artister = db.getArtists()
    return dict(test="test", artister=artister)


@bottle.route('/album/<id:int>')
@bottle.view('albumliste')
def albumliste(id):
    #bruker ikke ID i dette eksempelet ettersom vi ikke har DB.
    #Bruker artistnavn i stedet
    mappe = bottle.request.query.mappe or None
    if mappe:
        albumer = db.getAlbums(mappe)
        return dict(test="test", albumer=albumer)
    else:
        return "ERROR"

