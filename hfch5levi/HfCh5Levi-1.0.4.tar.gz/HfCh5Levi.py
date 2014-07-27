import os;
os.getcwd()
os.chdir('/Users/AnQiuPing/Documents/Python/HfCh5Levi')

julieList = []
jamesList  = []
sarahList  = []
mikeyList  = []

'''four new lists for storing the ordered and uniformed lists from original lists'''
sanitizedJames = []
sanitizedJulie = []
sanitizedMikey = []
sanitizedSarah = []

'''new lists for removing the duplicates and displaying the top 3 plays' time'''
uniqueJames = []
uniqueJulie = []
uniqueMikey = []
uniqueSarah = []
        
def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
 
    else:
        return(time_string)
    (mins, secs) = time_string.split(splitter)
    return (mins + '.' + secs)

def getFiles(file_name):
    try:
        with open(file_name) as fileSubject:
            data = fileSubject.readline()
            return data.strip().split(',')

    except IOError as err:
        print("File IO Error:", + str(err))

def getData():
    try:
        jamesList = getFiles('james.txt')
        julieList = getFiles('julie.txt')
        mikeyList = getFiles('mikey.txt')
        sarahList = getFiles('sarah.txt')
        '''
        with open('james.txt') as james:
            data = james.readline()
            jamesList = data.strip().split(',')
        
        with open('julie.txt') as julie:
            data = julie.readline()
            julieList = data.strip().split(',')
        with open('mikey.txt') as mikey:
            data = mikey.readline()
            mikeyList = data.strip().split(',')
        with open('sarah.txt') as sarah:
            data = sarah.readline()
            sarahList = data.strip().split(',')
        '''
            
        '''for item in jamesList:
            sanitizedJames.append(sanitize(item))'''
        '''the below code is a new way for list comprehension'''
        sanitizedJames = sorted([sanitize(each_item) for each_item in jamesList])
        '''for item in julieList:
            sanitizedJulie.append(sanitize(item))'''
        sanitizedJulie = sorted([sanitize(each_item) for each_item in julieList])
        '''for item in mikeyList:
            sanitizedMikey.append(sanitize(item))'''
        sanitizedMikey = sorted([sanitize(each_item) for each_item in mikeyList])
        '''for item in sarahList:
            sanitizedSarah.append(sanitize(item))'''
        sanitizedSarah = sorted([sanitize(each_item) for each_item in sarahList])

        print("now print the non-duplication result using set() rather than list()")
        print(sorted(set(sanitize(t) for t in jamesList))[0:3])
        print(sorted(set(sanitize(t) for t in julieList))[0:3])
        print(sorted(set(sanitize(t) for t in mikeyList))[0:3])
        print(sorted(set(sanitize(t) for t in sarahList))[0:3])
        
        '''now refiene the code for removing the duplicates using set() rather than list()'''
        
        for each_item in sanitizedJames:
            if each_item not in uniqueJames:
                uniqueJames.append(each_item)

        for each_item in sanitizedJulie:
            if each_item not in uniqueJulie:
                uniqueJulie.append(each_item)

        for each_item in sanitizedMikey:
            if each_item not in uniqueMikey:
                uniqueMikey.append(each_item)

        for each_item in sanitizedSarah:
            if each_item not in uniqueSarah:
                uniqueSarah.append(each_item)

        print("now print the top 3 fastest time from different players:")
        print("James:", uniqueJames[0:3])
        print("Julie:", uniqueJulie[0:3])
        print("James:", uniqueMikey[0:3])
        print("Julie:", uniqueSarah[0:3])

        '''
        print("now print the sorted athletes' list in asending order:")
        print(sanitizedJames)       
        print(sanitizedJulie)       
        print(sanitizedMikey)       
        print(sanitizedSarah)

        print("now print the sorted athletes' list in descending order:")
        print(sorted(sanitizedJames, reverse = True))       
        print(sorted(sanitizedJulie, reverse = True))       
        print(sorted(sanitizedMikey, reverse = True))       
        print(sorted(sanitizedSarah, reverse = True))
        '''
        

#        print(jamesList)
#        print(sorted(jamesList))
#        print(julieList)
#        print(sorted(julieList))
#        print(mikeyList)
#        print(sorted(mikeyList))
#        print(sarahList)
#        print(sorted(sarahList))

    except IOError as err:
        print('File Error:' + str(err))



getData()

