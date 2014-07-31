#from django.contrib.auth.decorators import login_required
from django.shortcuts import render


#@login_required
def iface(request):
    return render(request, 'js/iface.js', content_type='application/javascript')


def vlanconfig(request):
    return render(request, 'js/vlanconfig.js', content_type='application/javascript')


def conflicting_ip(request):
    return render(request, 'js/conflicting_ip.js', content_type='application/javascript')


def machine(request):
    return render(request, 'js/machine.js', content_type='application/javascript')


def service(request):
    return render(request, 'js/service.js', content_type='application/javascript')
