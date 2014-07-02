__author__ = 'cltanuki'
import json
from django.views.generic import FormView, UpdateView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, HttpResponse


class AjaxFormMixin(FormView):

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            if request.is_ajax():
                form.save()
                return HttpResponse('OK')
            else:
                form.save()
                return HttpResponse('OK')
        else:
            if request.is_ajax():
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        errors_dict[error] = form.errors[error]
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                return render(request, self.template_name, {'form': form})


class AjaxUpdateFormMixin(AjaxFormMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxFormMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxFormMixin, self).post(request, *args, **kwargs)