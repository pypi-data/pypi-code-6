# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from rg.prenotazioni.interfaces import IPrenotazione
from plone import api


@indexer(IPrenotazione)
def prenotazione(context, **kw):
    ''' Reindex prenotazione
    '''
    parts = set((
        context.SearchableText(),
        context.REQUEST.form.get('cmfeditions_version_comment', ''),
    ))
    view = api.content.get_view('contenthistory', context, context.REQUEST)
    rh = view.revisionHistory()
    for item in rh[:-1]:
        comments = item.get('comments', '')
        if comments:
            if isinstance(comments, unicode):
                comments = comments.encode('utf8')
        parts.add(comments)

    searchable_text = " ".join(sorted(set(" ".join(parts).split())))
    return searchable_text
