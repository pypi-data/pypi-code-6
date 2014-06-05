#!/usr/bin/env python3

"""ownCloud and Seafile conflict resolver

ownCloud often generates bunch of conflict files. Seafile is far better, but it
happens. Some of conflict files are completely senseless (they are equivalent to
non conflict files laying beside them), some of them really differs from their
neighborhoods. The aim of this script is to resolve conflict files of both
types.
"""

__version__ = "0.0.3"

# pylint: disable=C0103, C0111, W0105, W0141, W0142

import argparse
import filecmp
import logging as logger
import os
import re
try:
    # noinspection PyUnresolvedReferences
    from send2trash import send2trash
    can_delete_to_trash = True
except ImportError:
    can_delete_to_trash = False
import shlex
import shutil
import string
import subprocess
import tarfile
from pathlib import Path
try:
    from enum import IntEnum
except ImportError:
    from flufl.enum import IntEnum


class Keep(IntEnum):
    none = 0
    conflict = 1
    normal = 2
    both = 3


class FileManipulatorMeta(type):
    def __str__(cls):
        return cls.__name__.replace(cls.__base__.__name__, '').lower()


class FileManipulator:
    __metaclass__ = FileManipulatorMeta
    log_message = 'Processed: "{}"'

    def __init__(self, files):
        self.files = files

    @staticmethod
    def action(self, *args, **kwargs):
        pass


class BaseDeleter(FileManipulator):
    def __init__(self, files=None):
        super().__init__(files=files if files else [])

    def apply(self):
        for f in self.files:
            try:
                self.action(str(f))
                logger.info(self.__class__.log_message.format(f))
            except FileNotFoundError:
                logger.debug("File not found: {}, not deleting it".format(f))

    def delete(self, file_path):
        self.files.append(file_path)


class RemoveDeleter(BaseDeleter):
    log_message = 'Removed: "{}"'
    action = staticmethod(os.remove)


class TrashDeleter(BaseDeleter):
    log_message = 'Sent to trash: "{}"'
    action = staticmethod(send2trash)


class LogDeleter(BaseDeleter):
    pass


class BaseRenamer(FileManipulator):
    log_message = 'Renamed: "{0}" -> "{1}"'

    def __init__(self, files=None):
        super().__init__(files=files if files else {})

    def apply(self):
        for src, dst in self.files.items():
            try:
                self.action(str(src), str(dst))
                logger.info(self.__class__.log_message.format(src, dst))
            except FileNotFoundError:
                logger.debug("File not found: {}, not renaming it".format(src))
            except FileExistsError:
                logger.debug("File exists: {dst}, not renaming {src} -> {dst} "
                             "it".format(src=src, dst=dst))

    def rename(self, src, dst):
        self.files[src] = dst

    def rename_conflict_to_normal_file(self, conflict_file_path):
        self.rename(conflict_file_path,
                    ConflictResolver.normal_file(conflict_file_path))


class Renamer(BaseRenamer):
    action = staticmethod(os.rename)


class LogRenamer(BaseRenamer):
    pass


class ResolverException(Exception):
    pass


class ResetResolving(ResolverException):
    pass


class StopResolving(ResolverException):
    pass


