'''this is the code for Code Magnet in Ch4 of Headfirst Python'''
import os; os.chdir('/Users/AnQiuPing/Documents/Python/HfCh4Levi')
import sys
import pickle
man = []
other = []

def printNestList(tatgetList, indent = False, tapNumber = 0, fh = sys.stdout):
    for each_item in tatgetList:
        if isinstance(each_item, list):
            printNestList(each_item, indent, tapNumber + 1, fh)
        else:
            if indent:
                for tapNumbers in range(tapNumber):
                    print('\t', end=' ', file = fh)
            print(each_item, file = fh)

def printFile():
    try:
        data = open('sketch.txt')
        for each_line_item in data:
            try:
                (role, line_spoken) = each_line_item.split(':', 1)
                print(role, end= '')
                print('said:', end='')
                print(line_spoken, end='')
                
                line_spoken = line_spoken.strip()
                if role == 'Man':
                    man.append(line_spoken)
                elif role == 'Other Man':
                    other.append(line_spoken)
            except ValueError:
                pass
    except IOError as err:
        print('File Error:' +str(err))
    finally:
        if 'data' in locals():
            data.close()

    try:
        with open('man_data.txt', 'wb') as manData, open('other_data.txt', 'wb') as otherManData:
            pickle.dump(man, manData)
            pickle.dump(other, otherManData)


        with open('man_data.txt', 'rb') as manDataRestore, open('other_data.txt', 'rb') as otherManDataRestore:
            manDataList = pickle.load(manDataRestore)
            otherManDataList = pickle.load(otherManDataRestore)

        printNestList(manDataList)
        printNestList(otherManDataList)
            
        '''
        with open('man_data.txt', 'wb') as manDataSaved, open('other_data.txt', 'wb') as otherManDataSaved:
            pickle.dump([1, 2, 'three', 'manDataSaved'], manDataSaved)
            pickle.dump([1, 2, 'three', 'otherManDataSaved'], otherManDataSaved)

        with open('man_data.txt', 'rb') as manDataRestored:
            manDataRestoredList = pickle.load(manDataRestored)

            print(manDataRestoredList)
        '''
        
#        with open('man_data.txt', 'w') as manData, open('other_data.txt', 'w') as otherManData:
        ''' pay attention to the second parameter of function printNestList, fh should be used  '''
#            printNestList(man, fh = manData)
#            printNestList(other, fh = otherManData)
        '''
        with open('man_data.txt', 'w') as manData, open('other_data.txt', 'w') as otherManData:
            print(man, file = manData)
            print(other, file = otherManData)
        

        with open('man_data.txt', 'w') as manData:
            print(man, file = manData)
        with open('other_data.txt', 'w') as otherManData:
            print(other, file = otherManData)
'''                
#        manData = open('man_data.txt', 'w')
#        otherManData = open('other_data.txt', 'w')

#        print(man, file = manData)
#        print(other, file = otherManData)

#        manData.close()
#        otherManData.close()

    except IOError as err:
        print('File Error:' + str(err))

    except pickle.PickleError as perr:
        print('Pickling Error:' + str(perr))

'''
    finally:
        if 'manData' in locals():
            manData.close()
        if 'otherManData' in locals():
            otherManData.close()
'''

printFile()


