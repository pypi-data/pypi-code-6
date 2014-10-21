from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

import io
import sys
import os

log = logging.getLogger(__name__)


leader = 'from __future__ import '


def find_future_imports(f):
    """
    Return a list of __future__ import statements in a file. Each list element
    is a tuple of (start_line_no, end_line_no, imports).

    Note that although a __future__ import statement must always be the first
    logical code line in a Python file, it may be preceded by comments,
    docstrings, or blank lines, and we want to preserve those.
    """
    so_far = []
    inside_parens = False
    inside_docstring = False
    start_line_no = end_line_no = None

    for line_no, line in enumerate(f, start=1):
        if inside_docstring:
            if line.startswith('"""') or line.startswith("'''"):
                inside_docstring = False
            continue

        elif line.startswith('"""') or line.startswith("'''"):
            inside_docstring = True
            continue

        if inside_parens:
            so_far.append(line)
            if ')' in line:
                end_line_no = line_no
                inside_parens = False
            else:
                continue

        elif line.startswith(leader):
            end_line_no = start_line_no = line_no
            so_far.append(line)
            if '(' in line:
                inside_parens = True
                continue

        if so_far:
            imports = ''.join(so_far)[len(leader):].strip()
            imports = imports.rstrip(')').lstrip('(')
            imports = [word.strip() for word in imports.split(',')]
            yield start_line_no, end_line_no, imports
            so_far = []

    if inside_parens:
        raise SyntaxError("got to end of file without closing paren")


def intervals_to_set(intervals):
    """
    Convert a list of intervals into a set of line_numbers represented by those
    intervals.
    """
    line_nos = set()
    for start, end in intervals:
        line_nos.update(range(start, end + 1))
    return line_nos


def make_new_import_statement(imports, line_length=80):
    """
    Make a new __future__ import statement with the supplied keywords. Don't
    exceed ``line_length`` per line: use parantheses continuations and wrap if
    necessary. Sort import keywords so that the same set of keywords always
    generates the same import statement: we want to minimize the SCM changeset
    when manipulating a large project, and avoid 'false changes'.
    """
    imports = list(imports)
    imports.sort()

    s = leader + ', '.join(imports)
    if len(s) <= line_length:
        return s
    else:
        # Use parens and split up lines.
        this_line = leader + '('
        indent = len(this_line) * ' '
        last_import = imports[-1]

        lines = []
        for word in imports:
            if word == last_import:
                add_word = word + ')'
            else:
                add_word = word + ', '
            candidate_line = this_line + add_word

            if len(candidate_line) > line_length:
                # This candidate will be too long, go to the next line.
                lines.append(this_line)
                this_line = indent + add_word
            else:
                this_line = candidate_line

        lines.append(this_line)
        return '\n'.join(line.rstrip() for line in lines)


def rewrite_file(filename, import_intervals, new_imports):
    exclude_line_nos = intervals_to_set(import_intervals)

    lines = []
    with io.open(filename) as f:
        for line_no, line in enumerate(f, start=1):
            if line_no not in exclude_line_nos:
                lines.append(line)

    if import_intervals:
        new_import_line_no = import_intervals[0][0]
    else:
        new_import_line_no = 1

    new_import_statement = make_new_import_statement(new_imports)
    lines.insert(new_import_line_no - 1, new_import_statement + '\n')

    lines = ''.join(lines)

    with io.open(filename, 'w') as f:
        f.write(lines)


def process_file(filename, add=(), remove=(), dry_run=False):
    """
    Update the __future__ imports in a single file.
    """
    log.info('Processing file: %s with add=%s, remove=%s', filename,
             ', '.join(add), ', '.join(remove))
    add = set(add)
    remove = set(remove)

    # Strategy: iterate through twice. The first time, gather all of the
    # __future__ imports. The second time, replace the first one with the
    # finalized __future__ import, and remove the rest.

    # Look for existing __future__ imports and try to modify them in-place
    # rather than moving or creating a new one.
    all_imports = set()
    import_intervals = []
    with io.open(filename) as f:
        for start_line_no, end_line_no, imports in find_future_imports(f):
            all_imports.update(set(imports))
            import_intervals.append((start_line_no, end_line_no))

    if dry_run:
        would_remove = all_imports & remove
        would_add = add - all_imports
        if would_add or would_remove:
            log.warn("Changes to %s", filename)
        if would_remove:
            log.warn("  Would remove: %s", ', '.join(would_remove))
        if would_add:
            log.warn("  Would add: %s", ', '.join(would_add))
    else:
        all_imports.update(add)
        all_imports.difference_update(remove)
        rewrite_file(filename, import_intervals, all_imports)


def process_tree(path, add=(), remove=(), dry_run=False):
    """
    Update the __future__ imports in a directory tree.
    """
    log.info('Processing tree: %s with add=%s, remove=%s', path,
             ', '.join(add), ', '.join(remove))
    if not os.path.exists(path):
        raise ValueError("path not found: %r" % path)
    if not os.path.isdir(path):
        process_file(path, add=add, remove=remove, dry_run=dry_run)
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename.endswith('.py'):
                    filepath = os.path.join(dirpath, filename)
                    process_file(filepath, add=add, remove=remove, dry_run=dry_run)


def configure_logging(verbosity=4):
    """
    Configure logging for use with the asset compilation command.
    """
    levels = [logging.CRITICAL,
              logging.ERROR,
              logging.WARNING,
              logging.INFO,
              logging.DEBUG]

    ch = logging.StreamHandler()
    ch.setLevel(levels[verbosity])

    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)

    log.setLevel(logging.DEBUG)
    log.addHandler(ch)


def main(args=sys.argv):
    """
    Command-line tool entry point.
    """
    paths = []
    options = set()
    add = set()
    remove = set()
    for arg in args[1:]:
        if arg.startswith('--'):
            options.add(arg[2:])
        elif arg.startswith('+'):
            add.add(arg[1:])
        elif arg.startswith('-'):
            remove.add(arg[1:])
        else:
            paths.append(arg)

    if paths and (add or remove):
        verbosity = 2
        if 'verbose' in options:
            verbosity = 4
        if 'silent' in options:
            verbosity = 1
        configure_logging(verbosity)
        log.info('Adding imports: %s', ', '.join(add))
        log.info('Removing imports: %s', ', '.join(remove))

        dry_run = 'dry-run' in options

        for path in paths:
            process_tree(path, add=add, remove=remove, dry_run=dry_run)
    else:
        print("usage: %s <+keywords> <-keywords> <paths>" %
              os.path.basename(args[0]))
