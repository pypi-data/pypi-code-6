from writer import Writer
from Bio import SeqIO


class Fasta(Writer):
    suffix = 'fa'

    def write(self):
        self.OutputFilesClass.extension = self.suffix
        next_output_file = self.OutputFilesClass.get_next_file()
        self.used_filenames.append(next_output_file)
        SeqIO.write(self.data, next_output_file, 'fasta')

