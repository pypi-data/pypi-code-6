# encoding: utf-8

from .base import Resource, ResourceIterator
from .exceptions import InvalidResponse, ImageActionError
import time


class Image(Resource):
    """This class represents an Image.
    """
    
    def __init__(self, attrs={}):
        super(Image, self).__init__(attrs)

    def rename(self, name):
        """Rename current image.
        """
        data = self.call_api(self._resource, method='post', data={'name': name})
        try:
            self._attrs = data['image']
        except KeyError:
            raise InvalidResponse('Retrieved invalid response from DigitalOcean API.')
        return self

    def transfer_to(self, region_name):
        """Transfer this image to another region.
        """
        data = {
            'type': 'transfer',
            'region': region_name
        }
        path = 'images/%s/actions' % str(self.id)
        res = self.call_api(path, method='post', data=data)
        try:
            while res['action']['status'] == 'in-progress':
                time.sleep(1)
                res = self.call_api('%s/%s' % (path, res['action']['id']))
                if res['action']['status'] == 'errored':
                    raise ImageActionError("Action '%s' on image failed." % \
                                           res['action']['type'])
        except KeyError:
            raise InvalidResponse('Retrieved invalid response from DigitalOcean API.')
        else:
            return res['action']

    def __str__(self):
        return "<Image '%s' (%s)>" % \
                (self._attrs.get('slug') or self._attrs.get('id'), self.name)


class ImageIterator(ResourceIterator):
    """This class represents collection of Images.
    """

    def __init__(self, droplet_id=None, image_type=None):
        super(ImageIterator, self).__init__()
        if droplet_id:
            self._resource = 'droplets/%s/%s' % (droplet_id, image_type)
