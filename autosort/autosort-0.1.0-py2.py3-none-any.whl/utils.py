def interpose(lists, sep):
    result = []
    for lst in lists:
        if result:
            result.extend(sep)
        result.extend(lst)
    return result
