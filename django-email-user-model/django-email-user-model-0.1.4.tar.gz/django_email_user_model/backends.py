from django.contrib.auth import get_user_model


class EmailAuthBackend(object):
    """Docstring for EmailAuthBackend """
    
    def authenticate(self, username=None, password=None):
        """todo: Docstring for authenticate
        
        :param username: arg description
        :type username: type description
        :param password: arg description
        :type password: type description
        :return:
        :rtype:
        """

        user_model = get_user_model()
    
        try:
            user = user_model.objects.get(email=username)

            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None

    # authenticate()

    def get_user(self, user_id):
        """todo: Docstring for get_user
        
        :param user_id: arg description
        :type user_id: type description
        :return:
        :rtype:
        """
        user_model = get_user_model()

        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
    # get_user()
# EmailAuthBackend

