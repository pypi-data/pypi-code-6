import os;
os.getcwd()
os.chdir('/Users/AnQiuPing/Documents/Python/HfCh5Levi')

julieList = []
jamesList  = []
sarahList  = []
mikeyList  = []

def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
 
    else:
        return(time_string)
    (mins, secs) = time_string.split(splitter)
    return (mins + '.' + secs)


def getData():
    try:
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

        sanitizedJames = []
        sanitizedJulie = []
        sanitizedMikey = []
        sanitizedSarah = []

        for item in jamesList:
            sanitizedJames.append(sanitize(item))
        for item in julieList:
            sanitizedJulie.append(sanitize(item))
        for item in mikeyList:
            sanitizedMikey.append(sanitize(item))
        for item in sarahList:
            sanitizedSarah.append(sanitize(item))

        print("now print the unsorted athletes' list:")
        print(sanitizedJames)
        print(sanitizedJulie)
        print(sanitizedMikey)
        print(sanitizedSarah)

        print("now print the sorted athletes' list:")
        print(sorted(sanitizedJames))       
        print(sorted(sanitizedJulie))       
        print(sorted(sanitizedMikey))       
        print(sorted(sanitizedSarah))
        

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

