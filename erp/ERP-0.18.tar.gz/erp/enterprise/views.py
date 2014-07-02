import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.views.generic import View
from django.http import HttpResponseBadRequest
from . import models
from .forms import UserCreationForm


type_dict = {'user': 'CorpUser', 'unit': 'CorpUnit'}


class Register(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, "registration/register.html", {'form': form, })

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if request.is_ajax():
                form.save()
                return HttpResponse('OK')
            else:
                form.save()
                return HttpResponseRedirect('/')
        else:
            if request.is_ajax():
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        errors_dict[error] = form.errors[error]
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                return render(request, "registration/register.html", {'form': form, })