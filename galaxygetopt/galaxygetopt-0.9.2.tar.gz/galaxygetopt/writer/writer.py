from ..exceptions import WriterProcessingIncompleteError


class Writer(object):

    def __init__(self):
        self.OutputFilesClass = None
        self.galaxy_override = False
        self.data = None
        self.processed_data = None
        self.processing_complete = False
        self.used_filenames = []
        self.name = None

    def process(self):
        self.processed_data = self.data
        self.processing_complete = True

    def suffix(self):
        return 'ext'

    def write(self):
        if self.processing_complete:
            # Set the extension in the class that generates the filename
            # TBH this can probably be changed from a method to a var
            self.OutputFilesClass.extension = self.suffix()
            # Get next filename
            next_output_file = self.OutputFilesClass.get_next_file()
            # Store the filename
            self.used_filenames.append(next_output_file)
            # Write the data
            with open(next_output_file, 'w') as outfile:
                outfile.write(self.processed_data)
        else:
            raise WriterProcessingIncompleteError("""Write called but processing was not marked as
                            complete. Not writing""")

    def get_name(self):
        return self.OutputFilesClass._get_filename()
