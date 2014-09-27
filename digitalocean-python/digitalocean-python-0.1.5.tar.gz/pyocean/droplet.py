# encoding: utf-8

from .base import Resource, ResourceIterator
from .image import ImageIterator
from .action import ActionIterator
from .exceptions import *
import time
import re


class Droplet(Resource):
    """This class represents a Droplet.
    """

    def __init__(self, attrs={}):
        super(Droplet, self).__init__(attrs)

    def reboot(self):
        """Reboot current droplet.
        """
        return self.__do_action('reboot')

    def power_cycle(self):
        """Power off current droplet and then back on.
        """
        return self.__do_action('power_cycle')

    def shutdown(self):
        """Shutdown current droplet.
        """
        return self.__do_action('shutdown')

    def power_off(self):
        """Power off current droplet.
        """
        return self.__do_action('power_off')

    def power_on(self):
        """Power on current droplet.
        """
        return self.__do_action('power_on')

    def password_reset(self):
        """Password reset current droplet. New password will be emailed to you.
        """
        return self.__do_action('password_reset')

    def resize(self, size):
        """Resize current droplet.
        """
        return self.__do_action({'type': 'resize', 'size': size})

    def restore_image(self, image_id):
        """Rebuild an image using a backup image.
        """
        return self.__do_action({'type': 'restore', 'image': int(image_id)})

    def rebuild(self, image):
        """Rebuild droplet using the specified image.
        """
        if re.match('^\d+$', str(image).strip()):
            image = int(image)
        return self.__do_action({'type': 'rebuild', 'image': image})

    def rename(self, name):
        """Rename current droplet.
        """
        return self.__do_action({'type': 'rename', 'name': name})

    def change_kernel(self, kernel_id):
        """Change the kernel of current droplet.
        """
        return self.__do_action({'type': 'change_kernel', 'kernel': kernel_id})

    def enable_ipv6(self):
        """Enable IPv6 for current droplet.
        """
        return self.__do_action('enable_ipv6')

    def disable_backups(self):
        """Disable backups for current droplet.
        """
        return self.__do_action('disable_backups')

    def disable_backups(self):
        """Enable private networking for current droplet.
        """
        return self.__do_action('enable_private_networking')

    def create_snapshot(self, name):
        """Snapshot current droplet.
        """
        return self.__do_action({'type': 'snapshot', 'name': name})

    def get_snapshots(self):
        """Get the snapshots that have been created for this droplet.
        """
        return ImageIterator(self.id, 'snapshots')

    def get_available_kernels(self):
        """Get available kernels for this droplet.
        """
        return ImageIterator(self.id, 'kernels')

    def get_backups(self):
        """Retrieve any backups associated with this droplet.
        """
        return ImageIterator(self.id, 'backups')

    def get_actions(self):
        """Retrieve all actions that have been executed on this droplet.
        """
        return ActionIterator(self.id)

    def __do_action(self, params={}):
        """Perform action on droplet.
        """
        if not self.id:
            raise ValueError('Droplet not loaded.')
        if type(params) == str:
            params = {'type': params}
        path = "droplets/%s/actions" % self.id
        res = self.call_api(path, method='post', params=params)
        try:
            while res['action']['status'] == 'in-progress':
                time.sleep(1)
                res = self.call_api('%s/%s' % (path, res['action']['id']))
                if res['action']['status'] == 'errored':
                    raise DropletActionError("Action '%s' on dropled failed." % \
                                             res['action']['type'])
        except KeyError:
            raise InvalidResponse('Retrieved invalid response from DigitalOcean API.')
        else:
            return res['action']

    def __str__(self):
        return "<Droplet '%s' (%s)>" % (self.name, self.image['name'])


class DropletIterator(ResourceIterator):

    def __init__(self):
        super(DropletIterator, self).__init__()
