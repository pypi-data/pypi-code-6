# -*- coding: utf-8 -*-
from rope.base.project import Project
from rope.base.exceptions import ModuleSyntaxError
from rope.contrib import codeassist
from django.conf import settings

__author__ = 'ZIgi'

def get_code_proposals(code, offset):

    proj = Project(settings.PROJECT_ROOT)
    props = []
    result = {
        'props' :[],
        'error':None,
        'success': True
    }

    try:
        props = codeassist.code_assist(proj, code, offset, resource=None,
                templates=None, maxfixes=1)
        props = codeassist.sorted_proposals(props)
    except ModuleSyntaxError as exc:
        result['success'] = False
        result['error'] = {
            'lineno':exc.lineno,
            'message':exc.message
        }

    for p in props:
        obj = {
            'text':p.name,
            'type':p.type,
            'scope':p.scope
        }
        result['props'].append(obj)

    return result

