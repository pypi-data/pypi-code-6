import os
from galaxygetopt.exceptions import *


class OutputFiles(object):

    def __init__(self, name="", GGO=None):

        # User supplied options
        self.name = name
        self.GGO = GGO
        if GGO is not None:
            self.galaxy = GGO.galaxy
        else:
            # Otherwise assume false
            self.galaxy = False

        # Extracted from GGO
        self.output_id = None
        self.output_label = None
        self.output_opts = {}
        # From galaxy
        self.new_file_path = None
        self.files_path = None
        self.files_id = None
        # ???
        self.parent_filename = None
        self.parent_internal_format = None
        self.parent_default_output_format = None
        # Internal use
        self.init_called = False
        # Other
        self.times_called = 0
        self.naming_strategy = 'norm'
        self.extension = None
        self.given_filename = None



        self.acceptable_formats = {
            'text/tabular': ['TSV', 'TSV_U', 'CSV', 'CSV_U', 'JSON', 'YAML',
                             'ODS','XLS', 'XLSX', 'Dumper'],
            'genomic/annotated': ['Genbank'],
            'genomic/raw': ['Fasta'],
            'text/html': ['HTML'],
            'text/plain': ['TXT', 'CONF'],
            'archive': ['tar.gz', 'zip', 'tar'],
        }

        self.format_mapping = {
            'TSV': 'tabular',
            'TSV_U': 'tabular',
            'CSV': 'tabular',
            'CSV_U': 'tabular',
            'XLS': 'data',
            'XLSX': 'data',
            'ODS': 'data',
            'JSON': 'txt',
            'YAML': 'txt',
            'Dumper': 'txt',
            'Genbank': 'txt',
            'Fasta': 'fasta',
            'HTML': 'html',
            'TXT': 'txt',
            'CONF': 'txt',
            'tar.gz': 'data',
            'zip': 'data',
            'tar': 'data',
        }

    def valid_formats(self, format_str):
        if format_str in self.acceptable_formats:
            return self.acceptable_formats[format_str]
        else:
            raise UnknownDataFormatExcpetion(format_str)

    def get_format_mapping(self, format_str):
        if format_str in self.format_mapping:
            return self.format_mapping[format_str]
        else:
            raise UnknownDataHandlerException(format_str)

    def initFromArgs(self, **kwargs):

        if self.GGO is None:
            raise UnspecifiedGGOObjectError("GGO object must be specified")

        # Grab registered outputs from GGO
        registered_outputs = self.GGO.registered_outputs
        if self.name is None:
            raise UnspecifiedOutputFileError("Author must supply a name of an output file during CRR instantiation")

        if self.name not in registered_outputs:
            raise UnknownRequestedOutputFileError("Requested output file is not known to GGO object")

        # Carrying on
        # We grab the pre-specified data regarding that output
        reg_out_params = registered_outputs[self.name]
        self.output_id = self.name
        self.output_label = reg_out_params['description']
        self.output_opts = reg_out_params['options']

        self.parent_internal_format = reg_out_params['options']['data_format']
        self.parent_default_output_format = reg_out_params['options']['default_format']
        self.parent_filename = reg_out_params['options']['default']

        # Special variables
        # --genemark "${genemark}" --genemark_format "${genemark_format}"
        # --genemark_files_path "${genemark_files_path}"
        # --genemark_id "${genemark_id}"

        # If they've specified a filename on the command line, that should
        # override the default value
        if self.GGO.opt[self.name] is not None:
            self.parent_filename = self.GGO.opt[self.name]

        # If they've specified a {str}_format option on the command line, that
        # should override the default value
        if self.GGO.opt[self.name + '_format'] is not None:
            self.parent_default_output_format = self.GGO.opt[self.name + '_format']

        # Grab supporting files path (added as new history items)
        self.new_file_path = self.GGO.opt['outfile_supporting']

        # Copy galaxy specific variables
        if self.GGO.opt[self.name + '_files_path'] is not None:
            self.files_path = self.GGO.opt[self.name + '_files_path']
        else:
            self.files_path = self.name + '_files_path'
        if self.GGO.opt[self.name + '_id'] is not None:
            self.files_id = self.GGO.opt[self.name + '_id']

        if self.GGO.opt['galaxy']:
            self.galaxy = True
        else:
            self.galaxy = False

        self.init_called = True

    def _genCRR(self, extension=None, data=None, data_format=None, format_as=None, filename=None):
        if not self.init_called:
            self.initFromArgs()

        # If the user supplied a custom extension, pull that (useful in
        # dummy/data output type)
        if extension is not None:
            self.extension = extension

        # This is a mandatory parameter
        if filename is not None:
            self.given_filename = filename
        else:
            self.given_filename = self.parent_filename

        # Allow overriding default format parameters
        df = self.parent_internal_format
        if data_format is not None:
            df = data_format

        fa= self.parent_default_output_format
        if format_as is not None:
            fa = format_as

        self.writer = self.writer_for_format(
            data_format=df, format_as=fa
        )

        # Wonder if this will translate well to py from pl
        self.writer.OutputFilesClass = self

        if data is not None:
            self.writer.data = data
        self.writer.process()
        self.writer.write()

        returned_filenames = self.writer.used_filenames
        self.bump_times_called
        return returned_filenames

    def CRR(self, extension=None, data=None, data_format=None, format_as=None,
            filename=None):
        return self._genCRR(extension=extension, data=data,
                            data_format=data_format, format_as=format_as,
                            filename=filename)

    def subCRR(self, extension=None, data=None, data_format=None,
               format_as=None, filename=None):
        self.naming_strategy = 'sub'
        return self._genCRR(extension=extension, data=data,
                            data_format=data_format, format_as=format_as,
                            filename=filename)

    def varCRR(self, extension=None, data=None, data_format=None,
               format_as=None, filename=None):
        self.naming_strategy = 'var'
        return self._genCRR(extension=extension, data=data,
                            data_format=data_format, format_as=format_as,
                            filename=filename)

    def bump_times_called(self):
        self.times_called = self.times_called + 1
        return self.times_called

    def writer_for_format(self, data_format=None, format_as=None):
        acceptable_handlers = self.acceptable_formats[data_format]

        if format_as not in acceptable_handlers:
            raise UnacceptableOutputFormatError("""Unacceptable output format choice [%s] for
                                internal data type for type %s. Acceptable formats
                            are [%s]. Alternatively, unacceptable output
                            file."""
                            % (data_format, format_as,
                               ', '.join(acceptable_handlers)))

        if format_as == 'TXT':
            from galaxygetopt.writer.txt import TXT
            return TXT()
        elif format_as == 'TSV_U':
            from galaxygetopt.writer.tsv_u import TSV_U
            return TSV_U()
        elif format_as == 'TSV':
            from galaxygetopt.writer.tsv import TSV
            return TSV()
        elif format_as == 'CSV_U':
            from galaxygetopt.writer.csv_u import CSV_U
            return CSV_U()
        elif format_as == 'CSV':
            from galaxygetopt.writer.csv_w import CSV_W
            return CSV_W()
        else:
            raise NoAvailableOutputHandlerError("Could not find an appropriate output handler")

    def generate_galaxy_variable(self):
        if not os.path.isdir(self.new_file_path):
            os.path.mkdir(self.new_file_path)

        filename = os.path.join(
            self.new_file_path, "primary_%s_%s_visible_%s" % (self.files_id,
                                                              self.given_filename,
                                                              self.extension)
        )

        return filename

    def generate_nongalaxy_variable(self):
        filename = "%s.%s" % (self.given_filename, self.extension,)
        return filename

    def generate_galaxy_subfile(self, create_dir=True):
        """Generate galaxy subfiles, i.e., data used within an HTML report, not
        as separate history items.

        create_dir may be set to false to disable creation of directories
        (e.g., in testing)"""
        if create_dir and not os.path.isdir(self.files_path):
            os.makedirs(self.files_path)

        filename = os.path.join(
            self.files_path, "%s.%s" % (self.given_filename, self.extension)
        )

        return filename

    def generate_nongalaxy_subfile(self):
        return self.generate_galaxy_subfile()

    def get_next_file(self):
        filename = ""
        if self.galaxy:
            if self.times_called == 0:
                filename = self.parent_filename
            else:
                if self.naming_strategy == 'sub':
                    filename = self.generate_galaxy_subfile()
                elif self.naming_strategy == 'var':
                    filename = self.generate_galaxy_variable()
                else:
                    raise UnknownStrategyError("Unknown strategy for multiple output files")
        else:
            if self.times_called == 0:
                filename = "%s.%s" % (self.given_filename, self.extension)
            else:
                if self.naming_strategy == 'sub':
                    filename = self.generate_nongalaxy_subfile()
                elif self.naming_strategy == 'var':
                    filename = self.generate_nongalaxy_variable()
                else:
                    raise UnknownStrategyError("Unknown strategy for multiple output files")
        return filename
