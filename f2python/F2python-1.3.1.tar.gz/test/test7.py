import sys, time

db_url = 'rpc:127.0.0.1:8080'
if len(sys.argv) > 1:
	db_url = sys.argv[1]

import F2
db = F2.connect(db_url)

Color = db.class_create('Color', schema={'name' : db.String})
blue = Color.create(name = 'blue')
red = Color.create(name = 'red')
green = Color.create(name = 'green')
yellow = Color.create(name = 'yellow')
black = Color.create(name = 'black')
white = Color.create(name = 'white')

Flag = db.class_create('Flag', schema = {'colors' : (Color, 1, 'n')})

Country = db.class_create(className = 'Country',
                          schema = {'name' : db.String,
                                    'flag' : Flag})

fr = Country.create(name = 'France',
                    flag = Flag.create(colors = [blue, white, red]))
de = Country.create(name = 'Deutschland',
                    flag = Flag.create(colors = [black, red, yellow]))
us = Country.create(name = 'USA',
                    flag = Flag.create(colors = [red, blue, white]))
it = Country.create(name = 'Italy',
                    flag = Flag.create(colors = [green, white, red]))

db.close()