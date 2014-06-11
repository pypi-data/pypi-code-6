from util import *
import os

# NOTE: all events should have onsets and durations in seconds. change to in ms as needed.

class FileWriter(object):
    """Abstract class for file writers.

    Subclasses should override supported_format() to return the string name of
    the format they support (this can be any arbitrary name, but should be
    something sensible). They should also override write_file().

    """
    format_output_dir = None
    @classmethod
    def write_set(cls, format, event_lists, output_dir, forced_concat_events, **kwargs):
        subs = [SPM_FileWriter, FIDL_FileWriter, Pickle_FileWriter, TDF_FileWriter]
        writer = None
        for sub in subs:
            if format == sub.supported_format():
                writer = sub
                break
        if writer == None:
            raise ValueError("Could not find valid writer for format %s" % format)
        if writer.requires_concat():
            event_lists = forced_concat_events
        writer = writer()
        new_files = []
        for i, event_list in enumerate(event_lists):
            idx = i
            if len(event_lists) == 1:
                idx = None
            file_path = writer.write_file(event_lists[i], output_dir, idx, **kwargs)
            if file_path:
                new_files.append(file_path)
        return new_files

    """Override in subclasses"""
    @classmethod
    def supported_format(cls):
        return NotImplementedError()
    @classmethod
    def requires_concat(cls):
        return False
    def write_file(self, event_list, output_dir, idx=None):
        """ Empty implementation of the main file writing method.

        Parameters
        ----------
        event_list (list of dicts)
            The events to be written.
        output_dir (path to directory)
            Directory in which files should be written.
        idx (int)
            The run index of the current file, or None.

        Returns
        -------
        file_list (list of paths)
            The full path of the file that was written.
        """
        return NotImplementedError()

class SPM_FileWriter(FileWriter):
    """writer of spm event files"""
    @classmethod
    def supported_format(cls):
        return 'spm'
    def write_file(self, event_list, output_dir, idx=None, **kwargs):
        import os
        from scipy.io import savemat
        import numpy as np
        import warnings
        warnings.simplefilter("ignore")
        # make sure there's an spm dir to write to
        od = os.path.join(output_dir, 'spm')
        ensure_dir(od)
        f_name = 'events'
        if idx != None:
            f_name += '_' + str(idx)
        f_name += '.mat'
        out_path = os.path.join(od, f_name)
        # TODO: get the data into spm format, write the file
        names = []
        onsets = []
        durations = []
        for e in event_list:
            if [e['name']] not in names:
                names.append([e['name']])
                onsets.append([])
                durations.append([])
            d = names.index([e['name']])
            onsets[d].append([e['onset']])
            durations[d].append([e['duration']])
        names = np.array([names], dtype=object)
        onsets = np.array([onsets], dtype=object)
        durations = np.array([durations], dtype=object)
        savemat(out_path, mdict={'names':names, 'onsets':onsets, 'durations':durations})
        return os.path.abspath(out_path)


class FIDL_FileWriter(FileWriter):
    """writer of fidl event files"""
    @classmethod
    def supported_format(cls):
        return 'fidl'
    @classmethod
    def requires_concat(cls):
        return True
    def write_file(self, event_list, output_dir, idx=None, **kwargs):
        # for fidl, we have to have a tr
        tr = kwargs.get('tr', None)
        if tr == None:
            raise ValueError("fidl output requires a TR")
        # make sure there's a fidl dir to write to
        od = os.path.join(output_dir, 'fidl')
        ensure_dir(od)
        f_name = 'events'
        if idx != None:
            f_name += '_' + str(idx)
        f_name += '.fidl'
        out_path = os.path.join(od, f_name)
        lines = []
        e_names = {}
        for e in event_list:
            if not e['name'] in e_names.keys():
                d = len(e_names)
                e_names[e['name']] = d
            else:
                d = e_names[e['name']]
            lines.append('%.2f %d %.2f' % (e['onset'], d, e['duration']))
        e_names = sorted(['%d_%s' % (e_names[key], key) for key in e_names.keys()])
        lines.insert(0, '%.2f %s\n' % (tr, ' '.join(e_names)))
        with open(out_path, 'w') as f:
            for line in lines:
                print>>f, line
        return os.path.abspath(out_path)

class Pickle_FileWriter(FileWriter):
    """writer of spm event files"""
    @classmethod
    def supported_format(cls):
        return 'pickle'
    def write_file(self, event_list, output_dir, idx=None, **kwargs):
        import cPickle
        # make sure there's a fidl dir to write to
        od = os.path.join(output_dir, 'pickle')
        ensure_dir(od)
        f_name = 'events'
        if idx != None:
            f_name += '_' + str(idx)
        f_name += '.pkl'
        out_path = os.path.join(od, f_name)
        with open(out_path, 'wb') as f:
            cPickle.dump(event_list, f)
        return os.path.abspath(out_path)

class TDF_FileWriter(FileWriter):
    """writer of tdf .txt files"""
    @classmethod
    def supported_format(cls):
        return 'txt'
    def write_file(self, event_list, output_dir, idx=None, **kwargs):
        from csv import DictWriter, excel_tab
        # flatten
        cols = []
        for ev in event_list:
            cols += [k for k in ev.keys() if not k in cols]
        # make sure there's a fidl dir to write to
        od = os.path.join(output_dir, 'txt')
        ensure_dir(od)
        # save
        f_name = 'events'
        if idx != None:
            f_name += '_' + str(idx)
        f_name += '.txt'
        out_path = os.path.join(od, f_name)
        cols.sort()
        with open(out_path, 'wb') as out_file:
            dw = DictWriter(out_file,
                            cols,
                            restval='',
                            extrasaction='raise',
                            dialect=excel_tab)
            dw.writer.writerow(cols)
            dw.writerows(event_list)
        return os.path.abspath(out_path)

