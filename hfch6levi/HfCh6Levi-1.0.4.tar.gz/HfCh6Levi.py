'''code for HfCh6, bundling code with data'''
''' the first thing is to modify the work directory'''
import os
os.chdir('/Users/AnQiuPing/Documents/Python/HfCh6Levi')

'''this function is used to read data into a list from a specific file'''
'''version2: add more function to enable this function to return processed data with the format of Dict rathen than unprocessed List'''
'''version3: using Class to get the top 3 times rather than Dict'''
'''version4: add two fuctions called addTime() and addTimes()'''
class Athlete:
    def __init__(self, a_name, a_bod=None, a_times=[]):
        self.name = a_name
        self.bod = a_bod
        self.times = a_times

    def top3(self):
        '''return the sorted result for the top 3 items from the list'''
        return sorted(set([sanitize(t) for t in self.times]))[0:3]

    def addTime(self, time):
        self.times.append(time)

    def addTimeList(self, timeList):
        '''to enlarge a list by another list, extend() can be used'''
        self.times.extend(timeList)

def get_coach_data(file_name):
    try:
        with open(file_name) as file_object:
            data = file_object.readline()
            returnList = data.strip().split(',')
            '''just return the relevant items, based on a general type, rather than any other specific values'''
            return (Athlete(returnList.pop(0), returnList.pop(0), returnList))
            
#            atheleteDict = dict()
#            atheleteDict['name'] = returnList.pop(0)
#            atheleteDict['bod'] = returnList.pop(0)
#            atheleteDict['time'] = returnList
#     print(atheleteDict['name'] + " 's fatest times are: " + str(sorted([sanitize(t) for t in returnList])[0:3]))
#            return {'Name':returnList.pop(0), 'Bod':returnList.pop(0), 'Time': str(sorted(set([sanitize(t) for t in returnList]))[0:3])}
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

'''version2: refine the code for process the data using Dict into get_coach_data'''
'''version3: using Class to get the top 3 times rather than Dict'''
def pop():
#    sarah = get_coach_data('sarah2.txt')

    '''now use dictionary to refine the below code using list'''
    '''
    sarahDict = dict()
    jamesDict = dict()
    julieDict = dict()
    mikeyDict = dict()

    sarahDict = get_coach_data('sarah2.txt')
    jamesDict = get_coach_data('james2.txt')
    julieDict = get_coach_data('julie2.txt')
    mikeyDict = get_coach_data('mikey2.txt')
    '''    
    sarah = get_coach_data('sarah2.txt')
    james = get_coach_data('james2.txt')
    julie = get_coach_data('julie2.txt')
    mikey = get_coach_data('mikey2.txt')

    levi = Athlete('Levi',)
    levi.addTime('2.01')
    print(levi.name + " 's time is: " + str(levi.top3()))

    bobby = Athlete('bobby')
    bobby.addTimeList(['1.1', '1.2', '1.3'])
    print(bobby.name + " 's time are: " + str(levi.top3()))

    print(sarah.name + " 's updated fatest times are: " + str(sarah.top3()))
    print(james.name + " 's updated fatest times are: " + str(james.top3()))
    
    '''version2: now using the refined Dict keys to display the desired results'''
    '''version3: using Class to get the top 3 times rather than Dict'''
    '''
    print(sarahDict['Name'] + " 's fatest times are: " + sarahDict['Time'])
    print(jamesDict['Name'] + " 's fatest times are: " + jamesDict['Time'])
    print(julieDict['Name'] + " 's fatest times are: " + julieDict['Time'])
    print(mikeyDict['Name'] + " 's fatest times are: " + mikeyDict['Time'])
    '''
    print(sarah.name + " 's fatest times are: " + str(sarah.top3()))
    print(james.name + " 's fatest times are: " + str(james.top3()))
    print(julie.name + " 's fatest times are: " + str(julie.top3()))
    print(mikey.name + " 's fatest times are: " + str(mikey.top3()))

    '''now print one more attribute from Sarah'''
    print(sarah.name + " 's bod is: " + sarah.bod)
#    sarahDict = {}
#    sarahDict['name'] = sarah.pop(0)
#    sarahDict['dob'] = sarah.pop(0)
#    sarahDict['time'] = sarah
#    print(sarahDict['name']  + " 's fatest times are: " + str(sorted(set([sanitize(t) for t in sarahDict['time']]))[0:3]))
#    (sarah_name, sarah_dob) = sarah.pop(0), sarah.pop(0)
#    print(sarah_name + " 's fatest times are: " + str(sorted(set([sanitize(t) for t in sarah]))[0:3]))


pop()
    
    
