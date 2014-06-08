__author__ = 'Aadit Kapoor'
__version__ = '1.0.0.0'

def compute(word):
    '''
        compute(str) -> list(int)
        Computes the mean of the word and then returns a list
    '''
    numbers = range(len(word))
    flag = 0
    total = sum(numbers)
    if total % 2 == 0:
        flag = 1
    mean = total / len(word)
    if flag == 1:
        return range(mean+1)
    else:
        return range(mean)
