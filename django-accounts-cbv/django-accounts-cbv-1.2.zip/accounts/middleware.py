from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required


class LoginRequiredMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated() or self.is_public_url(request.path_info):
            return

        return login_required(view_func)(request, *view_args, **view_kwargs)

    @staticmethod
    def get_public_urls():
        named_urls = ['auth_login', 'auth_logout', 'auth_password_reset', 'auth_password_reset_confirm']
        urls = []
        for named_url in named_urls:
            try:
                urls.append(reverse(named_url))
            except NoReverseMatch:
                pass
        return urls

    def is_public_url(self, url):
        return url in self.get_public_urls()

