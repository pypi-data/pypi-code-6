##Testing Module:

import pymethyl.functions
import unittest
import os

class TestSequenceFunctions(unittest.TestCase):
    
    def test_1(self):
        ##Type NUF2
        ##Type hg18
        ##Type Y
        ans = 'NUF2\t1\t161556346\t161557346'
        self.assertEqual(pymethyl.functions.regionInfo(), ans)


    def test_2(self):
        file_handle = open("NUF2.txt", "w")
        file_handle.write('NUF2\t1\t161556346\t161557346')
        file_handle.close()
        ##Choose this file for test ^
        ##Type NUF2
        ##Type nucl
        ##Type hg18
        pymethyl.functions.makeDatabase()
        self.assertTrue(os.path.isfile(os.path.extenduser('~') + "/Desktop/ncbi-blast-2.2.29+/db/NUF2.nhr"))

    def test_3(self):
        ##Choose NUF2.txt
        ##Choose bam file in test directory
        ##Type Sample1
        ##Type 50
        pymethyl.functions.extractBamFile()
        self.assertTrue(os.path.isfile(os.path.extenduser('~') + "/Desktop/Sample1/NUF2.txt"))
        
        
    def test_4(self):
        file_handle = open("NUF2.txt", "w")
        file_handle.write("161556450	161556500	37	TCAATAGTAATATTAACCCCCAAATAAACAATATTTATTGTTGATATAAC\n\
161556810	161556860	37	ATTTTAAAGATGCAGAAACGAGCTCAGTTAGGTTAAATAGCTCGCCTAAG\n\
161556821	161556871	37	GCAGAAACGAGCTCAGTTAGGTTAAATAGCTCGCCTAAGTCCACCTAGGT\n\
161556830	161556880	37	AGCTCAGTTAGGTTAAATAGCTCGCCTAAGTCCACCTAGGTAGTAAATGG\n\
161556865	161556915	37	CTAGGTAGTAAATGGTGTGATCAGGGATTTCAATCCAACTCCCTTTGACC\n\
161556876	161556926	34	ATGGTGTGATCAGGGATTTCAATCCAACTCCCTTTGACCGTAGAGATGTG\n\
161556985	161557035	34	AATTATGCATGTATCAGTAATCAATTTGATTTGGCAAGTGTCAATGAGAC\n\
161556985	161557035	34	AATTATGCATGTATCAGTAATCAATTTGATTTGGCAAGTGTCAATGAGAC\n\
161557094	161557144	34	AATCTCCTTTTGGGTCTTACTAGATTCCGACTTTGAGACTTACATCAGTA\n\
161557098	161557148	34	TCCTTTTGGGTCTTACTAGATTCCGACTTTGAGACTTACATCAGTAAATA\n\
161557129	161557179	34	AGACTTACATCAGTAAATAGACATTGAAAGGAAAGACAAAAGCCCTGAAC\n\
161557145	161557195	34	ATAGACATTGAAAGGAAAGACAAAAGCCCTGAACTAATGATATGAAATGT\n\
161557196	161557246	37	TTTTTATTTAGAATTGGTATAGACTTCACTATCAATAGGTTTAGTTCTTC\n\
161557249	161557299	34	ACAGGACAAAGCAGCGGAATTTGTGTCTACATTCAATACAACCTTTCTAG\n\
161557266	161557316	34	AATTTGTGTCTACATTCAATACAACCTTTCTAGCACTTTTTTCACATAAT")
        file_handle.close()
        ##Choose this file for test ^
        ##Type NUF2
        ##Type 0
        ##Type 5
        pymethyl.functions.findMethylation()
        self.assertTrue(os.path.isfile(os.path.extenduser('~')+ "/Desktop/Methylated Results/NUF2.txt"))
        os.remove("NUF2.txt")

    def test_5(self):
        ##Type blastn
        ##Type NUF2
        pymethyl.functions.blastIt()
        self.assertTrue(os.path.isfile(os.path.extenduser('~')+ "/Desktop/Result_From_Blast/NUF2_0.txt"))

    def test_6(self):
        ##Type NUF2
        ans = 'There are 1 events of methylation within this region.'
        self.assertEqual(pymethyl.functions.findResults(), ans)

    def test_7(self):
        os.remove(os.path.extenduser('~') + "/Desktop/ncbi-blast-2.2.29+/db/NUF2.nhr")
        os.remove(os.path.extenduser('~') + "/Desktop/ncbi-blast-2.2.29+/db/NUF2.nin")
        os.remove(os.path.extenduser('~') + "/Desktop/ncbi-blast-2.2.29+/db/NUF2.nsq")                     
        os.remove(os.path.extenduser('~') + "/Desktop/Methylated Results/NUF2.txt")
        os.remove(os.path.extenduser('~') + "/Desktop/Result_From_Blast/NUF2_0.txt")
        self.assertTrue(os.path.extenduser('~') + "/Desktop/Result_From_Blast/NUF2_0.txt", False)

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
