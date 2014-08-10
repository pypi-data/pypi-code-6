from __future__ import absolute_import

import datetime

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _

from common.utils import encapsulate
from generic_views.views import (GenericCreateView, GenericDeleteView,
                                 GenericListView, GenericUpdateView)
from inventory.models import Supplier, ItemTemplate, InventoryTransaction

from . import purchase_order_state_filter, purchase_request_state_filter
from .forms import (PurchaseOrderForm, PurchaseOrderForm_view,
                    PurchaseOrderItem, PurchaseOrderItemForm,
                    PurchaseOrderItemTransferForm, PurchaseOrderWizardItemForm,
                    PurchaseRequestForm, PurchaseRequestForm_view,
                    PurchaseRequestItemForm)
from .models import (PurchaseOrder, PurchaseOrderItemStatus,
                     PurchaseOrderStatus, PurchaseRequest,
                     PurchaseRequestItem, PurchaseRequestStatus)


class PurchaseOrderItemDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase order item')}
    model = PurchaseOrderItem

    def get_success_url(self):
        return self.get_object().purchase_order.get_absolute_url()


class PurchaseOrderItemUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase order item')}
    form_class = PurchaseOrderItemForm
    model = PurchaseOrderItem


class PurchaseOrderItemStatusCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Purchase order item state')}
    model = PurchaseOrderItemStatus


class PurchaseOrderItemStatusDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase order item state')}
    model = PurchaseOrderItemStatus
    success_url = reverse_lazy('purchase_order_item_state_list')


class PurchaseOrderItemStatusListView(GenericListView):
    extra_context = {'title': _(u'Purchase order item status')}
    model = PurchaseOrderItemStatus


class PurchaseOrderItemStatusUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase order item state')}
    model = PurchaseOrderItemStatus


class PurchaseOrderCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Purchase order')}
    form_class = PurchaseOrderForm


class PurchaseOrderDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase order')}
    model = PurchaseOrder
    success_url = reverse_lazy('purchase_order_list')


class PurchaseOrderListView(GenericListView):
    extra_context = {
        'title': _(u'Purchase orders'),
        'extra_columns': [
            {'name': _(u'Active'), 'attribute': encapsulate(lambda x: _(u'Open') if x.active else _(u'Closed'))}
        ]
    }
    list_filters = [purchase_order_state_filter]
    model = PurchaseOrder


class PurchaseOrderUpdateView(GenericUpdateView):
    form_class = PurchaseOrderForm
    model = PurchaseOrder


class PurchaseOrderStatusCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Purchase order status')}
    model = PurchaseOrderStatus


class PurchaseOrderStatusDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase order status')}
    model = PurchaseOrderStatus
    success_url = reverse_lazy('purchase_order_state_list')


class PurchaseOrderStatusListView(GenericListView):
    extra_context = {'title': _(u'Purchase order status')}
    model = PurchaseOrderStatus


class PurchaseOrderStatusUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase order status')}
    model = PurchaseOrderStatus


class PurchaseRequestCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Purchase request')}
    form_class = PurchaseRequestForm


class PurchaseRequestDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase request')}
    model = PurchaseRequest
    success_url = reverse_lazy('purchase_request_list')


class PurchaseRequestListView(GenericListView):
    model = PurchaseRequest
    extra_context = {
        'title': _(u'Purchase requests'),
        'extra_columns': [
            {'name': _(u'Active'), 'attribute': encapsulate(lambda x: _(u'Open') if x.active else _(u'Closed'))}
        ]
    }
    list_filters = [purchase_request_state_filter]


class PurchaseRequestUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase request')}
    form_class = PurchaseRequestForm
    model = PurchaseRequest


class PurchaseRequestStateCreateView(GenericCreateView):
    extra_context = {'object_name': _(u'Purchase request state')}
    model = PurchaseRequestStatus


class PurchaseRequestStateDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase request state')}
    model = PurchaseRequestStatus
    success_url = reverse_lazy('purchase_request_state_list')


class PurchaseRequestStateListView(GenericListView):
    extra_context = {'title': _(u'Purchase request states')}
    model = PurchaseRequestStatus


class PurchaseRequestStateUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase request state')}
    model = PurchaseRequestStatus


class PurchaseRequestItemDeleteView(GenericDeleteView):
    extra_context = {'object_name': _(u'Purchase request item')}
    model = PurchaseRequestItem

    def get_success_url(self):
        return self.get_object().purchase_request.get_absolute_url()


class PurchaseRequestItemUpdateView(GenericUpdateView):
    extra_context = {'object_name': _(u'Purchase request item')}
    model = PurchaseRequestItem


