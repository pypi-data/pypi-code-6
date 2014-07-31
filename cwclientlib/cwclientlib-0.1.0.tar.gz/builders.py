# -*- coding: utf-8 -*-

"""
Build common queries usable with rqlcontroller

Each returned query is a couple (rql, kwargs) to be used to build the
'queries' argument of the CWProxy.rqlio() method, like::


  import cwproxy, builders

  client = cwproxy.CWProxy('http://www.cubicweb.org/')
  queries = [builders.create_entity('CWUser', login='Babar', password='secret'),
             builders.build_trinfo('__r0', 'disable', 'not yet activated'),
            ]
  resp = client.rqlio(queries)


"""

def create_entity(cwetype, **kw):
    '''Build the rqlio query thath will create a new <cwetype> entity,
    with given attributes.
    '''
    args = ', '.join('X %s %%(%s)s' % (key, key) for key in kw)
    return ('INSERT %s X: %s' % (cwetype, args), kw)


def build_trinfo(eid, transition_name,  comment=None):
    """Build the rqlio query that will fire the transistion <transition_name>
    for the entity <eid> and attach the optional <comment>.
    """
    return ('INSERT TrInfo X: X comment %(comment)s, '
            'X by_transition BT, X wf_info_for Y '
            'WHERE Y eid %(eid)s, Y in_state S, S state_of W, '
            'BT transition_of W, BT name %(trname)s',
            {'eid': eid,
             'trname': transition_name,
             'comment': comment or ''})
