from writer import Writer
from Bio import SeqIO


class Genbank(Writer):
    suffix = 'gbk'

    def write(self):
        self.OutputFilesClass.extension = self.suffix
        next_output_file = self.OutputFilesClass.get_next_file()
        self.used_filenames.append(next_output_file)

        with open(next_output_file, 'w') as handle:
            if isinstance(self.data, list):
                for record in self.data:
                    SeqIO.write(record, handle, 'genbank')
            else:
                SeqIO.write(self.data, handle, 'genbank')

