'''code for HfCh6, bundling code with data'''
''' the first thing is to modify the work directory'''
import os
os.chdir('/Users/AnQiuPing/Documents/Python/HfCh6Levi')

'''this function is used to read data into a list from a specific file'''
def get_coach_data(file_name):
    try:
        with open(file_name) as file_object:
            data = file_object.readline()
            return (data.strip().split(','))
    except IOError as err:
        print('File IO Error:', + str(err))
        return (None)

'''this function is used to adjust the data format for data from list'''
def sanitize(target_list):
    if '-' in target_list:
        splitter = '-'
    elif ':' in target_list:
        splitter = ':'
    else:
        return target_list

    (mins, secs) = target_list.split(splitter)
    return (mins + '.' + secs)

def pop():
    sarah = get_coach_data('sarah2.txt')
    (sarah_name, sarah_dob) = sarah.pop(0), sarah.pop(0)
    print(sarah_name + " 's fatest times are: " + str(sorted(set([sanitize(t) for t in sarah]))[0:3]))


pop()
    
    
