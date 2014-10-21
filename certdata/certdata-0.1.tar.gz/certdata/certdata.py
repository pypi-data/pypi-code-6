

class Exception_certdata_parse(Exception):
    pass


def parse_certdata_text(text):
    """
    parse certdata.txt content

    Input is UTF-8 text. Output is list of lists of tuples of names types and
    values.

    raises Exception_certdata_parse in case of parse errors
    """

    blocks = []

    lines = text.split('\n')
    lines_l = len(lines)

    # input and intermediate data can be huge, so disposing unneeded
    # valiables might be not a bad idea
    del text

    block = []

    i = 0
    while True:

        if i == lines_l:
            if len(block) != 0:
                blocks.append(block)
            break

        line = lines[i]

        if len(line) == 0 or line.isspace() or line.startswith('#'):
            i += 1
            continue

        line_elements = line.split()

        if line_elements[0] == 'CKA_CLASS':
            if len(block) != 0:
                blocks.append(block)
            block = []

            docstring = None
            if i != 0:
                if lines[i - 1].startswith('#'):
                    docstring = []
                    j = i - 1
                    while lines[j].startswith('#'):
                        docstring.insert(0, lines[j])
                        j -= 1
                        if j < 0:
                            break

            block.append(('docstring', docstring))
            docstring = None

        if len(line_elements) > 1 and line_elements[1] == 'MULTILINE_OCTAL':

            i += 1

            multiline = []

            while True:
                if i > lines_l:
                    raise Exception_certdata_parse(
                        "Can't find multiline datatype END (line {})".format(i)
                        )
                line = lines[i]

                if line != 'END':
                    tl = line.split('\\')
                    while '' in tl:
                        tl.remove('')
                    multiline.append(tl)
                    del tl
                    i += 1
                else:
                    # i += 1
                    break

            line_elements.append(multiline)
            del multiline

        block.append(tuple(line_elements))

        i += 1

    ret = blocks

    return ret


def read_certdata_txt(filename):
    with open(filename) as f:
        t = f.read()
    return parse_certdata_text(t)


def handy_conversions(parse_result):
    ret = []
    for i in parse_result:
        d = {}
        for j in i:
            len_j = len(j)
            key = None
            value = None
            if j[0] == 'docstring':
                key = 'docstring'
                if j[1] is not None:
                    value = '\n'.join(j[1])
            elif len_j > 1 and j[1] == 'MULTILINE_OCTAL':
                key = j[0]
                value = multiline_oct_to_bytes(j[2])
            else:
                if len_j > 2:
                    key = j[0]
                    value = j[2]

            if key is not None:
                d[key] = value
        ret.append(d)
    return ret


def multiline_oct_to_bytes(data):
    lst = []
    for i in data:
        for j in i:
            lst.append(int(j, 8))
    return bytes(lst)
