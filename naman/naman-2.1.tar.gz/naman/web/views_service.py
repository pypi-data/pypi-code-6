from naman.core.models import Service
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render_to_response
from naman.web.forms import ServiceForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext


@user_passes_test(lambda u: u.is_staff)
def edit(request, id=None):
#from django.forms.util import ErrorList
    if id is None:
        obj = Service()
    else:
        obj = get_object_or_404(Service, pk=id)

    wrong = False
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=obj)

        try:
            if form.is_valid():
                print "is valid!"
                obj = form.save(commit=False)
                obj.save()
                messages.info(request, 'Service successfully saved')
                return redirect(reverse('service', args=[obj.pk]))

            wrong = True
            messages.error(request, "Wrong fields!")

        except Exception as ex:
            print "exception: %s" % ex
            messages.error(request, ex)
    else:
        form = ServiceForm(instance=obj)

    response = render_to_response(
            'service/edit.html',
            {
            'form': form,
             "id": obj.pk,
             "obj": obj,
             },
            context_instance=RequestContext(request))
    if wrong:
        response.status_code = 400
    return response