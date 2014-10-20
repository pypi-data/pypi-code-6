from flask import Flask, render_template, request, jsonify, Response

from . import database as db

app = Flask(__name__)

SQL_PATH = 'sql'
SETTINGS_FILENAME = 'settings.json'

# set path names and db connection settings, and build a list of queries
settings, queries = db.build_settings(SQL_PATH, SETTINGS_FILENAME)


def query_string_from_post(request_form):
    """ creates a query string from POST data
    """
    return '?' + '&'.join(["{}={}".format(k, request_form[k]) for k in request_form])


@app.route('/')
def index():
    print(queries)
    return render_template('index.html',
                           query_list=queries,
                           description=settings['website_description'],
                           title=settings['website_title'])


@app.route('/setup/<string:site_name>/<string:query_filename>')
def setup(site_name, query_filename):
    return render_template('setup_query.html',
                           site_name=site_name,
                           query_name=query_filename,
                           query_list=queries,
                           # only use each parameter once
                           params_list=list(set(db.get_params(SQL_PATH, site_name, query_filename))),
                           title=settings['website_title'])


@app.route('/run/<string:site_name>/<string:query_filename>', methods=['POST', 'GET'])
def run(site_name, query_filename):
    # TODO: check the form has the right data
    # if it's a GET request, use the query string, otherwise use the form data
    if request.method == 'GET':
        query_params = request.args.to_dict()
    elif request.method == 'POST':
        query_params = request.form.to_dict()
    else:
        query_params = None

    header, data = db.run_query(settings, SQL_PATH, site_name, query_filename,
                                query_params, data_format='list')

    # api links to download data in json and csv formats
    json_link = '/api/{}/{}.json{}'.format(site_name, query_filename,
                                           query_string_from_post(query_params))
    csv_link = '/api/{}/{}.csv{}'.format(site_name, query_filename,
                                         query_string_from_post(query_params))
    return render_template('results.html',
                           site_name=site_name,
                           query_name=query_filename,
                           query_list=queries,
                           title=settings['website_title'],
                           header=header,
                           data=data,
                           json_link=json_link,
                           csv_link=csv_link)


@app.route('/api/<string:site_name>/<string:query_filename>.json')
def api_json(site_name, query_filename):
    query_params = request.args.to_dict()
    data = db.run_query(settings, SQL_PATH, site_name, query_filename,
                        query_params, data_format='dict')
    return jsonify(params=query_params, data=data)


@app.route('/api/<string:site_name>/<string:query_filename>.csv')
def api_csv(site_name, query_filename):
    query_params = request.args.to_dict()
    data = db.run_query(settings, SQL_PATH, site_name, query_filename,
                        query_params, data_format='csv')
    return Response(data, mimetype='text/csv')
