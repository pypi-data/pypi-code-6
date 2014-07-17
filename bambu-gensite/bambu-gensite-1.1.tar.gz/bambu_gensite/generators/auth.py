import requests

def user(model, count, log, **kwargs):
    data = requests.get('http://api.randomuser.me/?results=%d' % count).json()['results']
    for u in data:
        yield model.objects.create_user(
            username = u['user']['username'],
            password = u['user']['password'],
            email = u['user']['email'],
            first_name = u['user']['name']['first'].capitalize(),
            last_name = u['user']['name']['last'].capitalize()
        )
