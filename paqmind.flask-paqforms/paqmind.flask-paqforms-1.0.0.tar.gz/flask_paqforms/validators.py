import flask
import requests

from paqforms import ValidationError


class RecaptchaValidator(): # TODO: depends on requests
    def __init__(self, message=None):
        self.message = message


    def __call__(self, value, field):
        if value:
            data = {
                'privatekey': field.privatekey,
                'remoteip': flask.request.remote_addr,
                'challenge': value['challenge'],
                'response': value['response']
            }
            response = requests.post('http://www.google.com/recaptcha/api/verify', data=data)
            if 'true' in response.text:
                return
        message = self.message or field.translations.gettext('Wrong solution')
        raise ValidationError(message)


'''
class RecaptchaValidator:
    error_codes = {
        'invalid-site-public-key': 'The public key for reCAPTCHA is invalid',
        'invalid-site-private-key': 'The private key for reCAPTCHA is invalid',
        'invalid-referrer': 'The public key for reCAPTCHA is not valid for this domain',
        'verify-params-incorrect': 'The parameters passed to reCAPTCHA verification are incorrect'
    }

    def __call__(self, field, message=None):
        if request.json:
            challenge = request.json.get('recaptcha_challenge_field', '')
            response = request.json.get('recaptcha_response_field', '')
        else:
            challenge = request.form.get('recaptcha_challenge_field', '')
            response = request.form.get('recaptcha_response_field', '')
        remote_ip = request.remote_addr

        if not challenge or not response:
            raise ValidationError(field.translations.gettext(self.message))

        if not self._validate_recaptcha(challenge, response, remote_ip):
            message = message or self.message or field.translations.gettext('Invalid word. Please try again!')
            field.recaptcha_error = 'incorrect-captcha-sol'
            raise ValidationError(message)

    def _validate_recaptcha(self, challenge, response, remote_addr):
        """Performs the actual validation."""
        try:
            private_key = current_app.config['RECAPTCHA_PRIVATE_KEY']
        except KeyError:
            raise RuntimeError("No RECAPTCHA_PRIVATE_KEY config set")

        data = url_encode({
            'privatekey': private_key,
            'remoteip':   remote_addr,
            'challenge':  challenge,
            'response':   response
        })

        response = http.urlopen(RECAPTCHA_VERIFY_SERVER, to_bytes(data))

        if response.code != 200:
            return False

        rv = [l.strip() for l in response.readlines()]

        if rv and rv[0] == to_bytes('true'):
            return True

        if len(rv) > 1:
            error = rv[1]
            if error in self._error_codes:
                raise RuntimeError(self._error_codes[error])

        return False
'''
