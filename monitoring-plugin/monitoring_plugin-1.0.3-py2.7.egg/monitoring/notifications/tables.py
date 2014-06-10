# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables

from . import constants
from monitoring import api

LOG = logging.getLogger(__name__)


class DeleteNotification(tables.DeleteAction):
    name = "delete_notification"
    verbose_name = _("Delete Notification")
    data_type_singular = _("Notification")
    data_type_plural = _("Notifications")

    def allowed(self, request, datum=None):
        return True

    def delete(self, request, obj_id):
        try:
            api.monitor.notification_delete(request, obj_id)
        except Exception as e:
            exceptions.handle(
                request,
                _('Unable to delete notification: %s') %
                e)


class CreateNotification(tables.LinkAction):
    name = "create_notification"
    verbose_name = _("Create Notification")
    classes = ("ajax-modal", "btn-create")

    def get_link_url(self):
        return reverse(constants.URL_PREFIX + 'notification_create',)

    def allowed(self, request, datum=None):
        return True


class EditNotification(tables.LinkAction):
    name = "edit_notification"
    verbose_name = _("Edit Notification")
    classes = ("ajax-modal", "btn-create")

    def get_link_url(self, datum):
        return reverse(constants.URL_PREFIX + 'notification_edit',
                       datum['id'], )

    def allowed(self, request, datum=None):
        return True


class NotificationsTable(tables.DataTable):
    target = tables.Column('name', verbose_name=_('Name'))
    type = tables.Column('type', verbose_name=_('Type'))
    address = tables.Column('address', verbose_name=_('Address'))

    def get_object_id(self, obj):
        return obj['id']

    def get_object_display(self, obj):
        return obj['name']

    class Meta:
        name = "notifications"
        verbose_name = _("Notifications")
        row_actions = (DeleteNotification, )
        table_actions = (CreateNotification, )
