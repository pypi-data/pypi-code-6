def format_group(kind, imports, indent, config):
    func = {'import': format_imports, 'from': format_froms}
    noqa, regular = [], []
    for im in imports:
        (noqa if im.noqa else regular).append(im)
    rv = add_noqas(func[kind](noqa, indent, config, noqa=True))
    rv += func[kind](regular, indent, config, noqa=False)
    return [indent + line + '\n' for line in rv]


def add_noqas(lines):
    offset = lines and max(len(line) for line in lines)
    return [add_noqa(line, offset) for line in lines]


def add_noqa(line, offset):
    padding = offset - len(line)
    return line + (padding * ' ') + '  # noqa'


def format_imports(imports, indent, config, noqa):
    return ['import {0}'.format(im.module) for im in imports]


def format_froms(imports, indent, config, noqa):
    limit = config['limit'] - len(indent) - (8 if noqa else 0)
    return [line for im in imports for line in format_from(im, limit)]


def format_from(im, limit):
    first = 'from {0} import '.format(im.module)
    names = [str(n) for n in im.names]
    sizes = [len(n) + 2 for n in names]

    # skip parens if it fits on single line
    if len(first) + sum(sizes) < limit + 2:
        return [first + ', '.join(names)]

    first += '('
    size = len(first)
    lines = [' ' * size + ', '.join(names[start:end]) + ','
             for start, end in _dynamic_wrap(sizes, limit - size)]

    lines[0] = first + lines[0][size:]
    lines[-1] = lines[-1][:-1] + ')'
    return lines


def _dynamic_wrap(items, limit):
    scores, trace = [0], []
    for j in range(len(items)):
        best, index = float('inf'), -1
        psum = limit
        for i in reversed(range(j + 1)):
            psum -= items[i]
            score = scores[i] + psum ** 2
            if score < best and psum >= 0 or index < 0:
                best, index = score, i

        scores.append(best)
        trace.append(index)

    return _build_indices(trace)


def _build_indices(trace):
    indices, index = [], len(trace) - 1
    while index >= 0:
        indices.append((trace[index], index + 1))
        index = trace[index] - 1

    return indices[::-1]
