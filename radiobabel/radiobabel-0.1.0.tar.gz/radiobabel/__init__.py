"""radiobabel

Interact with a number of online music services using a single unified API.
"""
# local imports
from .backends.soundcloud import SoundcloudClient

__version__ = '0.1.0'
__author__ = 'Paddy Carey <patrick@rehabstudio.com>'
__maintainer__ = 'Paddy Carey <patrick@rehabstudio.com>'

__all__ = ['SoundcloudClient']