class ConflictResolver:
    class Program:
        default_name = "kdiff3"

        def __init__(self, name=None, arguments=None):
            self.name = name if name else self.default_name
            self.arguments = arguments
            self.process = None

        def __bool__(self):
            return bool(shutil.which(self.name))

        def execute(self, conflict_file_path):
            normal_file_path = ConflictResolver.normal_file(conflict_file_path)
            program_args = [arg.safe_substitute(normal=normal_file_path,
                                                conflict=conflict_file_path)
                            for arg in self.arguments]
            self.process = subprocess.Popen([self.name] + program_args)

        def terminate(self):
            if self.process:
                self.process.terminate()

        def wait(self):
            if self.process:
                return self.process.wait()

    re_conflict_file_path_part = {
        'owncloud': r"_conflict-\d{8,8}-\d{6,6}",
        'seafile': r" \(.*@.* \d{4}-[01]\d-[0-3]\d-[0-2]\d-[0-5]\d-[0-5]\d\)",
    }

    def __init__(self, root=Path('.'), *, deleter=RemoveDeleter, renamer=Renamer,
                 program=Program(), backup=True):
        self.root = root
        self.deleter = deleter()
        self.renamer = renamer()
        self.program = program
        self.backup = backup

    @staticmethod
    def is_conflict_file(file_path):
        return any((re.search(re_conflict_file_path_part, str(file_path)))
                   for re_conflict_file_path_part in
                   ConflictResolver.re_conflict_file_path_part.values())

    @staticmethod
    def normal_file(conflict_file_path):
        result = str(conflict_file_path)
        for re_conflict_file_path_part in (
                ConflictResolver.re_conflict_file_path_part.values()):
            result = re.sub(re_conflict_file_path_part, '', result)
        return Path(result)

    def conflict_files(self):
        return (f for f in self.root.rglob('*') if self.is_conflict_file(f))

    def resolve(self, conflict_file_path):
        normal_file_path = self.normal_file(conflict_file_path)
        if normal_file_path.exists():
            symlinks = [f for f in (conflict_file_path, normal_file_path)
                        if f.is_symlink()]
            if len(symlinks) == 0:
                result = equal = filecmp.cmp(
                    str(normal_file_path), str(conflict_file_path),
                    shallow=False)
                if equal:
                    self.deleter.delete(conflict_file_path)
            else:
                for symlink in symlinks:
                    logger.info('File {} symlink is symlink. Removing symlinks '
                                'is not implemented'.format(symlink))
                result = True
        else:
            logger.debug(
                'There is file with name "{}" but file with name "{}" not '
                'found. Assume that is not a conflict.'.format(
                    conflict_file_path, normal_file_path))
            self.renamer.rename(conflict_file_path, normal_file_path)
            result = True
        return result

    def create_backup(self):
        def backup_file_path():
            def backup_file_name(number):
                backup_file_name_template = 'conflict_files_backup{sep}{i}.tar'
                return (backup_file_name_template.format(sep='', i='')
                        if number == -1 else
                        backup_file_name_template.format(sep=' - ', i=i))

            def make_backup_file_path(number):
                return self.root/backup_file_name(number)

            i = -1
            while make_backup_file_path(i).exists():
                i += 1
            return make_backup_file_path(i)

        with tarfile.open(str(backup_file_path()), 'w') as backup_file:
            save_cwd = os.getcwd()
            try:
                os.chdir(str(self.root))
                for conflict_file in self.conflict_files():
                    backup_file.add(str(conflict_file.relative_to(self.root)))
                    normal_file = self.normal_file(conflict_file)
                    if normal_file.exists():
                        backup_file.add(str(normal_file.relative_to(self.root)))
            finally:
                os.chdir(save_cwd)

    def apply_actions(self):
        self.deleter.apply()
        self.renamer.apply()

    def resolve_all(self):
        """Resolve all files in root directory (recursively)"""

        if self.backup:
            self.create_backup()
        if not self.program:
            if self.program is not None:
                logger.error('Program "{}" not found, please install it or '
                             "specify different program with option "
                             '"--program"'.format(self.program.name))
            exit()
        try:
            for conflict_file_path in self.conflict_files():
                try:
                    self.resolve(conflict_file_path)
                except StopResolving:
                    break
        except ResetResolving:
            return
        self.apply_actions()


class CompareConflictResolver(ConflictResolver):
    def resolve_manually(self, conflict_file_path, *, keep=Keep.both):
        result = True
        normal_file_path = self.normal_file(conflict_file_path)
        if keep is Keep.none:
            self.deleter.delete(conflict_file_path)
            self.deleter.delete(normal_file_path)
        elif keep is Keep.conflict:
            self.deleter.delete(normal_file_path)
            self.renamer.rename_conflict_to_normal_file(conflict_file_path)
        elif keep is Keep.normal:
            self.deleter.delete(conflict_file_path)
        elif keep is Keep.both:
            pass
        else:
            result = False
        return result

    def resolve(self, conflict_file_path):
        result = super().resolve(conflict_file_path)
        while not result and self.program is not None:
            self.program.execute(conflict_file_path)
            keep = None
            try:
                while keep is None:
                    def print_help():
                        print()
                        print("0 - don't save any file, remove both files\n"
                              "1 - remove normal file, save and rename conflict file\n"
                              "2 - save normal file, remove conflict file\n"
                              "r - reset all actions, leave all files as are\n"
                              "s - stop processing and apply all actions\n")

                    answer = input(
                        "What file do you want to save (1 - conflict, 2 - normal, "
                        "3 - both, ? - show all options) [3]: ")
                    if answer == '':
                        keep = Keep.both
                    elif answer == '?':
                        print_help()
                    elif answer == 'r':
                        raise ResetResolving
                    elif answer == 's':
                        raise StopResolving
                    else:
                        try:
                            keep = Keep(int(answer))
                        except ValueError:
                            print_help()
            finally:
                self.program.terminate()
            result = self.resolve_manually(conflict_file_path, keep=keep)
        return result


class MergeConflictResolver(ConflictResolver):
    def resolve(self, conflict_file_path):
        result = super().resolve(conflict_file_path)
        if not result and self.program:
            self.program.execute(conflict_file_path)
            result = self.program.wait() == 0
            if result:
                self.deleter.delete(conflict_file_path)
        return result


class ListConflictResolver(ConflictResolver):
    def __init__(self, root=Path('.'), *, list_normal=False, **kwargs):
        super().__init__(root, **kwargs)
        self.list_normal = list_normal

    def resolve_all(self):
        for f in self.conflict_files():
            print(f)
            if self.list_normal:
                print(self.normal_file(f))


class ListAllConflictResolver(ListConflictResolver):
    def __init__(self, root=Path('.'), **kwargs):
        super().__init__(root, list_normal=True, **kwargs)


