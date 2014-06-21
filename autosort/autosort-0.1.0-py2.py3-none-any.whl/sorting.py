import os
from collections import defaultdict

from .parsing import parse_imports
from .formatting import format_group
from .utils import interpose
from .config import get_config


def sort_imports(source, path):
    config = get_config(path)
    lines = source.splitlines(True)
    diff = []
    for block in parse_imports(lines):
        diff += [(im.start, im.end, []) for im in block.imports]
        diff += [(line, line, rows)
                 for line, rows in organize_block(block, lines, config)]

    for start, end, change in sorted(diff, reverse=True):
        lines[start:end] = change

    return ''.join(lines)


def organize_block(block, lines, config):
    def sort(group):
        return sort_group(group, block.indent, config)

    regular, groups = extract_groups(block, lines)
    regulars = [sort(g) for g in split_regular_imports(regular, config)]

    return ([(g[0].start, sort(g)) for g in groups] +
            [(block.start, interpose(regulars, ['\n']))])


def split_regular_imports(imports, config):
    result = defaultdict(list)
    for im in imports:
        result[classify_import(im, config)].append(im)

    return [result[key] for key in sorted(result.keys())]


def classify_import(im, config):
    DUNDER, STDLIB, THIRDPARTY, LOCAL, RELATIVE = range(5)
    name = im.module.name.split('.')[0]

    if name == '':
        return RELATIVE
    if name in config['local_modules']:
        return LOCAL
    if name in config['dunders']:
        return DUNDER
    if name in config['stdlib']:
        return STDLIB
    return THIRDPARTY


def flatten(imports):
    result = {}
    for im in imports:
        result[im.module] = result.get(im.module, im).merge(im)
    return result.values()


def sort_group(group, indent, config):
    imports = flatten([im for im in group if im.kind == 'import'])
    froms = flatten([im for im in group if im.kind == 'from'])

    return (format_group('import', imports, indent, config) +
            format_group('from', froms, indent, config))


def cut_group(imports, index):
    j = index + 1
    while j < len(imports) and imports[j].start == imports[j-1].end:
        j += 1
    res, imports[index:j] = imports[index:j], []
    return res


def extract_groups(block, lines):
    index = 0
    groups = []
    imports = block.imports
    while index < len(imports):
        start = imports[index].start
        if start > 0 and lines[start - 1].startswith(block.indent + '#'):
            groups.append(cut_group(imports, index))
        else:
            index += 1

    return imports, groups
