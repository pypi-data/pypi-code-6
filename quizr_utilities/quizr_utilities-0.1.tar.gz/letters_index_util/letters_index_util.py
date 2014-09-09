
def add_letters_indexes(list_param):
    """
    Changes provided list into a list of tuples
    containing letter index and original value
    e.g. [('A',orig_val1),('B',orig_val2)]
    :param list_param:
    :return:
    """
    list_with_tuples = []
    ord_pos = ord('A')
    for i in xrange(len(list_param)):
        list_with_tuples.append((chr(ord_pos+i), list_param[i]))
    return list_with_tuples