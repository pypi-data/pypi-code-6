from django.http import HttpResponse

def index(request):
	return HttpResponse('The index of some bullshit trash django app.')