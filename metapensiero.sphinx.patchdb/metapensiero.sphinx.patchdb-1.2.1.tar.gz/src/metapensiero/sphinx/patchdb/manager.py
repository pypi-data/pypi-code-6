# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Script&Patch Manager
# :Creato:    ven 14 ago 2009 13:09:28 CEST
# :Autore:    Lele Gaifax <lele@nautilus.homeip.net>
# :Licenza:   GNU General Public License version 3 or later
#

from __future__ import absolute_import

import logging

try:
    from sqlalchemy.util.topological import sort
except ImportError:
    # SQLAlchemy < 0.7
    from sqlalchemy.topological import sort


logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class PatchManager(object):
    """
    An instance of this class collects a set of patches and acts as
    a dictionary. It's able to serialize the patches taking into
    account the dependencies.
    """

    def __init__(self):
        self.db = {}

    def __getitem__(self, patchid):
        """
        Return the patch given its `patchid`, or ``None`` if it does not exist.
        """
        return self.db.get(patchid)

    def __setitem__(self, patchid, patch):
        """
        Register the given `patch` identified by `patchid`.
        """
        self.db[patchid] = patch

    def neededPatches(self, context):
        """
        Return an iterator over *not yet applied* patches, in the
        right order to satisfy their inter-dependencies.

        >>> from .contexts import ExecutionContext
        >>> from .patch import make_patch
        >>> ctx = ExecutionContext()
        >>> pm = patch_manager(None)
        >>> first = make_patch(u'first', u'script',
        ...                    dict(revision=1, language='test',
        ...                         depends='second'))
        >>> pm[u'first'] = first
        >>> second = make_patch(u'second', u'script',
        ...                     dict(revision=2, language='test'))
        >>> pm[u'second'] = second
        >>> third = make_patch(u'third', u'script',
        ...                    dict(depends='second@1',
        ...                         preceeds='first',
        ...                         language='test'))
        >>> pm[u'third'] = third
        >>> always_beg = make_patch(u'always_beg', u'script',
        ...                         dict(always='first', language='test'))
        >>> pm[u'always_beg'] = always_beg
        >>> always_last = make_patch(u'always_last', u'script',
        ...                          dict(always='last', language='test'))
        >>> pm[u'always_last'] = always_last
        >>> assert ['%s' % p for p in pm.neededPatches(ctx)] == [
        ...     str(always_beg),
        ...     str(third),
        ...     str(second),
        ...     str(first),
        ...     str(always_last),
        ...     ]
        """

        # SA topological sort relies on objects id()
        uniquified = {}
        def uniquify(t):
            return uniquified.setdefault(t, t)

        skippedcnt = 0
        constraints = set()
        missing = []
        always_first = []
        always_last = []

        logger.debug(u"Collecting and ordering patches...")
        for pid, patch in self.db.items():
            if not patch.always and patch.revision == context[pid]:
                logger.debug(u"Skipping %s, already applied", patch)
                continue

            patch.adjustUnspecifiedRevisions(self)

            if patch.verifyConditions(context.for_language(patch.language)):
                skip = False
                if patch.brings:
                    for depid, deprev in patch.depends:
                        current = context[depid]
                        if current is not None and current > deprev:
                            logger.debug(u"Ignoring %s because it depends on"
                                         u" '%s@%d', currently at version %s",
                                         patch, depid, deprev, current)
                            skip = True
                            break
                if skip:
                    skippedcnt += 1
                    continue

                this = uniquify((patch.patchid, patch.revision))
                if patch.always:
                    if patch.always == 'first':
                        always_first.append(this)
                    else:
                        always_last.append(this)
                else:
                    missing.append(this)

                for dep in patch.depends:
                    constraints.add( (uniquify(dep), this) )
                for preceed in patch.preceeds:
                    constraints.add( (this, uniquify(preceed)) )
                for bring in patch.brings:
                    constraints.add( (this, uniquify(bring)) )
            else:
                logger.debug(u"Ignoring %s, because it does not satisfy the"
                             u" conditions", patch)

        if always_first:
            logger.info(u"Applying execute-always-first patches...")
            for pid, rev in sort(constraints, always_first):
                yield self[pid]

        logger.info(u"Applying missing patches...")
        for pid, rev in sort(constraints, missing):
            if (pid, rev) in missing:
                currrev = context[pid]
                patch = self[pid]

                if currrev is None or currrev < rev:
                    ignore = False
                    if patch.brings:
                        for depid,deprev in patch.depends:
                            currdeprev = context[depid]
                            if currdeprev is None or currdeprev != deprev:
                                logger.debug(u"Ignoring %s, because it depends"
                                             u" on '%s@%d' which is currently"
                                             u" at revision %s",
                                             patch, depid, deprev, currdeprev)
                                ignore = True
                    if not ignore:
                        yield patch
                else:
                    logger.debug(u"Skipping %s, already applied", patch)
            else:
                logger.debug(u"Skipping '%s@%d', introduced by dependencies",
                             pid, rev)

        if always_last:
            logger.info(u"Applying execute-always-last patches...")
            for pid, rev in sort(constraints, always_last):
                yield self[pid]


