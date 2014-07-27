# pylint: disable=W0105, W0403
"""
This module provides an API for managing virtual representations of objects
that are being carved from a disk image file. Currently the two types of
objects defined are files and ASCII strings.
"""
# Standard library imports
import errno
import md5
import operator
import os
import re
import sys
import warnings
import zipfile

# LaZy_NT module imports
import config

# Optional 3rd party imports.
# If not installed, the respective metadata functionality is safely disabled.
module_status = {}
"""
(dict): Tracks whether optional dependency modules have been imported.
Values are boolean, and the keys represent the dependency package names.
"""
try:
    from PIL import Image as PILimage
    from PIL.ExifTags import TAGS as _TAGS
    module_status['pillow (or PIL)'] = True
except ImportError:
    warnings.warn(
        "\nOptional module 'Pillow' (or 'PIL') is not installed.\n"
        "Exif metadata will not be available for .jpg/.tiff files.")
    module_status['pillow (or PIL)'] = False
try:
    import pyPdf
    from pyPdf import PdfFileReader
    module_status['pyPdf'] = True
except ImportError:
    warnings.warn(
        "\nOptional module 'pyPdf' is not installed.\n"
        "Metadata will not be available for .pdf files.")
    module_status['pyPdf'] = False
module_status['hachoir'] = True
try:
    from hachoir_core.cmd_line import unicodeFilename
    module_status['hachoir-core'] = True
except ImportError:
    module_status['hachoir-core'] = False
    module_status['hachoir'] = False
try:
    from hachoir_parser import createParser
    module_status['hachoir-parser'] = True
except ImportError:
    module_status['hachoir-parser'] = False
    module_status['hachoir'] = False
try:
    from hachoir_metadata import extractMetadata
    module_status['hachoir-metadata'] = True
except ImportError:
    module_status['hachoir-metadata'] = False
    module_status['hachoir'] = False
if not module_status['hachoir']:
    warnings.warn(
        "\nOptional module(s) 'hachoir-core', 'hachoir-parser' and/or"
        "'hachoir-metadata' are not installed.\nMetadata will not be "
        "available for .bmp/.gif/.png/.doc/.xls/.zip files.")
try:
    import openxmllib
    module_status['openxmllib'] = True
except ImportError:
    warnings.warn(
        "\nOptional module 'openxmllib' is not installed.\n"
        "Metadata will not be available for .docx/.xlsx files.")
    module_status['openxmllib'] = False