def to_(s, delimiter='_'):
    return re.sub(r'(?!^)([A-Z]+)', delimiter + r'\1', s).lower()


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__.partition('\n')[0])

    def class_from_action(cls):
        return globals()[cls.__name__.replace("Action", "")]

    class Action(argparse.Action):
        def __init__(self, option_strings, dest, **kwargs):
            super().__init__(option_strings=option_strings, dest=dest, nargs=0,
                             const=class_from_action(self.__class__), **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, self.const)

    class BaseDeleterAction(Action):
        def __init__(self, option_strings, dest, **kwargs):
            super().__init__(option_strings, dest='deleter', **kwargs)

    class LogDeleterAction(BaseDeleterAction):
        pass

    class RemoveDeleterAction(BaseDeleterAction):
        pass

    class TrashDeleterAction(BaseDeleterAction):
        pass

    class ConflictResolverAction(Action):
        def __init__(self, option_strings, dest, **kwargs):
            super().__init__(option_strings, dest='conflict_resolver', **kwargs)

    class CompareConflictResolverAction(ConflictResolverAction):
        pass

    class MergeConflictResolverAction(ConflictResolverAction):
        pass

    class ListConflictResolverAction(ConflictResolverAction):
        pass

    class ListAllConflictResolverAction(ConflictResolverAction):
        pass

    parser.add_argument('dirs', nargs='*', default='.',
                        help="directories to process "
                        "[default: current directory]")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {}".format(__version__))
    parser.add_argument('-v', '--verbose', dest="verbose_count",
                        action="count", default=0,
                        help="increases log verbosity for each occurrence.")
    deleter_group = parser.add_mutually_exclusive_group()
    deleter_group.add_argument('-n', '--dry-run', action=LogDeleterAction,
                               help="only log, do not delete files")
    deleter_group.add_argument('-r', '--remove', action=RemoveDeleterAction,
                               help="remove deleted files completely")
    deleter_group.add_argument('-t', '--trash', action=TrashDeleterAction,
                               help="send deleted files to trash")
    conflict_resolver_group = parser.add_mutually_exclusive_group()
    conflict_resolver_group.add_argument('-c', '--compare',
                                         action=CompareConflictResolverAction,
                                         help="compare conflict files to "
                                              "select required [default]")
    conflict_resolver_group.add_argument('-m', '--merge',
                                         action=MergeConflictResolverAction,
                                         help="merge conflict files")
    conflict_resolver_group.add_argument('-l', '--list',
                                         action=ListConflictResolverAction,
                                         help="list conflict files")
    conflict_resolver_group.add_argument('-al', '--list-all',
                                         action=ListAllConflictResolverAction,
                                         help="list conflict files and "
                                              "their corresponding normal "
                                              "files")
    parser.add_argument('-p', '--program', default='',
                        help="program to compare files [default: kdiff3]")
    parser.add_argument('-a', '--arguments', default='',
                        help="arguments that should be passed to conflict "
                             "resolver program; you can use predefined "
                             "variables (use brackets) to substitute with file "
                             "name: ($conflict — file with conflict appendix, "
                             "$normal — file without conflict appendix)")
    backup_group = parser.add_mutually_exclusive_group()
    backup_group.add_argument('-b', '--backup', action="store_true",
                              default=True, help="create backup [default]")
    backup_group.add_argument('-B', '--no-backup', action="store_false",
                              dest="backup", help="don't create backup")
    parser.set_defaults(conflict_resolver=CompareConflictResolver,
                        deleter=RemoveDeleter)
    if not can_delete_to_trash:
        parser.epilog += " To enable deleting to trash, please install python "
        "module send2trash. You can do it with pip:\n"
        "  pip3 install send2trash"
    result = parser.parse_args()
    result.dirs = [Path(d) for d in result.dirs]
    if result.deleter is not LogDeleter:
        result.renamer = Renamer
    else:
        result.renamer = LogRenamer
    if not result.arguments:
        if result.conflict_resolver is MergeConflictResolver:
            result.arguments = "-m $conflict $normal -o $normal"
        else:
            result.arguments = "$conflict $normal"
    result.arguments = [string.Template(arg) for arg in shlex.split(result.arguments)]
    return result


def run(args):
    for dir_path in args.dirs:
        log_level = max(logger.INFO - 10*args.verbose_count, logger.NOTSET)
        logger.basicConfig(level=log_level, format='%(message)s')
        program = ConflictResolver.Program(args.program, args.arguments)
        logger.debug("Using {}".format(
            to_(args.conflict_resolver.__name__, delimiter=' ')))
        resolver = args.conflict_resolver(
            dir_path, deleter=args.deleter, renamer=args.renamer,
            program=program, backup=args.backup)
        if len(args.dirs) > 1:
            logger.info('Working on directory: "{}"'.format(dir_path))
        resolver.resolve_all()


if __name__ == "__main__":
    try:
        args = parse_arguments()
        run(args)
    finally:
        logger.shutdown()
