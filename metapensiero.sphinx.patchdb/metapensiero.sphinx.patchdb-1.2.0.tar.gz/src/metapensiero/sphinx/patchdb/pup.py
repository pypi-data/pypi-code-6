#!/usr/bin/env python
# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Apply collected patches to a database
# :Creato il: Wed Nov 12 23:10:22 2003
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later

from __future__ import absolute_import

from .contexts import ExecutionContext, ExecutionError
from .patch import DependencyError
from .manager import patch_manager


def main():
    import locale, logging
    from argparse import ArgumentParser

    locale.setlocale(locale.LC_ALL, '')

    parser = ArgumentParser(description="Database script applier")

    parser.add_argument("--sqlalchemy", metavar="URL",
                        help=u"Select the SQLAlchemy context. URL is a"
                        u" string of the kind ``mysql+cymysql://test:test@127.0.0.1/test``.")
    parser.add_argument("--postgres", metavar="DSN",
                        help=u"Select the PostgresQL context. DSN is a"
                        u" string of the kind ``dbname=gam``.")
    parser.add_argument("--firebird", metavar="DSN",
                        help=u"Select the Firebird context.")
    parser.add_argument("--mysql", metavar="DBNAME",
                        help=u"Select the MySQL context.")
    parser.add_argument("-u", "--username", metavar="USER",
                        help=u"Username to log into the database.")
    parser.add_argument("-p", "--password", metavar="PASSWORD",
                        help=u"Password")
    parser.add_argument("--host", metavar="HOSTNAME", default="localhost",
                        help=u"Host name where MySQL server runs, defaults to ``localhost``.")
    parser.add_argument("-s", "--patch-storage", metavar="SHELVE",
                        dest="storage_path",
                        help=u"Specify the archive containing collected scripts.")
    parser.add_argument("-l", "--log-file", metavar="FILE",
                        dest="log_path",
                        help=u"Specify where to write the execution log.")
    parser.add_argument("--assume-already-applied", default=False, action="store_true",
                        help=u"Assume missing patches are already applied, do not"
                        " re-execute them.")
    parser.add_argument("-a", "--assert", metavar="NAME", action="append", dest="assertions",
                        help="Introduce an arbitrary assertion usable as a pre-condition"
                        " by the scripts. NAME may be a simple string or something like"
                        " ``production=true``. This option may be given multiple times.")
    parser.add_argument("-n", "--dry-run", default=False, action="store_true",
                        help=u"Don't apply patches, just list them.")
    parser.add_argument("-v", "--verbose", default=False, action="store_true",
                        help=u"Emit noise.")
    parser.add_argument("-d", "--debug", default=False, action="store_true",
                        help=u"Emit debug messages.")

    args = parser.parse_args()

    if args.log_path:
        level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(filename=args.log_path, level=level,
                            format="%(asctime)s [%(levelname).1s] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    else:
        if args.debug:
            level = logging.DEBUG
        elif args.verbose:
            level = logging.INFO
        else:
            level = logging.WARNING
        logging.basicConfig(level=level, format="[%(levelname).1s] %(message)s")

    if args.sqlalchemy:
        from .contexts.alchemy import SQLAlchemyContext
        sqlctx = SQLAlchemyContext(url=args.sqlalchemy)
    elif args.postgres:
        from .contexts.postgres import PostgresContext
        sqlctx = PostgresContext(dsn=args.postgres)
    elif args.firebird:
        from .contexts.firebird import FirebirdContext
        sqlctx = FirebirdContext(dsn=args.firebird,
                                 username=args.username, password=args.password)
    elif args.mysql:
        from .contexts.mysql import MySQLContext
        sqlctx = MySQLContext(host=args.host, db=args.mysql,
                              username=args.username, password=args.password)
    else:
        print(u"You must select exactly one database with either '--postgres',"
              u" '--firebird', '--sqlalchemy' or '--mysql'!")
        return 128

    if args.storage_path:
        pm = patch_manager(args.storage_path)
    else:
        print(u"Option --patch-storage is mandatory")
        return 128

    if args.assertions:
        try:
            sqlctx.addAssertions(args.assertions)
        except ValueError as e:
            print(u"Invalid assertion: %s" % e)
            return 128

    patches = pm.neededPatches(sqlctx)
    execute = ExecutionContext.execute

    try:
        count = 0
        for p in patches:
            count += 1
            if not args.dry_run:
                execute(p, args)
            else:
                print(u"I would execute %s... " % p)
        print(u"\nDone, applied %d script%s" %
              (count, "s" if count != 1 else ""))
        return 0 # OK
    except (DependencyError, ExecutionError) as e:
        try:
            print(u"\nError: %s" % e)
        except:
            import sys
            if sys.version_info >= (3,):
                print("\nError:", str(e).encode('ascii', 'ignore'))
            else:
                print("\nError:", unicode(e).encode('ascii', 'ignore'))
        return 1


if __name__ == '__main__':
    from sys import exit

    exit(main())
