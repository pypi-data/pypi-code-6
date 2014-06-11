import os
from glob import glob
from util import *
from LogParser import *
from FileWriter import *

class EventBuilder(object):
    """ Abstract EventBuilder class.

    passes a list of files to the appropriate LogParser subclass to get a list
    of dictionaries representing rows of the log file, then passes those lists
    to self.events_for_rows() to generate a list of dictionaries representing
    events.

    The start of a new file is always the start of a new run. If run_field is
    set, we'll also break up the files into sections with identical values for
    that field. Take note, we'll do this by stepping through the rows in
    sequence, and looking for changes in the field's value. This means that if
    the field has value A, then B, then A again, you will get three runs out
    of that file. This would be a weird thing to have happen in your file, but
    be forewarned.

    Note that we'll take care of adding the duration of the preceding runs to
    any onsets provided. Just implement duration_for_run(), and we'll handle
    the rest. That means that if you're going to be concatenating runs, you
    only need to provide onsets relative to the beginning of the run.

    Supported output formats include 'spm', 'fidl', 'pickle'

    # TODO: More doco

    # TODO: look for multiple runs in the same file if you have run_field
    """

    def __init__(self,*args,**kwargs):
        self.subjects = None
        self.data_glob_templates = None
        self.run_field = None
        self.output_dir = None
        self.concat_sets = None
        self.output_formats = None
        self.current_sub = None
        self.sub_data = None
        self.output_dir = os.path.join(os.getcwd(), 'events_parsed')
        self.output_formats = ['pickle']
        self.last_event_sets = None
        self.skip_output = False
        self.event_files = None
        self.sub_data = {}
        super(EventBuilder, self).__init__()
    
    def run(self):
        self.check_settings()
        # convert raw logs per subject
        self.sub_data = {}
        self.event_files = {}
        for sub in self.subjects:
            self.current_sub = sub
            # so subclasses can do... whatever
            self.pre_subj_setup()
            # gather all of the raw files
            gs = [temp % sub for temp in self.data_glob_templates]
            raw_bs = []
            for g in gs:
                raw_bs += glob(g)
            if not raw_bs:
                print "Couldn't find any files for subject %s" % str(sub)
                continue
            # make sure we've got a subject output dir
            sub_dir = os.path.join(self.output_dir, str(sub))
            if not self.skip_output:
                ensure_dir(sub_dir, overwrite=True)
            # parse all of the files... memory intensive, but hey
            data = [LogParser.parse_file(bs) for bs in raw_bs]
            # break the files into runs. should come back as:
            # [[f1_run1_rows_list, f1_run2_rows_list], [f2_run1_rows_list], ...]
            data_runs_separated = [self.separate_runs(fd) for fd in data]
            concat_needed = self.concat_sets != None and len(self.concat_sets) > 0
            forced_concat = 'fidl' in self.output_formats # fidl has to have concatenated runs
            event_lists = []
            durations = []
            r = 0
            for i, file_rows in enumerate(data_runs_separated):
                for run_rows in file_rows:
                    self.handle_run_start(r, run_rows, raw_bs[i])
                    es = self.events_for_rows(run_rows)
                    if es == None:
                        es = []
                    event_lists.append(es)
                    # if we're going to concat, we'll need a duration for each of the files
                    if concat_needed or forced_concat:
                        durations.append(self.duration_for_run(r, raw_bs[i], data[i], es))
                    self.handle_run_end(r, run_rows, raw_bs[i])
                    r += 1
            # make sure all of the events belong to a set
            check_events_for_set_names(event_lists)
            # get all of the unique event set names
            eset_names = get_all_event_set_names(event_lists)
            # make a dict whose keys are set names, and whose values are lists of lists of event dicts
            event_sets = events_to_event_sets(event_lists, eset_names)
            # concatenate any sets that need concatenation
            forced_concat_events = {}
            if forced_concat:
                for set_name in event_sets.keys():
                    forced_concat_events[set_name] = concat_event_lists(event_sets[set_name], durations)
            if concat_needed:
                for set_name in event_sets.keys():
                    if not set_name in self.concat_sets:
                        continue
                    event_sets[set_name] = concat_event_lists(event_sets[set_name], durations)
            # write each of the requested file formats, plus a pickle format
            if not self.skip_output:
                self.event_files[sub] = {}
                for set_name in event_sets.keys():
                    self.event_files[sub][set_name] = {}
                    set_dir = os.path.join(sub_dir, set_name)
                    ensure_dir(set_dir)
                    ofs = self.output_formats
                    if not 'pickle' in ofs:
                        ofs.append('pickle')
                    for format in ofs:
                        ev_files = FileWriter.write_set(format,
                                             event_sets[set_name],
                                             set_dir,
                                             forced_concat_events.get(set_name,None),
                                             **self.get_write_args())
                    self.event_files[sub][set_name][format] = ev_files
            self.sub_data[sub] = event_sets
        self.current_sub = None

    def separate_runs(self, dict_list):
        if self.run_field == None or self.run_field not in dict_list[0].keys():
            return [dict_list]
        r_val = dict_list[0][self.run_field]
        runs = [[]]
        for d in dict_list:
            if d[self.run_field] != r_val:
                r_val = d[self.run_field]
                runs.append([])
            runs[-1].append(d)
        return runs

    def check_settings(self):
        if self.output_dir == None:
            raise ValueError("output_dir must be set")
        if self.data_glob_templates == None:
            raise ValueError("data_glob_templates must be set")
        if self.output_formats == None:
            raise ValueError("output_formats must be set")
        if self.subjects == None or len(self.subjects) == 0:
            raise ValueError("no subjects to convert...")
        pass

    def pre_subj_setup(self):
        self._run_num = 0

    """ OVERRIDE IN SUBCLASSES """

    def events_for_rows(self, rows):
        """ events_for_rows() should return a list of dictionaries with the keys:
        {set:(string) name:(string), onset:(float)seconds, duration:(float)seconds}
        'set' is the name of the event set. sets will be saved into separate folders.
        This is so you can use one EventBuilder to create multiple event sets, for 
        example, you might want one set listing all events with duration 0, and another
        that lists block events with their true durations.
        The rows will always be from the same trial.
        """
        raise NotImplementedError()

    def duration_for_run(self, run_idx, file_name, raw_rows, events):
        """ return duration of the given run in seconds.
        only needed if you're concatenating files, or using fidl output
        """
        raise NotImplementedError()

    def get_write_args(self):
        """return a dict of extra args to be passed to write_set().
        eg. 'tr' if you want to write fidl files
        """
        return {}

    def handle_run_start(self, run_idx, run_data, file_name):
        """do anything you need to do at the start of a run.
        a good example is setting aside some time that you'd like to use as
        the run's '0' point, which you'll subtract from the onset time of all
        events in the run.
        """
        pass

    def handle_run_end(self, run_idx, run_data, file_name):
        """do anything you need to do at the end of a run."""
        pass

