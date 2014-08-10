from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from dynamic_search.api import register
from inventory.models import ItemTemplate, Location
from photos.models import GenericPhoto


class State(models.Model):
    name = models.CharField(max_length=32, verbose_name=_(u'Name'))
    exclusive = models.BooleanField(default=False, verbose_name=_(u'Exclusive'))

    class Meta:
        verbose_name = _(u'Asset state')
        verbose_name_plural = _(u'Asset states')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.exclusive and _(u'Exclusive') or _(u'Inclusive'))

    @models.permalink
    def get_absolute_url(self):
        return ('state_list', [])


class ItemStateManager(models.Manager):
    def states_for_item(self, item):
        return self.filter(item=item)


class ItemState(models.Model):
    item = models.ForeignKey('Item', verbose_name=_(u'Item'))
    state = models.ForeignKey(State, verbose_name=_(u'State'))
    date = models.DateField(auto_now_add=True, verbose_name=_(u'Date'))

    objects = ItemStateManager()

    class Meta:
        verbose_name = _(u'Item state')
        verbose_name_plural = _(u'Item state')

    def __unicode__(self):
        return _(u'%(asset)s, %(state)s since %(date)s') % {'asset': self.item, 'state': self.state.name, 'date': self.date}

    @models.permalink
    def get_absolute_url(self):
        return ('state_update', [str(self.id)])


class Item(models.Model):
    item_template = models.ForeignKey(ItemTemplate, related_name='items', verbose_name=_(u'Item template'))
    property_number = models.CharField(max_length=48, verbose_name=_(u'Asset number'))
    notes = models.TextField(blank=True, null=True, verbose_name=_(u'Notes'))
    serial_number = models.CharField(blank=True, max_length=48, null=True, verbose_name=_(u'Serial number'))
    location = models.ForeignKey(Location, blank=True, null=True, verbose_name=_(u'Location'))
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['property_number']
        verbose_name = _(u'Asset')
        verbose_name_plural = _(u'Assets')

    @models.permalink
    def get_absolute_url(self):
        return ('item_view', [str(self.id)])

    def __unicode__(self):
        states = ', '.join([itemstate.state.name for itemstate in ItemState.objects.states_for_item(self)])
        return "#%s, '%s' %s" % (self.property_number, self.item_template.description, states and '(%s)' % states)

    def is_orphan(self):
        if self.person_set.all():
            return False
        else:
            return True

    def get_owners(self):
        try:
            return self.person_set.all()
        except:
            return None

    def get_nonowners(self):
        return Person.objects.all().exclude(id__in=self.person_set.values_list('id', flat=True))

    def add_owner(self, person):
        if self not in person.inventory.all():
            person.inventory.add(self)

    def remove_owner(self, person):
        person.inventory.remove(self)

    def states(self):
        return [State.objects.get(pk=id) for id in self.itemstate_set.all().values_list('state', flat=True)]


class ItemGroup(models.Model):
    name = models.CharField(verbose_name=_(u'Name'), max_length=32)
    items = models.ManyToManyField(Item, blank=True, null=True, verbose_name=_(u'Item'))

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Item group')
        verbose_name_plural = _(u'Item groups')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('group_view', [str(self.id)])


class Person(models.Model):
    last_name = models.CharField(verbose_name=_(u'Last name'), max_length=32)
    second_last_name = models.CharField(verbose_name=_(u'Second last name'), max_length=32, blank=True, null=True)
    first_name = models.CharField(verbose_name=_(u'First name'), max_length=32)
    second_name = models.CharField(verbose_name=_(u'Second name or initial'), max_length=32, blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True, verbose_name=_(u'Location'))
    inventory = models.ManyToManyField(Item, blank=True, null=True, verbose_name=_(u'Assigned assets'))

    class Meta:
        ordering = ['last_name', 'second_last_name', 'first_name', 'second_name']
        verbose_name = _(u'Person')
        verbose_name_plural = _(u'People')

    @models.permalink
    def get_absolute_url(self):
        return ('person_view', [str(self.id)])

    def __unicode__(self):
        if self.second_last_name:
            second_last_name = ' %s' % self.second_last_name
        else:
            second_last_name = ''

        if self.second_name:
            second_name = ' %s' % self.second_name
        else:
            second_name = ''

        return '%s%s, %s%s' % (self.last_name, second_last_name and second_last_name, self.first_name, second_name)


register(ItemState, _(u'Asset states'), ['state__name'])
register(Item, _(u'Assets'), ['property_number', 'notes', 'serial_number', 'person__first_name', 'person__last_name', 'person__second_last_name', 'person__second_name'])
register(ItemGroup, _(u'Asset groups'), ['name'])
register(Person, _(u'People'), ['last_name', 'second_last_name', 'first_name', 'second_name', 'location__name'])
