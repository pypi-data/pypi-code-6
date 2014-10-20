import re

from spelltinkle.fromimp import complete


def complete_word(doc):
    r, c = doc.view.pos
    line = doc.lines[r]
    match = re.search('[a-zA-Z]\w*$', line[:c])
    if not match:
        return
    word = line[match.start():match.end()]
    n = len(word)
    regex = re.compile(r'\b' + word + '\w*')
    words = set()
    for R, line in enumerate(doc.lines):
        for match in regex.finditer(line):
            c1, c2 = match.span()
            if R != r or c1 != c - n:
                words.add(line[c1:c2])
    newword = complete(word, list(words))
    if newword != word:
        doc.change(r, c, r, c, [newword[n:]])
