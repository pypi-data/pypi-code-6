import arrow
from requests import Session

class basisAPI:
    """ Basis connection object

    :param str username: The username or email you use to log in to the Basis site
    :param str password: The password you use to log in to the Basis site
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.me = None
        self.points = None

        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.email = None
        self.joined = None
        self.level = None
        self.id = None
        self.device = None
        self.last_synced = None
        self.anatomy = None

        self.session = Session()
        self.login_payload = {"next": "https://app.mybasis.com", "username": self.username, "password": self.password, "submit": "Login"}

        self.session.post("https://app.mybasis.com/login", data=self.login_payload)
        self.access_token = self.session.cookies['access_token']
        self.refresh_token = self.session.cookies['refresh_token']
        self.headers = {"X-Basis-Authorization": "OAuth "+self.access_token}


    # Profile Initialization Methods
    # ===============

    def getMe(self):
        '''
        This will grab profile information like name, id, etc. Not necessary for methods below to work.
        '''
        resp = self.session.get("https://app.mybasis.com/api/v1/user/me.json", headers=self.headers)
        self.me = resp.json()
        self.first_name = self.me['profile']['first_name']
        self.last_name = self.me['profile']['last_name']
        self.full_name = self.me['profile']['full_name']
        self.email = self.me['email']
        self.joined = arrow.get(self.me['profile']['joined'])
        self.level = self.me['level']
        self.id = self.me['id']
        self.device = self.me['device']
        self.last_synced = arrow.get(self.me['last_synced'])
        self.anatomy = self.me['anatomy']

    def getPoints(self):
        '''
        This will grab the number of points. Not necessary for methods below to work.
        '''
        resp = self.session.get("https://app.mybasis.com/api/v1/points", headers=self.headers)
        self.points = resp.json()['points']


    # Sleep Methods
    # =============

    def sleepData(self,startdate, enddate=None):
        '''
        Returns a list of sleep data for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        If enddate is specified, gets sleep data for all dates in the range and returns them all in the list.
        '''
        startdate = arrow.get(startdate)
        sleepList = []

        if enddate:
            enddate = arrow.get(enddate)

            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleepData(date)
                sleepList += data


        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/activities?type=sleep&expand=activities.stages,activities.events", headers=self.headers)
            sleepList += resp.json()['content']['activities']

        return sleepList

    def sleepSummary(self,startdate,enddate=None):
        '''
        Returns a list with the sleep summary for a date as the element - can take a string in YYYY-MM-DD, datetime or
        arrow objects.
        If enddate is specified, gets sleep summaries for all dates in the range and returns them all as elements in the
        list.
        '''
        startdate = arrow.get(startdate)
        sleepList = []

        if enddate:
            enddate = arrow.get(enddate)
            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleepSummary(date)
                sleepList += data

        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/summary/activities/sleep", headers=self.headers)
            sleepList.append(resp.json()['content'])

        return  sleepList

    def sleepActivities(self,startdate,enddate=None):
        '''
        Returns a list of sleep activities for a date - can take a string in YYYY-MM-DD, datetime or arrow objects.
        If enddate is specified, gets sleep activities for all dates in the range.
        '''

        startdate = arrow.get(startdate)
        sleepList = []

        if enddate:
            enddate = arrow.get(enddate)
            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.sleepActivities(date)
                sleepList += data

        else:
            resp = self.session.get("https://app.mybasis.com/api/v2/users/me/days/" + startdate.format('YYYY-MM-DD') + "/activities?type=sleep", headers=self.headers)
            sleepList += resp.json()['content']['activities']

        return sleepList



    # Physiological Data
    # ==================

    def physData(self, startdate, enddate=None):
        '''
        Get physiological data for a date over 60 second intervals -- can take a string in 
        YYYY-MM-DD, datetime or arrow object. If enddate and metric arguments passed  are specified, gets physiological data for all
        dates in the range and returns metric in a list.



        '''
        startdate = arrow.get(startdate)
        physList = []

        if enddate:
            enddate = arrow.get(enddate)


            dates = [r.format('YYYY-MM-DD') for r in arrow.Arrow.range('day', startdate, enddate)]
            for date in dates:
                data = self.physData(date)
                physList += data

        else:
            resp = self.session.get("https://app.mybasis.com/api/v1/chart/me?summary=true&interval=60&units=ms&start_date=" + startdate.format('YYYY-MM-DD') + "&start_offset=0&end_offset=0&heartrate=true&steps=true&calories=true&gsr=true&skin_temp=true&air_temp=true&bodystates=true", headers=self.headers)
            physList.append(resp.json())

        return physList


    def getPhysMetrics(self,startdate,endDate=None,metrics=None):
        """
        Get one ore more physiological data metrics (steps, heartrate, calories, skin_temp, gsr) for a single day or
        range of days, and return an object containing those metrics, along with the start time, end time, and timezones
        during the collection.

        *gsr is skin perspiration
        """

        # This is the structure of the returned dictionary
        physMetrics = {'metrics': {}, 'starttime': None,'endtime': None, 'timezone_history' : []}

        # If metric exists and is not iterable (e.g. a string), make it so.
        if metrics and not hasattr(metrics, '__iter__'):
            metrics = [metrics]

        # If metric is not specified, get all of them
        if not metrics:
            metrics = ['skin_temp', 'heartrate', 'air_temp', 'calories', 'gsr', 'steps']

        # Create empty lists for each metric
        for metric in metrics:
            physMetrics['metrics'][metric] = []

        # Get all the data in range
        data = self.physData(startdate,endDate)

        if data:
            physMetrics['starttime'] = data[0]['starttime']
            physMetrics['endtime'] = data[0]['endtime']

            for element in data:
                physMetrics['starttime'] = min(physMetrics['starttime'], element['starttime'])
                physMetrics['endtime'] = max(physMetrics['endtime'], element['endtime'])
                physMetrics['timezone_history'] += element['timezone_history']

                for metric in metrics:
                    physMetrics['metrics'][metric] +=  element['metrics'][metric]['values']

        return physMetrics