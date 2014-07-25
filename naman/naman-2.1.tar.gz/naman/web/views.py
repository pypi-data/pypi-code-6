from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from django.template import RequestContext
# Create your views here.


@user_passes_test(lambda u: u.is_staff)
def home(request):
    return render_to_response(
        "base.html",
        {},
        context_instance=RequestContext(request))
