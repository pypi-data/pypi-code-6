# -*- coding: utf-8 -*-

# This software is released under the MIT License.
#
# Copyright (c) 2014 Cloudwatt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flameclient.flame import TemplateGenerator  # noqa


class Client(object):
    def __init__(self, api_version, **kwargs):

        username = kwargs.get('username')
        password = kwargs.get('password')
        tenant_name = kwargs.get('tenant_name')
        tenant_id = kwargs.get('tenant_id')
        auth_url = kwargs.get('auth_url')
        insecure = kwargs.get('insecure')
        nova = kwargs.get('nova')
        neutron = kwargs.get('neutron')
        cinder = kwargs.get('cinder')

        self.template_generator = TemplateGenerator(username, password,
                                                    tenant_name, auth_url,
                                                    insecure)
        if nova:
            self.template_generator.nova.set_client(nova)
        if neutron and tenant_id:
            self.template_generator.neutron.set_client(neutron)
            self.template_generator.neutron.set_project_id(tenant_id)
        if cinder:
            self.template_generator.cinder.set_client(cinder)


    def generate_template(self, include_instances, include_volumes,
                          include_data_file):
        self.template_generator.extract_vm_details(
            exclude_servers=not include_instances,
            exclude_volumes=not include_volumes,
            generate_data=include_data_file)
        self.template_generator.extract_data()
        flame_stream = self.template_generator.heat_template()
        data_stream = self.template_generator.stack_data_template()

        return (flame_stream,  data_stream)
