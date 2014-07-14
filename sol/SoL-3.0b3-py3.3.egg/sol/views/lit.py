# -*- coding: utf-8 -*-
# :Progetto:  SoL -- Light user interface controller
# :Creato:    ven 12 dic 2008 09:18:37 CET
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from datetime import date
import logging

from markupsafe import escape

from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.view import view_config

from sqlalchemy import distinct, func, select
from sqlalchemy.orm.exc import NoResultFound

from . import get_request_logger
from ..i18n import translatable_string as _, translator, gettext, ngettext
from ..models import (
    DBSession,
    Championship,
    Club,
    Player,
    Rating,
    Tourney,
    )


logger = logging.getLogger(__name__)


@view_config(route_name="lit", renderer="lit/index.mako")
def index(request):
    from collections import defaultdict

    sess = DBSession()

    clubs = sess.query(Club).all()
    nclubs = len(clubs)
    nfeds = len([c for c in clubs if c.isfederation])
    ntourneys = sess.query(func.count(Tourney.idtourney)).scalar()
    nchampionships = sess.query(func.count(Championship.idchampionship)).scalar()
    nplayers = sess.query(func.count(Player.idplayer)).scalar()
    npcountries = sess.query(func.count(distinct(Player.nationality))) \
                      .filter(Player.nationality != None).scalar()
    nratings = sess.query(func.count(Rating.idrating)).scalar()
    bycountry = defaultdict(list)
    for club in clubs:
        bycountry[(club.country, club.nationality)].append(club)

    return {
        "_": gettext,
        "clubsbycountry": bycountry,
        "nccountries": len(bycountry),
        "nchampionships": nchampionships,
        "nclubs": nclubs,
        "nfederations": nfeds,
        "ngettext": ngettext,
        "npcountries": npcountries,
        "nplayers": nplayers,
        "nratings": nratings,
        "ntourneys": ntourneys,
        "request": request,
        "session": sess,
        "today": date.today(),
        "version": request.registry.settings['desktop.version'],
    }


def get_data(request, klass):
    t = translator(request)

    guid = request.matchdict['guid']
    sess = DBSession()

    try:
        entity = sess.query(klass).filter_by(guid=guid).one()
    except NoResultFound:
        e = t(_('No $entity with guid $guid'),
              mapping=dict(entity=klass.__name__.lower(), guid=guid))
        get_request_logger(request, logger).error("Couldn't create page: %s", e)
        raise HTTPBadRequest(str(e))
    except Exception as e: # pragma: no cover
        get_request_logger(request, logger).critical("Couldn't create page: %s", e,
                                                     exc_info=True)
        raise HTTPInternalServerError(str(e))
    else:
        return {
            '_': gettext,
            'entity': entity,
            'escape': escape,
            'ngettext': ngettext,
            'request': request,
            'session': sess,
            'today': date.today(),
            'version': request.registry.settings['desktop.version'],
        }


@view_config(route_name="lit_championship", renderer="lit/championship.mako")
def championship(request):
    return get_data(request, Championship)


@view_config(route_name="lit_club", renderer="lit/club.mako")
def club(request):
    return get_data(request, Club)


@view_config(route_name="lit_player", renderer="lit/player.mako")
def player(request):
    return get_data(request, Player)


@view_config(route_name="lit_rating", renderer="lit/rating.mako")
def rating(request):
    data = get_data(request, Rating)
    sess = data['session']
    rating = data['entity']
    tt = Tourney.__table__
    data['ntourneys'] = sess.execute(select([func.count(tt.c.idtourney)],
                                            tt.c.idrating==rating.idrating)).first()[0]
    return data


@view_config(route_name="lit_tourney", renderer="lit/tourney.mako")
def tourney(request):
    t = translator(request)

    turn = request.params.get('turn')
    if turn is not None:
        try:
            turn = int(turn)
        except ValueError:
            e = t(_('Invalid turn: $turn'), mapping=dict(turn=repr(turn)))
            get_request_logger(request, logger).error("Couldn't create page: %s", e)
            raise HTTPBadRequest(str(e))

    data = get_data(request, Tourney)
    data["turn"] = turn
    data["player"] = request.params.get('player')
    return data


@view_config(route_name="lit_latest", renderer="lit/latest.mako")
def latest(request):
    t = translator(request)

    n = request.params.get('n')
    if n is not None:
        try:
            n = int(n)
        except ValueError:
            e = t(_('Invalid number of tourneys: $n'), mapping=dict(n=repr(n)))
            get_request_logger(request, logger).error("Couldn't create page: %s", e)
            raise HTTPBadRequest(str(e))
    else:
        n = 20

    sess = DBSession()
    tourneys = sess.query(Tourney).filter_by(prized=True).order_by(Tourney.date.desc())[:n]

    return {
        '_': gettext,
        'escape': escape,
        'n': len(tourneys),
        'ngettext': ngettext,
        'request': request,
        'session': DBSession(),
        'today': date.today(),
        'tourneys': tourneys,
        'version': request.registry.settings['desktop.version'],
    }
