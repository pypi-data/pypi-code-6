import re


def numbers_extractor(string, multiple=True):
    """
    :param string: a text that contains zero, one or # numbers
    :param multiple: if True return a list of # numbers
    that can be empty if no numbers are found.
    If False, return the first number found, or None.
    :return: integer or list of integer.
    If no numbers are found return None or []

    Example:

    >>> numbers_extractor("20 is 10 plus 10")
    [20, 10, 10]
    >>> numbers_extractor("20 is 10 plus 10", multiple=False)
    20
    >>> numbers_extractor("no numbers here")
    []
    >>> numbers_extractor("no numbers here", multiple=False)
    >>>

    """

    numbers = re.findall(r'\d+', string)
    if multiple:
        return [int(n) for n in numbers]
    else:
        if not numbers:
            return None
        else:
            return int(numbers[0])
