from flask import Flask, request
from jinja2 import Template
from sweetcaptchawt import SweetCaptchaField
from wtforms import Form, StringField
import sys


index_t = Template('''
<html><head><title>Sweet Captcha Demo</title></head>

<body>
    <form method="post">
        {{ form.sweetcaptcha() }}

        {{ msg }}

        <input type="submit"/>
    </form>
</body>

</html>

''')


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    print request.form
    form = make_form(APP_ID, APP_KEY)
    if request.method == 'POST':
        if form.validate():
            return 'SUCCESS'
        return index_t.render(form=form, msg='Invalid Captcha')
    return index_t.render(form=form)


def make_form(app_id, app_key):
    class MyForm(Form):
        sweetcaptcha = SweetCaptchaField('sweetcaptcha', app_id=app_id,
                                         app_key=app_key)
        sckey = StringField('sckey')
        scvalue = StringField('scvalue')

    # form is an empty dict for get requests.
    return MyForm(request.form)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Pass APPID APPKEY on commandline.')
    APP_ID = sys.argv[1]
    APP_KEY = sys.argv[2]
    app.run(debug=1)