import os
'''code to use if to check one more exception'''
'''if os.path.exists('sketch.txt'):'''

'''below code is to add one more try-except block to handle the exception scenarios'''
try:
        data = open('sketch.txt')
        try: 

                for each_line in data:
                        (role, spoken_word) = each_line.split(':', 1)
                        print(role, end='')
                        print('said:', end='')
                        print(spoken_word, end='')
        except ValueError:
                pass

        data.close
except IOError:
        print('this file to be open does not exist any more')

  
'''the code below is to add some extra code for those circumstances
    where split() function cannot handle rather than using exception handling.
    status = each_line.find(':')
    if status != -1:
        (role, spoken_word) = each_line.split(':', 1)
        print(role, end = ' ')
        print('said:', end = ' ')
        print(spoken_word, end = '')
    else:
        print(each_line, end = ' ')
'''





    
