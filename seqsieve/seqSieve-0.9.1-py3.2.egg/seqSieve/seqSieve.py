#!/usr/bin/env python

'''
Copyright (C) 2014 Janina Mass

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import sys
import getopt
import subprocess
import threading
import os
import shutil
import matplotlib
import math
#don't use X:
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy
from distutils import spawn

GAP = "-"
LOCK = threading.Lock()
SEMAPHORE = threading.BoundedSemaphore()
PREFIXOUT = "sqs_out"
PREFIXTMP = "sqs_tmp"


class Alignment(object):
    """ Store alignment information """
    def __init__(self, name=None, fasta=None):
        self.name = name
        self.fasta = fasta
        self.members = []
        self.gap_pos = []
        self.mismatch_pos = []
        self.match_pos = []
        self.match_gap_pos = []
        self.attach_sequences()
        self.calc_numbers()

    def __repr__(self):
        ids = self.members
        return "Alignment:{},{}".format(self.name, ids)

    def __len__(self):
        try:
            return len(self.members[0].sequence)
        except TypeError as err:
            sys.stderr.write(err)
            sys.stderr.write("attach_sequences first")
            return 0

    def get_stats(self):
        """Return information about alignment (str, 6 comma-separated col)"""
        res = ""
        res += "{},{},{},{},{},{}".format(len(self.match_pos),
                                          len(self.match_gap_pos),
                                          len(self.mismatch_pos),
                                          len(self)-len(self.gap_pos),
                                          len(self.gap_pos),
                                          len(self))
        return res

    def get_stats_num(self):
        """Return information about alignment as list of ints """
        res = [len(self.match_pos), len(self.match_gap_pos),
               len(self.mismatch_pos), len(self)-len(self.gap_pos),
               len(self.gap_pos), len(self)]
        return res

    def attach_sequences(self):
        """Read fasta file, create Sequence objects and attach them to self.members"""
        print("FASTA:", self.fasta)
        for seq in FastaParser.read_fasta(self.fasta):
            new_seq = Sequence(name=seq[0], sequence=seq[1])
            self.members.append(new_seq)

    #todo ignore hanging ends
    def calc_numbers(self):
        """For each position in the alignment, calculate
         the ratio of gaps vs non-gaps. If the majority is gaps,
         insertions are penalized for each sequence. Similarly,
         if the majority is non-gaps, gaps are penalized.
         At 50 percent gaps and non-gaps, there is no penalty added.
        """
        for i in range(0, len(self)):
            curpos = [m.sequence[i] for m in self.members]
            if GAP in curpos:
                #dynamic penalty:
                tmp = "".join(curpos)
                gappyness = tmp.count(GAP)/float(len(self.members))
                if gappyness > 0.5:
                    to_punish = [m for m in self.members if m.sequence[i] != GAP]
                    for tpu in to_punish:
                        tpu.dynamic_penalty += gappyness
                elif gappyness < 0.5:
                    #punish gappers
                    to_punish = [m for m in self.members if m.sequence[i] == GAP]
                    for tpu in to_punish:
                        tpu.dynamic_penalty += 1-gappyness
                else:
                    pass
                #/dyn penalty
                self.gap_pos.append(i)
                #sequences that cause gaps:
                gappers = [m for m in self.members if m.sequence[i] == GAP]
                for seq in gappers:
                    seq.gaps_caused.append(i)
                #unique gaps caused:
                if len(gappers) == 1:
                    gappers[0].unique_gaps_caused.append(i)
                #insertions
                inserters = [m for m in self.members if m.sequence[i] != GAP]
                for seq in inserters:
                    seq.insertions_caused.append(i)
                #unique insertions caused:
                if len(inserters) == 1:
                    inserters[0].unique_insertions_caused.append(i)

            nongap = [c for c in curpos if c != GAP]
            cpset = set(curpos)
            if len(cpset) > 1 and GAP not in cpset:
                self.mismatch_pos.append(i)
                for seq in self.members:
                    seq.mismatch_shared.append(i)
            elif len(cpset) == 1 and GAP not in cpset:
                self.match_pos.append(i)
                for seq in self.members:
                    seq.match_shared.append(i)
            elif len(cpset) == 2 and GAP in cpset and len(nongap) > 2:
                self.match_gap_pos.append(i)

    def show_alignment(self, numbers=False):
        """Return column-wise string representation of alignment"""
        res = []
        alignment_length = len(self.members[0].sequence)
        for i in range(0, alignment_length):
            curpos = [m.sequence[i] for m in self.members]
            if numbers:
                try:
                    res.append(" "*(int(math.log(alignment_length, 10))-int(math.log(i, 10)))+str(i)+" "+" ".join(curpos))
                except ValueError as err:
                    if i == 0:
                        res.append(" "*int(math.log(alignment_length, 10))+str(i)+" "+" ".join(curpos))
                    else:
                        sys.stderr.write(err)
            else:
                res.append(" ".join(curpos))
        return "\n".join(res)


class Sequence(object):
    def __init__(self, name="", sequence=None, is_foreground=False):
        self.name = name
        self.sequence = sequence
        self.is_foreground = is_foreground
        self.insertions_caused = [] #positions
        self.unique_insertions_caused = []
        self.gaps_caused = []#positions
        self.unique_gaps_caused = []
        self.match_shared = []
        self.mismatch_shared = []
        self._penalty = None
        # penalize by site:
        # > n/2 gaps (@site): penalize inserts by gaps/n
        # < n/2 gaps (@site): penalize gaps by inserts/n
        self.dynamic_penalty = 0

    def set_foreground(self, boolean=True):
        self.is_foreground = boolean

    def __repr__(self):
        return "Sequence: {}".format(self.name)

    @property
    def penalty(self,
                unique_gap_penalty=10,
                unique_insert_penalty=10,
                gap_penalty=1,
                insert_penalty=1):

        self._penalty = sum(
            [len(self.insertions_caused)*insert_penalty,
             len(self.unique_insertions_caused)*unique_insert_penalty,
             len(self.gaps_caused)*gap_penalty,
             len(self.unique_gaps_caused)*unique_gap_penalty]
        )
        return self._penalty

    def summary(self, noheaders=False):
        res = ""
        if noheaders:
            res += "{},{},{},{},{},{},{}".format(self.name,
                                                 len(self.insertions_caused),
                                                 len(self.unique_insertions_caused),
                                                 len(self.gaps_caused),
                                                 len(self.unique_gaps_caused),
                                                 self.penalty,
                                                 self.dynamic_penalty)
        else:
            res += self.name
            res += ",insertions_caused:{},unique_insertions_caused:{}," \
                   "gaps_caused:{},unique_gaps_caused:{},penalty:{}," \
                   "dynPenalty:{}".format(len(self.insertions_caused),
                                          len(self.unique_insertions_caused),
                                          len(self.gaps_caused),
                                          len(self.unique_gaps_caused),
                                          self.penalty,
                                          self.dynamic_penalty)
        return res

    def get_custom_penalty(self,
                           gap_penalty,
                           unique_gap_penalty,
                           insertion_penalty,
                           unique_insertion_penalty,
                           mismatch_penalty,
                           match_reward):
        res = (len(self.gaps_caused)-len(self.unique_gaps_caused))*gap_penalty\
            + len(self.unique_gaps_caused) * unique_gap_penalty\
            + (len(self.insertions_caused) - len(self.unique_insertions_caused))\
            * insertion_penalty\
            + len(self.unique_insertions_caused) * unique_insertion_penalty\
            + len(self.mismatch_shared) * mismatch_penalty\
            + len(self.match_shared) * match_reward
        return res


class FastaParser(object):
    @staticmethod
    def read_fasta(fasta, delim=None, as_id=0):
        """read from fasta fasta file 'fasta'
        and split sequence id at 'delim' (if set)\n
        example:\n
        >idpart1|idpart2\n
        ATGTGA\n
        and 'delim="|"' returns ("idpart1", "ATGTGA")
        """
        name = ""
        fasta = open(fasta, "r")
        while True:
            line = name or fasta.readline()
            if not line:
                break
            seq = []
            while True:
                name = fasta.readline()
                name = name.rstrip()
                if not name or name.startswith(">"):
                    break
                else:
                    seq.append(name)
            joined_seq = "".join(seq)
            line = line[1:]
            if delim:
                line = line.split(delim)[as_id]
            yield (line.rstrip(), joined_seq.rstrip())
        fasta.close()

###########################################


def usage():
    print("""
    ######################################
    # seqSieve.py v0.9.1
    ######################################
    usage:
        seqSieve.py -f multifasta alignment
    options:
        -f, --fasta=FILE    multifasta alignment (eg. "align.fas")
        OR
        -F, --fasta_dir=DIR directory with multifasta files (needs -s SUFFIX)
        -s, --suffix=SUFFIX will try to work with files that end with SUFFIX (eg ".fas")

        -o, --outdir=STR    output directory (default: base directory of input file)
        -a, --msa_tool=STR  supported: "mafft", prank, prankf (= prank +F) [default:"mafft"]
        -i, --max_iterations=NUM    force stop after NUM iterations
        -n, --num_threads=NUM   max number of threads to be executed in parallel [default: 1]
        -m, --mode=MODE         set strategy to remove outlier sequences [default: "Sites"]
                                available modes (not case sensitive):
                                    "Sites", "Gaps", "uGaps","Insertions",
                                    "uInsertions","uInsertionsGaps", "custom"

        -q, --no-realign        don't realign with each iteration (not recommended)
        -l, --log       write logfile
        -p, --print_alignment   print column-wise alignment to command line
        -h, --help      prints this

    only for mode "custom":
        -g, --gap_penalty=NUM        set gap penalty [default: 1.0]
        -G, --unique_gap_penalty=NUM set unique gap penalty [default: 10.0]
        -j, --insertion_penalty=NUM  set insertion penalty [default:1.0]
        -J, --unique_insertion_penalty=NUM set insertion penalty [default:1.0]
        -M, --mismatch_penalty=NUM   set mismatch penalty [default:1.0]
        -r, --match_reward=NUM       set match reward [default: -10.0]

    """)
    sys.exit(2)
############################################


def check_path(progname, no_realign):
    if no_realign:
        return "no-realign"
    progname = progname.lower()
    avail = ["mafft", "prank", "prankf"]
    if progname not in avail:
        raise Exception("Program not supported."
                        " Only {} allowed.".format(",".join(avail)))
    else:
        if progname == "prankf":
            path = spawn.find_executable("prank")
            print("Found {} in {}\n".format("prank", path))
            print("Using prank with +F option")
        else:
            path = spawn.find_executable(progname)
            print("Found {} in {}\n".format(progname, path))
    if not path:
        raise Exception("Could not find {} on your system!"
                        " Exiting. Available options:{}\n".format(progname, ",".join(avail)))

    return progname
        #sys.exit(127)


def check_mode(mode):
    avail = ["sites", "gaps", "ugaps", "insertions", "uinsertions", "uinsertionsgaps", "custom"]
    if mode not in avail:
        raise Exception("Mode {} not available. Only {} allowed\n".format(mode, ",".join(avail)))


class TooFewSequencesException(Exception):
    pass


def adjust_dir(dirname, mode):
    if mode == "uinsertionsgaps":
        abbr = "uig"
    else:
        abbr = mode[0:2]
    return dirname+"_"+abbr


def get_seq_to_keep(alignment, mode, gap_penalty, unique_gap_penalty, insertion_penalty,
                    unique_insertion_penalty, mismatch_penalty, match_reward):
    if mode == "keepall":
        to_keep = [k for k in alignment.members]
    elif mode == "sites":
        to_keep = rm_dyn_penalty(alignment)
    elif mode == "gaps":
        to_keep = rm_custom_penalty(alignment,
                                    gap_penalty=1,
                                    unique_gap_penalty=1,
                                    insertion_penalty=0,
                                    unique_insertion_penalty=0,
                                    mismatch_penalty=0,
                                    match_reward=0)
        if not to_keep:
            rm_dyn_penalty(alignment)
    elif mode == "ugaps":
        to_keep = rm_max_unique_gaps(alignment)
        if not to_keep:
            to_keep = rm_dyn_penalty(alignment)

    elif mode == "insertions":
        to_keep = rm_custom_penalty(alignment,
                                    gap_penalty=0,
                                    unique_gap_penalty=0,
                                    insertion_penalty=1,
                                    unique_insertion_penalty=1,
                                    mismatch_penalty=0,
                                    match_reward=0)
        if not to_keep:
            rm_dyn_penalty(alignment)
    elif mode == "uinsertions":
        to_keep = rm_max_unique_inserters(alignment)
        if not to_keep:
            rm_dyn_penalty(alignment)
    elif mode == "uinsertionsgaps":
        to_keep = rm_max_unique_inserts_plus_gaps(alignment)
        if not to_keep:
            rm_dyn_penalty(alignment)
    elif mode == "custom":
        to_keep = rm_custom_penalty(alignment,
                                    gap_penalty=gap_penalty,
                                    unique_gap_penalty=unique_gap_penalty,
                                    insertion_penalty=insertion_penalty,
                                    unique_insertion_penalty=unique_insertion_penalty,
                                    mismatch_penalty=mismatch_penalty,
                                    match_reward=match_reward)
        if not to_keep:
            rm_dyn_penalty(alignment)
    else:
        raise Exception("Sorry, sth went wrong at get_seq_to_keep\n")
    return to_keep


def schoenify(fasta=None,
              max_iter=None,
              finaldir=None,
              tmpdir=None,
              msa_tool=None,
              mode=None,
              logging=None,
              print_alignment = None,
              gap_penalty=None,
              unique_gap_penalty=None,
              insertion_penalty=None,
              unique_insertion_penalty=None,
              mismatch_penalty=None,
              match_reward=None):

    if not fasta:
        raise Exception("Schoenify: Need alignment in fasta format.")
    else:
        arr = numpy.empty([1, 8], dtype='int32')
        iteration = 0

        fastabase = os.path.basename(fasta)
        statsout = finaldir + os.sep + ".".join(fastabase.split(".")[0:-1]) + "_seqstats.csv"
        tabout = finaldir + os.sep + ".".join(fastabase.split(".")[0:-1]) + "_iter.csv"
        resout = finaldir + os.sep + ".".join(fastabase.split(".")[0:-1]) + "_ranks.txt"

        if logging:
            #write header
            info = open(statsout, "w")
            info.write("{},{},{},{},{},{},{}\n".format("id",
                                                       "insertions_caused",
                                                       "unique_insertions_caused",
                                                       "gaps_caused",
                                                       "unique_gaps_caused",
                                                       "penalty",
                                                       "dynPenalty"))
        iter_tab = []
        header_tab = ["matches",
                      "matchesWithGaps",
                      "mismatches",
                      "noGap",
                      "gaps",
                      "length",
                      "iteration",
                      "numSeq",
                      '(length-gaps)*numSeq']

        alignmentstats = []
        alignment = Alignment(fasta=fasta)
        #sanity check
        if len(alignment.members) < 3:
            raise TooFewSequencesException("Need more than 2 "
                                           "sequences in alignment:"
                                           " {}\n".format(alignment.fasta))

        if not max_iter or (max_iter > len(alignment.members)-2):
            max_iter = len(alignment.members)-2
        print("# max iterations: {}".format(str(max_iter)))
        #todo: score original alignment, and save to table
        while iteration < max_iter:
            if iteration == 0:
                #keep all on iteration 0
                to_keep = get_seq_to_keep(alignment=alignment,
                                          mode="keepall",
                                          gap_penalty=gap_penalty,
                                          unique_gap_penalty=unique_gap_penalty,
                                          insertion_penalty=insertion_penalty,
                                          unique_insertion_penalty=unique_insertion_penalty,
                                          mismatch_penalty=mismatch_penalty,
                                          match_reward=match_reward)
            else:
                to_keep = get_seq_to_keep(alignment=alignment, mode=mode,
                                          gap_penalty=gap_penalty,
                                          unique_gap_penalty=unique_gap_penalty,
                                          insertion_penalty=insertion_penalty,
                                          unique_insertion_penalty=unique_insertion_penalty,
                                          mismatch_penalty=mismatch_penalty,
                                          match_reward=match_reward)
            print("# iteration: {}/{} \n".format(iteration, max_iter))
            if len(to_keep) < 2:
                break
            res = ""
            for k in to_keep:
                seq = "".join([s for s in k.sequence if s != GAP])
                res += (">{}\n{}\n".format(k.name, seq))
            iterfile = tmpdir+os.sep+".".join(fastabase.split(".")[0:-1])+"_"+str(iteration+1)

            with open(iterfile+".fa", 'w') as out:
                out.write(res)
            if msa_tool == "no-realign":
                with open(iterfile+"_aln.fa", 'w') as out:
                    no_realign_res = "".join([">{}\n{}\n".format(k.name, k.sequence) for k in to_keep])
                    out.write(no_realign_res)
            #log
            if logging:
                for m in alignment.members:
                    info.write(m.summary(noheaders=True)+"\n")

            alignmentstats.append(alignment.get_stats().split(","))
            tmp_stats_num = alignment.get_stats_num()
            iter_tab.append((",".join(x for y in alignmentstats for x in y))+","+str(iteration) +
                            "," + str(len(alignment.members)) + "," +
                            str((tmp_stats_num[5]-tmp_stats_num[4])*len(alignment.members)))
            alignmentstats = []
            if msa_tool == "mafft":
                proc = subprocess.Popen(["mafft", "--auto", iterfile+".fa"],
                                        stderr=subprocess.PIPE,
                                        stdout=open(iterfile+"_aln.fa", 'w'),
                                        bufsize=1)
                proc.stderr.read()
                proc.communicate()
                alignment = Alignment(name=iterfile, fasta=iterfile+"_aln.fa")

            #prank +F
            elif msa_tool == "prankf":
                proc = subprocess.Popen(["prank", "+F", "-d="+iterfile+".fa", "-o="+iterfile],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                perr, pout = proc.communicate()
                if logging:
                    print(pout)
                if perr:
                    sys.stderr.write(str(perr))
                shutil.move(iterfile+".best.fas", iterfile+"_aln.fa")
                alignment = Alignment(name=iterfile, fasta=iterfile+"_aln.fa")

            elif msa_tool == "prank":
                proc = subprocess.Popen(["prank", "-d="+iterfile+".fa", "-o="+iterfile],
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                perr, pout = proc.communicate()
                if logging:
                    print(pout)
                if perr:
                    sys.stderr.write(str(perr))
                shutil.move(iterfile+".best.fas", iterfile+"_aln.fa")
                alignment = Alignment(name=iterfile, fasta=iterfile+"_aln.fa")
            elif msa_tool == "no-realign":
                alignment = Alignment(name=iterfile, fasta=iterfile+"_aln.fa")
            if print_alignment:
                print(alignment.show_alignment(numbers=True))
            iteration += 1
        if logging:
            info.write("\n")
            info.close()
        with open(tabout, 'w') as taboutf:
            taboutf.write(",".join(header_tab))
            taboutf.write("\n")
            taboutf.write("\n".join(iter_tab))
        for i in iter_tab:
            row = [int(j) for j in i.split(",")[:-1]]
            arr = numpy.vstack((arr, numpy.array(row)))
        #delete row filled with zeros
        arr = numpy.delete(arr, 0, 0)
        ###########
        LOCK.acquire()
        plt.figure(1)
        plt.suptitle(fastabase, fontsize=12)
        ax = plt.subplot(3, 1, 1)

        try:
            plt.xticks(numpy.arange(min(arr[:, 6]), max(arr[:, 6])+1, 2.0))
        except ValueError as e:
            sys.stderr.write(str(e))
        #
        for i, l in zip([0, 1, 2, 3, 4, 5, 6, 7], ['match', 'matchWithGap', 'mismatch', 'nogap',
                                                   'gap', 'length', 'iteration', 'numSeq']):
            if not i in [6, 7]:
                plt.plot(arr[:, 6], arr[:, i], label=l)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0.)
        ax = plt.subplot(3, 1, 2)
        plt.xticks(numpy.arange(min(arr[:, 6]), max(arr[:, 6])+1, 2.0))
        plt.plot(arr[:, 6], arr[:, 7])
        ax.set_ylabel('count')
        ax.legend(["numSeq"], bbox_to_anchor=(1.03, 0.3), loc=2, borderaxespad=0.)
        ax = plt.subplot(3, 1, 3)
        plt.xticks(numpy.arange(min(arr[:, 6]), max(arr[:, 6])+1, 2.0))
        scoring = (arr[:, 5]-arr[:, 4])*arr[:, 7]

        try:
            max_index = scoring.argmax()
            #todo inconsistent if equally bad
            with open(resout, 'w')as resouth:
                resouth.write("# Ranking: {}\n".format(scoring[:].argsort()[::-1]))
                resouth.write("# Best set: {}".format(str(max_index)))
            plt.plot(arr[:, 6], scoring)
            ax.legend(["(length-gaps)*numSeq"],
                      bbox_to_anchor=(1.03, 0.3),
                      loc=2, borderaxespad=0.)

            ax.set_xlabel('iteration')
            plt.savefig(finaldir+os.sep +
                        ".".join(fastabase.split(".")[0:-1]) +
                        '_iter.svg', bbox_inches='tight', ext="svg")
            plt.clf()



            #original was best, original and 1st iteration have the same sequences
            if max_index == 0:
                finalfa = tmpdir+os.sep+".".join(fastabase.split(".")[0:-1]) + "_"+str(1)+".fa"
                finalfa_aln = fasta
                shutil.copy(finalfa, finaldir+os.sep+os.sep+".".join(fastabase.split(".")[0:-1]) + "_"+"orig"+".fa")
                print(finalfa_aln, finalfa)
            else:
                finalfa = tmpdir+os.sep+".".join(fastabase.split(".")[0:-1]) + "_"+str(max_index)+".fa"
                finalfabase = os.path.basename(finalfa)
                shutil.copy(finalfa, finaldir+os.sep+finalfabase)
                finalfa_aln = tmpdir+os.sep+".".join(fastabase.split(".")[0:-1]) + "_"+str(max_index)+"_aln.fa"
            shutil.copy(finalfa_aln, finaldir+os.sep+os.path.basename(finalfa_aln))
        except ValueError as e:
            sys.stderr.write(str(e))
        finally:
            LOCK.release()


def rm_max_unique_gaps(alignment):
    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")

    mx_unique_gaps = max([len(k.unique_gaps_caused) for k in alignment.members])
    keepers = [k for k in alignment.members if len(k.unique_gaps_caused) < mx_unique_gaps]
    return keepers


def rm_max_unique_inserters(alignment):
    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")

    mx_unique_ins = max([len(k.unique_insertions_caused) for k in alignment.members])
    keepers = [k for k in alignment.members if len(k.unique_insertions_caused) < mx_unique_ins]
    return keepers


def rm_max_penalty(alignment):
    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")

    mx_penalty = max([k.penalty for k in alignment.members])
    keepers = [k for k in alignment.members if k.penalty < mx_penalty]
    return keepers


def rm_custom_penalty(alignment,
                      gap_penalty=None,
                      unique_gap_penalty=None,
                      insertion_penalty=None,
                      unique_insertion_penalty=None,
                      mismatch_penalty=None,
                      match_reward=None):

    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")
    mx = max([k.get_custom_penalty(gap_penalty=gap_penalty,
                                   unique_gap_penalty=unique_gap_penalty,
                                   insertion_penalty=insertion_penalty,
                                   unique_insertion_penalty=unique_insertion_penalty,
                                   mismatch_penalty=mismatch_penalty,
                                   match_reward=match_reward) for k in alignment.members])

    keepers = [k for k in alignment.members
               if k.get_custom_penalty(gap_penalty=gap_penalty,
                                       unique_gap_penalty=unique_gap_penalty,
                                       insertion_penalty=insertion_penalty,
                                       unique_insertion_penalty=unique_insertion_penalty,
                                       mismatch_penalty=mismatch_penalty,
                                       match_reward=match_reward)
               < mx]
    return keepers


def rm_dyn_penalty(alignment):
    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")

    mx_penalty = max([k.dynamic_penalty for k in alignment.members])
    keepers = [k for k in alignment.members if k.dynamic_penalty < mx_penalty]
    return keepers


def rm_max_unique_inserts_plus_gaps(alignment):
    if not isinstance(alignment, Alignment):
        raise Exception("Must be of class Alignment")

    #s = alignment.show_alignment(numbers=True)
    mx_unique_ins = max([len(k.unique_insertions_caused) +
                         len(k.unique_gaps_caused) for k in alignment.members])
    keepers = [k for k in alignment.members if (len(k.unique_insertions_caused) +
                                                len(k.unique_gaps_caused))
               < mx_unique_ins]
    return keepers


class SchoenifyThread(threading.Thread):
    def __init__(self, fasta, max_iter, finaldir, tmpdir, msa_tool,
                 mode, logging, print_alignment, gap_penalty, unique_gap_penalty,
                 insertion_penalty, unique_insertion_penalty,
                 mismatch_penalty, match_reward):
        super(SchoenifyThread, self).__init__()
        self.fasta = fasta
        self.max_iter = max_iter
        self.finaldir = finaldir
        self.tmpdir = tmpdir
        self.msa_tool = msa_tool
        self.mode = mode
        self.logging = logging
        self.print_alignment = print_alignment
    #custom
        self.gap_penalty = gap_penalty
        self.unique_gap_penalty = unique_gap_penalty
        self.insertion_penalty = insertion_penalty
        self.unique_insertion_penalty = unique_insertion_penalty
        self.mismatch_penalty = mismatch_penalty
        self.match_reward = match_reward

    def run(self):
        SEMAPHORE.acquire()
        try:
            schoenify(fasta=self.fasta, max_iter=self.max_iter, finaldir=self.finaldir,
                      tmpdir=self.tmpdir, msa_tool=self.msa_tool, mode=self.mode,
                      logging=self.logging, print_alignment=self.print_alignment,
                      gap_penalty=self.gap_penalty,
                      unique_gap_penalty=self.unique_gap_penalty,
                      insertion_penalty=self.insertion_penalty,
                      unique_insertion_penalty=self.unique_insertion_penalty,
                      mismatch_penalty=self.mismatch_penalty,
                      match_reward=self.match_reward)
        except TooFewSequencesException as e:
            sys.stderr.write(str(e))
        SEMAPHORE.release()


def get_fasta_list(directory=None, suffix=None):
    for fafile in os.listdir(directory):
        if fafile.endswith(suffix):
            yield os.sep.join([directory, fafile])


def main():
    """Main"""
    fastalist = []
    fastadir = None
    suffix = None
    outdir = None
    max_iter = None
    finaldir = None
    tmpdir = None
    msa_tool = "mafft"
    num_threads = 1
    mode = "sites"
    logging = False
    print_alignment = False
    no_realign = False
  #custom penalty:
    gap_penalty = 1.0
    unique_gap_penalty = 10.0
    insertion_penalty = 1.0
    unique_insertion_penalty = 1.0
    mismatch_penalty = 1.0
    match_reward = -10.0

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       "f:F:s:o:i:a:n:m:g:G:j:J:M:r:qlhp",
                                       ["fasta=",
                                        "fasta_dir=",
                                        "suffix=",
                                        "outdir=",
                                        "max_iteration=",
                                        "msa_tool=",
                                        "num_threads=",
                                        "mode=",
                                        "gap_penalty",
                                        "unique_gap_penalty",
                                        "insertion_penalty=",
                                        "unique_insertion_penalty=",
                                        "mismatch_penalty=",
                                        "match_reward=",
                                        "no-realign",
                                        "log",
                                        "help",
                                        "print_alignment"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o in ("-f", "--fasta"):
            fastalist = a.split(",")
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-o", "--outdir"):
            outdir = a
        elif o in ("-n", "--num_threads"):
            num_threads = int(a)
        elif o in ("-F", "--fasta_dir"):
            fastadir = a
        elif o in ("-s", "--suffix"):
            suffix = a
        elif o in ("-i", "--max_iteration"):
            max_iter = int(a)
        elif o in ("-a", "--msa_tool"):
            msa_tool = a.lower()
        elif o in ("-m", "--mode"):
            mode = a.lower()
        elif o in ("-l", "--log"):
            logging = True
        elif o in ("-p", "--print_alignment"):
            print_alignment = True
        elif o in ("-q", "--no-realign"):
            no_realign = True
    #only for mode "custom":
        elif o in ("-g", "--gap_penalty"):
            gap_penalty = float(a)
        elif o in ("-G", "--unique_gap_penalty"):
            unique_gap_penalty = float(a)
        elif o in ("-j", "--insertion_penalty"):
            insertion_penalty = float(a)
        elif o in ("-J", "--unique_insertion_penalty"):
            unique_insertion_penalty = float(a)
        elif o in ("-M", "--mismatch_penalty"):
            mismatch_penalty = float(a)
        elif o in ("-r", "--match_reward"):
            match_reward = float(a)
        else:
            print(o)
            assert False, "unhandled option"
    if not fastalist and not (fastadir and suffix):
        usage()

    if not outdir:
        if fastadir:
            finaldir = fastadir + os.sep + PREFIXOUT
            tmpdir = fastadir + os.sep + PREFIXTMP
        else:
            finaldir = os.path.dirname(fastalist[0])+os.sep+PREFIXOUT
            tmpdir = os.path.dirname(fastalist[0])+os.sep+PREFIXTMP
    else:
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        finaldir = outdir + os.sep + PREFIXOUT
        tmpdir = outdir + os.sep + PREFIXTMP

    msa_tool = check_path(progname=msa_tool, no_realign=no_realign)
    check_mode(mode=mode)
    finaldir = adjust_dir(finaldir, mode)
    tmpdir = adjust_dir(tmpdir, mode)
    global SEMAPHORE
    SEMAPHORE = threading.BoundedSemaphore(num_threads)
    if not os.path.exists(finaldir):
        os.mkdir(finaldir)
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)
    if fastadir:
        print(suffix)
        for fastafile in get_fasta_list(fastadir, suffix):
            print(fastafile)
            fastalist.append(fastafile)
    for fasta in fastalist:
        SchoenifyThread(fasta,
                        max_iter,
                        finaldir,
                        tmpdir,
                        msa_tool,
                        mode,
                        logging,
                        print_alignment,
                        gap_penalty,
                        unique_gap_penalty,
                        insertion_penalty,
                        unique_insertion_penalty,
                        mismatch_penalty,
                        match_reward).start()
#############################################


if __name__ == "__main__":
    main()
