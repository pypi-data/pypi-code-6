# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from .models import PortfolioPlugin
from .models import TeamPlugin
from .models import Team
from .models import Project
from .models import Service
from .models import Client
from .models import Testimonial


class PortafolioBase(CMSPluginBase):
    module = 'Portafolio'


class PortfolioCMSPlugin(PortafolioBase):
    model = PortfolioPlugin
    render_template = 'aldryn_portafolio/plugins/portafolio/portafolio.html'
    name = _("Portafolio")

    def render(self, context, instance, placeholder):
        context.update({'projects': Project.objects.filter(is_featured=True)})
        return context


class ServicesCMSPlugin(PortafolioBase):
    model = CMSPlugin
    render_template = 'aldryn_portafolio/plugins/portafolio/services.html'
    name = _("Services")

    def render(self, context, instance, placeholder):
        context.update({'services': Service.objects.filter(is_featured=True)})
        return context


class ClientsCMSPlugin(PortafolioBase):
    model = CMSPlugin
    render_template = 'aldryn_portafolio/plugins/portafolio/clients.html'
    name = _("Clients")

    def render(self, context, instance, placeholder):
        context.update({'clients': Client.objects.filter(is_featured=True)})
        return context


class TeamCMSPlugin(PortafolioBase):
    model = TeamPlugin
    render_template = 'aldryn_portafolio/plugins/portafolio/team.html'
    name = _("Team")


class TestimonialsCMSPlugin(PortafolioBase):
    model = CMSPlugin
    render_template = 'aldryn_portafolio/plugins/portafolio/testimonials.html'
    name = _("Testimonials")

    def render(self, context, instance, placeholder):
        context.update({'testimonials': Testimonial.objects.filter(is_active=True)})
        return context


plugin_pool.register_plugin(PortfolioCMSPlugin)
plugin_pool.register_plugin(ClientsCMSPlugin)
plugin_pool.register_plugin(ServicesCMSPlugin)
plugin_pool.register_plugin(TeamCMSPlugin)
plugin_pool.register_plugin(TestimonialsCMSPlugin)
