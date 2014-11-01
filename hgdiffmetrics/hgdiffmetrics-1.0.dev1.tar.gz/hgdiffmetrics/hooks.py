# Copyright 2014 Neal Finne <neal@nealfinne.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


from hgdiffmetrics import cmdtable, uisetup


def check_commit(ui, repo, **kwargs):
    '''
    [hooks]
    pretxncommit = python:path/to/script/hg.py:check_commit
    '''
    uisetup(ui)

    ctx = repo['tip']
    parents = ctx.parents()

    if len(parents) > 1:
        return False

    parent = parents[0]

    result = cmdtable['diffmetrics'][0](
        ui,
        repo,
        rev=[parent.rev(), ctx.rev()],
        exclude=[],
    )
    if result:
        print
        override = raw_input('Continue with commit? [Y/N] ')
        return override.lower() not in ('y', 'yes')
