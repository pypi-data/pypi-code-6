from flask_security import url_for_security, current_user
from flask import redirect, url_for

class LoginMixin:
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for_security('login', next=url_for(".%s" % name)))

    def is_accessible(self):
        return current_user.is_authenticated() and \
                (current_user.has_role('admin') or \
                 current_user.has_role('superadmin'))
       

class UserPanelMixin:
    def additionnal_context(self):        
        return dict(current_user=current_user)