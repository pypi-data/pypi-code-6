import io
import sys
if sys.version[0] == "2":
    from urllib2 import build_opener,ProxyHandler,HTTPHandler,HTTPSHandler
    from httplib import HTTPConnection
    from StringIO import StringIO
else:
    from urllib.request import build_opener,ProxyHandler,HTTPHandler,HTTPSHandler
    from http.client import HTTPConnection
    from io import StringIO
    global unicode
    unicode = str

import mimetypes
import hashlib
import datetime
import os
import time
from xml.dom.minidom import parseString # lxml2

def pack_text_node(base_node):
    txt = ""
    for node in base_node.childNodes:
        txt += node.nodeValue
    return txt


class FilePath(object):
    def __init__(self,path):
        self.path = path

class MultiRead(object):
    """ This class will present a read()able object to
    the httplib send() method. This object represents
    an HTTP multiple part/form data collection. Each item
    in the collection is either :

    * key value parts
    * files

    This object has the property of allowing httplib to
    work with a read block size. That in turns allows
    us to send files over http wich are bigger than
    the RAM.
    """

    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$' # BUG That's a hack, I can't send myself to mediafire :-)
    CRLF = '\r\n'

    def __init__(self,logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = DevNullLogger()
        self.to_read = []
        self.current_file_dnx = 0
        self.current_file = None
        self._size = 0

    def add_field(self, key, value):

        L = []
        # L.append('--' + self.BOUNDARY)
        # L.append('Content-Disposition: form-data; name="{}"'.format(key))
        # L.append('')
        # L.append("{}".format(value))

        L.append(u'--' + self.BOUNDARY)
        L.append(u'Content-Disposition: form-data; name="{}"'.format(key))
        L.append(u'')
        L.append(u"{}".format(value))
        data = self.CRLF.join(L) + self.CRLF
        data = bytearray(data, 'utf-8')
        self.to_read.append(data)
        self._size += len(data)


    def add_file_part(self,filepath):

        # Extract the filename... FIXME May have encoding issues
        filename = os.path.split(filepath)[-1]

        # CRLF must be set very accurately to respect http://tools.ietf.org/html/rfc1867
        s = '--' + self.BOUNDARY + self.CRLF
        s += 'Content-Disposition: form-data; name="%s"; filename="%s"' % ('uploaded_file', filename) + self.CRLF
        s += ('Content-Type: %s' % mimetypes.guess_type(filepath)[0] or 'application/octet-stream') + self.CRLF
        s += self.CRLF

        s = bytearray(s, 'utf-8')
        self.to_read.append(s)
        self._size += len(s)

        self.to_read.append(FilePath(filepath))
        s = os.path.getsize(filepath)
        self._size += s

        self.logger.debug(u"Appended {} with {} bytes".format(filepath,s))


    def close_parts(self):
        data = self.CRLF + '--' + self.BOUNDARY + '--' + self.CRLF
        data += self.CRLF
        data = bytearray(data, 'utf-8')
        self.to_read.append(data)
        self._size += len(data)

    def content_type(self):
        return 'multipart/form-data; boundary={}'.format(self.BOUNDARY)

    def total_size(self):
        return self._size

    def open(self):
        self.current_file_ndx = 0
        self.current_file = None
        self._pick_next_file()

    def close(self):
        if self.current_file:
            self.current_file.close()
            self.current_file = None

        self.current_file_ndx = len(self.to_read)

    def _pick_next_file(self):


        if self.current_file_ndx >= len(self.to_read):
            self.current_file = None
            self.logger.debug("Picking next item to upload : reached the end")

        else:
            self.logger.debug("Picking next item to upload : opening one more")
            to_send = self.to_read[self.current_file_ndx]

            if type(to_send) == str or type(to_send) == unicode:
                if sys.version[0] == "2":
                    self.current_file = io.BytesIO(bytearray(to_send.encode('utf-8')))
                else:
                    self.current_file = io.BytesIO(bytes(to_send,'utf-8'))

            # elif type(to_send) == unicode:
            #     self.current_file = StringIO(to_send.encode('utf-8'))
            elif type(to_send) == FilePath:
                self.current_file = open( to_send.path, "rb")
            elif type(to_send) == bytearray:
                self.current_file = io.BytesIO(to_send)
            else:
                raise Exception("Internal error type={}".format(type(to_send)))

            self.current_file_ndx += 1

        return self.current_file


    def read(self,size=None):
        if not size:
            return self._read(size=self.total_size())
        else:
            return self._read(size)

    def _read(self,size=8192):

        if not self.current_file or size == 0:
            return []

        else:
            r = self.current_file.read(size)
            self.logger.debug("Read {}/{} bytes".format(len(r),self.total_size()))

            if not r: # EOF
                self.current_file.close()
                if self._pick_next_file():
                    return self._read(size)
                else:
                    return ''

            elif 0 < len(r) <= size:
                return r

            else:
                raise Exception("Something unbelievable occured : len(r)={}, size={}".format(len(r),size))



class MediaFireFolder(object):
    """ Represents a folder located at MediaFire
    """

    def __init__(self,token,filexml=None):
        self._session_token = token

        if filexml:
            self._load_info(filexml)

    def __repr__(self):
        return "FOLDER: {} {}".format(self.name, self.folder_key)

    def setup(self,name,folder_key):
        self.name = name
        self.folder_key = folder_key

    def _load_info(self,f):
        """ Parse an XML fragment to get folder's informations
        """

        self.name = pack_text_node(f.getElementsByTagName("name")[0])
        self.folder_key = pack_text_node(f.getElementsByTagName("folderkey")[0])





class MediaFireFile(object):
    """ Represents a file located at MediaFire
    """

    def __init__(self,token,filexml):
        self._session_token = token
        self._load_info(filexml)

    def __repr__(self):
        return u"FILE: {} {} bytes {} {}".format(self.filename, self.size, self.creation_date, self.quick_key)

    def _load_info(self,f):
        """ Parse an XML fragment to get file's informations
        """

        self.filename = pack_text_node(f.getElementsByTagName("filename")[0])
        size = pack_text_node(f.getElementsByTagName("size")[0])
        self.size = int(size)

        self.quick_key = pack_text_node(f.getElementsByTagName("quickkey")[0])

        creation_date_text = pack_text_node(f.getElementsByTagName("created")[0])
        self.creation_date = datetime.datetime.strptime(creation_date_text,'%Y-%m-%d %H:%M:%S')


class DevNullLogger(object):
    def __init__(self):
        pass

    def debug(self,p):
        pass

    def error(self,p):
        pass

    def info(self,p):
        pass

    def exception(self,p):
        pass


class MediaFireSession(object):
    """ Represents a session with MediaFire.
    This is the main class you'll use to interact with MediaFire.
    It supports the very basic subset of the MediaFire API (download/upload, read/create folders).
    Feel free to contribute patches.
    """


    MEDIAFIRE_DOMAIN = 'www.mediafire.com'

    def _call(self,selector,https=True):
        protocol = ""
        if https:
            protocol = "s"

        url = "http{}://{}/api{}".format(protocol,self.MEDIAFIRE_DOMAIN,selector)
        self.logger.debug("Calling {}".format(url))
        f = self.urlopener.open(url)
        res = f.read()
        return res



    def __init__(self,email,password,appid,sessionkey,proxy_url=None,proxy_port=None,logger=None):
        """ Initialize a session to MediaFire
        email, password, appid and sessionkey is the authorization tuple for MediaFire.
        proxy_url and proxy_port are optional. Since some MediaFire operations
        require https, we expect http and https proxy to be located at the
        same address and port.
        """

        if logger:
            self.logger = logger
        else:
            self.logger = DevNullLogger()

        self.proxy_url = proxy_url
        self.proxy_port = proxy_port

        if proxy_url:
            proxy = "{}:{}".format(proxy_url,proxy_port)
            self.logger.debug("Using a proxy : {}".format(proxy))

            self.urlopener = build_opener(
                ProxyHandler({'https': proxy,
                              'http' : proxy}))
        else:
            self.urlopener = build_opener(
                HTTPHandler(),
                HTTPSHandler())

        h = hashlib.sha1()
        h.update(u"{}{}{}{}".format(email,password,appid,sessionkey).encode('utf-8'))

        try:
            tokenxml = self._call("/user/get_session_token.php?email={}&password={}&application_id={}&signature={}&version=1".format(email,password,appid,h.hexdigest()))

            dom = parseString(tokenxml)
            self._session_token = dom.getElementsByTagName('session_token')[0].firstChild.toxml()

            self.logger.debug("Session opened!")
        except Exception as ex:
            self.logger.error("Unable to open a session on mediafire")
            self.logger.exception(ex)
            self._session_token = None
            raise ex



    def load_folder(self,mfdir=None):
        """ Load a directory represented by a MediaFireFolder without recursion.
        If no folder is given, then the root folder is loaded.
        Returns a sequence of MediaFireFile and MediaFireFolder
        """
        assert mfdir is None or type(mfdir) == MediaFireFolder

        folder_key = ""
        if mfdir is not None:
            folder_key = "&folder_key=" + mfdir.folder_key

        content = self._call("/folder/get_content.php?session_token={}&content_type=files{}".format(self._session_token,folder_key))
        allfiles = []
        for f in parseString(content).getElementsByTagName("file"):
            allfiles.append(MediaFireFile(self._session_token,f))

        content = self._call("/folder/get_content.php?session_token={}&content_type=folders{}".format(self._session_token,folder_key))
        for f in parseString(content).getElementsByTagName("folder"):
            # print f.toprettyxml()
            allfiles.append(MediaFireFolder(self._session_token,f))

        return allfiles



    def create_folder(self,foldername):
        """ Create a folder with the given name.
        Returns a MediaFireFolder representing the created folder.
        """

        content = self._call("/folder/create.php?session_token={}&foldername={}".format(self._session_token,foldername))

        folder_key = pack_text_node(parseString(content).getElementsByTagName("folder_key")[0])

        folder = MediaFireFolder(self._session_token)
        folder.setup(foldername,folder_key)
        return folder


    def upload(self,mediafire_folder,outfile):
        """ Upload the file of path outfile into the given folder.
        If the give folder is None, then we upload to the root directory.
        The name of the file in MediaFire is the filename without the path.
        This will block until the file is successfuly uploaded.
        """

        assert mediafire_folder is None or type(mediafire_folder) == MediaFireFolder

        in_file = open(outfile,'rb')

        upload_key = ""
        if mediafire_folder:
            upload_key = "&uploadkey={}".format(mediafire_folder.folder_key)

        self.logger.debug(u"Uploading {} as {}".format(outfile,os.path.split(outfile)[-1]))

        res = self._post_multipart(self.MEDIAFIRE_DOMAIN + ":80",
                                   "/api/upload/upload.php?session_token={}{}".format(self._session_token,upload_key),
                                   outfile)
        in_file.close()

        upload_key = pack_text_node(parseString(res).getElementsByTagName("key")[0])

        status = None
        while status != '99':
            if status is not None:
                time.sleep(5)

            res = self._call("/upload/poll_upload.php?session_token={}&key={}".format(self._session_token,upload_key),https=False)
            status = pack_text_node(parseString(res).getElementsByTagName("status")[0])

    def delete(self, f):
        """ Deletes the given MediaFireFile
        """

        resp = self._call("/file/delete.php?session_token={}&quick_key={}".format(self._session_token,f.quick_key))


    def download(self, f, outfile):
        """ Download the given MediaFireFile into outfile.
        We check that the downloaded file size equals he file size reported
        by Mediafire.
        """

        resp = self._call("/file/get_links.php?session_token={}&quick_key={}&link_type=direct_download".format(self._session_token,f.quick_key))

        download_url = pack_text_node(parseString(resp).getElementsByTagName("direct_download")[0])

        out = open(outfile,'wb')
        datasource = self.urlopener.open(download_url)
        while True:
            d = datasource.read(8192)
            # self.logger.debug("Downloaded {} bytes".format(len(d)))
            if not d:
                break
            else:
                out.write( d)
                out.flush()
        out.close()

        dlsize = os.path.getsize(outfile)

        if f.size != dlsize:
            raise Exception("Downloaded file size is {} bytes and DOES NOT correspond to mediafire ({})".format(dlsize,f.size))


    def _post_multipart(self,host, selector, filepath):
        """
        Post a file with an http host as multipart/form-data.
        Return the server's response page.
        """

        # That's a bit of overkill but well, it works...
        mr = MultiRead(self.logger)
        mr.add_file_part(filepath)
        mr.close_parts()

        h = None
        if self.proxy_url:
            h = HTTPConnection(self.proxy_url, self.proxy_port)
            h.putrequest('POST', "http://" + host + selector)
        else:
            h = HTTPConnection(host)
            h.putrequest('POST', selector)

        h.putheader('content-type', mr.content_type())
        h.putheader('content-length', str(mr.total_size()))
        h.putheader('x-filesize', str(mr.total_size()))
        h.endheaders()

        mr.open()
        h.send(mr)
        mr.close()

        t = h.getresponse().read()
        return t