def validate_output_dir(path, val_empty=True):
    """ Ensure that a directory exists, creating it if necessary, and
      (optionally) ensure that it's empty.

    ### Args:
    * **val_empty (bool):** Indicates that the directory must be
    empty to return True.

    ### Returns:
    * **True** if directory exists or was created and, if requested, is
    empty.
    * **False** if directory cannot be created or is not empty when
    requested.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    if val_empty:
        if os.listdir(path):
            return False
    return True

def write_histogram(image_name):
    """
    Write a histogram summary at the bottom of each ASCII string log file.
    Clears the histogram data after writing, to prepare for processing another
    image file.

    ### Args:
    * **image_name (str):** The name of the disk image file associated with
    the current histogram data.
    """
    for key in config.histogram:
        filename = key + 's.txt'
        absname = os.path.join(config.options['outdir'], filename)
        if os.path.isfile(absname):
            temp_file = open(absname, 'a+')
            temp_file.write("\nHistogram Summary for '" + image_name + "':\n")
            temp_file.write('-' * (25 + len(image_name)) + '\n')
            # Per PEP 265 this is the best way to sort a dict on it's values
            tuples = sorted(config.histogram[key].iteritems(),
                            key=operator.itemgetter(1),
                            reverse=True)
            for item in tuples:
                temp_file.write("{0:<80}".format(item[0]) + str(item[1]) + '\n')
            temp_file.write('=' * 100 + '\n')
            temp_file.close()
        # Clear this key
        config.histogram[key] = {}

class CarveObject(object):
    """
    A base class representation of a data object that should be carved from a
    disk image file.
    """
    def __init__(self, subclass, image_id, image_name, id_, type_, offset,
                 compressed):
        """Instantiate a representation of the data being carved."""
        self.subclass = subclass
        """
        (str): Identify the subclass of this `LaZy_NT.carve_object.CarveObject`
        """
        self.image_id = image_id
        """
        (int): Numeric identifier for the disk image file within which this
        `LaZy_NT.carve_object.CarveObject` was identified.
        """
        self.image_name = image_name
        """
        (str): Fully qualified path to the disk image file within which this
        `LaZy_NT.carve_object.CarveObject` was identified.
        """
        self.id = id_
        """
        (int): A unique ID number assigned to this
        `LaZy_NT.carve_object.CarveObject`.
        """
        self.type = type_
        """
        (str): A specific description of this object type, ie: 'bmp' or 'email'.
        """
        self.offset = offset
        """
        (str): The offset of a chunk of the disk image file within which this
        `LaZy_NT.carve_object.CarveObject` was found. Formatted as 10 digits
        of hexadecimal with leading zeroes, i.e. '0x0000123456'. A '+' sign
        appended to the string indicates that the
        `LaZy_NT.carve_object.CarveObject` was found in the decompressed
        stream, with the orginal compressed data stored near this offset.
        """
        self.compressed = compressed
        """
        (bool): Indicate whether the `LaZy_NT.carve_object.CarveObject`
        was stored compressed within the disk image file.
        """
        self.status = "Processing"
        """
        (str): Indicate the processing status of the
        `LaZy_NT.carve_object.CarveObject`, one of:

        * **"Processing"** - The `LaZy_NT.carve_object.CarveObject` is still
        open and receiving data from the disk image processor.
        * **"Finished"** - The `LaZy_NT.carve_object.CarveObject` is finalized
        and has been written to disk.
        * **"Deleted"** - The `LaZy_NT.carve_object.CarveObject` was finalized
        and written to disk, but later found to be invalid and deleted.
        """
        self.data = ""
        """
        (str): Contains the stream of bytes, extracted from the disk image
        file, that make up this `LaZy_NT.carve_object.CarveObject`.
        """

class vFile(CarveObject):
    """
    Represent the state of a file that is in the process of being carved.
    """
    def __init__(self, image_id, image_name, id_, type_, offset,
                 max_bytes=5242880, stop_sig="", compressed=False):
        """Instantiate a virtual file representation."""
        offset = "{0:#010x}".format(offset)
        if (type_[-1] == '_' or type_ in ['_deepcarve_raw', '_ASCII_raw']):
            offset += '+'
        CarveObject.__init__(self, 'vFile', image_id, image_name, id_, type_,
                             offset, compressed)
        self.stop_sig = stop_sig
        """
        (str): The footer bytes that indicate the end of a file of this type
        if discovered in the input to `LaZy_NT.carve_object.vFile.in_bytes`.
        """
        self.max_bytes = max_bytes
        """
        (int): The maximum number of data bytes to read into the
        `LaZy_NT.carve_object.vFile` before finalizing it.
        """
        self.meta = {}
        """
        (dict): Contains all of the metadata, in 'Attribute : Value' pairs,
        that could be extracted from this file after it was carved to disk.
        """
        self.ASCII_flag = False
        """
        (bool): Indicates whether or not this `LaZy_NT.carve_object.vFile`s
        `LaZy_NT.carve_object.vFile.type` is 'ASCII-like',
        i.e. containing predominantly uncompressed ASCII text.
        """
        if (self.type in ['bat', 'c', 'html', 'py', 'rtf', 'sh', 'txt', 'xml',
                          'doc', '_ASCII_raw'] or
                self.type[:-1] in ['bat', 'c', 'html', 'py', 'rtf', 'sh',
                                   'txt', 'xml', 'doc']):
            self.ASCII_flag = True

    def in_bytes(self, byte_stream):
        """
        Stream data bytes into a `LaZy_NT.carve_object.vFile` while checking
        for `LaZy_NT.carve_object.vFile.stop_sig` and
        `LaZy_NT.carve_object.vFile.max_bytes`.

        ### Args:
        * **byte_stream (str):** The stream of bytes to be appended to this
        `LaZy_NT.carve_object.vFile`'s `LaZy_NT.carve_object.vFile.data`
        attribute.
        """
        # Special handling for raw ASCII files
        if self.type == '_ASCII_raw':
            match = re.search(r'[^\x09\x0D\x0A\x20-\x7E]', byte_stream)
            if match:
                self.data = "".join([self.data,
                                     byte_stream[:match.start()]])
                self.to_file()
            else:
                self.data = "".join([self.data, byte_stream])
            return
        # All others check stop for signature
        if not self.stop_sig == "":
            stop_sig_test = byte_stream.find(self.stop_sig)
        else:
            stop_sig_test = -1
        # If no stop signature detected, check for max length
        if stop_sig_test == -1:
            if len(self.data) + len(byte_stream) <= self.max_bytes:
                self.data = "".join([self.data, byte_stream])
            # If max length reached, finish the vFile
            else:
                remaining = self.max_bytes - len(self.data)
                self.data = "".join([self.data, byte_stream[0:remaining]])
                self.to_file()
        # If stop signature was detected, finalize the vFile
        else:
            self.data = "".join(
                [self.data,
                 byte_stream[0:stop_sig_test + len(self.stop_sig) + 1]])
            # Special handling for .zip-based files
            if (self.type in ['docx', 'zip'] or
                    self.type[:-1] in ['docx', 'zip']):
                self.data = "".join([
                    self.data,
                    byte_stream[stop_sig_test + len(self.stop_sig) + 1:
                                stop_sig_test + len(self.stop_sig) + 15]])
            self.to_file()
        return

    def to_file(self):
        """
        Finalize a `LaZy_NT.carve_object.vFile` and write its data content
        to disk.
        """
        self.__analyze_subheaders()
        path = os.path.join(config.options['outdir'], self.type)
        if not config.options['no_carve']:
            if not validate_output_dir(path, val_empty=False):
                raise IOError("Couldn't create output directory: %s" % path)
        filename = (str(self.image_id) + str(self.id).zfill(5) +
                    "." + self.type)
        # Special handling for 'deep-carved' file types
        if self.type[-1] == '_':
            filename = filename[:-1]
        if self.type == '_deepcarve_raw' or self.type == '_ASCII_raw':
            filename = str(self.image_id) + str(self.id).zfill(5) + ".txt"
        absname = os.path.join(path, filename)
        # Strip null bytes from the end of files
        if not self.type in ['bmp', 'docx', 'xlsx', 'pptx', 'zip']:
            while self.data[-1:] == chr(0x00):
                self.data = self.data[0:-1]
        # Special handling for PDF stop signatures
        if self.type == 'pdf' and not self.data.find('%EOF') == -1:
            while not (self.data[-4:] == '%EOF' or
                       self.data[-5:] == '%EOF' + chr(0x0A) or
                       self.data[-5:] == '%EOF' + chr(0x0D) or
                       self.data[-6:] == '%EOF' + chr(0x0D) + chr(0x0A)):
                self.data = self.data[0:-4]
        # Write the vFile data to disk
        if not config.options['no_carve']:
            temp_file = open(absname, 'w+b')
            temp_file.write(self.data)
            temp_file.close()
            # Perform validation if requested
            if config.options['val_files']:
                self.__validate_carved_file(absname)
            # Attempt to extract metadata
            if config.options['metadata'] and not self.status == 'Deleted':
                self.__get_meta(absname)
        self.__write_audits(filename, absname)

    def __analyze_subheaders(self):
        """
        Analyze the `LaZy_NT.carve_object.vFile.data` content for subheader
        information. Modify the `LaZy_NT.carve_object.CarveObject.type`
        attribute to disambiguate between file types with a common signature
        header, i.e. MS Office documents.
        """
        # Differentiate .xls and .ppt from .doc
        if self.type == 'doc' or self.type[:-1] == 'doc':
            if (self.data[512:520] == chr(0x09) + chr(0x08) + chr(0x10) +
                    chr(0x00) + chr(0x00) + chr(0x06) + chr(0x05) + chr(0x00)):
                self.type = 'xls'
            elif (self.data[512:515] == chr(0xA0) + chr(0x46) + chr(0x1D) +
                      chr(0xF0)):
                self.type = 'ppt'
            elif (self.data[512:515] == chr(0x0F) + chr(0x00) + chr(0xE8) +
                      chr(0x03)):
                self.type = 'ppt'
            elif (self.data[512:515] == chr(0x00) + chr(0x6E) + chr(0x1E) +
                      chr(0xF0)):
                self.type = 'ppt'
            elif (self.data[512:516] == chr(0xFD) + chr(0xFF) + chr(0xFF) +
                  chr(0xFF)):
                if self.data[518:520] == chr(0x00) + chr(0x00):
                    if not self.data[516:518] == chr(0x20) + chr(0x00):
                        self.type = 'ppt'
                    else:
                        self.type = 'xls'
                if (self.data[517:518] == chr(0x00) or
                        self.data[517:518] == chr(0x02)):
                    self.type = 'xls'
        # Differentiate .xlsx and .pptx from .docx
        if self.type == 'docx' or self.type[:-1] == 'docx':
            if not self.data.find("word/document.xml") == -1:
                pass
            elif not self.data.find("xl/worksheets/sheet1.xml") == -1:
                self.type = 'xlsx'
            elif not self.data.find("ppt/slideMasters/slideMaster1.xml") == -1:
                self.type = 'pptx'

    def __validate_carved_file(self, filename):
        """
        Validate that a carved file can be opened normally and delete
        it if found to be unreadable.

        ### Args:
        * **filename (str):** Fully qualified path to the carved file
        on disk.
        """
        # pylint: disable=W0702
        delete = False
        # Test zip-like files, including Office 2007+
        if (self.type in ['zip', 'docx', 'xlsx', 'pptx'] or
                self.type[:-1] in ['zip', 'docx', 'xlsx', 'pptx']):
            try:
                with zipfile.ZipFile(filename, 'r') as ziptest:
                    ziptest.infolist()
            except:
                delete = True
        # Test image files
        if (self.type in ['bmp', 'gif', 'jpg', 'png', 'tif'] or
                self.type[:-1] in ['bmp', 'gif', 'jpg', 'png', 'tif']):
            if module_status['pillow (or PIL)']:
                try:
                    img = PILimage.open(filename)
                except:
                    delete = True
        # Test PDF files
        if ((self.type == 'pdf' or self.type[:-1] == 'pdf') and
                module_status['pyPdf']):
            try:
                pdf_file = PdfFileReader(file(filename, 'rb'))
            except:
                delete = True
        if delete:
            while os.path.isfile(filename):
                try:
                    os.remove(filename)
                    self.data = ""
                    self.status = "Deleted"
                except:
                    sys.exc_clear()
                    print ".",

    def __get_meta(self, filename):
        """
        Process a carved file on disk to extract metadata.

        ### Args:
        * **filename (str):** Fully qualified path to the carved file
        on disk.
        """
        # pylint: disable=W0702
        # Parse Exif data from .jpg and .tif images
        if ((self.type in ['jpg', 'tif'] or
             self.type[:-1] in ['jpg', 'tif']) and
                module_status['pillow (or PIL)']):
            try:
                img = PILimage.open(filename)
                if hasattr(img, '_getexif'):
                    exifinfo = img._getexif()
                else:
                    exifinfo = None
                if exifinfo != None:
                    for tag, value in exifinfo.items():
                        decoded = _TAGS.get(tag, tag)
                        self.meta[decoded] = value
            except:
                sys.exc_clear()
        # Parse PDF metadata
        if ((self.type == 'pdf' or self.type[:-1] == 'pdf') and
                module_status['pyPdf']):
            try:
                pdf_file = PdfFileReader(file(filename, 'rb'))
                pdf_info = pdf_file.getDocumentInfo()
                for tag, value in pdf_info.items():
                    self.meta[tag] = value.encode('ascii', 'ignore')
            except:
                sys.exc_clear()
        # Parse .doc, .xls, .ppt (Office 97 - 2003) metadata
        # Parse .jpg, .tif, .bmp, .gif, .png, .zip metadata
        if (self.type in ['bmp', 'doc', 'gif', 'jpg', 'ppt', 'tif',
                          'xls', 'zip'] or
                self.type[:-1] in ['bmp', 'doc', 'gif', 'jpg', 'ppt', 'tif',
                                   'xls', 'zip']) and module_status['hachoir']:
            try:
                filename, origname = unicodeFilename(filename), filename
                parser = createParser(filename, origname)
                metadata = extractMetadata(parser)
                metatext = metadata.exportPlaintext()
                for item in metatext:
                    item = item.encode('ascii', 'ignore')
                    itemlist = item.split(': ', 1)
                    if not itemlist == ['Metadata:']:
                        tag = itemlist[0][2:]
                        value = itemlist[1]
                        self.meta[tag] = value
            except:
                sys.exc_clear()
        # Parse .docx, .xlsx, .pptx (Office 2007 - present) metadata
        if ((self.type in ['docx', 'pptx', 'xlsx'] or
             self.type[:-1] in ['docx', 'pptx', 'xlsx']) and
                module_status['openxmllib']):
            try:
                doc = openxmllib.openXmlDocument(path=filename)
                self.meta = doc.allProperties
            except:
                sys.exc_clear()

    def __write_audits(self, filename, absname):
        """
        Write summary information and metadata to the audit logs and
        sqlite database, as appropriate.

        ### Args:
        * **filename (str):** Base name of the file being finalized.
        * **absname (str):** Fully qualified path to the carved file
        on disk.
        """
        log_md5 = md5.new(self.data).hexdigest()
        # First handle the supplemental "raw" logs
        if (self.type == '_deepcarve_raw' and config.options['keep_raw'] and
                config.deep_raw_log is not None):
            config.deep_raw_log.write(
                '{:<15}'.format(filename) + absname + '\n' +
                ' ' * 15 + '{:<20}'.format('Found in Image') + ' = ' +
                self.image_name + '\n' +
                ' ' * 15 + '{:<20}'.format('Start Offset') + ' = ' +
                self.offset + '\n' +
                ' ' * 15 + '{:<20}'.format('File Length') + ' = ' +
                str(len(self.data)) + ' bytes' + '\n' +
                ' ' * 15 + '{:<20}'.format('Was Compressed?') + ' = ' +
                str(self.compressed) + '\n' +
                ' ' * 15 + '{:<20}'.format('md5 Digest') + ' = ' +
                log_md5 + '\n\n')
        elif (self.type == '_ASCII_raw' and config.options['keep_raw'] and
              config.ascii_raw_log is not None):
            config.ascii_raw_log.write(
                '{:<15}'.format(filename) + absname + '\n' +
                ' ' * 15 + '{:<20}'.format('Found in Image') + ' = ' +
                self.image_name + '\n' +
                ' ' * 15 + '{:<20}'.format('Start Offset') + ' = ' +
                self.offset + '\n' +
                ' ' * 15 + '{:<20}'.format('File Length') + ' = ' +
                str(len(self.data)) + ' bytes' + '\n' +
                ' ' * 15 + '{:<20}'.format('Was Compressed?') + ' = ' +
                str(self.compressed) + '\n' +
                ' ' * 15 + '{:<20}'.format('md5 Digest') + ' = ' +
                log_md5 + '\n\n')
        # Then the standard audit log
        elif (self.subclass == 'vFile' and self.type[0] != '_' and
              config.audit is not None):
            config.audit.write('{:<15}'.format(filename) + absname + '\n')
            if self.status == "Deleted":
                config.audit.write(' ' * 15 + '*** Failed validity check - '
                                   'Deleted ***\n')
            else:
                config.audit.write(
                    ' ' * 15 + '{:<20}'.format('Found in Image') + ' = ' +
                    self.image_name + '\n' +
                    ' ' * 15 + '{:<20}'.format('Start Offset') + ' = ' +
                    self.offset + '\n' +
                    ' ' * 15 + '{:<20}'.format('File Length') + ' = ' +
                    str(len(self.data)) + ' bytes' + '\n' +
                    ' ' * 15 + '{:<20}'.format('Was Compressed?') + ' = ' +
                    str(self.compressed) + '\n' +
                    ' ' * 15 + '{:<20}'.format('md5 Digest') + ' = ' +
                    log_md5 + '\n')
            if not (self.meta == {} or self.status == 'Deleted'):
                config.audit.write(
                    ' ' * 15 + '----- Extracted Metadata -----' + '\n')
                for tag in self.meta:
                    config.audit.write(' ' * 15 +
                                       '{:<20}'.format(str(tag)) +
                                       ' = ' + str(self.meta[tag]) + '\n')
            config.audit.write('\n')
        # Finally the audit db, but only if requested by the user
        if (self.type != '_ASCII_raw' and config.sqldb is not None and
                not config.options['db_off']):
            with config.sqldb:
                cursor = config.sqldb.cursor()
                db_filename = "".join(["'", filename, "'"])
                db_offset = "".join(["'", str(self.offset), "'"])
                db_compressed = "".join(["'", str(self.compressed), "'"])
                db_this_image = "".join(["'", self.image_name, "'"])
                db_md5 = "".join(["'", log_md5, "'"])
                if self.meta == {}:
                    db_meta = "'NULL'"
                else:
                    db_meta = "".join(["'",
                                       str(self.meta).replace("'", ""),
                                       "'"])
                dbargs = ",".join([db_filename, db_offset, str(len(self.data)),
                                   db_compressed, db_this_image, db_md5,
                                   db_meta])
                dbcmd = "".join(['INSERT INTO Files VALUES(', dbargs, ');'])
                cursor.execute(dbcmd)
        # Finalize the vFile
        self.data = ""
        self.status = "Finished"

class vString(CarveObject):
    """
    Represent the state of an ASCII string that is in the process of being
    extracted.
    """
    def __init__(self, image_id, image_name, id_, type_, offset, stop,
                 compressed=False):
        """Instantiate a virtual ASCII string representation."""
        offset = "{0:#010x}".format(offset)
        if (type_[-1] == '_' or type_ in ['_deepcarve_raw', '_ASCII_raw']):
            offset += '+'
        CarveObject.__init__(self, 'vString', image_id, image_name, id_, type_,
                             offset, compressed)
        self.stop = stop
        """
        The set of characters, in regular expression notation, that is
        disallowed within this string type. Such characters indicate the end of
        this string if discovered in the input to
        `LaZy_NT.carve_object.vString.in_bytes`.
        """
    def in_bytes(self, byte_stream):
        """
        Stream data bytes into a `LaZy_NT.carve_object.vString` while
        checking for disallowed `LaZy_NT.carve_object.vString.stop` characters
        to end the string.

        ### Args:
        * **byte_stream (str):** The stream of bytes to be appended to this
        `LaZy_NT.carve_object.vString`'s `LaZy_NT.carve_object.vFile.data`
        attribute.
        """
        match = re.search(self.stop, byte_stream)
        if match:
            self.data = "".join([self.data, byte_stream[:match.start()]])
            self.to_file()
        else:
            self.data = "".join([self.data, byte_stream])

    def to_file(self):
        """
        Finalize a `LaZy_NT.carve_object.vString` and write its data content
        to the appropriate log.
        """
        filename = self.type + 's.txt'
        absname = os.path.join(config.options['outdir'], filename)
        temp_file = open(absname, 'a+')
        temp_file.write("{0:<80}".format(self.data) + self.offset + ' (' +
                        self.image_name + ')\n')
        temp_file.close()
        # Increment count in the histogram, more efficient per PEP 265
        config.histogram[self.type][self.data] = (
            config.histogram[self.type].get(self.data, 0) + 1)
        self.data = ""
        self.status = "Finished"
