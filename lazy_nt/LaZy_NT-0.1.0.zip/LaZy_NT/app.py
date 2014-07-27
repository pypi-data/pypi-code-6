# pylint: disable=W0105, W0403
"""
This module provides a fully functional pre-made file carving and ASCII
extraction application, using the API provided by the `LaZy_NT` core modules.
"""
# Standard Python imports
import argparse
import datetime
import mmap
import os
import sqlite3
import sys
import warnings

# LaZy_NT module imports
import _version
__version__ = _version.get_version()
import config
import disk_image
import carve_object

def close_logs():
    """
    Close any output logs which were previously opened by the application.
    """
    config.audit.write(
        "Finished at: " +
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    config.audit.close()
    if config.deep_raw_log != None:
        config.deep_raw_log.write(
            "Finished at:" +
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        config.deep_raw_log.close()
    if config.ascii_raw_log != None:
        config.ascii_raw_log.write(
            "Finished at:" +
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        config.ascii_raw_log.close()

def create_db(name='audit.db'):
    """
    Create an audit database file in sqlite format.

    ### Args:
    * **name (str):** A filename, with extension, for the audit database.
    """
    config.sqldb = sqlite3.connect(
        os.path.join(config.options['outdir'], name))
    with config.sqldb:
        cursor = config.sqldb.cursor()
        cursor.execute(
            "CREATE TABLE Files(Name TEXT, Offset TEXT, Length INT, "
            "Compressed TEXT, From_Image TEXT, md5 TEXT, Metadata TEXT)")

def validate_arguments():
    """
    Ensure the current application options are valid.

    ### Raises:
    * **ValueError** on non-empty `outdir` or invalid `chunk_size`.
    """
    if not carve_object.validate_output_dir(config.options['outdir'],
                                            val_empty=True):
        raise ValueError(
            "Output directory '%s' is not empty" % config.options['outdir'])
    if config.options['deep_carve']:
        carve_object.validate_output_dir(
            os.path.join(config.options['outdir'], '_deepcarve_raw'))
    if config.options['ascii']:
        carve_object.validate_output_dir(
            os.path.join(config.options['outdir'], '_ASCII_raw'))
    if not config.options['chunk_size'] in range(64, 4097, 16):
        raise ValueError(
            "Invalid chunk size '%s' provided. Must be a multiple of 16"
            "in [64-4096]." % config.options['chunk_size'])

class App(object):
    """
    Represent a user-facing application.
    """
    def __init__(self, images, **kwargs):
    # pylint: disable=W1401
        """ Instantiate an application representation.

        ### Args:
        * **images (list of str):** A list of fully qualified file names to
        use as disk image file inputs.
        * **\*\*kwargs:** If a keyword argument's name matches a key in
        the `config.options` dictionary, the argument's value will override
        the option's default value.
        """
        self.__command_string = None
        config.options['images'] = images
        # If option values were provided, override config module defaults
        if kwargs is not None:
            for name, value in kwargs.items():
                if name in config.options:
                    config.options[name] = value
                if (name == 'double_carve' or name == 'ascii') and value:
                    config.options['deep_carve'] = True

    def create_logs(self, name='audit.txt'):
        """
        Create the audit log file and (if required) the supplemental deep
        carve and ASCII extraction log files.

        ### Args:
        * **name (str):** A filename, with extension, for the audit log.
        """
        config.audit = open(os.path.join(config.options['outdir'], name), 'w')
        config.audit.write("LaZy_NT v" + __version__ + " - Audit Log" + '\n\n')
        if self.__command_string is not None:
            config.audit.write(
                "Command line: " + self.__command_string + '\n\n')
        config.audit.write("Dependency Module Status:" + '\n')
        for module in sorted(carve_object.module_status):
            if not module == 'hachoir':
                config.audit.write('     ' + "{:<20}".format(module) + ' = ')
                if not carve_object.module_status[module]:
                    config.audit.write('Not ')
                config.audit.write('Installed' + '\n')
        config.audit.write(
            '\n' + "Started at: " +
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n')
        if config.options['deep_carve'] and config.options['keep_raw']:
            config.deep_raw_log = open(os.path.join(
                config.options['outdir'], '_deepcarve_raw',
                '_deepcarve_raw.txt'), 'w')
            config.deep_raw_log.write("LaZy_NT v" + __version__ +
                                      " - Supplemental Raw Data Extraction Log"
                                      "\n\n\n")
            config.deep_raw_log.write(
                "Started at: " +
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n')
        if config.options['ascii'] and config.options['keep_raw']:
            config.ascii_raw_log = open(os.path.join(
                config.options['outdir'], '_ASCII_raw', '_ASCII_raw.txt'), 'w')
            config.ascii_raw_log.write(
                "LaZy_NT v" + __version__ + " - Supplemental "
                "Raw ASCII Extraction Log\n\n\n")
            config.ascii_raw_log.write(
                "Started at: " +
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n\n')

    def set_command_string(self, string):
        """
        Set the private `__command_string` attribute explicitly.

        ### Args:
        * **string (str):** A string to set `__command_string` equal to.
        """
        self.__command_string = string

    def generate_command_string(self, argv):
        """
        Set the private `__command_string` attribute
        programmatically.

        ### Args:
        * **argv (list of str):** The caller's `sys.argv` to be parsed.
        """
        self.__command_string = ''
        for arg in argv:
            if arg == argv[0]:
                self.__command_string += (arg + ' ')
            else:
                if ' ' in arg:
                    self.__command_string += ('"' + arg + '"' + ' ')
                else:
                    self.__command_string += (arg + ' ')

    def run(self):
        """
        Run the user application.
        """
        validate_arguments()
        if config.audit == None:
            self.create_logs()
        if config.sqldb == None and config.options['database']:
            create_db()
        # Operate on all input images in sequence
        for image_num in range(0, len(config.options['images'])):
            this_image = config.options['images'][image_num]
            if not os.path.isfile(this_image):
                warnings.warn(
                    "Image file '%s' does not exist. [Skipping]" % this_image)
                continue # Bump for loop to the next image file
            print "***** Begin processing '%s' *****" % this_image
            image = disk_image.DiskImage(image_num, this_image)
            image_done = False
            files_this_image = 0
            with open(image.filename, 'r+b') as image_file:
                image.mm = mmap.mmap(image_file.fileno(), 0)
                while not image_done:
                    # Read a chunk of the image and dispatch it for analysis
                    image_done = not image.read_bytes(
                        config.options['chunk_size'])
                    if image_done:
                        continue
                    image.analyze_chunk()
                    # If a file is found, output the start offset and type
                    if len(image.carve_objects) > files_this_image:
                        for vfile in image.carve_objects:
                            if vfile.id >= files_this_image:
                                files_this_image += 1
                                print "{0:<11}".format(vfile.offset), \
                                      "- found file of type %s." \
                                      % vfile.type
                                if config.options['verbose'] >= 1:
                                    print "              file is",
                                    if not vfile.compressed:
                                        print "not",
                                    print "compressed."
                    # Only process this chunk if there are vFiles in-process.
                    if image.inprocess_carve_objects('vFile') > 0:
                        if not image.compression_state:
                            image.process_unc_chunk()
                        # Allow unc_chunk() to fall through into comp_stream()
                        if image.compression_state:
                            image.process_comp_stream()
                    else:
                        image.increment_abs_offset()
                # Once image_done is True, finalize any in-process vFiles
                image.finish_inprocess_vFiles(flush=True, force=True)
                carve_object.write_histogram(this_image)
                print "*****  End processing '%s'  *****" \
                      % this_image, '\n'
                image.mm.close()    # Close this image file
                continue            # Bump for loop to the next image file
        print "Finished processing all images!"
        close_logs()

def main():
    """
    Execute the pre-built application if this module is called as 'main'.
    Parse command line arguments, configure options and the command string,
    then run the application.
    """
    # Handle command line arguments, provide help and usage information
    parser = argparse.ArgumentParser(
        description='Carves files from NTFS compressed volume images.')
    parser.add_argument(
        'image', nargs='+', help='one or more image files to process')
    parser.add_argument(
        '-a', '--ascii', action='store_true',
        help='enables bulk ASCII extraction and string template parsing '
        'for forensic and personal data.')
    parser.add_argument(
        '-cs', '--chunk-size', type=int, default='512',
        help='smaller chunks may detect more files but will slow execution '
        'and produce more false detections. allows multiples of 16 from '
        '64 to 4096 [defaults to 512]')
    parser.add_argument(
        '-db', '--database', action='store_true',
        help='enables sqlite database output')
    parser.add_argument(
        '-dc', '--double-carve', action='store_true',
        help='performs a second carving pass on data after decompression. '
        'enables recovery of files not aligned on chunk size boundaries')
    parser.add_argument(
        '-pp', '--post-process', choices=['c', 'm', 'v'],
        help='Enables post processing options. (c)leanup removes intermediate '
        'raw files created by double carving and ASCII extraction. (m)etadata '
        'extracts the same from carved files and writes it to the output log. '
        "(v)alidate deletes some carved file types if they're found to be "
        'invalid')
    parser.add_argument(
        '-t', '--test', action='store_true',
        help='analyze image and create output logs only. '
        'does not carve anything to disk')
    parser.add_argument(
        '-o', '--outdir', default='LaZy_NT_out',
        help='fully qualified output directory path')
    parser.add_argument(
        '-u', '--unc-image', action='store_true',
        help='disables compression detection to improve accuracy with '
        'uncompressed disk images')
    parser.add_argument(
        '-v', '--verbose', action='count',
        help='three levels available, -v through -vvv')
    parser.add_argument(
        '--version', action='version', version=("LaZy_NT v" + __version__ +
                                                " Created by Marc Herndon."))
    args = parser.parse_args()

    keep_raw = False if args.post_process is not None and \
               'c' in args.post_process else True
    meta = True if args.post_process is not None and \
           'm' in args.post_process else False
    val = True if args.post_process is not None and \
          'v' in args.post_process else False

    # Instantiate and run the carver application
    carver = App(args.image,
                 ascii=args.ascii,
                 chunk_size=args.chunk_size,
                 database=args.database,
                 double_carve=args.double_carve,
                 keep_raw=keep_raw,
                 metadata=meta,
                 no_carve=args.test,
                 outdir=args.outdir,
                 unc_image=args.unc_image,
                 val_files=val,
                 verbose=args.verbose)
    carver.generate_command_string(sys.argv)
    carver.run()

if __name__ == '__main__':
    main()
