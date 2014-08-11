from jinja2 import Environment, PackageLoader



def get_env(templates_folder='templates'):
	return Environment(loader=PackageLoader('trellostats', templates_folder))	


def render_text(env, **data):
	template = env.get_template('text.tmpl')
	return template.render(**data)

def render_html(env, **data):
	template = env.get_template('html.tmpl')
	return template.render(**data)

# def render_panic(options):
#     data = []
#     for ctr in models.CycleTime.select().where(models.CycleTime.list_id
#                                                == options.list):
#         data.append({"title": ctr.when.strftime('%d/%m/%y'),
#                      'value': ctr.cycle_time})

#     d = {"graph": {
#             "title": options.title,
#             "type": "line",
#             "color": "orange",
#             "refreshEveryNSeconds" : 120,
#             "datasequences": [
#                 { "title": options.title,
#                     "datapoints": data,
#                 }
#             ]}
#         }

#     with open(options.outputfile, 'wb') as json_file:
#         json_file.write(json.dumps(d, indent=4, sort_keys=True))

