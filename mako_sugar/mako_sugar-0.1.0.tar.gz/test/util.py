import re
def result_lines(result):
    return [x.strip() for x in re.split(r'\r?\n', re.sub(r' +', ' ', result)) if x.strip() != '']
