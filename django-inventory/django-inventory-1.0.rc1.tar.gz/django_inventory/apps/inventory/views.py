from __future__ import absolute_import

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView

from assets.models import Person, Item, ItemGroup
from generic_views.views import (GenericCreateView, GenericDeleteView,
                                 GenericDetailView, GenericListView,
                                 GenericUpdateView, generic_assign_remove)
from inventory import location_filter
from photos.views import generic_photos

from .forms import (InventoryForm, InventoryForm_view, InventoryTransactionForm,
                    ItemTemplateForm, ItemTemplateForm_view, LocationForm_view,
                    SupplierForm)
from .models import (Inventory, InventoryTransaction, ItemTemplate, Location,
                     Supplier)


class InventoryCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Inventory')}
    model = Inventory


class InventoryDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Inventory')}
    model = Inventory
    success_url = reverse_lazy('inventory_list')


class InventoryDetailView(GenericDetailView):
    extra_context = {
        'object_name': _(u'Inventory'),
    }
    form_class = InventoryForm_view
    model = Inventory

    def get_context_data(self, **kwargs):
        context = super(InventoryDetailView, self).get_context_data(**kwargs)
        supply_qty = {}
        for transaction in self.get_object().transactions.all():
            if transaction.supply in supply_qty:
                supply_qty[transaction.supply] = supply_qty[transaction.supply] + transaction.quantity
            else:
                supply_qty[transaction.supply] = transaction.quantity

        supplies_list = [{'item_template': item_template, 'qty': qty} for item_template, qty in supply_qty.items()]

        context['title'] = _(u'current balances for inventory: %s') % self.get_object()
        context['subtemplates_dict'] = [
            {
                'title': _(u'Items'),
                'name': 'generic_views/generic_list_subtemplate.html',
                'object_list': supplies_list,
                'main_object': 'item_template',
                'extra_columns': [{'name': _(u'quantity'), 'attribute': 'qty'}],
            }
        ]
        return context


class InventoryListView(GenericListView):
    extra_context = {
        'title': _(u'Inventories'),
        'extra_columns': [{'name': _(u'Location'), 'attribute': 'location'}]
    }
    model = Inventory
    template_name = 'generic_views/generic_list.html'


class InventoryUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Inventory')}
    form_class = InventoryForm
    model = Inventory


class LocationCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Location')}
    model = Location


class LocationDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Location')}
    model = Location
    success_url = reverse_lazy('location_list')


class LocationDetailView(GenericDetailView):
    form_class = LocationForm_view
    model = Location


class LocationListView(GenericListView):
    extra_context = {'title': _(u'Locations')}
    model = Location


class LocationUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Location')}
    model = Location


class SupplierCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Supplier')}
    form_class = SupplierForm


class SupplierDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Supplier')}
    model = Supplier
    success_url = reverse_lazy('supplier_list')


class SupplierDetailView(GenericDetailView):
    form_class = SupplierForm
    model = Supplier


class SupplierListView(GenericListView):
    extra_context = {
        'title': _(u'Suppliers')
    }
    model = Supplier


