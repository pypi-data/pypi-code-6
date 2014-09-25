import os
from pathlib import Path
from string import Template

    # for root, dirs, files in os.walk(str(service_dir)):
    #     print(_(root), [_(d) for d in dirs], [_(f) for f in files])

# def _(original):
#     d = {'name': 'fizzgig'}
#     return Template(original).safe_substitute(d)

#def walk():

IGNORABLES = [
    '.git',
]

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


def petrify(source_dir, target_dir, replacements, ignorables=None, emptiables=None):

    if ignorables is None:
        ignorables = IGNORABLES

    if emptiables is None:
        emptiables = []

    p = Petrifier(replacements)

    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir()

    for root, dirs, files in os.walk(str(source_dir)):
        source_root = Path(root)
        target_root = Path(p(root.replace(source_dir, target_dir)))
        print(source_root)
        if not target_root.exists():
            target_root.mkdir()
        for ignorable in ignorables:
            if ignorable in dirs:
                dirs.remove(ignorable)
        for f in files:
            if f in ignorables:
                continue
            source_path = source_root / f
            target_path = target_root / p(f)
            if f in emptiables:
                with target_path.open('w') as t:
                    t.write('')
                continue
            print("  opening ", source_path)
            print("  creating", target_path)
            with source_path.open() as s:
                with target_path.open('w') as t:
                    for line in s:
                        t.write(p(line))

def rehydrate(source_dir, target_dir, replacements):

    h = Hydrator(replacements)

    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir()

    for root, dirs, files in os.walk(str(source_dir)):
        source_root = Path(root)
        target_root = Path(h(root.replace(source_dir, target_dir)))
        print(source_root)
        if not target_root.exists():
            target_root.mkdir()
        for f in files:
            source_path = source_root / f
            target_path = target_root / h(f)
            print("  opening ", source_path)
            print("  creating", target_path)
            with source_path.open() as s:
                with target_path.open('w') as t:
                    for line in s:
                        t.write(h(line))
