from datetime import date


def parse_date_string(date_str, type=3):
    if type == 3:
        date_str = '20' + date_str
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return date(year, month, day)


def format_esr_nr(esr_nr):
    return '%s-%s-%s' % (esr_nr[0:2], int(esr_nr[2:-1]), esr_nr[-1])


def groupr(s, l, c=' '):
    '''
    Groups a string into chunks from the right side.
    :param s: String to be grouped
    :param l: Length of the chunks
    :param c: Chunk separator, defaults to a space
    '''
    if not s:
        return ''
    if len(s) <= l:
        return s
    return groupr(s[:-l], l, c) + c + s[-l:]
