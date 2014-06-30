""" detects JIRA-style ticket number in commit messages

To activate, update your hgrc::

    [extensions]
    hgticket = path/to/hgticket.py

"""

from mercurial import commands, extensions, util
import re

def ticketed(orig, ui, repo, *pats, **opts):
    msg = opts['message']
    match = re.search('[A-Z][A-Z][A-Z]*?-[0-9][0-9]*', msg)
    if not match:
        raise util.Abort('commit message does not have ticket number')
    ui.status('ticket: detected ticket number "%s"\n' % match.group())
    return orig(ui, repo, *pats, **opts)

def uisetup(ui):
    if not hasattr(extensions, 'wrapcommand'):
        return
    extensions.wrapcommand(commands.table, 'commit', ticketed)
