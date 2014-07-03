#  specific language governing permissions and limitations
#  under the License.

import json
import os.path
from trac.attachment import Attachment, AttachmentModule
from trac.core import *

from trac.perm import PermissionError
from trac.resource import get_resource_name, Resource, resource_exists, ResourceNotFound
from trac.timeline.web_ui import TimelineModule
from trac.util import get_reporter_id
from trac.util.datefmt import to_datetime
from trac.util.text import to_unicode
from trac.util.translation import _

from bhlabs import util
from trac.config import ConfigurationError, Option
from trac.web.href import Href
from trac.web.chrome import add_stylesheet, add_script, add_script_data, ITemplateProvider
from trac.resource import Resource
from pkg_resources import get_distribution, resource_filename
from trac.web.api import HTTPBadRequest, IRequestFilter, IRequestHandler,\
ITemplateStreamFilter, RequestDone
from trac.web.chrome import Chrome
import unicodedata

#from bhdashboard.util import dummy_request

class InplaceAttachmentModule(Component):
    """Apache(TM) Bloodhound advanced attachment interface. Enhancements
    include multiple file uploads , drag and drop, and drop zones. The
    solution is powered by jQuery File Upload plugin
    ( https://github.com/blueimp/jQuery-File-Upload )
    """

    implements(IRequestFilter, IRequestHandler, ITemplateProvider)

    # IRequestFilter(Interface):

    def pre_process_request(self, req, handler):
        """ Intercept attachment upload request.
        """
        if handler is AttachmentModule(self.env) and\
           req.args.get('action') == 'inplace':
            return self
        return handler

    def post_process_request(self, req, template, data, content_type):
        """Activate jQuery File Upload form.
        """
        if data is not None:
            data.update({
                'bh_attach_advanced' : True,
                'max_size' : AttachmentModule(self.env).max_size
            })

            #if (data['zurb_attach_advanced']):
            #htdocsdir = req.href.chrome('jqfile') #self.get_htdocs_dirs()

            add_stylesheet(req, 'bhlabs/jquery/css/jquery.fileupload-ui.css')

            add_script(req, 'bhlabs/js/tmpl.js')
            add_script(req, 'bhlabs/js/load-image.js')
            add_script(req, 'bhlabs/js/canvas-to-blob.js')

            #add_script(req, self.jQuery_File_Upload_extras__href('jquery-1.8.2.js'))
            #add_script(req, 'jqfile/jquery/js/jquery-ui.min.js')

            add_script(req, 'bhlabs/jquery.fupload/js/jquery.iframe-transport.min.js')
            add_script(req, 'bhlabs/jquery.fupload/js/jquery.ui.widget.min.js')
            add_script(req, 'bhlabs/jquery.fupload/js/jquery.fileupload.min.js')
            add_script(req, 'bhlabs/jquery.fupload/js/jquery.fileupload-fp.min.js')
            add_script(req, 'bhlabs/jquery.fupload/js/jquery.fileupload-ui.min.js')

            add_stylesheet(req, 'bhlabs/css/jq.css')

        return template, data, content_type


    # IRequestHandler methods

    def match_request(self, req):
        """No need to match request.
        """

    def process_request(self, req):

        """Forward in-place attachment upload request to
        `trac.attachment.AttachmentModule` but return JSON suitable for
        jQuery File Upload processing in the client.

        Note: Only sequential file uploads supported.
        """
        self.log.debug("Processing upload request")
        parent_realm = req.args.get('realm')
        parent_id = req.args.get('id')

        #if not parent_realm or not parent_id:
        if not parent_realm:
            raise HTTPBadRequest(_('Bad request'))

        upload = req.args['attachment']
        if not hasattr(upload, 'filename') or not upload.filename:
            raise HTTPBadRequest(_('No file uploaded'))
        if hasattr(upload.file, 'fileno'):
            size = os.fstat(upload.file.fileno())[6]
        else:
            upload.file.seek(0, 2) # seek to end of file
            size = upload.file.tell()
            upload.file.seek(0)

        # We try to normalize the filename to unicode NFC if we can.
        # Files uploaded from OS X might be in NFD.
        filename = unicodedata.normalize('NFC', unicode(upload.filename, 'utf-8'))
        filename = filename.replace('\\', '/').replace(':', '/')
        filename = os.path.basename(filename)
        if not filename:
            raise HTTPBadRequest(_('No file uploaded'))

        # Default values sent back to the client on error
        result = {
            'author' : get_reporter_id(req, 'author'),
            'name' : filename,
            'size' : size,
            'delete_type' : '',
            'delete_url' : '',
            }


        parent = Resource(parent_realm, parent_id)
        attachment = Attachment(self.env, parent.child('attachment', None))

        fakereq = util.dummy_request(self.env, req.authname)
        fakereq.environ = req.environ

        fakereq.perm = req.perm
        fakereq.args = req.args

        try:
            data = AttachmentModule(self.env)._do_save(fakereq, attachment)
        except RequestDone:
            pass
        except (PermissionError, ResourceNotFound, TracError), exc:
            result['error'] = to_unicode(exc)
        else:
            if data is not None and data.get('is_replace'):
                # Invalid attachment submission
                result['error'] = fakereq.chrome['warnings'][-2]
            else:
                result = {
                    'author' : attachment.author,
                    'name' : attachment.filename,
                    'size' : attachment.size,
                    'url' : req.href.attachment(
                            parent_realm, parent_id, attachment.filename),
                    'download_url' : req.href('raw-attachment',
                            parent_realm, parent_id, attachment.filename),
                    'thumbnail_url' : req.href.chrome('common', 'file.png'),
                    'delete_url' : req.href.attachment(
                            parent_realm, parent_id, attachment.filename,
                            action="delete",
                            __FORM_TOKEN=req.args.get('__FORM_TOKEN')),
                    'delete_type' : 'POST',
                    'desc' : req.args.get('description', ''),
                }

        for header, value in req._inheaders:
            if header == 'accept':
                break
        else:
            value = ''
        if 'application/json' in value:
            ctype = 'application/json'
        else:
            ctype = 'text/plain'
        req.send(json.dumps([result]), ctype, 200)

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        yield 'bhlabs', resource_filename(__name__, 'htdocs')
    #def get_htdocs_dirs(self):
        #return [('jqfile', resource_filename('jqfile', 'htdocs'))]

    def get_templates_dirs(self):
        return []