def purchase_request_view(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)
    form = PurchaseRequestForm_view(
        instance=purchase_request,
        extra_fields=[
            {'field': 'purchaseorder_set.all', 'label': _(u'Related purchase orders')}
        ]
    )

    return render_to_response('generic_views/generic_detail.html', {
        'title': _(u'Details for purchase request: %s') % purchase_request,
        'object': purchase_request,
        'form': form,
        'subtemplates_dict': [
            {
                'name': 'generic_views/generic_list_subtemplate.html',
                'title': _(u'Purchase request items'),
                'object_list': purchase_request.items.all(),
                'extra_columns': [{'name': _(u'Qty'), 'attribute': 'qty'}],
            },
            #TODO: Used this instead when pagination namespace is supported
            #{
            #    'name':'generic_list_subtemplate.html',
            #    'title':_(u'related purchase orders'),
            #    'object_list':purchase_request.purchaseorder_set.all(),
            #    'extra_columns':[{'name':_(u'issue data'), 'attribute':'issue_date'}],
            #}
        ]
    }, context_instance=RequestContext(request))


def purchase_request_item_create(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)

    if request.method == 'POST':
        form = PurchaseRequestItemForm(request.POST)#, initial={'purchase_request':purchase_request})
        if form.is_valid():
            form.save()
            msg = _(u'The purchase request item was created successfully.')
            messages.success(request, msg, fail_silently=True)
            return redirect(purchase_request.get_absolute_url())
    else:
        form = PurchaseRequestItemForm(initial={'purchase_request': purchase_request})

    return render_to_response('generic_views/generic_form.html', {
        'form': form,
        'title': _(u'add new purchase request item'),
    }, context_instance=RequestContext(request))


