from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible
from django.utils.timezone import now


class Page(models.Model):
    title = models.CharField(_('title'), max_length=512, blank=True)

    url = models.CharField(_('URL'), max_length=200, unique=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('owner'))

    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'versionedpages/contact_page.html'. If this isn't provided, the system will use 'versionedpages/default.html'."))

    is_published = models.BooleanField(_('is published'), default=False)
    published = models.DateTimeField(_('published'), blank=True, null=True)
    published_version = models.ForeignKey(
        'Version',
        related_name='published_for',
        blank=True,
        null=True
    )

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        ordering = ['published', 'created']

    def edit(self, user):
        '''
        Get the latest version to edit or base an version off of. If the latest
        by this user is not saved it will be returned
        '''
        version = self.get_most_recent_version(user)

        # create a new version for this user or if the last version
        # was saved
        if version.is_saved == True:
            new_version = Version.objects.create(
                page=self,
                editor=user,
                parent=version,
                html=version.html,
            )
            return new_version
        else:
            return version

    def get_most_recent_version(self, user):
        '''
        Get the most recent version.
        '''
        # Just get the most recent save version. If the user has an unsaved version
        # something else should be done.
        versions = self.version_set.order_by('-created')
        if versions.exists():
            return versions[0]

        # else create one, should be the owner asking.
        version = Version.objects.create(
            page=self,
            editor=user,
        )
        return version

    def get_history(self):
        versions = self.version_set.all().order_by('-created')
        return versions

    def print_history(self):
        history = self.get_history()
        for version in history:
            output = version.created.isoformat() + u' ' + unicode(version)
            if self.published_version == version:
                output += " published"
            if version.is_saved == False:
                output += " not saved"
            print(output)

    @models.permalink
    def get_absolute_url(self):
        return ('versioned_page', [self.url])

    def __unicode__(self):
        return self.title


class Version(models.Model):
    page = models.ForeignKey(Page)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="versionpages_versions")
    parent = models.ForeignKey('self', blank=True, null=True)

    is_saved = models.BooleanField(_('is saved'), default=False)
    merged = models.BooleanField(_('merged'), default=False)

    html = models.TextField(_('html'), blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    def save_version(self):
        '''
        Version officially saved by the user, not
        just auto save
        '''
        self.is_saved = True
        self.save()

    def publish(self, update_time=False):
        if self.is_saved == False:
            self.save_version()
        page = self.page
        if page.published_version != self:
            page.published_version = self
            page.is_published = True
            if page.published is None or update_time:
                page.published = now()
            page.save()

    def __unicode__(self):
        return u' '.join((self.page.title, u'by', unicode(self.editor.get_full_name())))
