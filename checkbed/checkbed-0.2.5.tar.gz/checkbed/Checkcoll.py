import sys
import math
import os
import subprocess
import shutil
import glob
import random
from itertools import islice


class Checkcoll:
    def __init__(self, bedstem):
        self.bedstem = bedstem
        self.bedpath = self.bedstem + ".bed"
        self.bimpath = self.bedstem + ".bim"
        self.fampath = self.bedstem + ".fam"
        print("bed file path: " + self.bedpath)
        print("bim file path: " + self.bimpath)
        print("fam file path: " + self.fampath)
        if not os.path.isfile(self.bedpath) or not os.path.isfile(self.bimpath) or not os.path.isfile(self.fampath):
            raise Exception("One of the bed/bim/fam files does not exist!")

        self.shift_files = sorted(glob.glob(self.bedstem + "_shift_*.bed"))
        print("List of shifted bed files: ")
        print(self.shift_files[:10])
        print("......")

        self.nsnp           = self.countlines(self.bimpath)
        self.nindiv         = self.countlines(self.fampath)
        self.bytes_snp      = math.ceil(self.nindiv / 4)
        self.bytes_total    = self.bytes_snp * self.nsnp
        print("Number of SNPs: " + str(self.nsnp))
        print("Number of individuals: " + str(self.nindiv))
        print("Each SNP uses " + str(self.bytes_snp) + " bytes")
        print("All SNPs use " + str(self.bytes_total) + " bytes in total")

        if self.shift_files:
            self.largest_nshift = self.nshift_stem(self.shift_files[-1])[1]
        else:
            self.largest_nshift = 0

        self.corrupt_filelist = []

        self.greet = """
        bed file:           {}
        bim file:           {}
        fam file:           {}
        Number of SNPs:        {}
        Number of obs:         {}
        Bytes / SNP:           {}
        """.format(
            os.path.basename(self.bedpath),
            os.path.basename(self.bimpath),
            os.path.basename(self.fampath),
            self.nsnp, self.nindiv, self.bytes_snp
            )

        ################
        #    00 01 10 11
        # 00 00
        # 01 00 01
        # 10 00 01 00
        # 11 00 01 11 11
        ################
        self.bitsdict = {
          "0000":"00", #
          "0001":"00", #
          "0010":"00", #
          "0011":"00", #
          "0100":"00", #
          "0101":"01", ##
          "0110":"01", ##
          "0111":"01", ##
          "1000":"00", #
          "1001":"01", ##
          "1010":"00", ###
          "1011":"11", ####
          "1100":"00", #
          "1101":"01", ##
          "1110":"11", ####
          "1111":"11", ####
          }

    def countlines(self, fname):
        i = -1
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def nshift_stem(self, shiftpath):
        if not os.path.isfile(shiftpath):
            raise Exception("File {} does not exist!".format(os.path.basename(shiftpath)))
        shiftstem, ext = os.path.splitext(shiftpath)
        stempath, nshift = shiftstem.split("_shift_")
        nshift = int(nshift)
        print("Stem of shifted bed file: " + shiftstem)
        print("Number of shifts: " + str(nshift))
        return (shiftstem, nshift)

    def checkcoll(self, shiftpath, nskip, nsnp_to_check):
        shiftstem, nshift = self.nshift_stem(shiftpath)
        if nshift == 0:
            print("File not shifted, no need to check.")
            return 0;

        logpath = shiftstem + ".log"

        nsnp_left   = self.nsnp - nshift
        bytes_skip  = self.bytes_snp * nskip
        bytes_shift = self.bytes_snp * nshift
        bytes_left  = self.bytes_total - bytes_shift - bytes_skip
        bytes_to_check = self.bytes_snp * nsnp_to_check

        if(nsnp_to_check > nsnp_left - nskip):
            raise Exception("There are not so many SNPs to check!")

        try:
            with open(self.bedpath, "rb") as fh1, open(self.bedpath, "rb") as fh2, open(shiftpath, "rb") as fh3, open(logpath, "a") as logfh:
                fh1.seek(3 + bytes_skip)
                fh2.seek(3 + bytes_skip + bytes_shift)
                fh3.seek(3 + bytes_skip)

                n_right = 0
                n_wrong = 0
                skip_rest = False
                for i in range(bytes_to_check):
                    if skip_rest:
                        break
                    b1 = fh1.read(1)
                    b2 = fh2.read(1)
                    b3 = fh3.read(1)
                    b1str = "{:08b}".format(ord(b1))
                    b2str = "{:08b}".format(ord(b2))
                    b3str = "{:08b}".format(ord(b3))
                    b1bits = [b1str[i:(i+2)] for i in range(0, 8, 2)]
                    b2bits = [b2str[i:(i+2)] for i in range(0, 8, 2)]
                    b3bits = [b3str[i:(i+2)] for i in range(0, 8, 2)]
                    for j in range(4):
                        if self.bitsdict[b1bits[j] + b2bits[j]] == b3bits[j]:
                            n_right = n_right + 1
                        else:
                            n_wrong = n_wrong + 1
                            logfh.write("\n=============== byte index: {}, error index: {} ==================\n".format(str(i), str(j)))
                            logfh.write("byte1 integer: {}\n".format(ord(b1)))
                            logfh.write("byte2 integer: {}\n".format(ord(b2)))
                            logfh.write("byte3 integer: {}\n".format(ord(b3)))
                            logfh.write("{}\n".format(str(b1bits)))
                            logfh.write("{}\n".format(str(b2bits)))
                            logfh.write("{}\n".format(str(b3bits)))
                            if n_wrong > 10:
                                sys.stderr.write("More than 10 errors have been found, skip the rest of the file: \n")
                                sys.stderr.write("\t" + os.path.basename(shiftpath) + "\n")
                                skip_rest = True

                    printout = """
        Collapsed bed file:     {}
        Shift width:            {}
        SNPs skipped:           {}
        Right results count:    {}
        Wrong results count:    {}
                    """.format(
                        os.path.basename(shiftpath),
                        nshift, nskip, n_right, n_wrong)
                    tmp = subprocess.call("clear", shell=True)
                    print(self.greet)
                    print(printout)

                if n_wrong > 0 and os.path.basename(shiftpath) not in self.corrupt_filelist:
                    self.corrupt_filelist.append(os.path.basename(shiftpath))

        finally:
            print("Check finished for %s." % os.path.basename(shiftpath))

    def checkall(self, ncheck_each=None):
        try:
            if not self.shift_files:
                raise Exception("Collapsed genotype files have not been generated yet, nothing to check.")
            if ncheck_each != None and ncheck_each > self.nsnp - self.largest_nshift:
                raise Exception("ncheck_each too large. ")

            for shiftpath in self.shift_files:
                shiftstem, nshift = self.nshift_stem(shiftpath)
                snp_pool = range(self.nsnp - nshift - 1)

                ncheck_each_i = 1
                if ncheck_each == None:
                    if len(snp_pool) <= 10:
                        ncheck_each_i = 5
                    else:
                        ncheck_each_i = 10
                else:
                    ncheck_each_i = ncheck_each

                snp_sample = random.sample(snp_pool, ncheck_each_i)
                # if you skip 0, then you are at the first SNP, and so on...
                for snp in snp_sample:
                    self.checkcoll(shiftpath, snp, 1)
            if self.corrupt_filelist:
                print("After sanity check, I found the following file(s) corrupt:")
                for f in self.corrupt_filelist:
                    print(f)
            else:
                print("I didn't see anything abnormal.")
        except KeyboardInterrupt:
            print("\n\n\nChecking process ended by your request. \nHave a nice day, :-)")
        finally:
            print("Check finished.")

    def bedinfo(self):
        bedsize = os.stat(self.bedpath).st_size
        bedsize_est = self.nsnp * self.bytes_snp + 3
        print(self.greet)
        if(bedsize == bedsize_est):
            print("Size of bed file agrees with bim and fam files.")
        else:
            raise Exception("Size of bed file does not agree with bim and fam files!")

    def bimfamgen(self):
        if self.shift_files:
            for shiftf in self.shift_files:
                shiftstem, nshift = self.nshift_stem(shiftf)
                nsnp_left   = self.nsnp - nshift

                shiftbim = shiftstem + ".bim"
                shiftfam = shiftstem + ".fam"
                if os.path.isfile(shiftbim):
                    os.remove(shiftbim)
                if os.path.isfile(shiftfam):
                    os.remove(shiftfam)

                os.symlink(self.fampath, shiftfam)
                os.symlink(self.bimpath, shiftbim)
                # with open(shiftbim, "w") as shiftbim_fh, open(self.bimpath, "r") as bim_fh:
                #     first_snps = "".join(list(islice(bim_fh, nsnp_left)))
                #     shiftbim_fh.write(first_snps)
        else:
            print("There are no collapsed genotype files, why do you want to generate bim and fam files then? :P")


