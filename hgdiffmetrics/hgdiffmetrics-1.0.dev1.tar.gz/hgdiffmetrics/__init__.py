# Forked from hg extdiff.py in October 2014. This extension has been modified
# to use the diffmetrics package for comparing revisions.
#
# Copyright 2006 Vadim Gelfer <vadim.gelfer@gmail.com>
# Modifications copyright 2014 Neal Finne <neal@nealfinne.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

'''command to compare code metrics between revisions

The diffmetrics Mercurial extension allows you to compare Python code
metrics between revisions or between a revision and the working directory.

You can use -I/-X and list of file or directory names like normal
:hg:`diff` command. The diffmetrics extension makes snapshots of only
needed files, so the code analysis can be performed efficiently.
'''

from copy import copy
import os
import shutil
import tempfile
import re

from mercurial.node import short, nullid
from mercurial import scmutil, util, commands


testedwith = 'internal'


def snapshot(ui, repo, files, node, tmproot):
    '''snapshot files as of some revision
    if not using snapshot, -I/-X does not work and recursive diff
    in tools like kdiff3 and meld displays too many files.'''
    dirname = os.path.basename(repo.root)
    if dirname == "":
        dirname = "root"
    if node is not None:
        dirname = '%s.%s' % (dirname, short(node))
    base = os.path.join(tmproot, dirname)
    os.mkdir(base)
    if node is not None:
        ui.note('making snapshot of %d files from rev %s\n'
                % (len(files), short(node)))
    else:
        ui.note('making snapshot of %d files from working directory\n'
                % (len(files)))
    wopener = scmutil.opener(base)
    fns_and_mtime = []
    ctx = repo[node]
    for fn in files:
        wfn = util.pconvert(fn)
        if wfn not in ctx:
            # File doesn't exist; could be a bogus modify
            continue
        ui.note('  %s\n' % wfn)
        dest = os.path.join(base, wfn)
        fctx = ctx[wfn]
        data = repo.wwritedata(wfn, fctx.data())
        if 'l' in fctx.flags():
            wopener.symlink(data, wfn)
        else:
            wopener.write(wfn, data)
            if 'x' in fctx.flags():
                util.setflags(dest, False, True)
        if node is None:
            fns_and_mtime.append((dest, repo.wjoin(fn),
                                  os.lstat(dest).st_mtime))
    return dirname, fns_and_mtime


