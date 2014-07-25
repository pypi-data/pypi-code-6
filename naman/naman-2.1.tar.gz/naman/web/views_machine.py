from naman.core.models import Machine
from forms import MachineForm
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from naman.core.tools.views import paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseServerError
import logging


@user_passes_test(lambda u: u.is_staff)
def delete(request, id):
    try:
        get_object_or_404(Machine, pk=id).delete()
        return HttpResponse("OK")
    except Exception as er:
        logging.error("Exception in machine deletion: %s" % er)
        return HttpResponseServerError("An error has ocurred.")


@user_passes_test(lambda u: u.is_staff)
def listado(request):
    #TODO change from icontains to iregex
    if "query_machine" in request.GET and request.GET["query_machine"] != "":
        query = Machine.objects.filter(
            Q(hostname__icontains=request.GET["query_machine"]) |
            Q(dns_zone__name__icontains=request.GET["query_machine"])|
            Q(mtype__name__icontains=request.GET["query_machine"])|
            Q(environment__code__icontains=request.GET["query_machine"])
            )
        print query.query
    else:
        query = Machine.objects.all()

    listado = paginator(query, request)

    if len(listado.object_list) == 1:
        obj = listado.object_list[0]
        return redirect(reverse("machine", args=[obj.pk, ]))
    return render_to_response(
        'machine/list.html',
        {"listado": listado},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def edit(request, id=None):
#from django.forms.util import ErrorList
    if id is None:
        obj = Machine()
    else:
        obj = get_object_or_404(Machine, pk=id)

    wrong = False
    if request.method == "POST":
        form = MachineForm(request.POST, instance=obj)

        try:
            if form.is_valid():
                print "is valid!"
                obj = form.save(commit=False)
                obj.save()
                messages.info(request, 'Machine successfully saved')
                return redirect(reverse('machine', args=[obj.pk]))

            wrong = True
            messages.error(request, "Wrong fields!")

        except Exception as ex:
            print "exception: %s" % ex
            messages.error(request, ex)
    else:
        form = MachineForm(instance=obj)

    response = render_to_response(
            'machine/edit.html',
            {
            'form': form,
             "id": obj.pk,
             "obj": obj,
             },
            context_instance=RequestContext(request))
    if wrong:
        response.status_code = 400
    return response
