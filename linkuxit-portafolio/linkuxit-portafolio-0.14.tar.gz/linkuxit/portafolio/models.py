# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


SOCIAL_NETWORK_CHOICES = (
    ('facebook', 'Facebook'),
    ('google-plus', 'Google+'),
    ('linkedin', 'LinkedIn'),
    ('rss', 'RSS'),
    ('share-this', 'ShareThis'),
    ('skype', 'Skype'),
    ('twitter', 'Twitter'),
    ('stackoverflow', 'Stack Overflow'),
    ('github', 'Github'),
)


class TeamMember(models.Model):
    """ Member of a team"""

    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True, default=None)
    full_name = models.CharField(_('Full Name'), max_length=250)
    slug = models.SlugField()
    is_active = models.BooleanField(_('Is active'), default=True)
    position = models.CharField(verbose_name=_('Position'), max_length=100)
    strong_skills = models.CharField(_('Strong skills'), max_length=50)
    summary = HTMLField(verbose_name=_('Summary'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ('created_at',)


class SocialLink(models.Model):
    """Social link"""
    member = models.ForeignKey(TeamMember, related_name='social_links', verbose_name=_('Member'))
    website = models.CharField(verbose_name=_('Website'), max_length=250, choices=SOCIAL_NETWORK_CHOICES)
    url = models.URLField(verbose_name=_('URL'))

    def __unicode__(self):
        return u'%s\'s %s' % (self.member.name, self.website)


class Service(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    slug = models.SlugField()
    html_class = models.CharField(verbose_name=_('Html Class'), blank=True, max_length=30, help_text=_('Use to add some font icon or to customize the item'), default='')
    description = HTMLField(verbose_name=_('Description'))
    is_featured = models.BooleanField(verbose_name=_('Is featured'), default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('order', 'created_at')


class Client(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    logo = FilerImageField(verbose_name=_('Logo'), null=True)
    description = HTMLField(verbose_name=_('Description'))
    is_featured = models.BooleanField(verbose_name=_('Is featured'), default=False)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class Project(models.Model):

    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.SlugField()
    description = HTMLField(verbose_name=_('Description'))
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(verbose_name=_('Is featured'), default=False)

    main_photo = FilerImageField(verbose_name=_('Photo'))

    country = models.ForeignKey(Country, related_name="projects", verbose_name=_('Country'))
    client = models.ForeignKey(Client, related_name="projects", verbose_name=_('Client'))
    developers = models.ManyToManyField(TeamMember, related_name='projects')
    services = models.ManyToManyField(Service, related_name="projects", verbose_name=_('Service'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('created_at',)


class Image(models.Model):
    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_('Photo'))
    description = HTMLField(verbose_name=_('Description'))
    project = models.ForeignKey(Project, related_name="images")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)


class Team(models.Model):
    name = models.CharField(verbose_name=_('Team name'), max_length=250)
    slug = models.SlugField(default='')
    description = HTMLField(verbose_name=_('Description'), default='')
    members = models.ManyToManyField(TeamMember, related_name='teams', verbose_name=_('Members'))

    def __unicode__(self):
        return self.name


class TeamPlugin(CMSPlugin):
    """Team plugin"""
    team = models.ForeignKey(Team, related_name='plugins', verbose_name=_('team'))

    def __unicode__(self):
        return self.team.name


class PortfolioPlugin(CMSPlugin):
    pass


class Testimonial(models.Model):
    testimonial = models.CharField(verbose_name=_('Testimonial'), max_length=300)
    client = models.ForeignKey(Client, related_name="testimonials", verbose_name=_('Client'))
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')

    def __unicode__(self):
        return self.testimonial[:30]
