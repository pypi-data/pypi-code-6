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


from __future__ import absolute_import

from openstack_dashboard.api import neutron

neutronclient = neutron.neutronclient


class EP(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron endpoint group."""

    def get_dict(self):
        ep_dict = self._apidict
        ep_dict['ep_id'] = ep_dict['id']
        return ep_dict


class EPG(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron endpoint group."""

    def get_dict(self):
        epg_dict = self._apidict
        epg_dict['epg_id'] = epg_dict['id']
        return epg_dict


class Contract(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron contract."""

    def get_dict(self):
        contract_dict = self._apidict
        contract_dict['contract_id'] = contract_dict['id']
        return contract_dict


class PolicyRule(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron policy rule."""

    def get_dict(self):
        policyrule_dict = self._apidict
        policyrule_dict['policyrule_dict_id'] = policyrule_dict['id']
        return policyrule_dict


class PolicyClassifier(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron classifier."""

    def get_dict(self):
        classifier_dict = self._apidict
        classifier_dict['classifier_id'] = classifier_dict['id']
        return classifier_dict


class PolicyAction(neutron.NeutronAPIDictWrapper):
    """Wrapper for neutron action."""

    def get_dict(self):
        action_dict = self._apidict
        action_dict['action_id'] = action_dict['id']
        return action_dict


def epg_create(request, **kwargs):
    body = {'endpoint_group': kwargs}
    epg = neutronclient(request).create_endpoint_group( body).get('endpoint_group')
    return EPG(epg)


def ep_create(request,**kwargs):
    body = {'endpoint': kwargs}
    ep = neutronclient(request).create_endpoint(body).get('endpoint')
    return EPG(ep)


def ep_list(request, **kwargs):
    eps = neutronclient(request).list_endpoints(**kwargs).get('endpoints')
    return [EP(ep) for ep in eps]


def epg_list(request, **kwargs):
    epgs = neutronclient(request).list_endpoint_groups(
        **kwargs).get('endpoint_groups')
    return [EPG(epg) for epg in epgs]


def epg_get(request, epg_id):
    epg = neutronclient(request).show_endpoint_group(
        epg_id).get('endpoint_group')
    return EPG(epg)


def epg_delete(request, epg_id):
    neutronclient(request).delete_endpoint_group(epg_id)


def epg_update(request, epg_id, **kwargs):
    body = {'endpoint_group': kwargs}
    epg = neutronclient(request).update_endpoint_group(
        epg_id, body).get('endpoint_group')
    return EPG(epg)


def contract_create(request, **kwargs):
    body = {'contract': kwargs}
    contract = neutronclient(request).create_contract(
        body).get('contract')
    return Contract(contract)


def contract_list(request, **kwargs):
    contracts = neutronclient(request).list_contracts(
        **kwargs).get('contracts')
    return [Contract(contract) for contract in contracts]


def contract_get(request, contract_id):
    contract = neutronclient(request).show_contract(
        contract_id).get('contract')
    return Contract(contract)


def contract_delete(request, contract_id):
    neutronclient(request).delete_contract(contract_id)


def contract_update(request, contract_id, **kwargs):
    body = {'contract': kwargs}
    contract = neutronclient(request).update_contract(
        contract_id, body).get('contract')
    return Contract(contract)


def policyrule_create(request, **kwargs):
    body = {'policy_rule': kwargs}
    policy_rule = neutronclient(request).create_policy_rule(
        body).get('policy_rule')
    return PolicyRule(policy_rule)


def policyrule_list(request, **kwargs):
    policyrules = neutronclient(request).list_policy_rules(
        **kwargs).get('policy_rules')
    return [PolicyRule(pr) for pr in policyrules]


def policyclassifier_create(request, **kwargs):
    body = {'policy_classifier': kwargs}
    classifier = neutronclient(request).create_policy_classifier(
        body).get('policy_classifier')
    return PolicyClassifier(classifier)


def policyclassifier_list(request, **kwargs):
    classifiers = neutronclient(request).list_policy_classifiers(
        **kwargs).get('policy_classifiers')
    return [PolicyClassifier(pc) for pc in classifiers]


def policyaction_create(request, **kwargs):
    body = {'policy_action': kwargs}
    action = neutronclient(request).create_policy_action(
        body).get('policy_action')
    return PolicyAction(action)


def policyaction_list(request, **kwargs):
    actions = neutronclient(request).list_policy_actions(
        **kwargs).get('policy_actions')
    return [PolicyAction(pa) for pa in actions]


def policyaction_delete(request, pa_id):
    neutronclient(request).delete_policy_action(pa_id)


def policyaction_get(request, pa_id):
    policyaction = neutronclient(request).show_policy_action(
        pa_id).get('policy_action')
    return PolicyAction(policyaction)


def policyrule_get(request, pr_id):
    policyrule = neutronclient(request).show_policy_rule(
        pr_id).get('policy_rule')
    return PolicyRule(policyrule)


def policyrule_delete(request, pr_id):
    neutronclient(request).delete_policy_rule(pr_id)


def policyrule_update(request, pr_id, **kwargs):
    return {}


def policyclassifier_get(request, pc_id):
    policyclassifier = neutronclient(request).show_policy_classifier(
        pc_id).get('policy_classifier')
    return PolicyClassifier(policyclassifier)


def policyclassifier_delete(request, pc_id):
    neutronclient(request).delete_policy_classifier(pc_id)


def policyclassifier_update(request, pc_id, **kwargs):
    return {}
