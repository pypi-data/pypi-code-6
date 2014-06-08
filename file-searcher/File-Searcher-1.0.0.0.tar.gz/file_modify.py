_author__ = "Aadit Kapoor"
__version__ = "1.0.0"

def store_data(file_):
    '''
        (str,file) -> list[]
        Return the content of the file into a list
    '''
    data = []
    for line in file_:
        data.append(line)
    return data # Returning processed data

def remove_slashn(data):
    '''
        (list) -> list
        return a modified list with '\n' removed.
    '''
    if len(data) == 0:
        print "**** List empty! *** "
    for i in range(len(data)):
        if '\n' in data[i]:
            data[i] = data[i].replace('\n','')
        else:
            pass

def to_lower(data):
    '''
        to_lower(data) -> list
        Return the lowercases version of the list
    '''
    
    for i in range(len(data)):
        data[i] = data[i].lower()
