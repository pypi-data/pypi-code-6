from __future__ import unicode_literals

import unittest

from orm.api import Api

from .utils import login, random_ascii, fake_file


class FileHandlerTests(unittest.TestCase):
    def setUp(self):
        login(self)
        uri = 'http://microsoft.com/templates/Windows98-ServicePack-2.tgz'
        sha256 = '76a71abd164ce3b149c84d52a4bd313e74cae75539bd5c10628b784792ba039c'
        name = 'RandomTemplate-%s' % random_ascii(10)
        self.template = self.api.templates.create(name=name, image_uri=uri,
                type='debian', image_sha256=sha256, is_active=True,
                node_archs=["i686"])
    
    def test_file_handler(self):
        template = self.template
        foo_file, content = fake_file('Windows98-ServicePack-2.tgz')
        template.upload_image(foo_file)
        template.retrieve()
        template.image.retrieve()
        template.image.validate_sha256()
        self.assertEqual(content, template.image.content)
        template.delete()
        template.image.retrieve(save_to='/dev/shm/')
        with open(template.image.file.name, 'ru') as f:
            self.assertEqual(content, f.read())
        template.image.validate_sha256()
        async = template.image.retrieve(async=True)
        async.get()
        template.image.sha256 += '1'
        self.assertRaises(ValueError, template.image.validate_sha256)
    
    def test_save_after_upload_file(self):
        # create sliver
        rand = random_ascii(10)
        self.group = self.api.groups.create(name='Group-%s' % rand)
        node = self.api.nodes.create(name='Node-%s' % rand, group=self.group,
                        arch='i686', mgmt_net=dict(backend='tinc'))
        slice = self.api.slices.create(name='Slice-%s' % rand,
                group=self.group, template=self.template)
        ifaces =[dict(name='priv', type='private', nr='0')]
        sliver = node.slivers.create(slice=slice, interfaces=ifaces)
        
        # upload exp_data
        foo_file, content = fake_file('test_exp_data.tgz')
        sliver.upload_exp_data(foo_file)
        sliver.retrieve()
        
        # Check that file can be retrieved
        async = sliver.exp_data.retrieve(async=True)
        async.get()
        
        # Update sliver via PUT request (#494)
        sliver.set_state = "start"
        sliver.save()
        sliver.retrieve()
        
        # Check that file can be retrieved
        async = sliver.exp_data.retrieve(async=True)
        async.get()
