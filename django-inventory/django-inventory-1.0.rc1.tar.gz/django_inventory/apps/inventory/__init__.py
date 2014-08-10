from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from .models import Location, ItemTemplate, Inventory, InventoryTransaction, Supplier

inventory_list = {'text': _('View all inventories'), 'view': 'inventory_list', 'famfam': 'package_go'}
inventory_create = {'text': _('Create new inventory'), 'view': 'inventory_create', 'famfam': 'package_add'}
inventory_update = {'text': _(u'Edit'), 'view': 'inventory_update', 'args': 'object.id', 'famfam': 'package_green'}
inventory_delete = {'text': _(u'Delete'), 'view': 'inventory_delete', 'args': 'object.id', 'famfam': 'package_delete'}
inventory_create_transaction = {'text': _('Add transaction'), 'view': 'inventory_create_transaction', 'args': 'object.id', 'famfam': 'book_add'}
inventory_view = {'text': _(u'Details'), 'view': 'inventory_view', 'args': 'object.id', 'famfam': 'package_go'}
inventory_list_transactions = {'text': _(u'Inventory transactions'), 'view': 'inventory_list_transactions', 'args': 'object.id', 'famfam': 'book_go'}

inventory_transaction_update = {'text': _(u'Edit'), 'view': 'inventory_transaction_update', 'args': 'object.id', 'famfam': 'book_add'}
inventory_transaction_delete = {'text': _(u'Delete'), 'view': 'inventory_transaction_delete', 'args': 'object.id', 'famfam': 'book_delete'}
inventory_transaction_view = {'text': _(u'Details'), 'view': 'inventory_transaction_view', 'args': 'object.id', 'famfam': 'book_go'}

location_list = {'text': _('Locations'), 'view': 'location_list', 'famfam': 'map'}
location_create = {'text': _(u'Create new location'), 'view': 'location_create', 'famfam': 'map_add'}
location_update = {'text': _(u'Edit'), 'view': 'location_update', 'args': 'object.id', 'famfam': 'map_edit'}
location_delete = {'text': _(u'Delete'), 'view': 'location_delete', 'args': 'object.id', 'famfam': 'map_delete'}

supplier_create = {'text': _('Create new supplier'), 'view': 'supplier_create', 'famfam': 'lorry_add'}
supplier_list = {'text': _('Suppliers'), 'view': 'supplier_list', 'famfam': 'lorry'}
supplier_update = {'text': _('Edit'), 'view': 'supplier_update', 'args': 'object.id', 'famfam': 'lorry'}
supplier_delete = {'text': _('Delete'), 'view': 'supplier_delete', 'args': 'object.id', 'famfam': 'lorry_delete'}
supplier_assign_itemtemplate = {'text': _(u'Assign templates'), 'view': 'supplier_assign_itemtemplates', 'args': 'object.id', 'famfam': 'page_go'}
supplier_purchase_orders = {'text': _(u'Related purchase orders'), 'view': 'supplier_purchase_orders', 'args': 'object.id', 'famfam': 'cart_go'}

template_list = {'text': _('View all'), 'view': 'template_list', 'famfam': 'page_go'}
template_create = {'text': _('Create new template'), 'view': 'template_create', 'famfam': 'page_add'}
template_orphan_list = {'text': _('Orphans templates'), 'view': 'template_orphans_list'}
template_update = {'text': _(u'Edit'), 'view': 'template_update', 'args': 'object.id', 'famfam': 'page_edit'}
template_delete = {'text': _(u'Delete'), 'view': 'template_delete', 'args': 'object.id', 'famfam': 'page_delete'}
template_photos = {'text': _(u'Add / remove photos'), 'view': 'template_photos', 'args': 'object.id', 'famfam': 'picture_go'}
template_assets = {'text': _(u'Related assets'), 'view': 'template_items_list', 'args': 'object.id', 'famfam': 'computer_go'}
template_assign_supplies = {'text': _(u'Assign supplies'), 'view': 'template_assign_supply', 'args': 'object.id', 'famfam': 'monitor'}
template_assign_suppliers = {'text': _(u'Assign suppliers'), 'view': 'template_assign_suppliers', 'args': 'object.id', 'famfam': 'lorry_go'}

jump_to_template = {'text': _(u'Template'), 'view': 'template_view', 'args': 'object.supply.id', 'famfam': 'page_go'}
jump_to_inventory = {'text': _(u'Return to inventory'), 'view': 'inventory_view', 'args': 'object.inventory.id', 'famfam': 'package_go'}

template_menu_links = [template_list, template_orphan_list, supplier_list]
inventory_menu_links = [
    inventory_list,
]

location_filter = {'name': 'Location', 'title': _(u'location'), 'queryset': Location.objects.all(), 'destination': 'location'}

register_links(['template_list', 'template_create', 'template_view', 'template_orphans_list', 'template_update', 'template_delete', 'template_photos', 'template_assign_supply', 'template_assign_suppliers'], [template_create], menu_name='sidebar')
register_links(ItemTemplate, [template_update, template_delete, template_photos, template_assets, template_assign_supplies, template_assign_suppliers])

register_links(['supplier_list', 'supplier_create', 'supplier_update', 'supplier_view', 'supplier_delete', 'supplier_assign_itemtemplates'], [supplier_create], menu_name='sidebar')
register_links(Supplier, [supplier_update, supplier_delete, supplier_assign_itemtemplate, supplier_purchase_orders])

register_links(['inventory_view', 'inventory_list', 'inventory_create', 'inventory_update', 'inventory_delete'], [inventory_create], menu_name='sidebar')
register_links(Inventory, [inventory_update, inventory_delete, inventory_list_transactions, inventory_create_transaction])
register_links(Inventory, [inventory_view], menu_name='sidebar')

register_links(['inventory_transaction_update', 'inventory_transaction_delete', 'inventory_transaction_view'], [inventory_create_transaction], menu_name='sidebar')
register_links(InventoryTransaction, [inventory_transaction_view, inventory_transaction_update, inventory_transaction_delete, jump_to_template])
register_links(InventoryTransaction, [jump_to_inventory], menu_name='sidebar')

register_links(['location_list', 'location_create', 'location_update', 'location_delete'], [location_create], menu_name='sidebar')
register_links(Location, [location_update, location_delete])

register_menu([
    {'text': _('Templates'), 'view': 'template_list', 'links': template_menu_links, 'famfam': 'page', 'position': 1},
    {'text': _('Inventories'), 'view': 'inventory_list', 'links': inventory_menu_links, 'famfam': 'package', 'position': 4},
])
