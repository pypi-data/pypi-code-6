"""Mail Backend for testing 
========================

Django offers a mail backend that is not easy to use as it does not create a
simple mbox to browse.

This EmailBackend offers the possibility to create a maildir that can be
browsed simply with::

  mutt -f /tmp/django.mbox

If you set::

  EMAIL_BACKEND = 'jmb.core.utils.mail_backends.MboxEmailBackend'
  EMAIL_FILE_PATH = '/tmp/' 

"""
import os
import datetime

from django.core.mail.backends.filebased import EmailBackend

class MboxEmailBackend(EmailBackend):
    def _get_filename(self):
        """Return a unique file name."""
        return os.path.join(self.file_path, 'django.mbox')

    def open(self):
        now = datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')
        if self.stream is None:
            self.stream = open(self._get_filename(), 'a')
            self.stream.write('From jumbo@thundersystems.it ' + now + "\n")
            return True
        return False
