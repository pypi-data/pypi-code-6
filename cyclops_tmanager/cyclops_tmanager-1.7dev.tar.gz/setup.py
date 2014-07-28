'''

Created on Jul 28, 2014

@author:  Tea Kolevska
@contact: tea.kolevska@gmail.com
@organization: ICCLab, Zurich University of Applied Sciences
@summary: Setup script

 Copyright 2014 Zuercher Hochschule fuer Angewandte Wissenschaften
 All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"); you may
    not use this file except in compliance with the License. You may obtain
    a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.
    
'''

from distutils.core import setup

setup(name='cyclops_tmanager',
      version='1.7dev',
      description='Rating Charging and Billing engine for the cloud service providers',
      author='ICCLab, ZHAW Switzerland',
      packages=['cyclops_tmanager','cyclops_tmanager/logs','cyclops_tmanager/os_api'],
      #py_modules=['periodic_web','server_socket'],
      data_files=[('config',['cyclops_tmanager/config.conf'])],
       install_requires = [
        'django',
        'sympy',
        'httplib2',],
      
     )