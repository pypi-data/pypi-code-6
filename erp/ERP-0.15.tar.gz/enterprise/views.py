from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect, render_to_response
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from enterprise import models
from rest_framework import viewsets, generics
from enterprise.forms import UserCreationForm
from .serializers import UserSerializer, GroupSerializer, ObjSerializer
from django.core import serializers

type_dict = {'user': 'CorpUser', 'unit': 'CorpUnit'}


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/accounts/login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


class CorpObjectListView(ListView):

    def get(self, request, *args, **kwargs):
        units = serializers.serialize("json", models.CorpObject.objects.all())
        return render_to_response("maps/map.html", locals())