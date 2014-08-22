import requests
from icalendar import Calendar, Event
import icalendar
import pytz
import sys
import datetime
from lxml import html
import getpass

reload(sys);
sys.setdefaultencoding("utf8") #Page uses UTF

class Course:
	name = ""
	code = ""
	sections = []

	def __init__(self, n, c):
		self.name = n
		self.code = c
		self.sections = []

class Section:
	name =""
	location = ""
	startDateTime = 0
	endDateTime =0
	lastClass = 0

	def __init__(self, _name, _location, _startDateTime, _endDateTime, _lastClass):
		self.name = _name
		self.location = _location
		self.startDateTime = _startDateTime
		self.endDateTime = _endDateTime
		self.lastClass = _lastClass

	def __repr__(self):
		return self.name + ", Location: " + self.location + " start Time: " + str(self.startDateTime) + " End Time: " + str(self.endDateTime)


def uwoDaytoWeekDay(day):
	if day == "Mo":
		return 1
	elif day == "Tu":
		return 2
	elif day == "We":
		return 3
	elif day == "Th":
		return 4
	elif day == "Fr":
		return 5

def getScheduleHTML(userName, password):
	LoginURL = 'https://student.uwo.ca/psp/heprdweb/EMPLOYEE/HRMS/c/UWO_WISG.WSA_STDNT_CENTER.GBL&languageCd=ENG';
	schedURL = 'https://student.uwo.ca/psc/heprdweb/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL';

	#These are the post varible the web form sends
	payload = {'httpPort2' : '',		
			'timezoneOffset2':0,
			'userid':userName.upper(),	#Server expect the username in uppercase for some reason
			'pwd':password,
			'Submit':'Sign In'}

	s = requests.Session(); #this creates a session that will keep track of cookies across requests

	#login in
	s.post(LoginURL, params=payload);

	#get Sched
	r = s.post(schedURL, {'Page':'SSR_SSENRL_LIST'})

	return r.text

def parseSchedule(schedHTML):
	courseList = []
	EST = pytz.timezone('US/Eastern')

	
	tree = html.fromstring(schedHTML)
	courses = tree.xpath("//div[starts-with(@id,'win0divDERIVED_REGFRM1_DESCR20$')]")

	#Parse the raw HTML into objects
	for course in courses:
		#Get the course title
		name = course.xpath("descendant::td[@class = 'PAGROUPDIVIDER']")

		dashLoc = name[0].text.find('-')
		c = Course(name[0].text[dashLoc+2:].title(), name[0].text[:dashLoc])
		
		#Find the sections we're signed up for
		sections =  course.xpath("descendant::tr[starts-with(@id,'trCLASS_MTG_VW$')]")

		typeClass  = ""
		for s in sections:
			col = s.xpath("descendant::span[@class = 'PSEDITBOX_DISPONLY']")

			#We only want to grab the type of class if there is one, otherwise its the same as the last row
			if col[1].text.strip() != "":
				typeClass  = col[1].text
			
			#This the start and end date of the term, not the course 
			startDate = datetime.datetime.strptime(col[len(col)-1].text[0:10], "%Y/%m/%d")
			
			recurEndDate = datetime.datetime.strptime(col[len(col)-1].text[13:23], "%Y/%m/%d")

			#Get The times
			times = col[len(col)-3].text;

			#Get the day of the week
			day = uwoDaytoWeekDay(times[0:2])
			
			#Check to see if the start times hour is 1 digit and pad it
			if(times[4] == ':'):
				startTime = '0' + times[3:9];
				if(times[13] == ':'):
					endTime = '0' + times[12:18]
				else:
					endTime = times[12:19]
			else:
				startTime = times[3:10];
				if(times[14] == ':'):
					endTime = '0' + times[13:19]
				else:
					endTime = times[13:20]

			startTime = datetime.datetime.strptime(startTime, "%I:%M%p")
			startTime = EST.localize(startTime)
			endTime = datetime.datetime.strptime(endTime, "%I:%M%p")
			endTime = EST.localize(endTime)
			#adjust the start day to line up with the day the course starts(rather the when the term starts)
			while (startDate.isoweekday() != day):
				startDate = startDate + datetime.timedelta(days=1)

			#Figure out the DateTime of the course
			zeroed = EST.localize(datetime.datetime(1900, 1, 1))

			startDateTime = startDate + (startTime - zeroed)
			startDateTime = EST.localize(startDateTime)
			endDateTime = startDateTime + (endTime-startTime)

			#get Location
			location = col[len(col)-2].text
			c.sections.append(Section(typeClass, location, startDateTime, endDateTime, recurEndDate))
		courseList.append(c)
	return courseList

def makeICal(courseList):
	# Start building the calendar
	cal = Calendar()

	#Required to be complient with th RFC
	cal.add('prodid', '-//pargall//UWO Class Calendar//EN')
	cal.add('version', '2.0')

	tzc = icalendar.Timezone()
	tzc.add('tzid', 'US/Eastern')
	tzc.add('x-lic-location', 'Europe/Eastern')

	#Define the timezone that UWO is in
	tzs = icalendar.TimezoneStandard()
	tzs.add('tzname', 'EST')
	tzs.add('dtstart', datetime.datetime(1970, 10, 25, 3, 0, 0))
	tzs.add('rrule', {'freq': 'yearly', 'bymonth': 10, 'byday': '-1su'})
	tzs.add('TZOFFSETFROM', datetime.timedelta(hours=-5))
	tzs.add('TZOFFSETTO', datetime.timedelta(hours=-4))

	tzd = icalendar.TimezoneDaylight()
	tzd.add('tzname', 'EDT')
	tzd.add('dtstart', datetime.datetime(1970, 3, 29, 2, 0, 0))
	tzs.add('rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '-1su'})
	tzd.add('TZOFFSETFROM', datetime.timedelta(hours=-4))
	tzd.add('TZOFFSETTO', datetime.timedelta(hours=-5))

	tzc.add_component(tzs)
	tzc.add_component(tzd)
	cal.add_component(tzc)

	for course in courseList:
		for section in course.sections:
			event = Event()
			event.add('uid', course.name+section.startDateTime.isoformat()+userName+"@uwo.ca")
			event.add('summary', section.name + ": " + course.name)
			event.add('description', course.code)
			event.add('location', section.location)

			event.add('dtstart', section.startDateTime)
			event.add('rrule', {'freq': 'weekly', 'until': section.lastClass})
			event.add('dtend', section.endDateTime)
			event.add('dtstamp', datetime.datetime.utcnow())
			cal.add_component(event)
	return cal

def writeTempFile(cal):
	import tempfile, os
	directory = tempfile.mkdtemp()
	f = open(os.path.join(directory, 'classes.ics'), 'wb')
	f.write(cal.to_ical())
	f.close()
	return f.name

def gen():
	userName = raw_input('Enter your uwo username: ')
	password = getpass.getpass()

	schedHTML = getScheduleHTML(userName, password)
	courseList = parseSchedule(schedHTML)
	cal = makeICal(courseList)

	print "Your calendar: " + writeTempFile(cal)
