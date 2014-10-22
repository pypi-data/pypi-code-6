import urllib

from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.http.response import HttpResponseRedirect

from .forms import IPNForm


class IPNGeneratorView(FormView):

    form_class = IPNForm
    template_name = "mpesa/test_tools/ipn-form.html"

    def form_valid(self, form):
        ipn_receiver_url = reverse("ipn-receiver")

        data = form.save()

        full_url = "%s?%s" % (ipn_receiver_url, urllib.urlencode(data))

        return HttpResponseRedirect(full_url)
