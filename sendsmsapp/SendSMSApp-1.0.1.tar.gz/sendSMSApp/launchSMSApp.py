'''
Created on Jun 29, 2014

@author: bhavyaj
'''
import getpass
import smsUtilities

def launchSMSApp():
    username = raw_input("Please enter Username: ")
    passwd = getpass.getpass("Password: ")
    inputMethod = raw_input("Would you like to provide file for contacts (y/N): ")
    
    contactsObtained = False
    
    while(not contactsObtained):
        if inputMethod == 'y':
            fileName = raw_input("Please provide file name.")
            contactsObtained = True
        elif inputMethod == 'N':
            contacts = raw_input("Enter the numbers you want to send message to(comma-separated): ")
            contactsObtained = True
        else:
            inputMethod = raw_input("Would you like to provide file for contacts (y/N): ")
   
    message = raw_input("Great, now please enter the message you want to sent: ")
    
    numberList = None
    try:
        if inputMethod == 'y':
            numberList = getNumbersList(fileName, None)
        else:
            numberList = getNumbersList(None, contacts)
    except Exception:
        raise Exception('Could not fetch numbers from the input provided.')
    
    if numberList is None:
        raise Exception('Could not fetch numbers from the input provided.')
    
    smsUtilities.sendSMS(username, passwd, message, numberList)
    print("Woohoo!! All messages sent.")
    
def getNumbersList(fileName = None, contacts = None):
    if fileName is None:
        return contacts.split(',')
    elif contacts is None:
        return [line.strip() for line in open(fileName).readlines()]

if __name__ == '__main__':
    launchSMSApp()