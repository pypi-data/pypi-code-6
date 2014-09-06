def transform(deck, sideboard=False):
    # Strip whitespace
    lines = (l.strip() for l in deck.splitlines())
    # Remove empty and comment lines
    lines = (l for l in lines if l and not l.startswith('//'))

    # Do or do not use sideboard lines
    if sideboard:
        lines = (l[3:] for l in lines if l.startswith('SB:'))
    else:
        lines = (l for l in lines if not l.startswith('SB:'))

    # Do transformation
    lines = (transform_line(l) for l in lines)

    return '\n'.join(lines)


def transform_line(deck_line):
    deck_line = _remove_brackets(deck_line)
    return deck_line.strip()


def _remove_brackets(deck_line):
    "Remove set information bracket."
    b_start = deck_line.find('[')
    if b_start != -1:
        b_end = deck_line.find(']')
        deck_line = deck_line[:b_start] + deck_line[b_end + 1:]
    return deck_line
