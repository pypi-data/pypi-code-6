from naman.core.models import Service
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render_to_response
from naman.web.forms import ServiceForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext
from naman.core.tools.views import paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
import logging


@user_passes_test(lambda u: u.is_staff)
def delete(request, id):
    try:
        get_object_or_404(Service, pk=id).delete()
        return HttpResponse("OK")
    except Exception as er:
        logging.error("Exception in service deletion: %s" % er)
        return HttpResponseServerError("An error has ocurred.")


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



@user_passes_test(lambda u: u.is_staff)
def listado(request):
    #TODO change from icontains to iregex
    if "query_service" in request.GET and request.GET["query_service"] != "": #Si busco un service concreto
        qs = request.GET["query_service"]
        query = Service.objects.filter(
            Q(name__icontains=qs) |
            Q(description__icontains=qs) |
            Q(iface__ip__icontains=qs) |
            Q(iface__vlan__name__icontains=qs) |
            Q(iface__vlan__tag__icontains=qs)
        )
        print query.query
    else: #Si quiero un listado de todos los services
        query = Service.objects.all()

    listado = paginator(query, request)

#    if len(listado.object_list) == 1:
#        obj = listado.object_list[0]
#        return redirect(reverse("service", args=[obj.pk, ]))
    return render_to_response(
        'service/list.html',
        {"listado": listado},
        context_instance=RequestContext(request))
