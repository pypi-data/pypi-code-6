# -*- coding: utf-8 -*-
"""
us in hooks::

    call = load_extension('commit_parser.py')
    if call:
        # extra arguments in kwargs
        my_kw = {
            'reviewers_extra_field': 'reviewers', # defines if we have a comma
                                                  # separated list of reviewers
                                                  # in this repo stored in extra_fields
        }
        my_kw.update(kwargs) # pass in hook args
        parsed_revs = call(**kwargs)
        # returns list of dicts with changesets data

"""

def run(*args, **kwargs):

    revs = kwargs.get('pushed_revs')
    if not revs:
        return 0

    from rhodecode.lib.utils2 import extract_mentioned_users
    from rhodecode.model.db import Repository

    repo = Repository.get_by_repo_name(kwargs['repository'])
    changesets = []
    reviewers = []

    # reviewers fields from extra_fields, users can store their custom
    # reviewers inside the extra fields, to pre-define set of people who will
    # get notifications about changesets
    field_key = kwargs.get('reviewers_extra_field')
    if field_key:
        for xfield in repo.extra_fields:
            if xfield.field_key == field_key:
                reviewers.extend(xfield.field_value.split())

    vcs_repo = repo.scm_instance_no_cache()
    for rev in kwargs['pushed_revs']:
        cs = vcs_repo.get_changeset(rev)
        cs_data = cs.__json__()
        cs_data['mentions'] = extract_mentioned_users(cs_data['message'])
        cs_data['reviewers'] = reviewers
        # optionaly add more logic to parse the commits, like reading extra
        # fields of repository to read managers of reviewers ?
        changesets.append(cs_data)

    return changesets
