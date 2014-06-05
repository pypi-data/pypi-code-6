import os

import requests
from randua import generate as ua
from randomsleep import randomsleep

import scarsdale_property_inquiry.params as p

def home(warehouse):
    if 'home' in warehouse:
        response = warehouse['home']
    else:
        randomsleep()
        response = requests.get(p.url(), headers = p.headers(ua()))
        warehouse['home'] = response
    return response

def _post(section_name, data_func):
    def f(warehouse, session, _id):
        key = (section_name, _id)
        if key in warehouse:
            response = warehouse[key]
        else:
            cookies, publickeytoken, viewstate, eventvalidation = session
            data = data_func(publickeytoken, viewstate, eventvalidation, _id)
            files = [(key, ('', str(value))) for key, value in data]
            randomsleep()
            response = requests.post(p.url(), headers = p.headers(ua()), files = files, cookies = cookies)
            warehouse[key] = response
        return response
    return f

street = _post('street', p.street_data)
house  = _post('house',  p.house_data)
