import os
from pathlib import Path
from string import Template


IGNORABLES = (
    'CVS',
    '.svn',
    '.git',
    'tmp',
)


def petrify(source_dir, target_dir, replacements,
            ignorables=None, emptiables=None):
    """
    Create a skeleton in *target_dir* based on *source_dir*.

    *replacements* is a dict of (string, var) pairs where
    each occurence of *string* in file names or contents will
    be replaced by a template variable *var*.
    For example, {'myproject': 'projname'} would replace each
    occurence of 'myproject' with the string '${projname}'.

    *ignorables* is a list of file/directory names which will not
    be copied. *emptiables* is a list of file names which should
    exist in the destination, but without any contents.
    """

    if ignorables is None:
        ignorables = IGNORABLES

    petrifier = Petrifier(replacements)

    source_dir = Path(source_dir).resolve()

    for root, dirs, files in os.walk(str(source_dir)):

        for ignorable in ignorables:
            if ignorable in dirs:
                dirs.remove(ignorable)

        process_dir(source_dir, target_dir,
                    root, dirs, files,
                    petrifier, replacements, ignorables, emptiables)


def rehydrate(source_dir, target_dir, replacements):
    """
    Fill out the skeleton in *source_dir*, copying the contents to *target_dir*.

    *replacements* is a dict of (var, string) pairs where
    the stdlib Template object is used to replace all occurrences
    of $var or ${var} is replaced with *string*.
    """

    hydrator = Hydrator(replacements)

    source_dir = Path(source_dir).resolve()

    for root, dirs, files in os.walk(str(source_dir)):
        process_dir(str(source_dir), str(target_dir),
                    root, dirs, files,
                    hydrator, replacements)


class Petrifier():

    def __init__(self, replacements):
        self.replacements = {k: '${' + v + '}'
                             for (k, v) in replacements.items()}

    def __call__(self, original):
        modified = original
        for key, val in self.replacements.items():
            modified = modified.replace(key, val)
        return modified


class Hydrator():

    def __init__(self, replacements):
        self.replacements = replacements

    def __call__(self, original):
        return Template(original).safe_substitute(self.replacements)


def process_dir(source_dir, target_dir,
                root, dirs, files,
                munger, replacements, ignorables=None, emptiables=None):

    if ignorables is None:
        ignorables = []
    if emptiables is None:
        emptiables = []

    root = str(root)
    source_dir = str(source_dir)
    target_dir = str(target_dir)

    source_root = Path(root)
    target_root = Path(munger(root.replace(source_dir, target_dir)))
    print("In directory:", source_root)
    print(" with target:", target_root)

    if not target_root.exists():
        target_root.mkdir()

    for f in files:
        if f in ignorables:
            continue
        source_path = source_root / f
        target_path = target_root / munger(f)
        print("  creating", target_path)
        print("      from", source_path)
        if f in emptiables:
            with target_path.open('w') as t:
                t.write('')
            continue
        with source_path.open() as s:
            with target_path.open('w') as t:
                for line in s:
                    t.write(munger(line))
