__author__ = 'cltanuki'
from django.conf.urls import patterns, url
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views, api_views, models

urlpatterns = patterns('',
    url(r'^$', views.user_taskset),
    url(r'prj/$', login_required(TemplateView.as_view(template_name='items_page.html'))),
    url(r'task/$', login_required(TemplateView.as_view(template_name='items_page.html'))),
    url(r'prj/types$', login_required(views.PrjTypes.as_view())),
    url(r'task/types$', login_required(views.TaskTypes.as_view())),
    url(r'prj/public$', login_required(views.public_prjs)),
    url(r'task/public$', login_required(views.public_tasks)),
    url(r'prj/performer$', login_required(views.user_prjset)),
    url(r'task/performer$', login_required(views.user_taskset)),
    url(r'task/create/from_template$', login_required(views.CreateTaskFromTemplate.as_view())),
    url(r'prj/create/from_template$', login_required(views.CreatePrjFromTemplate.as_view())),
    url(r'prj/(?P<pk>[0-9]+)$', login_required(DetailView.as_view(model=models.Project)), name='prj_item'),
    url(r'prj/master/(?P<to_create>[\w.,/_\->]+)', login_required(views.get_master), name='prj-wiz'),
    url(r'task/(?P<pk>[0-9]+)$', login_required(DetailView.as_view(model=models.Task)), name='task_item'),
    url(r'prj/(?P<pk>[0-9]+)/edit$', login_required(UpdateView.as_view(model=models.Project, template_name = 'form.html', success_url='/pm'))),
    url(r'task/(?P<pk>[0-9]+)/edit$', login_required(UpdateView.as_view(model=models.Task, template_name = 'form.html', success_url='/pm'))),
    url(r'prj/(?P<pk>[0-9]+)/edit$', login_required(DeleteView.as_view(model=models.Project, template_name = 'form.html', success_url='/pm'))),
    url(r'task/(?P<pk>[0-9]+)/edit$', login_required(DeleteView.as_view(model=models.Task, template_name = 'form.html', success_url='/pm'))),
    url(r'task/create/form$', login_required(views.TaskCreate.as_view())),
    url(r'prj/create/form$', login_required(views.PrjCreate.as_view(success_url='/pm'))),
    url(r'(?P<item_type>[a-z]+)/create$', login_required(views.show_templates)),
    url(r'task/create_template$', login_required(CreateView.as_view(model=models.TaskTemplate, template_name = 'form.html', success_url='/pm'))),
    url(r'prj/create_template$', login_required(CreateView.as_view(model=models.ProjectTemplate, template_name = 'form.html', success_url='/pm'))),
    url(r'timeline/prj$', login_required(api_views.PrjDetailView)),
    url(r'timeline/task$', login_required(api_views.TaskDetailView)),
    url(r'timeline/prj/public$', login_required(api_views.PublicPrjViewSet)),
    url(r'timeline/task/public$', login_required(api_views.PublicTasksViewSet)),
    url(r'timeline/prj/performer$', login_required(api_views.PrjPerformerViewSet)),
    url(r'timeline/task/performer$', login_required(api_views.TaskPerformerViewSet)),
    url(r'timeline/prj/owner$', login_required(api_views.OwnedPrjViewSet)),
    url(r'timeline/task/owner$', login_required(api_views.OwnedTasksViewSet)),
    url(r'timeline/prj/joined$', login_required(api_views.PrjJoinedViewSet)),
    url(r'timeline/task/joined$', login_required(api_views.TaskJoinedViewSet)),
)