from flask import jsonify
from flask import render_template
from pgeo.config.settings import settings
from pgeo.error.custom_exceptions import PGeoException
from pgeorest import app



@app.errorhandler(PGeoException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def root():
    return 'Welcome to p-geo!'

if __name__ == '__main__':
    app.run(host='localhost', port=settings['port'], debug=settings['debug'], threaded=True)