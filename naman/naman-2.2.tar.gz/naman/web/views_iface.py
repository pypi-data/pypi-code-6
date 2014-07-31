from naman.core.models import Iface, ConflictingIP
from forms import IfaceForm, IfaceShortForm, IfaceByMachineForm
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from naman.core.tools.views import paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
import ipaddr
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_staff)
def delete(request, id):
    get_object_or_404(Iface, pk=id).delete()
    return HttpResponse("OK")


@user_passes_test(lambda u: u.is_staff)
def list_by_machine_json(request, machine_id, iface_id=None):

    if iface_id is None:
        ifaces = Iface.objects.filter(machines__id=machine_id)
    else:
        ifaces = Iface.objects.filter(id=iface_id)

    ifaces = [iface.to_json() for iface in ifaces]
    return render(
        request,
        'iface/list.json',
        {"ifaces": ifaces},
        content_type='application/json')


@user_passes_test(lambda u: u.is_staff)
def list_by_machine(request, machine_id, iface_id=None):

    if iface_id is None:
        ifaces = Iface.objects.filter(machines__id=machine_id)
    else:
        ifaces = Iface.objects.filter(id=iface_id)



    return render_to_response(
        "iface/list_by_machine.html",
        {"ifaces": ifaces,
         "iface_id": iface_id},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def listado(request):
    if "query_iface" in request.GET and request.GET["query_iface"] != "":
        query_sent = request.GET["query_iface"]

        query = Iface.objects.query_cmd(query_sent)
        if query is None:
            query = Iface.objects.filter(
                Q(vlan__name__iregex=query_sent)
                | Q(ip__iregex=query_sent)
                |Q(mac__icontains=query_sent))
    else:
        query = Iface.objects.all()
        query_sent = None
    print query.query
    listado = paginator(query, request)

    #if no iface is found, it shows advanced iface info
    if len(listado.object_list) == 0:
        try:
            ipaddr.IPv4Address(query_sent)
            vlan = Iface.find_vlan(query_sent)
            eirs = Iface.excluded_in_ranges(ip=query_sent, vlan=vlan)
            conflicts = ConflictingIP.objects.filter(ip=query_sent)
            return render_to_response(
                "iface/adv_info.html",
                {
                    "vlan": vlan,
                    "eirs": eirs,
                    "ip": query_sent,
                    "conflicts": conflicts,
                },
                context_instance=RequestContext(request)
            )
        except Exception:
            pass

#    if len(listado.object_list) == 1:
#        obj = listado.object_list[0]
#        return redirect(reverse("iface", args=[obj.pk, ]))
    return render_to_response(
        'iface/list.html',
        {"listado": listado},
        context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def edit_by_machine(request, id):
    print "id iface: %s" % id
    if id is None:
        obj = Iface()

    else:
        obj = get_object_or_404(Iface, pk=id)
    wrong = False
    if request.method == "POST":
        form = IfaceByMachineForm(request.POST, instance=obj)
        try:
            if form.is_valid():
                machine = request.POST["machines"]
                obj = form.save(commit=False)
                obj.save()
                try:
                    obj.machines.add(machine)
                except IntegrityError:
                    pass

                messages.info(request, 'Iface successfully saved')
                return redirect(reverse('ifaces_by_machine', args=[machine, ]))

            wrong = True
            messages.error(request, "Wrong fields!")
        except Exception, ex:
            return HttpResponseServerError(ex)

    else:
        try:
            machine = request.GET["machines"]
            form = IfaceByMachineForm(instance=obj, initial={"machines": [machine]})
        except MultiValueDictKeyError:
            form = IfaceByMachineForm(instance=obj)

    response = render_to_response(
        'iface/edit_by_machine.html',
        {
            'form': form,
            "id": obj.pk if obj.pk is not None else "",
            "obj": obj,
        },
        context_instance=RequestContext(request))
    if wrong:
        response["FORM_VALIDATE"] = "false"
        for msg in messages.get_messages(request):
            response["FORM_MSGS"] = msg

    return response


@user_passes_test(lambda u: u.is_staff)
def edit_short_old(request, id):
    if id is None:
        obj = Iface()
    else:
        obj = get_object_or_404(Iface, pk=id)

    if request.method == "POST":
        form = IfaceShortForm(request.POST, instance=obj)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.info(request, 'Iface successfully saved')
            return redirect(reverse('iface', args=[obj.pk]))
        else:
            messages.error(request, "Wrong fields!")

    else:
        form = IfaceShortForm(request.GET, instance=obj)

    return render_to_response(
            'iface/edit_form.html',
            {
                'form': form,
                 "id": obj.pk,
                 "obj": obj,
             },
            context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def edit(request, id=None):

    if id is None:
        obj = Iface()
    else:
        obj = get_object_or_404(Iface, pk=id)

    if request.method == "POST":
        form = IfaceForm(request.POST, instance=obj)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.save()
            if "machines" in form.cleaned_data:
                obj.machines.clear()
                cd = form.cleaned_data["machines"]
                for machine in form.cleaned_data["machines"]:
                    obj.machines.add(machine)

            messages.info(request, 'Iface successfully saved')
            return redirect(reverse('iface', args=[obj.pk]))

        messages.error(request, "Wrong fields!")

    else:
        form = IfaceForm(initial=request.GET, instance=obj)

    return render_to_response(
            'iface/edit.html',
            {
            'form': form,
             "id": obj.pk,
             "obj": obj,
             },
            context_instance=RequestContext(request))
