import urllib
import json

from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.http.response import HttpResponseRedirect, HttpResponse

from .forms import IPNForm


class IPNGeneratorView(FormView):

    form_class = IPNForm
    template_name = "mpesa/test_tools/ipn-form.html"

    def form_valid(self, form):
        ipn_receiver_url = reverse("ipn-receiver")

        data = form.save()

        if self.request.is_ajax():
            json_string = json.dumps(data)
            response = HttpResponse(json_string)
            response.content_type = "application/json"
        else:
            full_url = "%s?%s" % (ipn_receiver_url, urllib.urlencode(data))
            response = HttpResponseRedirect(full_url)

        return response