class fMRI_EventBuilder(EventBuilder):
    """a variant with some features specific to fMRI.
    These include the use of TR to calculate run durations, and passing
    TR to write_set so we can write fidl files.
    """
    def __init__(self,*args,**kwargs):
        self.TR = None
        super(fMRI_EventBuilder, self).__init__(*args, **kwargs)

    def duration_for_run(self, run_idx, file_name, raw_rows, events):
        return self.tr_count_for_run(run_idx, file_name, raw_rows, events) * self.get_tr()

    def get_write_args(self):
        return {'tr':self.get_tr()}

    """ OVERRIDE IN SUBCLASSES """

    def tr_count_for_run(self, run_idx, file_name, raw_rows, events):
        """ return the TR count for the given run. """
        raise NotImplementedError()

    def get_tr(self):
        """ return the TR used for bold runs """
        if not self.TR:
            raise ValueError("TR must not be None")
        return self.TR

class TrialWise_EventBuilder(EventBuilder):
    """a variant that collects events by run.
    
    Main changes are that you should override events_for_trial() as your main
    event returning method, and you can provide a value for trial_field to
    separate each run into trials, the same way the main class uses run_field
    to separate runs.
    
    """
    trial_field = None
    def events_for_rows(self, rows):
        es = []
        trials = self.separate_trials(rows)
        for i, t in enumerate(trials):
            t_es = self.events_for_trial(i, t)
            if t_es != None and len(t_es) > 0:
                es.extend(t_es)
        return es

    def separate_trials(self, dict_list):
        if self.trial_field == None or self.trial_field not in dict_list[0].keys():
            return [dict_list]
        r_val = dict_list[0][self.trial_field]
        runs = [[]]
        for d in dict_list:
            if d[self.trial_field] != r_val:
                r_val = d[self.trial_field]
                runs.append([])
            runs[-1].append(d)
        return runs

    """ OVERRIDE IN SUBCLASSES """

    def events_for_trial(self, trial_idx, trial_rows):
        raise NotImplementedError()
        
