# -*- coding: utf-8 -*-

import csv
import os


REPLACE_CHARS = ['@', '-', '_', '+', '.', '~', '`', '!', '#', '$', '%', '^',
                 '&', '*', '(', ')', '=', '{', '}', '[', ']', '|', '\\', ':',
                 ';', '\'', '"', '<', '>', ',', '/', '?']


# ---------------------
# csvcleaner.csvcleaner
# ---------------------
class CSVCleaner(object):
    """
    CSV Cleaner.

    Removes rows containing blacklisted words from a CSV file.

    Parameters
    ----------
    blacklist : list
    replace_chars : list
    configure : bool
    lowercase : bool
    strict : bool

    Example
    -------
    >>> import csvcleaner
    >>> f = csvcleaner.CSVCleaner()
    >>> f.run('/path/to/file.csv')

    Notes
    -----
    See `README.md` for a more detailed explanation of each parameter.
    """
    def __init__(self, blacklist=[], replace_chars=[], configure=True,
                 lowercase=True, strict=False):

        self.blacklist = blacklist
        self.replace_chars = replace_chars
        self.configure = configure
        self.lowercase = lowercase
        self.strict = strict

    def _configure(self):
        """
        Configure defaults for `replace_chars` and `blacklist`. Only empty
        lists will be modified.
        """
        if not self.replace_chars:
            self.replace_chars = REPLACE_CHARS

        if not self.blacklist:
            path = os.path.join(os.path.dirname(__file__), 'blacklist', 'en')
            with open(path, 'rU') as f:
                self.blacklist = map(str.strip, f)

    def _files(self, path, name):
        """
        Create `[name]-accepted.csv` and `[name]-rejected.csv` files. Files are
        saved in the file directory referenced within `run`.

        Parameters
        ----------
        path : str
            Absolute path to the directory where CSV files will be stored.
        name : str
            Name of CSV file.

        Returns
        -------
        accepted : writer object
        rejected : writer object
        """
        path = os.path.dirname(path)
        accepted = csv.writer(open('{}/{}-accepted.csv'.format(path, name), 'w'))
        rejected = csv.writer(open('{}/{}-rejected.csv'.format(path, name), 'w'))
        return accepted, rejected

    def _lowercase(self, string):
        """
        Converts `string` and `self.blacklist` to lowercase. This offers more
        accurate word detection as case is ignored.

        Parameters
        ----------
        string : str

        Returns
        -------
        string : str
        """
        self.blacklist = [x.lower() for x in self.blacklist]
        return string.lower()

    def _replace_chars(self, string):
        """
        Replace characters. Instead of removing the character, it's replaced
        with a space. This offers more accurate word detection -- especially
        in common cases such as email addresses, urls and hyphenated words.

        Parameters
        ----------
        string : str

        Returns
        -------
        str
        """
        return [string.replace(x, ' ') for x in self.replace_chars][0]

    def _clean(self, row):
        """
        Clean string. Convert row into a string and transform the string for
        more accurate word detection.

        Parameters
        ----------
        row : list

        Returns
        -------
        string : str
        """
        string = ' '.join(row)
        string = self._replace_chars(string)  # todo: catch exceptions

        if self.lowercase:
            string = self._lowercase(string)  # todo: catch exceptions

        return string

    def _test(self, row):
        """
        Test a row to see if it should be accepted or rejected.

        Parameters
        ----------
        row : list

        Returns
        -------
        dict
        """
        string = self._clean(row)

        for word in self.blacklist:
            if word in string:

                # Fuzzy match. `string` may contain a word in the blacklist.
                # However, since strict is true, remove the row.
                if self.strict:
                    return {'passed': False, 'word': word}

                # `string` may contain a word in the blacklist. Since strict is
                # false, perform further analysis on the string.
                else:
                    for s in string.split():
                        if s == word:
                            return {'passed': False, 'word': word}

        # `string` either didn't contain a word in the blacklist or the word
        # couldn't be matched through further analysis.
        return {'passed': True}

    def run(self, path, headers=True, name='csv'):
        """
        Run `CSV Cleaner` against a CSV file.

        Parameters
        ----------
        path : str
            Absolute path to a valid CSV file.
        headers : bool
            Set to `True` if CSV contains a header row. Set to `False` if CSV
            file does not contain a header row.
        name : str
            Name prefix for CSV files generated by `CSV Cleaner`.
        """
        # Run base configuration.
        if self.configure:
            self._configure()

        # Process CSV.
        with open(path, 'rU') as f:
            reader = csv.reader(f)
            accepted, rejected = self._files(f.name, name)

            if headers:
                headers = reader.next()
                accepted.writerow(headers)
                rejected.writerow(['row', 'word'] + headers)

            for line, row in enumerate(reader):
                result = self._test(row)

                # Passed. Record in `[name]-accepted.csv`.
                if result['passed']:
                    accepted.writerow(row)

                # Failed. Record in `[name]-rejected.csv`.
                else:
                    rejected.writerow([line, result['word']] + row)