def purchase_request_close(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)

    data = {
        'object': purchase_request,
        'title': _(u'Are you sure you wish to close the purchase request: %s?') % purchase_request,
    }

    if not purchase_request.active:
        msg = _(u'This purchase request has already been closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())

    if request.method == 'POST':
        purchase_request.active = False
        purchase_request.save()
        msg = _(u'The purchase request has been closed successfully.')
        messages.success(request, msg, fail_silently=True)
        return redirect(purchase_request.get_absolute_url())

    return render_to_response('generic_views/generic_confirm.html', data,
        context_instance=RequestContext(request))


def purchase_request_open(request, object_id):
    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)

    data = {
        'object': purchase_request,
        'title': _(u'Are you sure you wish to open the purchase request: %s?') % purchase_request,
    }

    if purchase_request.active:
        msg = _(u'This purchase request is already open.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())

    if request.method == 'POST':
        purchase_request.active = True
        purchase_request.save()
        msg = _(u'The purchase request has been opened successfully.')
        messages.success(request, msg, fail_silently=True)
        return redirect(purchase_request.get_absolute_url())

    return render_to_response('generic_views/generic_confirm.html', data,
        context_instance=RequestContext(request))


def purchase_order_wizard(request, object_id):
    """
    Creates new purchase orders based on the item suppliers selected
    from a purchase request
    """

    purchase_request = get_object_or_404(PurchaseRequest, pk=object_id)

    # A closed purchase orders may also mean a PO has been generated
    # previously from it by this wizard
    if not purchase_request.active:
        msg = _(u'This purchase request is closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())

    if not purchase_request.items.all():
        msg = _(u'This purchase request is empty, add items before using the wizard.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_request.get_absolute_url())

    # Create a formset for all the items in the purchase request
    # and let the user select from the available suppliers from each
    # item
    ItemsFormSet = formset_factory(PurchaseOrderWizardItemForm, extra=0)

    initial = []
    for item in purchase_request.items.all():
        initial.append({
            'item': item
        })

    if request.method == 'POST':
        formset = ItemsFormSet(request.POST, initial=initial)
        if formset.is_valid():
            # Create a dictionary of supplier and corresponding items
            # to be ordered from them
            # TODO: Can this be done with a reduce function?
            suppliers = {}
            for form in formset.forms:
                supplier = get_object_or_404(Supplier, pk=form.cleaned_data['supplier'])
                item_template = get_object_or_404(ItemTemplate, pk=form.cleaned_data['template_id'])
                if supplier in suppliers:
                    suppliers[supplier].append({'item_template': item_template, 'qty': form.cleaned_data['qty']})
                else:
                    suppliers[supplier] = [{'item_template': item_template, 'qty': form.cleaned_data['qty']}]

            # Create a new purchase order for each supplier in the
            # suppliers directory
            new_pos = []
            for supplier, po_items_data in suppliers.items():
                purchase_order = PurchaseOrder(
                    purchase_request=purchase_request,
                    supplier=supplier
                )
                new_pos.append(purchase_order)
                purchase_order.save()

                # Create the purchase order items
                for po_item_data in po_items_data:
                    po_item = PurchaseOrderItem(
                        purchase_order=purchase_order,
                        item_template=po_item_data['item_template'],
                        qty=po_item_data['qty']
                    )
                    po_item.save()

            purchase_request.active = False
            purchase_request.save()
            msg = _(u'The following new purchase order have been created: %s.') % (', '.join(['%s' % po for po in new_pos]))
            messages.success(request, msg, fail_silently=True)

            return redirect('purchase_order_list')
    else:
        formset = ItemsFormSet(initial=initial)
    return render_to_response('generic_views/generic_form.html', {
        'form': formset,
        'form_display_mode_table': True,
        'title': _(u'Purchase order wizard, using purchase request source: <a href="%(url)s">%(name)s</a>') % {'url': purchase_request.get_absolute_url(), 'name': purchase_request},
        'object': purchase_request,
    }, context_instance=RequestContext(request))


def purchase_order_view(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)
    form = PurchaseOrderForm_view(instance=purchase_order)

    return render_to_response('generic_views/generic_detail.html', {
        'title': _(u'Details for purchase order: %s') % purchase_order,
        'object': purchase_order,
        'form': form,
        'subtemplates_dict': [{
            'name': 'generic_views/generic_list_subtemplate.html',
            'title': _(u'Purchase order items'),
            'object_list': purchase_order.items.all(),
            'extra_columns': [
                {'name': _(u'Qty'), 'attribute': 'qty'},
                {'name': _(u'Qty received'), 'attribute': 'received_qty'},
                {'name': _(u'Agreed price'), 'attribute': encapsulate(lambda x: '%s' % x.agreed_price if x.agreed_price else '-')},
                {'name': _(u'Status'), 'attribute': 'status'},
                {'name': _(u'Active'), 'attribute': encapsulate(lambda x: _(u'Open') if x.active else _(u'Closed'))}
            ],
        }]
    }, context_instance=RequestContext(request))


def purchase_order_close(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)
    items = purchase_order.items.all()

    data = {
        'object': purchase_order,
        'title': _(u'Are you sure you wish to close the purchase order: %s?') % purchase_order,
    }

    if items.filter(active=True):
        data['message'] = _(u'There are still open items.')

    if not purchase_order.active:
        msg = _(u'This purchase order has already been closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(purchase_order.get_absolute_url())

    if request.method == 'POST':
        purchase_order.active = False
        items.update(active=False)
        purchase_order.save()
        msg = _(u'The purchase order has been closed successfully.')
        messages.success(request, msg, fail_silently=True)
        return redirect(purchase_order.get_absolute_url())

    return render_to_response('generic_views/generic_confirm.html', data,
        context_instance=RequestContext(request))


def purchase_order_open(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)

    data = {
        'object': purchase_order,
        'title': _(u'Are you sure you wish to open the purchase order: %s?') % purchase_order,
    }

    if purchase_order.active:
        msg = _(u'This purchase order is already open.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order.get_absolute_url())

    if request.method == 'POST':
        purchase_order.active = True
        purchase_order.save()
        msg = _(u'The purchase order has been opened successfully.')
        messages.success(request, msg, fail_silently=True)
        return redirect(purchase_order.get_absolute_url())

    return render_to_response('generic_views/generic_confirm.html', data,
        context_instance=RequestContext(request))


def purchase_order_transfer(request, object_id):
    """
    Take a purchase order and call transfer_to_inventory to transfer and
    close all of its item and close the purchase order too
    """

    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)

    if not purchase_order.active:
        msg = _(u'This purchase order has already been closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order.get_absolute_url())

    return transfer_to_inventory(request, purchase_order)


def transfer_to_inventory(request, object_to_transfer):
    """
    Take an item from a purchase order, or an entire purchase order and
    create inventory transaction entries to add the items to an inventory
    and close the item and/or the purchase order
    """
    FormSet = formset_factory(PurchaseOrderItemTransferForm, extra=0)
    context = {}

    if isinstance(object_to_transfer, PurchaseOrderItem):
        # A single purchase order item
        context = {
            'object_name': _(u'Purchase order item'),
            'title': _(u'Transfer and close the received purchase orders item: %s') % object_to_transfer,
        }
        # Seed a formset of a single form
        initial = [{
            'qty': object_to_transfer.received_qty,
            'purchase_order_item': object_to_transfer,
            'purchase_order_item_id': object_to_transfer.id
        }]
    elif isinstance(object_to_transfer, PurchaseOrder):
        # An entire purchase order
        context = {
            'object_name': _(u'Purchase order'),
        }
        # Seed the formset for each PO item
        initial = []
        items = object_to_transfer.items.filter(active=True)
        if not items:
            # There are no PO items active
            context['title'] = _(u'All the items from this purchase order are either closed or transfered, continue to close the purchase order.')
        else:
            context['title'] = _(u'Transfer and close all the received items from the purchase order: %s') % object_to_transfer

        for item in items:
            initial.append({
                'qty': item.received_qty,
                'purchase_order_item': item,
                'purchase_order_item_id': item.id
            })
    # TODO: Raise error if object_to_transfer is neither a PO nor a PO item?
    # else:
    #    raise 'Unknown object type'

    if request.method == 'POST':
        formset = FormSet(request.POST)
        if formset.is_valid():
            if len(formset.forms):
                # In case of empty PO or PO w/ no active items
                for form in formset.forms:
                    # Create inventory transaction for each PO item
                    purchase_order_item = get_object_or_404(PurchaseOrderItem, pk=form.cleaned_data['purchase_order_item_id'])
                    transaction = InventoryTransaction(
                        inventory=form.cleaned_data['inventory'],
                        supply=purchase_order_item.item_template,
                        quantity=form.cleaned_data['qty'],
                        date=datetime.date.today(),
                        notes=_(u'Automatically transfered from purchase order:%s') % purchase_order_item.purchase_order
                    )
                    transaction.save()
                    purchase_order_item.active = False
                    purchase_order_item.save()

                if isinstance(object_to_transfer, PurchaseOrderItem):
                    msg = _(u'The purchase order item has been transfered and closed successfully.')
                    messages.success(request, msg, fail_silently=True)
                    return redirect(purchase_order_item.get_absolute_url())
                elif isinstance(object_to_transfer, PurchaseOrder):
                    object_to_transfer.active = False
                    object_to_transfer.save()
                    msg = _(u'All the purchase order items have been transfered and closed successfully, the purchase order has been closed as well.')
                    messages.success(request, msg, fail_silently=True)
                    return redirect(object_to_transfer.get_absolute_url())
            else:
                # Empty PO or PO w/ no active items
                object_to_transfer.active = False
                object_to_transfer.save()
                msg = _(u'All the purchase order items were closed or already transfered, closing the purchase order.')
                messages.success(request, msg, fail_silently=True)
                return redirect(object_to_transfer.get_absolute_url())

    else:
        formset = FormSet(initial=initial)

    context.update({
        'object': object_to_transfer,
        'form': formset,
        'form_display_mode_table': True
    })

    return render_to_response('generic_views/generic_form.html', context,
        context_instance=RequestContext(request))


def purchase_order_item_transfer(request, object_id):
    """
    Take a purchase order item and call transfer_to_inventory to
    transfer and close the item
    """

    purchase_order_item = get_object_or_404(PurchaseOrderItem, pk=object_id)

    if not purchase_order_item.active:
        msg = _(u'This purchase order item has already been closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order_item.get_absolute_url())

    return transfer_to_inventory(request, purchase_order_item)


def purchase_order_item_close(request, object_id):
    purchase_order_item = get_object_or_404(PurchaseOrderItem, pk=object_id)
    data = {
        'object': purchase_order_item,
        'title': _(u'Are you sure you wish close the purchase order item: %s') % purchase_order_item,
    }

    if not purchase_order_item.active:
        msg = _(u'This purchase order item has already been closed.')
        messages.error(request, msg, fail_silently=True)
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else purchase_order.get_absolute_url())

    if request.method == 'POST':
        purchase_order_item.active = False
        purchase_order_item.save()
        msg = _(u'The purchase order item has been closed successfully.')
        messages.success(request, msg, fail_silently=True)
        return redirect(purchase_order_item.get_absolute_url())

    return render_to_response('generic_views/generic_confirm.html', data,
        context_instance=RequestContext(request))


def purchase_order_item_create(request, object_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=object_id)

    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            msg = _(u'The purchase order item was created successfully.')
            messages.success(request, msg, fail_silently=True)
            return redirect(purchase_order.get_absolute_url())
    else:
        form = PurchaseOrderItemForm(initial={'purchase_order': purchase_order})

    return render_to_response('generic_views/generic_form.html', {
        'form': form,
        'title': _(u'Add new purchase order item'),
    }, context_instance=RequestContext(request))
