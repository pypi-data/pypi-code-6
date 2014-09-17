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

        print "AUTH ", username, " ,", password
        user_model = get_user_model()
    
        try:
            user = user_model.objects.get(email=username)

            print "AUTH FOUND", username
            if user.check_password(password):
                print "AUTH FOUND PASS GOOD", username
                return user
        except user_model.DoesNotExist:
            print "AUTH NOT FOUND", username
            return None

        print "AUTH FOUND PASS NO GOOD", username
    # authenticate()

    def get_user(self, user_id):
        """todo: Docstring for get_user
        
        :param user_id: arg description
        :type user_id: type description
        :return:
        :rtype:
        """
        user_model = get_user_model()

        print "GET USER", user_id
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
    # get_user()
# EmailAuthBackend