class SupplierPurchaseOrdersListView(GenericListView):
    def get_supplier(self):
        return get_object_or_404(Supplier, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_supplier().purchase_orders.all()

    def get_context_data(self, **kwargs):
        context = super(SupplierPurchaseOrdersListView, self).get_context_data(**kwargs)
        context['title'] = _(u'Purchase orders from supplier: %s') % self.get_supplier()
        return context


class SupplierUpdateView(GenericUpdateView):
    form_class = SupplierForm
    model = Supplier


class TemplateCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Item template')}
    form_class = ItemTemplateForm


class TemplateDeleteView(GenericDeleteView):
    extra_context = {
        'object_name': _(u'Item template'),
        'message': _(u'Will be deleted from any user that may have it assigned and from any item group.'),
    }
    model = ItemTemplate
    success_url = reverse_lazy('template_list')


class TemplateItemsListView(GenericListView):
    def get_template(self):
        return get_object_or_404(ItemTemplate, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_template().items.all()

    def get_context_data(self, **kwargs):
        context = super(TemplateItemsListView, self).get_context_data(**kwargs)
        context['title'] = _(u'Assets that use the template: %s') % self.get_template()
        return context


class TemplateListView(GenericListView):
    extra_context = {'title': _(u'Item template')}
    model = ItemTemplate


class TemplateOrphanListView(GenericListView):
    extra_context = {'title': _('Orphan templates')}
    queryset = ItemTemplate.objects.filter(items=None)


class TemplateUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Item template')}
    form_class = ItemTemplateForm
    model = ItemTemplate


class TemplateDetailView(GenericDetailView):
    form_class = ItemTemplateForm_view
    extra_context = {
        'object_name': _(u'Item template'),
        'sidebar_subtemplates': ['photos/generic_photos_subtemplate.html']
    }
    model = ItemTemplate


class TransactionDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Transaction')}
    model = InventoryTransaction
    success_url = reverse_lazy('inventory_list')


class TransactionDetailView(GenericDetailView):
    extra_context = {'object_name': _(u'Transaction')}
    form_class = InventoryTransactionForm
    model = InventoryTransaction


class TransactionUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Transaction')}
    model = InventoryTransaction


def supplier_assign_remove_itemtemplates(request, object_id):
    obj = get_object_or_404(Supplier, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign templates to the supplier: <a href="%(url)s">%(obj)s</a>' % {'url': obj.get_absolute_url(), 'obj': obj}),
        obj=obj,
        left_list_qryset=ItemTemplate.objects.exclude(suppliers=obj),
        right_list_qryset=obj.itemtemplate_set.all(),
        add_method=obj.itemtemplate_set.add,
        remove_method=obj.itemtemplate_set.remove,
        left_list_title=_(u'Unassigned templates'),
        right_list_title=_(u'Assigned templates'),
        item_name=_(u"templates"),
    )


def template_assign_remove_supply(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign supplies to the template: <a href="%(url)s">%(obj)s</a>' % {'url': obj.get_absolute_url(), 'obj': obj}),
        obj=obj,
        left_list_qryset=ItemTemplate.objects.exclude(supplies=obj).exclude(pk=obj.pk),
        right_list_qryset=obj.supplies.all(),
        add_method=obj.supplies.add,
        remove_method=obj.supplies.remove,
        left_list_title=_(u'Unassigned supplies'),
        right_list_title=_(u'Assigned supplies'),
        item_name=_(u"supplies"))


def template_assign_remove_suppliers(request, object_id):
    obj = get_object_or_404(ItemTemplate, pk=object_id)

    return generic_assign_remove(
        request,
        title=_(u'Assign suppliers to the template: <a href="%(url)s">%(obj)s</a>' % {'url': obj.get_absolute_url(), 'obj': obj}),
        obj=obj,
        left_list_qryset=Supplier.objects.exclude(itemtemplate=obj),
        right_list_qryset=obj.suppliers.all(),
        add_method=obj.suppliers.add,
        remove_method=obj.suppliers.remove,
        left_list_title=_(u'Unassigned suppliers'),
        right_list_title=_(u'Assigned suppliers'),
        item_name=_(u"suppliers"))


def inventory_list_transactions(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)
    form = InventoryForm_view(instance=inventory)

    return render_to_response('generic_views/generic_detail.html', {
        'object_name': _(u'Inventory'),
        'object': inventory,
        'form': form,
        'subtemplates_dict': [
            {
                'name': 'generic_views/generic_list_subtemplate.html',
                'title': _(u'Inventory transactions'),
                'object_list': inventory.transactions.all(),
                'hide_object': True,
                'extra_columns': [
                    {'name': _(u'Date'), 'attribute': 'date'},
                    {'name': _(u'Item'), 'attribute': 'supply'},
                    {'name': _(u'Qty'), 'attribute': 'quantity'},
                ],
            }
        ]
    }, context_instance=RequestContext(request))


def inventory_create_transaction(request, object_id):
    inventory = get_object_or_404(Inventory, pk=object_id)

    if request.method == 'POST':
        form = InventoryTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            msg = _(u'The inventory transaction was created successfully.')
            messages.success(request, msg, fail_silently=True)
            return redirect('inventory_list_transactions', inventory.id)
    else:
        form = InventoryTransactionForm(initial={'inventory': inventory})

    return render_to_response('generic_views/generic_form.html', {
        'form': form,
        'object': inventory,
        'title': _(u'Add new transaction'),
    }, context_instance=RequestContext(request))
