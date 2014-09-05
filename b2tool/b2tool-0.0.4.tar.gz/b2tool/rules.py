from datetime import datetime
import re


class Pull(object):
    """
    
    """

    def __init__(self, *args, **kwargs):
        self.args, self.kwargs = args, kwargs

    @staticmethod
    def oldest(objects):
        #  ['source']['repository']['name']
        #  "state": "OPEN",
        #  "created_on": "2014-08-17T05:39:38.501662+00:00",
        #  "updated_on": "2014-08-17T05:39:38.521747+00:00",
        #  "merge_commit": null,
        #  "id": 9
        #  ['source']['branch']['name']

        objs = []
        for obj in objects:
            if not objs:
                objs.append(obj)

            created_on = parse_date(obj.get('created_on'))
            if created_on < parse_date(objs[0].get('created_on')):
                objs.pop()
                objs.append(obj)
        if objs:
            return {'branch': objs[0]['source']['branch']['name'], 'id': objs[0].get('id')}
        else:
            return {}



def parse_date(dt):
    #['2014', '08', '16', '05', '39', '38', '501662', '00', '00']
    # 0 = year
    # 1 = month
    # 2 = day
    # 3 = hour
    # 4 = minutes
    # 5 = seconds

    result = map(lambda x: int(x), re.findall('\d{1,4}\d{1,2}', dt))
    for i in range(0,3):
        result.pop()

    return datetime(*result)

