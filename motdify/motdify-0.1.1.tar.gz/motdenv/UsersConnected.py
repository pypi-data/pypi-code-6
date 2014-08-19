import psutil

class UsersConnected:
    """ Returns the users connected on the system """

    def getVariableTuple(self):

        users = psutil.users()
        userlist = {}

        for user in users:
            if user.name not in userlist:
                userlist[user.name] = 1
            else:
                userlist[user.name] += 1

        # Actually, I don't really like this way. We need to join the dictionary to a string
        # while we want to append a number to each username, if its login count is > 1.
        userlist_joined = []

        for user in userlist:
            if userlist[user] == 1:
                userlist_joined.append(user)
            else:
                userlist_joined.append("%s (%s logins)" % (user, userlist[user]))

        return [
            ('USER_COUNT', len(users)),
            ('USER_LIST', ', '.join(sorted(userlist_joined)))
        ]            