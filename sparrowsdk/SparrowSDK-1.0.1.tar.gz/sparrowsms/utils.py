import requests

def url_call_get(url, values):
    try:                
        res = requests.get(url, params=values)
    except Exception as e:
        res = e
    return res

def url_call_post(url, values):
    try:                
        res = requests.post(url, data=values)
    except Exception as e:
        res = e
    return res
