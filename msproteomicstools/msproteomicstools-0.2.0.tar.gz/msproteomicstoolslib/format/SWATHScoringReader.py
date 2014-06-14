#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
=========================================================================
        msproteomicstools -- Mass Spectrometry Proteomics Tools
=========================================================================

Copyright (c) 2013, ETH Zurich
For a full list of authors, refer to the file AUTHORS.

This software is released under a three-clause BSD license:
 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
 * Neither the name of any author or any participating institution
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
--------------------------------------------------------------------------
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL ANY OF THE AUTHORS OR THE CONTRIBUTING
INSTITUTIONS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
$Maintainer: Hannes Roest$
$Authors: Hannes Roest$
--------------------------------------------------------------------------
"""

from sys import stdout
import csv

verb = False

"""
Doc :
    A class to read the SWATH scoring logs from Peakview and OpenSWATH

    The data is returned from the "parse_files" functions as a list of runs.
    Each run contains a number of precursors and each precursors contains
    peakgroups (e.g. peakgroups that were found in chromatographic space).

    usage: 
    reader = SWATHScoringReader.newReader(options.infiles, options.file_format)
    this_exp.runs = reader.parse_files(options.realign_runs)
"""

#
# The data structures of the reader
#
class PeakGroupBase(object):

    def __init__(self):
        self.fdr_score = None
        self.normalized_retentiontime = None
        self.id_ = None
        self.intensity_ = None
        self.selected_ = False
  
    def get_value(self, value):
        raise Exception("Needs implementation")

    def set_value(self, key, value):
        raise Exception("Needs implementation")

    def set_fdr_score(self, fdr_score):
        self.fdr_score = fdr_score

    def get_fdr_score(self):
        return self.fdr_score

    def set_normalized_retentiontime(self, normalized_retentiontime):
        self.normalized_retentiontime = float(normalized_retentiontime)

    def get_normalized_retentiontime(self):
        return self.normalized_retentiontime

    def set_feature_id(self, id_):
        self.id_ = id_

    def get_feature_id(self):
        return self.id_

    def set_intensity(self, intensity):
      self.intensity_ = intensity

    def get_intensity(self):
        return self.intensity_

    # Selected
    def is_selected(self):
        return self.selected_

    def select_this_peakgroup(self):
        self.selected_ = True

    def unselect_this_peakgroup(self):
        self.selected_ = False


class MinimalPeakGroup(PeakGroupBase):
    """
    A single peakgroup that is defined by a retention time in a chromatogram
    of multiple transitions. Additionally it has an fdr_score and it has an
    aligned RT (e.g. retention time in normalized space).
    A peakgroup can be selected for quantification or not.
    
    Note that for performance reasons, the peakgroups are created on-the-fly
    and not stored as objects but rather as tuples in "Peptide".

    Each peak group has a unique id, a score (fdr score usually), a retention
    time as well as a back-reference to the precursor that generated the
    peakgroup.
    In this case, the peak group can also be selected or unselected.
    
    """
    def __init__(self, unique_id, fdr_score, assay_rt, selected, peptide, intensity=None, dscore=None):
      super(MinimalPeakGroup, self).__init__()
      self.id_ = unique_id
      self.fdr_score = fdr_score
      self.normalized_retentiontime = assay_rt 
      self.selected_ = selected
      self.peptide = peptide
      self.intensity_ = intensity
      self.dscore_ = dscore
  
    ## Print
    def print_out(self):
        # return self.run.get_id() + "/" + self.get_id() + " " + str(self.get_fdr_score()) + " " + str(self.get_normalized_retentiontime()) + " " + str(self.get_value("RT")) + " " + str(self.get_value("rt_score")) # rt_score = delta iRT
        return self.peptide.run.get_id() + "/" + self.get_feature_id() + " score:" + str(self.get_fdr_score()) + " RT:" + str(self.get_normalized_retentiontime()) # + " " + str(self.get_value("RT")) + " " + str(self.get_value("rt_score")) # rt_score = delta iRT

    # Do not allow setting of any parameters (since data is not stored here)
    def set_fdr_score(self, fdr_score):
        raise Exception("Cannot set in immutable object")

    def set_normalized_retentiontime(self, normalized_retentiontime):
        raise Exception("Cannot set in immutable object")

    def set_feature_id(self, id_):
        raise Exception("Cannot set in immutable object")

    def set_intensity(self, intensity):
        raise Exception("Cannot set in immutable object")

    def get_dscore(self):
        return self.dscore_

    ## Select / De-select peakgroup
    def select_this_peakgroup(self):
        self.selected_ = True
        self.peptide.select_pg(self.get_feature_id())

    def unselect_this_peakgroup(self):
        self.selected_ = False
        self.peptide.unselect_pg(self.get_feature_id() )

class GuiPeakGroup(PeakGroupBase):
    """
    A single peakgroup that is defined by a retention time in a chromatogram
    of multiple transitions.
    """
    def __init__(self, fdr_score, intensity, leftWidth, rightWidth, peptide):
      super(PeakGroupBase, self).__init__()
      self.fdr_score = fdr_score
      self.intensity_ = intensity
      self.leftWidth_ = leftWidth
      self.rightWidth_ = rightWidth
      self.peptide = peptide
  
    def get_value(self, value):
        if value == "m_score":
            return self.fdr_score
        elif value == "Intensity":
            return self.intensity_
        elif value == "rightWidth":
            return self.rightWidth_
        elif value == "leftWidth":
            return self.leftWidth_
        elif value == "FullPeptideName":
            return self.peptide.sequence
        elif value == "Charge":
            return self.peptide.charge
        else:
            raise Exception("Do not have value " + value)

class GeneralPeakGroup(PeakGroupBase):

    def __init__(self, row, run, peptide):
      super(GeneralPeakGroup, self).__init__()
      self.row = row
      self.run = run
      self.peptide = peptide

    def get_value(self, value):
        return self.row[self.run.header_dict[value]]

    def set_value(self, key, value):
        if value is None:
            value = "NA"
        self.row[self.run.header_dict[key]] = value

    def get_dscore(self):
        return self.get_value("d_score")
  
class PrecursorBase(object):
    def __init__(self, this_id, run):
        raise NotImplemented

    def get_id(self):
        return self.id 
  
    def get_decoy(self):
        return self._decoy

    def set_decoy(self, decoy):
        if decoy == "FALSE" or decoy == "0":
            self._decoy = False
        elif decoy == "TRUE" or decoy == "1":
            self._decoy = True
        else:
            raise Exception("Unknown decoy classifier '%s', please check your input data!" % decoy)
  
    # store information about the peakgroup - tuples (e.g. whether they are selected)
    def select_pg(self, this_id):
        raise NotImplemented

    def unselect_pg(self, id):
        raise NotImplemented

    def get_best_peakgroup(self):
        raise NotImplemented

    def get_selected_peakgroup(self):
        raise NotImplemented

    def get_all_peakgroups(self):
        raise NotImplemented
  
    def find_closest_in_iRT(self, delta_assay_rt):
        raise NotImplemented

class GeneralPrecursor(PrecursorBase):
    # A collection of peakgroups that belong to the same precursor and belong
    # to one run.
    # A peptide can return its best transition group, the selected peakgroup,
    # or can return the transition group that is closest to a given iRT time.
    def __init__(self, this_id, run):
        self.id = this_id
        self.peakgroups = []
        self.run = run
        self._decoy = False
  
    def add_peakgroup(self, peakgroup):
        self.peakgroups.append(peakgroup)
  
    def get_run_id(self):
      return self.run.get_id()
  
    def append(self, transitiongroup):
        assert self.id == transitiongroup.get_id()
        self.peakgroups.append(transitiongroup)
  
    def get_best_peakgroup(self):
        """ Return the best peakgroup according to fdr score
        """
        if len(self.peakgroups) == 0: return None
        best_score = self.peakgroups[0].get_fdr_score()
        result = self.peakgroups[0]
        for peakgroup in self.peakgroups:
            if peakgroup.get_fdr_score() <= best_score:
                best_score = peakgroup.get_fdr_score()
                result = peakgroup
        return result
  
    def get_selected_peakgroup(self):
        # return the selected peakgroup of this peptide, we can only select 1 or
        # zero groups per chromatogram!
        selected = [peakgroup for peakgroup in self.peakgroups if peakgroup.is_selected()]
        assert len(selected) < 2
        if len(selected) == 1:
          return selected[0]
        else: 
            return None

    def get_all_peakgroups(self):
        return self.peakgroups
  
    def find_closest_in_iRT(self, delta_assay_rt):
      return min(self.peakgroups, key=lambda x: abs(float(x.get_normalized_retentiontime()) - float(delta_assay_rt)))

class Precursor(PrecursorBase):
    """
    A collection of peakgroups that belong to the same precursor and belong
    to one run.
    A peptide can return its best transition group, the selected peakgroup,
    or can return the transition group that is closest to a given iRT time.
    Its id is the transition_group_id (e.g. the id of the chromatogram)
    
    For memory reasons, we store all information about the peakgroup in a
    tuple (invariable). This tuple contains a unique feature id, a score and
    a retention time. Additionally, we also store, whether the feature was
    selected or not.

    A peakgroup has the following attributes: 
        - an identifier that is unique among all other precursors 
        - a set of peakgroups 
        - a backreference to the run it belongs to
    """
    def __init__(self, this_id, run):
        self.id = this_id  
        self.peakgroups = []
        self.run = run
        self.peakgroups_ = []
        self.selected_ = []
        self._decoy = False
  
    def __str__(self):
        return "%s (run %s)" % (self.id, self.run)

    def add_peakgroup_tpl(self, pg_tuple, tpl_id):
        """Adds a peakgroup to this precursor.

        The peakgroup should be a tuple of length 4 with the following components:
            0. id
            1. quality score (FDR)
            2. retention time (normalized)
            3. intensity
            (4. d_score optional)
        """
        assert self.id == tpl_id # Check that the peak group is added to the correct precursor
        if len(pg_tuple) == 4:
            pg_tuple = pg_tuple + (None,)
        assert len(pg_tuple) == 5
        self.peakgroups_.append(pg_tuple)
        self.selected_.append(False)

    def get_id(self):
        return self.id 
  
    def get_run_id(self):
      return self.run.get_id()
    
    def get_decoy(self):
        return self._decoy

    # store information about the peakgroup - tuples (e.g. whether they are selected)
    def select_pg(self, this_id):
        pg_id = [i for i,pg in enumerate(self.peakgroups_) if pg[0] == this_id]
        assert len(pg_id) == 1
        self.selected_[pg_id[0]] = True

    def unselect_pg(self, this_id):
        pg_id = [i for i,pg in enumerate(self.peakgroups_) if pg[0] == this_id]
        assert len(pg_id) == 1
        self.selected_[pg_id[0]] = False

    def unselect_all(self):
        for i in range(len(self.selected_)) : self.selected_[i] = False

    def get_best_peakgroup(self):
        if len(self.peakgroups_) == 0: return None
        best_score = self.peakgroups_[0][1]
        result = self.peakgroups_[0]
        for peakgroup in self.peakgroups_:
            if peakgroup[1] <= best_score:
                best_score = peakgroup[1]
                result = peakgroup
        index = [i for i,pg in enumerate(self.peakgroups_) if pg[0] == result[0]][0]
        return MinimalPeakGroup(result[0], result[1], result[2], self.selected_[index], self, result[3], result[4])

    def get_selected_peakgroup(self):
      # return the selected peakgroup of this peptide, we can only select 1 or
      # zero groups per chromatogram!
      selected = [i for i,pg in enumerate(self.selected_) if pg]
      assert len(selected) < 2
      if len(selected) == 1:
        index = selected[0]
        result = self.peakgroups_[index]
        return MinimalPeakGroup(result[0], result[1], result[2], self.selected_[index], self, result[3], result[4])
      else: 
          return None

    def get_all_peakgroups(self):
        for index, result in enumerate(self.peakgroups_):
            yield MinimalPeakGroup(result[0], result[1], result[2], self.selected_[index], self, result[3], result[4])
  
    def find_closest_in_iRT(self, delta_assay_rt):
      result = min(self.peakgroups_, key=lambda x: abs(float(x[2]) - float(delta_assay_rt)))
      index = [i for i,pg in enumerate(self.peakgroups_) if pg[0] == result[0]][0]
      return MinimalPeakGroup(result[0], result[1], result[2], self.selected_[index], self, result[3], result[4])

class Run():
    """
    One single SWATH run that contains peptides (chromatograms) 
    It has a unique id and stores the headers from the csv

    A run has the following attributes: 
        - an identifier that is unique to this run
        - a filename where it originally came from
        - a dictionary of precursors, accessible through a dictionary
    """

    def __init__(self, header, header_dict, runid, orig_input_filename=None, filename=None, aligned_filename=None):
        self.header = header
        self.header_dict = header_dict
        self.runid = runid
        self.orig_filename = orig_input_filename # the original input filename
        self.openswath_filename = filename # the original OpenSWATH filename
        self.aligned_filename = aligned_filename # the aligned filename
        self.all_peptides = {}
  
    def get_id(self):
        return self.runid

    def get_openswath_filename(self):
        return self.openswath_filename

    def get_aligned_filename(self):
        return self.aligned_filename
  
    def get_best_peaks(self):
        result = []
        for k, peptide in self.all_peptides.iteritems():
          result.append(peptide.get_best_peakgroup())
        return result
  
    def get_best_peaks_with_cutoff(self, cutoff):
        return [p for p in self.get_best_peaks() if p.get_fdr_score() < cutoff]
  
    def get_all_trgroups(self, cutoff):
      above_cutoff = []
      for k,peak in self.all_peptides.iteritems():
        if peak.get_fdr_score() < cutoff:
            above_cutoff.append(peak)
      return above_cutoff
  
    def get_peptide(self, id):
        try:
          return self.all_peptides[id]
        except KeyError:
          # this run has no peakgroup for that peptide
          return None

    def __iter__(self):
        for peptide in self.all_peptides.values():
            yield peptide

class ReadFilter(object):
    """
    A callable class which can pre-filters a row and determine whether the row can be skipped.

    If the call returns true, the row is examined but if it returns false, the row should be skipped.
    """

    def __call__(self, row, header):
        return True

#
# The Readers of the Scoring files
#

class SWATHScoringReader:

    def __init__(self):
        raise Exception("Abstract class")

    def parse_row(self, run, this_row, read_exp_RT):
        raise Exception("Abstract method")

    @staticmethod
    def newReader(infiles, filetype, readmethod="minimal", readfilter=ReadFilter(), errorHandling="strict"):
        """Factory to create a new reader"""
        if filetype  == "openswath": 
            return OpenSWATH_SWATHScoringReader(infiles, readmethod, readfilter, errorHandling)
        elif filetype  == "mprophet": 
            return mProphet_SWATHScoringReader(infiles, readmethod, readfilter)
        elif filetype  == "peakview": 
            return Peakview_SWATHScoringReader(infiles, readmethod, readfilter)
        else:
            raise Exception("Unknown filetype '%s', allowed types are %s" % (decoy, str(filetypes) ) )

    def parse_files(self, read_exp_RT=True, verbosity=10):
      """Parse the input file(s) (CSV).

      Args:
          read_exp_RT(bool) : to read the real, experimental retention time
              (default behavior) or the delta iRT should be used instead.
      
      Returns:
          runs(list(SWATHScoringReader.Run))

      A single CSV file might contain more than one run and thus to create
      unique run ids, we number the runs as xx_yy where xx is the current file
      number and yy is the run found in the current file. However, if an
      alignment has already been performed and each run has already obtained a
      unique run id, we can directly use the previous alignment id.
      """

      print "Parsing input files"
      from sys import stdout
      import csv
      skipped = 0; read = 0
      runs = []
      for file_nr, f in enumerate(self.infiles):
        if verbosity >= 10:
            stdout.write("\rReading %s" % str(f))
            stdout.flush()
        header_dict = {}
        if f.endswith('.gz'):
            import gzip 
            filehandler = gzip.open(f,'rb')
        else:
            filehandler = open(f)
        reader = csv.reader(filehandler, delimiter="\t")
        header = reader.next()
        for i,n in enumerate(header):
          header_dict[n] = i
        if verbosity >= 10:
            stdout.write("\rReading file %s" % (str(f)) )
            stdout.flush()

        # Check if runs are already aligned (only one input file and correct header)
        already_aligned = (len(self.infiles) == 1 and header_dict.has_key(self.aligned_run_id_name))

        for this_row in reader:
            if already_aligned:
                runid = this_row[header_dict[self.aligned_run_id_name]]
            else:
                runnr = this_row[header_dict[self.run_id_name]]
                runid = runnr + "_" + str(file_nr)

            current_run = [r for r in runs if r.get_id() == runid]
            # check if we have a new run
            if len(current_run) == 0:
                orig_fname = None
                aligned_fname = None
                if header_dict.has_key("align_origfilename"):
                    aligned_fname = this_row[header_dict[ "align_origfilename"] ]
                if header_dict.has_key("filename"):
                    orig_fname = this_row[header_dict[ "filename"] ]
                current_run = Run(header, header_dict, runid, f, orig_fname, aligned_fname)
                runs.append(current_run)
            else: 
                assert len(current_run) == 1
                current_run = current_run[0]

            if not self.readfilter(this_row, current_run.header_dict):
                skipped += 1
                continue

            read += 1
            # Unfortunately, since we are using csv, tell() will not work...
            # print "parse row at", filehandler.tell()
            self.parse_row(current_run, this_row, read_exp_RT)

      # Here we check that each run indeed has a unique id
      assert len(set([r.get_id() for r in runs])) == len(runs) # each run has a unique id
      if verbosity >= 10: stdout.write("\r\r\n") # clean up
      print "Found %s runs, read %s lines and skipped %s lines" % (len(runs), read, skipped)
      return runs

class OpenSWATH_SWATHScoringReader(SWATHScoringReader):

    def __init__(self, infiles, readmethod="minimal", readfilter=ReadFilter(), errorHandling="strict"):
        self.infiles = infiles
        self.run_id_name = "run_id"
        self.readmethod = readmethod
        self.aligned_run_id_name = "align_runid"
        self.readfilter = readfilter
        self.errorHandling = errorHandling
        self.sequence_col = "Sequence"
        if readmethod == "minimal":
            self.Precursor = Precursor
        elif readmethod == "gui":
            self.Precursor = GeneralPrecursor
            self.PeakGroup = GuiPeakGroup
            self.sequence_col = "FullPeptideName"
        else:
            self.Precursor = GeneralPrecursor
            self.PeakGroup = GeneralPeakGroup

    def parse_row(self, run, this_row, read_exp_RT):
        decoy_name = "decoy"
        fdr_score_name = "m_score"
        dscore_name = "d_score"
        unique_peakgroup_id_name = "transition_group_id"
        diff_from_assay_in_sec_name = "delta_rt"
        run_id_name = "run_id"
        protein_id_col = "ProteinName"
        unique_feature_id_name = "id"
        intensity_name = "Intensity"
        decoy = "FALSE"
        left_width_name = "leftWidth"
        right_width_name = "rightWidth"
        charge_name = "Charge"

        # use the aligned retention time if it is available!
        if "aligned_rt" in run.header_dict: 
            diff_from_assay_in_sec_name = "aligned_rt" ## use this if it is present
        # if we want to re-do the re-alignment, we just use the "regular" retention time
        if read_exp_RT: 
            diff_from_assay_in_sec_name = "RT"

        trgr_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        unique_peakgroup_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        sequence = this_row[run.header_dict[self.sequence_col]]

        # Attributes that only need to be present in strict mode
        diff_from_assay_seconds = -1
        fdr_score = -1
        protein_name = "NA"
        thisid = -1
        try:
            fdr_score = float(this_row[run.header_dict[fdr_score_name]])
            protein_name = this_row[run.header_dict[protein_id_col]]
            thisid = this_row[run.header_dict[unique_feature_id_name]]
            diff_from_assay_seconds = float(this_row[run.header_dict[diff_from_assay_in_sec_name]])
            d_score = float(this_row[run.header_dict[dscore_name]])
        except KeyError:
            if self.errorHandling == "strict": 
                raise Exception("Did not find essential column.")

        # Optional attributes
        intensity = -1
        if run.header_dict.has_key(intensity_name):
            intensity = float(this_row[run.header_dict[intensity_name]])
        if "decoy" in run.header_dict:
            decoy = this_row[run.header_dict[decoy_name]]

        # If the peptide does not yet exist
        if not run.all_peptides.has_key(trgr_id):
          p = self.Precursor(trgr_id, run)
          p.protein_name = protein_name
          p.sequence = sequence
          p.set_decoy(decoy)
          run.all_peptides[trgr_id] = p

        if self.readmethod == "minimal":
          peakgroup_tuple = (thisid, fdr_score, diff_from_assay_seconds, intensity, d_score)
          run.all_peptides[trgr_id].add_peakgroup_tpl(peakgroup_tuple, unique_peakgroup_id)
        elif self.readmethod == "gui":
          leftWidth = this_row[run.header_dict[left_width_name]]
          rightWidth = this_row[run.header_dict[right_width_name]]
          charge = this_row[run.header_dict[charge_name]]
          run.all_peptides[trgr_id].charge = charge
          peakgroup = self.PeakGroup(fdr_score, intensity, leftWidth, rightWidth, run.all_peptides[trgr_id])
          run.all_peptides[trgr_id].add_peakgroup(peakgroup)
        elif self.readmethod == "complete":
          peakgroup = self.PeakGroup(this_row, run, run.all_peptides[trgr_id])
          peakgroup.set_normalized_retentiontime(diff_from_assay_seconds)
          peakgroup.set_fdr_score(fdr_score)
          peakgroup.set_feature_id(thisid)
          peakgroup.set_intensity(intensity)
          run.all_peptides[trgr_id].add_peakgroup(peakgroup)

class mProphet_SWATHScoringReader(SWATHScoringReader):

    def __init__(self, infiles, readmethod="minimal", readfilter=ReadFilter()):
        self.infiles = infiles
        self.run_id_name = "run_id"
        self.readmethod = readmethod
        self.aligned_run_id_name = "align_runid"
        self.readfilter = readfilter
        if readmethod == "minimal":
            self.Precursor = Precursor
        else:
            self.Precursor = GeneralPrecursor
            self.PeakGroup = GeneralPeakGroup

    def parse_row(self, run, this_row, read_exp_RT):
        decoy_name = "decoy"
        fdr_score_name = "m_score"
        unique_peakgroup_id_name = "transition_group_id"
        # diff_from_assay_in_sec_name = "delta_rt"
        run_id_name = "run_id"
        protein_id_col = "protein"
        sequence_col = "transition_group_pepseq"
        intensity_name = "log10_max_apex_intensity"
        decoy = "FALSE"

        # use the aligned retention time if it is available!
        if "aligned_rt" in run.header_dict: 
            diff_from_assay_in_sec_name = "aligned_rt" ## use this if it is present
        # if we want to re-do the re-alignment, we just use the "regular" retention time
        if read_exp_RT: 
            diff_from_assay_in_sec_name = "Tr" 
            diff_from_assay_seconds = float(this_row[run.header_dict["Tr"]]) 
        else:
            diff_from_assay_seconds = float(this_row[run.header_dict["iRT_empirical"]]) - float(this_row[run.header_dict["iRT_prediced"]])

        # create some id
        import uuid 
        thisid = str(uuid.uuid1() )
        # thisid = this_row[run.header_dict[unique_feature_id_name]]

        trgr_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        protein_name = this_row[run.header_dict[protein_id_col]]
        sequence = this_row[run.header_dict[sequence_col]]
        fdr_score = float(this_row[run.header_dict[fdr_score_name]])
        unique_peakgroup_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        intensity = -1
        if run.header_dict.has_key(intensity_name):
            intensity = float(this_row[run.header_dict[intensity_name]])
        if "decoy" in run.header_dict:
            decoy = this_row[run.header_dict[decoy_name]]
        run_id = this_row[run.header_dict[run_id_name]]

        if not run.all_peptides.has_key(trgr_id):
          p = self.Precursor(trgr_id, run)
          p.protein_name = protein_name
          p.sequence = sequence
          p.run_id = run_id
          p.set_decoy(decoy)
          run.all_peptides[trgr_id] = p
        if self.readmethod == "minimal":
          peakgroup_tuple = (thisid, fdr_score, diff_from_assay_seconds, intensity)
          run.all_peptides[trgr_id].add_peakgroup_tpl(peakgroup_tuple, unique_peakgroup_id)
        else:
          peakgroup = self.PeakGroup(this_row, run, run.all_peptides[trgr_id])
          peakgroup.set_normalized_retentiontime(diff_from_assay_seconds)
          peakgroup.set_fdr_score(fdr_score)
          peakgroup.set_feature_id(thisid)
          peakgroup.set_intensity(intensity)
          run.all_peptides[trgr_id].add_peakgroup(peakgroup)

class Peakview_SWATHScoringReader(SWATHScoringReader):

    def __init__(self, infiles, readmethod="minimal", readfilter=ReadFilter()):
        self.infiles = infiles
        self.run_id_name = "Sample"
        self.aligned_run_id_name = "align_runid"
        self.readmethod = readmethod
        self.readfilter = readfilter
        if readmethod == "minimal":
            self.Precursor = Precursor
        else:
            self.Precursor = GeneralPrecursor
            self.PeakGroup = GeneralPeakGroupPeakView

    def parse_row(self, run, this_row, read_exp_RT):
        decoy_name = "Decoy"
        fdr_score_name = "Score" # TODO invert score!!!
        unique_peakgroup_id_name = "Peptide" ## Does not exist!!
        run_id_name = "Sample"
        protein_id_col = "Protein"
        sequence_col = "Peptide"
        unique_feature_id_name = "id" # does not exist!!!
        decoy = "FALSE"
        intensity_name = "MaxPeak.Intensity"

        diff_from_assay_in_sec_name = "empirical_iRT"
        if not diff_from_assay_in_sec_name in run.header_dict:
            diff_from_assay_in_sec_name = "Median RT"

        # use the aligned retention time if it is available!
        if "aligned_rt" in run.header_dict: 
            diff_from_assay_in_sec_name = "aligned_rt" ## use this if it is present
        # if we want to re-do the re-alignment, we just use the "regular" retention time
        if read_exp_RT: 
            diff_from_assay_in_sec_name = "Median RT"

        # create some id
        import uuid 
        thisid = str(uuid.uuid1() )
        # thisid = this_row[run.header_dict[unique_feature_id_name]]

        if len(this_row) < run.header_dict[fdr_score_name] :
            # what to do here!? 
            return

        protein_name = this_row[run.header_dict[protein_id_col]]
        sequence = this_row[run.header_dict[sequence_col]]
        trgr_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        unique_peakgroup_id = this_row[run.header_dict[unique_peakgroup_id_name]]
        intensity = float(this_row[run.header_dict[intensity_name]])
        #print run.header_dict
        #print run.header_dict["Score"]

        # compute 1/score to have a score that gets better when smaller
        fdr_score = float(this_row[run.header_dict[fdr_score_name]])
        fdr_score = 1/fdr_score

        diff_from_assay_seconds = float(this_row[run.header_dict[diff_from_assay_in_sec_name]])
        if "decoy" in run.header_dict:
            decoy = this_row[run.header_dict[decoy_name]]
        run_id = this_row[run.header_dict[run_id_name]]

        if not run.all_peptides.has_key(trgr_id):
          p = self.Precursor(trgr_id, run)
          p.protein_name = protein_name
          p.sequence = sequence
          p.run_id = run_id
          p.set_decoy(decoy)
          run.all_peptides[trgr_id] = p
          if verb: print "add peptide", trgr_id
        if self.readmethod == "minimal":
          if verb: print "append tuple", peakgroup_tuple
          peakgroup_tuple = (thisid, fdr_score, diff_from_assay_seconds,intensity)
          run.all_peptides[trgr_id].add_peakgroup_tpl(peakgroup_tuple, unique_peakgroup_id)
        else: raise NotImplemented

