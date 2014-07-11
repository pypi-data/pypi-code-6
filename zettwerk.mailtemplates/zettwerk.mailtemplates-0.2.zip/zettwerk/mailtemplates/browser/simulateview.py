from zope.interface import implements, Interface
from send_emailview import send_emailView, Isend_emailView


class IsimulateView(Interface):
    """ simulate view interface """


class simulateView(send_emailView):
    """
    simulate browser view
    """
    implements(IsimulateView, Isend_emailView)

    def __call__(self):
        """ do something """
        try:
            targets = self._getMemberTargets()
        except ValueError as e:
            return e.message

        response = self.request.RESPONSE

        output = ['userid;email;fullname;last_login']
        for member in targets:
            ## returning a simple csv structure
            output.append(
                '%s;%s;%s;%s;' % (member.getId(),
                                  member.getProperty('email'),
                                  member.getProperty('fullname'),
                                  member.getProperty('login_time'))
                )
        response.setHeader('content-type', 'text/plain')
        response.write('\n'.join(output))
