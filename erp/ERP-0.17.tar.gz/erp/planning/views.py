__author__ = 'cltanuki'
import logging
from itertools import chain
from operator import attrgetter

from django.contrib.contenttypes.models import ContentType
from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from . import models
from django.views.generic.edit import CreateView, View
from django.views.generic import ListView
from . import forms
from erp.enterprise import models as emodels
from django.utils.encoding import smart_text
from django.core.serializers.json import Serializer as Builtin_Serializer
from django.contrib.contenttypes.generic import generic_inlineformset_factory


logger = logging.getLogger(__name__)
type_dict = {'task': 'Task', 'prj': 'Project'}
template_dict = {'task': 'TaskTemplate', 'prj': 'ProjectTemplate'}


# Create your views here.
def public_tasks(request):
    tasks = models.Task.objects.filter(public=True)
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        tasks = models.Task.objects.filter(public=True).filter(item_type=type_name)
    return render_to_response('planning/public.html', locals())


def public_prjs(request):
    prjs = models.Project.objects.filter(public=True)
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        prjs = models.Project.objects.filter(public=True).filter(item_type=type_name)
    return render_to_response('planning/public_prj.html', locals())


class TaskTypes(ListView):

    def get(self, request, *args, **kwargs):
        perms = [x.split('_', 1)[-1] for x in request.user.get_all_permissions()]
        present = models.Task.objects.values_list('item_type__model', flat=True)
        types = [i for i in present if i in perms]
        return render_to_response('planning/filter_template.html', locals())


class PrjTypes(ListView):

    def get(self, request, *args, **kwargs):
        perms = [x.split('_', 1)[-1] for x in request.user.get_all_permissions()]
        present = models.Project.objects.values_list('item_type__model', flat=True)
        types = [i for i in present if i in perms]
        return render_to_response('planning/filter_template.html', locals())


def user_taskset(request):
    owned_tasks = request.user.owned_tasks.all()
    performer_of = request.user.task_performer.all()
    joined_tasks = request.user.task_assigned_users.all()
    tasks = sorted(chain(owned_tasks, performer_of, joined_tasks),
                   key=attrgetter('deadline'))
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        tasks = request.user.owned_tasks.filter(item_type=type_name)
    return render_to_response('planning/tasks_list_template.html', locals())


def user_prjset(request):
    owned_prjs = request.user.owned_prjs.all()
    performer_of = request.user.prj_performer.all()
    joined_prjs = request.user.prj_assigned_users.all()
    prjs = sorted(chain(owned_prjs, performer_of, joined_prjs),
                  key=attrgetter('deadline'))
    if request.GET.get('type') is not None:
        type_name = get_object_or_404(ContentType, name=request.GET.get('type'))
        prjs = request.user.owned_prjs.filter(item_type=type_name)
    return render_to_response('planning/prj_list_template.html', locals())


class TaskSet(ListView):
    pass
    #TODO: List taskset and prjset


def show_templates(request, item_type):
    #user_groups = request.user.corp_group.all()
    model = getattr(models, template_dict[item_type])
    templates = model.objects.all()
    return render_to_response('planning/item_templates.html', locals())


class CreateTaskFromTemplate(View):
    form_class = forms.TaskForm
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        template = get_object_or_404(models.TaskTemplate, id=request.GET.get('tmpl_id'))
        data = {'name': template.name, 'desc': template.desc}
        if request.GET.get('prj_id'):
            data['prj'] = request.GET.get('prj_id')
        form = self.form_class(initial=data)
        return render_to_response(self.template_name, {'form': form, 'template': template})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        template = get_object_or_404(models.TaskTemplate, id=request.GET.get('tmpl_id'))
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.responsible = template.responsible
            form.save()
            return redirect(new_task.get_absolute_url())

        return render_to_response(self.template_name, {'form': form})


class PrjTasksetCreateWizard(SessionWizardView):

    template_name = 'wizard.html'

    def get_form_initial(self, step):
        logger.error(self.initial_dict)
        return self.initial_dict.get(step, {})

    def done(self, form_list, **kwargs):
        for form in form_list:
            task = form.save(commit=False)
            task.owner = self.request.user
            logger.error(self.initial_dict)
            task.save()
            return redirect('/pm')


def get_master(request, to_create):
    form_list = []
    init_dict = {}
    to_create = to_create.split('->') if len(to_create) > 1 else to_create
    for idx, i in enumerate(to_create):
        template = get_object_or_404(models.TaskTemplate, id=i)
        data = {'name': template.name, 'desc': template.desc, 'responsible': template.responsible}
        form_list.append(generic_inlineformset_factory(models.Task, extra=2))
        init_dict[str(idx)] = data
    logger.error(init_dict)
    return PrjTasksetCreateWizard.as_view(form_list=form_list, initial_dict=init_dict)(request)


class CreatePrjFromTemplate(View):
    form_class = forms.PrjTmplForm
    template_name = 'planning/create_prj_from_template.html'

    def get(self, request, *args, **kwargs):
        template = get_object_or_404(models.ProjectTemplate, id=request.GET.get('tmpl_id'))
        data = {'name': template.name, 'desc': template.desc}
        form = self.form_class(initial=data)
        return render_to_response(self.template_name, {'form': form, 'template': template})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        template = get_object_or_404(models.ProjectTemplate, id=request.GET.get('tmpl_id'))
        if form.is_valid():
            to_create = list(template.req_tasks.values_list('id', flat=True))
            if request.POST.get('opt_tasks') is not None:
                opt_tasks = request.POST.get('opt_tasks').split(',')
                for task in opt_tasks:
                    to_create.append(int(task))
            new_prj = form.save(commit=False)
            new_prj.owner = request.user
            new_prj.responsible = template.responsible
            new_prj.save()
            to_create = '->'.join(str(i) for i in to_create) if len(to_create) > 1 else str(to_create[0])
            return redirect('prj-wiz', to_create=to_create)

        return render_to_response(self.template_name, {'form': form})


class TaskCreate(View):
    form_class = generic_inlineformset_factory(models.TaskRes, extra=3)
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('prj_id'):
            prj = get_object_or_404(models.Project, id=request.GET.get('prj_id'))
            form = self.form_class(initial={'prj': prj})
        else:
            form = self.form_class()
        return render_to_response(self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            #TODO: Add undefined tasks responsible CorpUnit
            task.responsible = emodels.CorpUnit.objects.get(id=1)
            form.save()
            return HttpResponseRedirect('/pm')


class PrjCreate(CreateView):
    model = models.Project
    template_name = 'form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PrjCreate, self).form_valid(form)


class Serializer(Builtin_Serializer):

    def get_dump_object(self, obj):
        metadata = {
            "pk": smart_text(obj._get_pk_val(), strings_only=True),
        }
        return (lambda a, b: a.update(b) or a)(self._current, metadata)


class ResListView(ListView):

    def get(self, request, *args, **kwargs):
        s = Serializer()
        model = ContentType.objects.get(id=request.GET.get('ctype')).model_class()
        if request.GET.get('pk') is not None:
            json = s.serialize(model.objects.get(id=request.GET.get('pk')), ensure_ascii=False)
        else:
            json = s.serialize(model.objects.all(), ensure_ascii=False)
        return HttpResponse(json, content_type="text/html; charset=utf-8")