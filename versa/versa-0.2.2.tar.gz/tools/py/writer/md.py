#versa.writer.md

'''
Write a Versa data model to Markdown format
'''

import itertools
from versa import I, VERSA_BASEIRI, ORIGIN, RELATIONSHIP, TARGET, ATTRIBUTES
from versa import util
from amara3 import iri

VERSA_TYPE = I(iri.absolutize('type', VERSA_BASEIRI))

def to_markdown(m, output, config=None):
    '''
    Write a Versa data model to Markdown format

    md -- markdown source text
    output -- Versa model to take the output relationship
    encoding -- character encoding (defaults to UTF-8)

    No return value
    '''
    #Read the configuration to help guide the output
    config = config or {}
    h1type = config.get('autotype-h1')
    h2type = config.get('autotype-h2')
    h3type = config.get('autotype-h3')
    header_by_type = {h1type: '#', h2type: '##', h3type: '###'}
    #XXX: Maybe use interpretations to avoid having to always specify data type?

    #For now work in multiple passes
    origins_handled = set()
    done = False

    #while not done:
    #    for (i, stmt) in enumerate(m.match()):
    #        if stmt[ORIGIN] in origins_handled: continue
    #        curr_origin = stmt[ORIGIN]
    #        for stmt in itertools.islice(m.match())

    count = 0
    for origin in util.all_origins(m):
        count += 1
        print(origin, count)
        #relationship -> (target, attrs)
        rel_etc = {}
        rtype = None
        for stmt in m.match(origin):
            rel = stmt[RELATIONSHIP]
            if rel == VERSA_TYPE:
                rtype = stmt[ATTRIBUTES]
            else:
                rel_etc.setdefault(rel, []).append((stmt[TARGET], stmt[ATTRIBUTES]))

        header_str = header_by_type.get(rtype, '#')
        type_str = ''
        if rtype and rtype not in header_by_type:
            type_str = ' [<' + rtype + '>]'
        print(header_str, origin, type_str, file=output)

        #Now to write the output
        for k, v in rel_etc.items():
            #Sort by rel for better output
            v.sort()
            for target, attrs in v:
                print('    ' + k + ': "' + target + '"', file=output)