class RowWise_EventBuilder(EventBuilder):
    """a variant that collects events by row.
    Take note that this is a subclass of Runwise_EventBuilder, so you also
    have the option to implement handle_run_start() and handle_run_end().
    # TODO: More doco on how to subclass.
    """
    def events_for_rows(self, rows):
        es = []
        for r in rows:
            r_es = self.events_for_row(r)
            if r_es != None and len(r_es) > 0:
                es.extend(r_es)
        return es

    """ OVERRIDE IN SUBCLASSES """

    def events_for_row(self, row_dict):
        """return an array containing any number of events.
        This is the heart of this class. We'll call this from within
        events_for_rows(). You might use this method to check the row for values
        that signify an event of interest, its onset time, and its duration.
        """
        return []

class RowWise_fMRI_EventBuilder(fMRI_EventBuilder, RowWise_EventBuilder):
     """a variant that combines rowwise and fmri-specific features
     The choice you'll probably want to make if you're implementing a behavioral
     log parser as part of an fMRI experiment. You'll most likely want to override
     events_for_row() and perhaps handle_run_start(). See doco on the two
     superclasses FMI.
     """
     def __init__(self):
         super(RowWise_fMRI_EventBuilder, self).__init__()
    
class FixedDuration_EventBuilder(RowWise_EventBuilder):
    """A simple event builder that handles well ordered tabular events.

    Still in testing.

    parameters
    ----------
    # TODO: document parameters
    """
    def __init__(self, duration=1.0, run_onset_cols=[], onset_cols=[], onset_func=None, name_cols=[], name_func=None, keep_names=None):
        super(FixedDuration_EventBuilder,RowWise_EventBuilder).__init__()
        self.duration = duration
        self.run_onset_cols = run_onset_cols
        self.onset_cols = onset_cols
        self.name_cols = name_cols
        self.name_func = name_func
        self.keep_names = keep_names
        # set at the start of each run:
        self.run_onset = 0

    def events_for_row(self, row_dict):
        # get onset, apply onset_func if needed
        onset = first_from_row(row_dict, self.onset_cols, float)
        if onset and self.onset_func:
            onset = self.onset_func(onset)
        # get name, using first value, or passing all found values to name_func
        if not self.name_func:
            name = first_from_row(row_dict, self.name_cols)
        else:
            parts = []
            for n in self.name_cols:
                parts.append(row_dict.get(n, None))
                name = self.name_func(*parts)
        # if you're only keeping some names, ignore those you don't care about
        if not name or not onset or (self.keep_names and not name in self.keep_names):
            return
        # build the event
        return [{"name":name,"onset":onset,"duration":self.duration}]

    def handle_run_start(self, run_idx, run_data, file_name):
        if not self.run_onset_cols or not len(run_data) > 0:
            self.run_onset = 0
        else:
            self.run_onset = first_from_row(run_data[0], self.run_onset_cols, func=float)
        if self.onset_func:
            self.run_onset = self.onset_func(self.run_onset)

def first_from_row(row, cols_names, func=None):
    val = None
    if not row or not cols_names:
        return val
    for c in self.cols_names:
        if not c in row or not row[c]:
            continue
        o = row[c]
        if func:
            try:
                o = func(c)
            except Exception, e:
                continue
        val = o
        break
    return val

def events_to_event_sets(dict_lists, set_names):
    sets = {}
    for s_name in set_names:
        sets[s_name] = []
    for d_list in dict_lists:
        for s_name in set_names:
            sets[s_name].append([])
        for d in d_list:
            dc = dict(d)
            s = dc['set']
            del dc['set']
            sets[s][-1].append(dc)
    return sets

def get_all_event_set_names(dict_lists):
    names = []
    for d_list in dict_lists:
        for d in d_list:
            if d['set'] not in names:
                names.append(d['set'])
    return names

def check_events_for_set_names(dict_lists):
    if not all(['set' in d for d_list in dict_lists for d in d_list]):
        raise ValueError('All events must have a value for key "set". '+
                         'Check your event definitions!')

def concat_event_lists(event_lists, durations):
    new_list = []
    d = 0
    for i, e_list in enumerate(event_lists):
        if i > 0:
            d += durations[i-1]
        for e in e_list:
            ec = dict(e)
            ec['onset'] += d
            new_list.append(ec)
    return [new_list]

