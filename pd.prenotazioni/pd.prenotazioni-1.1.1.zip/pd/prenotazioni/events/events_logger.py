# -*- coding: utf-8 -*-
from pd.prenotazioni import prenotazioniFileLogger as logger
from plone import api
import StringIO
import csv
import json


def csv2string(data):
    '''
    Converts an array of info to a proper cvs string
    '''
    dummy_file = StringIO.StringIO()
    cw = csv.writer(dummy_file)
    cw.writerow(data)
    return dummy_file.getvalue().strip('\r\n')


def on_workflow_change(obj, event):
    '''
    This handler logs a cvs string for
    each IPrenotazione workflow changes
    '''
    user = api.user.get_current()
    data = [obj.UID(), obj.Title(), user.getId(), event.action]
    logger.info(csv2string(data))


def on_move(obj, event):
    '''
    This handler logs a cvs string for
    every IPrenotazione document moved
    '''
    user = api.user.get_current()
    data = [obj.UID(), obj.Title(), user.getId(), 'moved']
    logger.info(csv2string(data))


def on_modify(obj, event):
    '''
    This handler logs a cvs string for
    every IPrenotazione document modified
    '''

    old_version = getattr(obj, 'version_id', 0) - 1
    if old_version < 0:
        return

    # Below a list of fields to be logged to
    fnames = ['title', 'description', 'email', 'telefono', 'mobile',
              'tipologia_prenotazione', 'azienda', 'gate']

    pr = api.portal.get_tool(name='portal_repository')
    old = pr.retrieve(obj, old_version).object
    changes = []
    for fname in fnames:
        c_value = obj.getField(fname, obj).get(obj)
        o_value = old.getField(fname, old).get(old)
        if c_value != o_value:
            changes.append({'new_' + fname: c_value,
                            'old_' + fname: o_value})

    user = api.user.get_current()
    data = [obj.UID(), obj.Title(), user.getId(), 'changed',
            json.dumps(changes)]
    logger.info(csv2string(data))
