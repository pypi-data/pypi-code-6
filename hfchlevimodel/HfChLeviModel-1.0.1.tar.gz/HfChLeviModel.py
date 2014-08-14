'''code for HfCh7, bundling web application'''
'''the first thing is to modify the work directory'''
import os
os.chdir('/Users/AnQiuPing/Documents/Python/HfCh7Levi')
import pickle
'''Template is a class in string, there are safe_substitute() and substitute() within this class'''
from string import Template

'''import the class named AthleteList frm file called athletelist.py under the same folder'''
from athletelist import AthleteList
       
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
            return (AthleteList(returnList.pop(0), returnList.pop(0), returnList))
            
    except IOError as err:
        print('File IO Error(get_coach_data(file_name)):', + str(err))
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

def put_to_store(file_list):
    all_athletes = {}
    for each_file in file_list:
        athlete = get_coach_data(each_file)
        all_athletes[athlete.name] = athlete

    try:
        '''modify the data into binary files using pickle'''
        with open('athlete.pickle', 'wb') as athf:
            '''save the entire dictionary of AtheleteLists to a pickle'''
            pickle.dump(all_athletes, athf)
    except IOError as ioerr:
        print('File IO Error(put_and_store):' + str(ioerr))
    return (all_athletes)

def get_from_store():
    all_athletes = dict()
    try:
        with open('athlete.pickle', 'rb') as athf:
            '''simply read the entire pickle into the dictionry.'''
            all_athletes = pickle.load(athf)
    except IOError as ioerr:
        print('File IO Error(get_from_store):' + str(ioerr))
    return (all_athletes)
'''
work_files = ['james2.txt', 'julie2.txt', 'mikey2.txt', 'sarah2.txt']
print('read data using pickle.dump')
data = put_to_store(work_files)
for each_item in data:
    print(data[each_item].name + " 's bod is: " + data[each_item].bod)
print('read data after pickle.load')
all_athlete_data = get_from_store()
for each_item in all_athlete_data:
    print(all_athlete_data[each_item].name + " 's bod is: " + all_athlete_data[each_item].bod)
print('the dumped binary data is:')
print(data)


def start_response(resp = 'text/html'):
    return ('Content-type:' + resp + '\n\n')

def include_header(the_title):

    with open('templates/header.html') as headf:
        head_text = headf.read()
    header = Template(head_text)
    return(header.substitute(title = the_title))

def include_footer(the_links):
    
    with open('templates/footer.html') as footf:
        foot_text = footf.read()
    link_string = ''
    for key in the_links:
        link_string += '<a href = " ' + the_links[key] + ' ">' + key + '</a>&nbso;&nbsp;&nbsp;&nbsp;'
    footer = Template(foot_text)
    return(footer.substitute(links = link_string))

def start_from(the_url, form_type = 'POST'):
    
    return ('<form action = " '+ the_url +' " method=" '+ form_type + '">')

def end_from(submit_msg = 'Submit'):
    
    return ('<p></p><input type=submit value=" ' +submit_msg+ '"></form>')

def radio_button(rb_name, rb_value):
    
    return('<input type = "radio" name=" '+rb_name+' "value=" ' +rb_value+' ">' +rb_value + '<br/>')

def u_list(items):
 
    u_string = '<ul>'
    for item in items:
        u_string += '<li>' + item + '</li>'
    u_string += '</ul>'
    return (u_string)

def header(header_text, header_level = 2):
  
    return ('<h' + str(header_level) + '>' +header_text +
            '</h' + str(header_level) + '>')

def para(para_text):
    
    return ('<p>' + para_text + '</p>')
'''
