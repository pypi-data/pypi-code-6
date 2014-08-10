from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from .models import State, Person, Item, ItemGroup

state_list = {'text': _('Assets states'), 'view': 'state_list', 'famfam': 'error_go'}
state_create = {'text': _('Create new asset state'), 'view': 'state_create', 'famfam': 'error_add'}
state_edit = {'text': _(u'Edit asset state'), 'view': 'state_update', 'args': 'object.id', 'famfam': 'error'}
state_delete = {'text': _(u'Delete asset state'), 'view': 'state_delete', 'args': 'object.id', 'famfam': 'error_delete'}

person_list = {'text': _('View all people'), 'view': 'person_list', 'famfam': 'user_go'}
person_create = {'text': _('Create new person'), 'view': 'person_create', 'famfam': 'user_add'}
person_update = {'text': _(u'Edit'), 'view': 'person_update', 'args': 'object.id', 'famfam': 'user_edit'}
person_delete = {'text': _(u'Delete'), 'view': 'person_delete', 'args': 'object.id', 'famfam': 'user_delete'}
person_photos = {'text': _(u'Add / remove photos'), 'view': 'person_photos', 'args': 'object.id', 'famfam': 'picture_edit'}
person_assign_item = {'text': _(u'Assign assets'), 'view': 'person_assign_item', 'args': 'object.id', 'famfam': 'computer_go'}

asset_list = {'text': _('View all assets'), 'view': 'item_list', 'famfam': 'computer'}
asset_create = {'text': _('Create new asset'), 'view': 'item_create', 'famfam': 'computer_add'}
asset_orphan_list = {'text': _('Orphan assets'), 'view': 'item_orphans_list'}
asset_edit = {'text': _(u'Edit'), 'view': 'item_update', 'args': 'object.id', 'famfam': 'computer_edit'}
asset_delete = {'text': _(u'Delete'), 'view': 'item_delete', 'args': 'object.id', 'famfam': 'computer_delete'}
asset_photos = {'text': _(u'Add / remove photos'), 'view': 'item_photos', 'args': 'object.id', 'famfam': 'picture_edit'}
asset_assign_person = {'text': _(u'Assign people'), 'view': 'item_assign_person', 'args': 'object.id', 'famfam': 'user_go'}
asset_template = {'text': _(u'Template'), 'view': 'template_view', 'args': 'object.item_template.id', 'famfam': 'page_go'}

group_list = {'text': _(u'View all item groups'), 'view': 'group_list', 'famfam': 'chart_pie'}
group_create = {'text': _(u'Create item group'), 'view': 'group_create', 'famfam': 'chart_pie_add'}
group_update = {'text': _(u'Edit'), 'view': 'group_update', 'args': 'object.id', 'famfam': 'chart_pie_edit'}
group_delete = {'text': _(u'Delete'), 'view': 'group_delete', 'args': 'object.id', 'famfam': 'chart_pie_delete'}

state_filter = {'name': 'state', 'title': _(u'State'), 'queryset': State.objects.all(), 'destination': 'itemstate'}

register_links(['item_list', 'item_view', 'item_create', 'item_orphans_list', 'item_update', 'item_delete', 'item_photos', 'item_assign_person', 'template_items_list'], [asset_create], menu_name='sidebar')
register_links(Item, [asset_edit, asset_delete, asset_photos, asset_assign_person, asset_template])

register_links(['person_list', 'person_create', 'person_view', 'person_update', 'person_delete', 'person_photos', 'person_assign_item'], [person_create], menu_name='sidebar')
register_links(Person, [person_update, person_delete, person_photos, person_assign_item])

register_links(['group_list', 'group_view', 'group_create', 'group_update', 'group_delete'], [group_create], menu_name='sidebar')
register_links(ItemGroup, [group_update, group_delete])

register_links(['state_list', 'state_create', 'state_update', 'state_delete'], [state_create], menu_name='sidebar')
register_links(State, [state_edit, state_delete])

register_menu([
    {'text': _('assets'), 'view': 'item_list', 'links': [
        asset_list, asset_orphan_list, group_list, person_list
    ], 'famfam': 'computer', 'position': 2},
])
