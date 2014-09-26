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
#
# @author: Ronak Shah

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class AddContractLink(tables.LinkAction):
    name = "addcontract"
    verbose_name = _("Create Contract")
    url = "horizon:project:contracts:addcontract"
    classes = ("ajax-modal", "btn-addcontract",)


class UpdateContractLink(tables.LinkAction):
    name = "updatecontract"
    verbose_name = _("Edit Contract")
    classes = ("ajax-modal",'edit_contract')

    def get_link_url(self, contract):
        base_url = reverse("horizon:project:contracts:updatecontract", kwargs={'contract_id': contract.id})
        return base_url


class DeleteContractLink(tables.DeleteAction):
    name = "deletecontract"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("Contract")
    data_type_plural = _("Contracts")


class AddPolicyRuleLink(tables.LinkAction):
    name = "addpolicyrules"
    verbose_name = _("Create Policy-Rule")
    url = "horizon:project:contracts:addpolicyrule"
    classes = ("ajax-modal", "btn-addpolicyrule",)


class UpdatePolicyRuleLink(tables.LinkAction):
    name = "updatepolicyrule"
    verbose_name = _("Edit PolicyRule")
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, policy_rule):
        base_url = reverse("horizon:project:contracts:updatepolicyrule",
                           kwargs={'policyrule_id': policy_rule.id})
        return base_url


class DeletePolicyRuleLink(tables.DeleteAction):
    name = "deletepolicyrule"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("PolicyRule")
    data_type_plural = _("PolicyRules")


class AddPolicyClassifierLink(tables.LinkAction):
    name = "addpolicyclassifiers"
    verbose_name = _("Create Policy-Classifier")
    url = "horizon:project:contracts:addpolicyclassifier"
    classes = ("ajax-modal", "btn-addpolicyclassifier",)


class UpdatePolicyClassifierLink(tables.LinkAction):
    name = "updatepolicyclassifier"
    verbose_name = _("Edit PolicyClassifier")
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, policy_classifier):
        base_url = reverse(
            "horizon:project:contracts:updatepolicyclassifier",
            kwargs={'policyclassifier_id': policy_classifier.id})
        return base_url


class DeletePolicyClassifierLink(tables.DeleteAction):
    name = "deletepolicyclassifier"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("PolicyClassifier")
    data_type_plural = _("PolicyClassifiers")


class AddPolicyActionLink(tables.LinkAction):
    name = "addpolicyactions"
    verbose_name = _("Create Policy-Action")
    url = "horizon:project:contracts:addpolicyaction"
    classes = ("ajax-modal", "btn-addpolicyaction",)


class UpdatePolicyActionLink(tables.LinkAction):
    name = "updatepolicyaction"
    verbose_name = _("Edit PolicyAction")
    classes = ("ajax-modal", "btn-update",)

    def get_link_url(self, policy_action):
        base_url = reverse("horizon:project:contracts:updatepolicyaction",
                           kwargs={'policyaction_id': policy_action.id})
        return base_url


class DeletePolicyActionLink(tables.DeleteAction):
    name = "deletepolicyaction"
    action_present = _("Delete")
    action_past = _("Scheduled deletion of %(data_type)s")
    data_type_singular = _("PolicyAction")
    data_type_plural = _("PolicyActions")


class ContractsTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"),
            link="horizon:project:contracts:contractdetails")

    class Meta:
        name = "contractstable"
        verbose_name = _("Contracts")
        table_actions = (AddContractLink, DeleteContractLink)
        row_actions = (UpdateContractLink, DeleteContractLink)


class PolicyRulesTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
            link="horizon:project:contracts:policyruledetails")

    class Meta:
        name = "policyrulestable"
        verbose_name = _("Policy Rules")
        table_actions = (AddPolicyRuleLink, DeletePolicyRuleLink)
        row_actions = (UpdatePolicyRuleLink, DeletePolicyRuleLink)


class PolicyClassifiersTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:project:contracts:policyclassifierdetails")

    class Meta:
        name = "policyclassifierstable"
        verbose_name = _("Policy Classifiers")
        table_actions = (AddPolicyClassifierLink, DeletePolicyClassifierLink)
        row_actions = (UpdatePolicyClassifierLink, DeletePolicyClassifierLink)


class PolicyActionsTable(tables.DataTable):
    name = tables.Column("name",
                         verbose_name=_("Name"),
                         link="horizon:project:contracts:policyactiondetails")

    class Meta:
        name = "policyactionstable"
        verbose_name = _("Policy Actions")
        table_actions = (AddPolicyActionLink, DeletePolicyActionLink)
        row_actions = (UpdatePolicyActionLink, DeletePolicyActionLink)
