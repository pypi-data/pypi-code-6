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
    Rate,
    Rating,
    Tourney,
    )
from ..models.errors import OperationAborted


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
        "ngettext": ngettext,
        "session": sess,
        "nclubs": nclubs,
        "nfederations": nfeds,
        "ntourneys": ntourneys,
        "nchampionships": nchampionships,
        "nplayers": nplayers,
        "nccountries": len(bycountry),
        "npcountries": npcountries,
        "nratings": nratings,
        "clubsbycountry": bycountry,
        "version": request.registry.settings['desktop.version'],
        "today": date.today(),
    }


def get_data(request, needsEntity=True):
    t = translator(request)

    try:
        sess = DBSession()
        params = request.params

        if 'championship' in params:
            guid = params['championship']
            try:
                entity = sess.query(Championship).filter_by(guid=guid).one()
            except NoResultFound:
                raise OperationAborted(
                    t(_('Championship $guid does not exist',
                        mapping=dict(guid=guid))))
        elif 'club' in params:
            guid = params['club']
            try:
                entity = sess.query(Club).filter_by(guid=guid).one()
            except NoResultFound:
                raise OperationAborted(
                    t(_('Club $guid does not exist',
                        mapping=dict(guid=guid))))
        elif 'player' in params:
            guid = params['player']
            try:
                entity = sess.query(Player).filter_by(guid=guid).one()
            except NoResultFound:
                raise OperationAborted(
                    t(_('Player $guid does not exist',
                        mapping=dict(guid=guid))))
        elif 'rating' in params:
            guid = params['rating']
            try:
                entity = sess.query(Rating).filter_by(guid=guid).one()
            except NoResultFound:
                raise OperationAborted(
                    t(_('Rating $guid does not exist',
                        mapping=dict(guid=guid))))
        elif 'tourney' in params:
            guid = params['tourney']
            try:
                entity = sess.query(Tourney).filter_by(guid=guid).one()
            except NoResultFound:
                raise OperationAborted(
                    t(_('Tourney $guid does not exist',
                        mapping=dict(guid=guid))))
        elif needsEntity:
            raise OperationAborted(t(_('No subject specified')))

        return dict(
            _=gettext,
            entity=entity,
            escape=escape,
            ngettext=ngettext,
            request=request,
            session=sess,
            version=request.registry.settings['desktop.version'],
            today=date.today(),
        )
    except OperationAborted as e:
        get_request_logger(request, logger).error("Couldn't create page: %s", e)
        raise HTTPBadRequest(str(e))
    except Exception as e:
        get_request_logger(request, logger).critical("Couldn't create page: %s", e,
                                                     exc_info=True)
        raise HTTPInternalServerError(str(e))


@view_config(route_name="lit_championship", renderer="lit/championship.mako")
def championship(request):
    return get_data(request)


@view_config(route_name="lit_club", renderer="lit/club.mako")
def club(request):
    return get_data(request)


@view_config(route_name="lit_player", renderer="lit/player.mako")
def player(request):
    return get_data(request)


@view_config(route_name="lit_rating", renderer="lit/rating.mako")
def rating(request):
    data = get_data(request)
    sess = data['session']
    rating = data['entity']
    tt = Tourney.__table__
    data['ntourneys'] = sess.execute(select([func.count(tt.c.idtourney)],
                                            tt.c.idrating==rating.idrating)).first()[0]
    return data


@view_config(route_name="lit_tourney", renderer="lit/tourney.mako")
def tourney(request):
    data = get_data(request)
    data["turn"] = request.params.get('turn')
    data["player"] = request.params.get('player')
    return data