class PersistentPatchManager(PatchManager):
    """
    Patch manager that uses a Pickle/YAML/JSON file as its persistent storage.

    >>> from os import unlink
    >>> from tempfile import mktemp
    >>> from .patch import make_patch
    >>> tempfile = mktemp(suffix='.yaml')
    >>> pm = PersistentPatchManager(tempfile)
    >>> first = make_patch(u'first', u'script',
    ...                    dict(revision=1, language='test',
    ...                         depends='second'),
    ...                    u'This patch costs € 0.1')
    >>> pm[u'first'] = first
    >>> second = make_patch(u'second', u'script',
    ...                     dict(revision=2, language='test'))
    >>> pm[u'second'] = second
    >>> third = make_patch(u'third', u'script',
    ...                    dict(depends='second@1',
    ...                         preceeds='first',
    ...                         language='test'))
    >>> pm[u'third'] = third
    >>> pm.save()
    >>> with open(tempfile, 'rb') as f:
    ...    content = f.read().decode('utf-8')
    ...    assert u'This patch costs ' in content
    >>> pm.load()
    >>> assert u'This patch costs € 0.1' == pm[u'first'].description
    >>> unlink(tempfile)
    """

    def __init__(self, storage_path=None):
        super(PersistentPatchManager, self).__init__()
        self.storage_path = storage_path

    def save(self):
        if self.storage_path is None:
            return

        logger.debug(u"Writing patches to %s", self.storage_path)
        spendswith = self.storage_path.endswith
        if spendswith('.yaml') or spendswith('.json'):
            storage = open(self.storage_path, 'w')

            # Order patches by id, both for easier lookup and to
            # avoid VCs stress

            asdicts = [self.db[sid].asdict for sid in sorted(self.db)]

            # Optimize for size and readability: store simple
            # dictionaries, with UTF-8 encoded strings; rename
            # "patchid" to "ID", as the latter will be the first key
            # in the YAML dictionary (entries are usually sorted
            # alphabetically).

            if spendswith('.yaml'):
                from yaml import dump_all

                storage.write(dump_all(asdicts, default_flow_style=False))
            else:
                from json import dumps

                storage.write(dumps(asdicts, sort_keys=True, indent=1))
        else:
            from pickle import dump

            storage = open(self.storage_path, 'wb')
            dump(self.db, storage)
        storage.close()
        logger.debug(u"Done writing patches")

    def load(self):
        import sys
        py2 = sys.version_info < (3,)
        logger.debug(u"Reading patches from %s", self.storage_path)
        storage = open(self.storage_path, 'rb')
        spendswith = self.storage_path.endswith
        if spendswith('.yaml') or spendswith('.json'):
            from .patch import make_patch

            if spendswith('.yaml'):
                from yaml import load_all
                asdicts = load_all(storage.read())
            else:
                from json import loads
                asdicts = loads(storage.read())

            db = self.db = {}
            for d in asdicts:
                if py2:
                    for i in d:
                        if isinstance(d[i], str):
                            d[i] = d[i].decode('utf-8')
                db[d['ID']] = make_patch(d['ID'], d['script'], d)
        else:
            from pickle import load
            self.db = load(storage)
        storage.close()
        logger.debug(u"Done reading patches")


__manager = None

def patch_manager(storage_path, overwrite=False, autosave=False):
    global __manager

    if not __manager:
        __manager = PersistentPatchManager(storage_path)
        if storage_path is not None: # used by doctests
            if not overwrite:
                __manager.load()
            if autosave:
                import atexit
                atexit.register(__manager.save)
    return __manager
