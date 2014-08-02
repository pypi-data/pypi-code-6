from apy.handler import Controller
from apy.http import JsonResponse
from .model import UsernameAlreadyInUseException, EmailAlreadyInUseException, \
    WrongConsumerAccessTokenException, EmailCurrentlyConfirmedException, WrongPasswordException, \
    UserBannedException, EmailNotConfirmedException


class SignUp(Controller):
    def create_account(self):
        response = JsonResponse()
        username = self._request.data.get('username')
        email = self._request.data.get('email')
        password = self._request.data.get('password')

        signup_service = self._services.get('sign_up')

        try:
            signup_service.create_account(username, email, password)
            response.data = {'valid': True}
        except UsernameAlreadyInUseException:
            response.data = {'valid': False, 'reason': 'username taken'}
        except EmailAlreadyInUseException:
            response.data = {'valid': False, 'reason': 'email taken'}
        return response

    def confirm_email(self):
        consumer_access_token = self._request.data.get('consumer_access_token')

        response = JsonResponse()

        signup_service = self._services.get('sign_up')
        try:
            signup_service.confirm_email(consumer_access_token)
            response.data = {'valid': True}
        except WrongConsumerAccessTokenException:
            response.data = {'valid': False, 'reason': 'wrong consumer access token'}
        except EmailCurrentlyConfirmedException:
            response.data = {'valid': False, 'reason': 'email currently confirmed'}
        return response


class ConsumerManager(Controller):
    def create_web_consumer(self):
        username = self._request.data.get('username')
        password = self._request.data.get('password')

        response = JsonResponse()

        consumer_manager = self._services.get('consumer_manager')
        try:
            access_token = consumer_manager.create_web_consumer(username, password)
            response.data = {'valid': True, 'access_token': access_token}
        except WrongPasswordException:
            response.data = {'valid': False, 'reason': 'wrong password'}
        except UserBannedException:
            response.data = {'valid': False, 'reason': 'user banned'}
        except EmailNotConfirmedException:
            response.data = {'valid': False, 'reason': 'email not confirmed'}

        return response
