from naman.core.models import VLanConfig
from forms import VLanConfigForm#, IfaceByMachineForm
from django.shortcuts import render_to_response, redirect#, get_object_or_404
from django.template import RequestContext
#from tools.views import paginator
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseServerError, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
import simplejson


@user_passes_test(lambda u: u.is_staff)
def edit(request, id):
    try:
        obj = VLanConfig.objects.get(id=id)
    except VLanConfig.DoesNotExist:
        obj = VLanConfig()

    try:
        wrong = False
        if request.method == "POST":
            form = VLanConfigForm(request.POST, instance=obj)
            try:
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.save()
                    #ifaces = []
                    #for vlan in obj.vlans.all():
                    #    iface = Iface(vlan=vlan)
                    #    iface.save()
                    #    iface.machines.add(obj.machine)
                    return redirect(reverse("ifaces_by_machine", args=[obj.machine.pk, ]))
    
                response = render_to_response(
                    'vlanconfig/edit.html',
                    {
                        'form': form,
                        "id": obj.pk,
                        "obj": obj,
                     },
                    context_instance=RequestContext(request))
                if wrong:
                    response.status_code = 400
                return response
            except Exception, ex:                
                return HttpResponseServerError(ex)
            wrong = True
            messages.error(request, "Wrong fields!")
    
        else:
            print request.GET
            if "machine" in request.GET:
                machine = request.GET["machine"]
                form = VLanConfigForm(instance=obj, initial={"machine": machine})
            else:
                form = VLanConfigForm(instance=obj)
    
        return render_to_response(
                'vlanconfig/edit.html',
                {
                    'form': form,
                    "id": obj.pk,
                    "obj": obj,
                 },
                context_instance=RequestContext(request))
    except Exception, ex:
        
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Error: %s" % ex, ]}),
            content_type="application/json",
            )