def diffmetrics(ui, repo, *pats, **opts):
    '''use diffmetrics to compare code metrics between revisions.'''

    opts['exclude'].extend(opts['default-exclude'])

    revs = opts.get('rev')
    change = opts.get('change')
    args = ''
    do3way = '$parent2' in args

    min_severity = opts.get('min')
    if min_severity:
        args += ' -n ' + min_severity

    if revs and change:
        msg = 'cannot specify --rev and --change at the same time'
        raise util.Abort(msg)
    elif change:
        node2 = scmutil.revsingle(repo, change, None).node()
        node1a, node1b = repo.changelog.parents(node2)
    else:
        node1a, node2 = scmutil.revpair(repo, revs)
        if not revs:
            node1b = repo.dirstate.p2()
        else:
            node1b = nullid

    # Disable 3-way merge if there is only one parent
    if do3way:
        if node1b == nullid:
            do3way = False

    matcher = scmutil.match(repo[node2], pats, opts)
    mod_a, add_a, rem_a = map(set, repo.status(node1a, node2, matcher)[:3])
    if do3way:
        mod_b, add_b, rem_b = map(set, repo.status(node1b, node2, matcher)[:3])
    else:
        mod_b, add_b, rem_b = set(), set(), set()
    modadd = mod_a | add_a | mod_b | add_b
    common = modadd | rem_a | rem_b
    if not common:
        return 0

    tmproot = tempfile.mkdtemp(prefix='diffmetrics.')
    try:
        # Always make a copy of node1a (and node1b, if applicable)
        dir1a_files = mod_a | rem_a | ((mod_b | add_b) - add_a)
        dir1a = snapshot(ui, repo, dir1a_files, node1a, tmproot)[0]
        rev1a = '@%d' % repo[node1a].rev()
        if do3way:
            dir1b_files = mod_b | rem_b | ((mod_a | add_a) - add_b)
            dir1b = snapshot(ui, repo, dir1b_files, node1b, tmproot)[0]
            rev1b = '@%d' % repo[node1b].rev()
        else:
            dir1b = None
            rev1b = ''

        fns_and_mtime = []

        # If node2 in not the wc or there is >1 change, copy it
        dir2root = ''
        rev2 = ''
        if node2:
            dir2 = snapshot(ui, repo, modadd, node2, tmproot)[0]
            rev2 = '@%d' % repo[node2].rev()
        elif len(common) > 1:
            # we only actually need to get the files to copy back to
            # the working dir in this case (because the other cases
            # are: diffing 2 revisions or single file -- in which case
            # the file is already directly passed to the diff tool).
            dir2, fns_and_mtime = snapshot(ui, repo, modadd, None, tmproot)
        else:
            # This lets the diff tool open the changed file directly
            dir2 = ''
            dir2root = repo.root

        label1a = rev1a
        label1b = rev1b
        label2 = rev2

        # If only one change, diff the files instead of the directories
        # Handle bogus modifies correctly by checking if the files exist
        if len(common) == 1:
            common_file = util.localpath(common.pop())
            dir1a = os.path.join(tmproot, dir1a, common_file)
            label1a = common_file + rev1a
            if not os.path.isfile(dir1a):
                dir1a = os.devnull
            if do3way:
                dir1b = os.path.join(tmproot, dir1b, common_file)
                label1b = common_file + rev1b
                if not os.path.isfile(dir1b):
                    dir1b = os.devnull
            dir2 = os.path.join(dir2root, dir2, common_file)
            label2 = common_file + rev2

        # Function to quote file/dir names in the argument string.
        # When not operating in 3-way mode, an empty string is
        # returned for parent2
        replace = dict(parent=dir1a, parent1=dir1a, parent2=dir1b,
                       plabel1=label1a, plabel2=label1b,
                       clabel=label2, child=dir2,
                       root=repo.root)

        def quote(match):
            key = match.group()[1:]
            if not do3way and key == 'parent2':
                return ''
            return util.shellquote(replace[key])

        # Match parent2 first, so 'parent1?' will match both parent1 and parent
        regex = '\$(parent2|parent1?|child|plabel1|plabel2|clabel|root)'
        if not do3way and not re.search(regex, args):
            args += ' $parent1 $child'
        args = re.sub(regex, quote, args)
        cmdline = util.shellquote('diffmetrics') + ' ' + args

        ui.debug('running %r in %s\n' % (cmdline, tmproot))
        rc = util.system(cmdline, cwd=tmproot, out=ui.fout)

        for copy_fn, working_fn, mtime in fns_and_mtime:
            if os.lstat(copy_fn).st_mtime != mtime:
                ui.debug('file changed while diffing. '
                         'Overwriting: %s (src: %s)\n' % (working_fn, copy_fn))
                util.copyfile(copy_fn, working_fn)

        return rc
    finally:
        ui.note('cleaning up temp directory\n')
        shutil.rmtree(tmproot)


cmdtable = {
    'diffmetrics':
    (diffmetrics,
     [('r', 'rev', [],
       'revision', 'REV'),
      ('c', 'change', '',
       'change made by revision', 'REV'),
      ('n', 'min', '',
       'minimum severity to display (low, medium, high)', 'SEV'),
      ] + commands.walkopts,
     'hg diffmetrics [OPT]... [FILE]...'),
}


def uisetup(ui):
    defaults = {'default-exclude': ui.configlist('diffmetrics', 'exclude')}

    def mydiff(ui, repo, *pats, **opts):
        opts = copy(opts)
        for k, v in defaults.items():
            opts.setdefault(k, v)
        return diffmetrics(ui, repo, *pats, **opts)

    command = cmdtable['diffmetrics']
    cmdtable['diffmetrics'] = (mydiff, command[1], command[2])


commands.inferrepo += " diffmetrics"
