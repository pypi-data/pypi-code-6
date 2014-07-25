from django.shortcuts import render_to_response, get_object_or_404
from naman.core.models import ConflictingIP
from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext
from forms import ConflictingIPForm
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff)
def edit_modal(request, id=None):

    if id is None:
        obj = ConflictingIP()
    else:
        obj = get_object_or_404(ConflictingIP, pk=id)

    wrong = False
    if request.method == "POST":
        form = ConflictingIPForm(request.POST, instance=obj)

        try:
            if form.is_valid():
                print "is valid!"
                obj = form.save(commit=False)
                obj.save()
                return HttpResponse("OK")

            wrong = True

        except Exception, ex:
            print "exception: %s" % ex
            return HttpResponseServerError(ex)
    else:
        form = ConflictingIPForm(instance=obj)

    return render_to_response(
        "conflicting_ip/edit_modal.html",
        {
        'form': form,
         "id": obj.pk,
         "obj": obj,
         },
        context_instance=RequestContext(request))
    if wrong:
        response.status_code = 400
    return response
