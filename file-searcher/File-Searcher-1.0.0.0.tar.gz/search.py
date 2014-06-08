__author__ = 'Aadit'
__version__ = '1.0.0'

import sys
import time
import mean

def letter(word,data):
    '''
        letter(word,data) -> word(s)
        Checks whether the word is equvalient 
    '''
    
    for i in range(len(data)):
        index = data[i].find(word)
        if index == -1:
            return False
            continue
        else:
            n_list = mean.compute(word) # Compute mean
            
            print data[index]
            #edit.highlight_search(word,data)
            time.sleep(1)
            continue
