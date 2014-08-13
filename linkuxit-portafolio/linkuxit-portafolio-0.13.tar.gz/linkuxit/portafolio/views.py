from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import TeamMember
from .models import Project
from .models import Team
from .models import Client
from .models import Service


class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = 'linkuxit/portafolio/member/detail.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'linkuxit/portafolio/project/detail.html'


class TeamDetailView(DetailView):
    model = Team
    template_name = 'linkuxit/portafolio/team/detail.html'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'linkuxit/portafolio/service/detail.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = "linkuxit/portafolio/client/detail.html"


class ProjectListView(ListView):
    model = Project
    template_name = "linkuxit/portafolio/project/list.html"


class ServiceListView(ListView):
    model = Service
    template_name = "linkuxit/portafolio/service/list.html"


class TeamListView(ListView):
    model = Team
    template_name = "linkuxit/portafolio/team/list.html"


class ClientListView(ListView):
    model = Client
    template_name = "linkuxit/portafolio/client/list.html"

project_detail = ProjectDetailView.as_view()
member_detail = TeamMemberDetailView.as_view()
team_detail = TeamDetailView.as_view()
service_detail = ServiceDetailView.as_view()
client_detail = ClientDetailView.as_view()

project_list = ProjectListView.as_view()
service_list = ServiceListView.as_view()
team_list = TeamListView.as_view()
client_list = ClientListView.as_view()
