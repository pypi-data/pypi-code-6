# pylint: disable=W0105, W1401
"""
This module contains configuration details for the `LaZy_NT` package. There
are four types of information within:

* File signature definitions
* ASCII string template definitions
* Command line option defaults
* Package-wide globals, shared across all `LaZy_NT` modules

### Note:
`LaZy_NT.config.Signature` definitions should be kept to 8 bytes or fewer
wherever possible, as longer signatures will be broken up by compression
metadata when stored on a compressed volume. Additionally the signature
itself is more likely to be stored compressed, thus unrecognizable, the
longer it is.

If a signature longer than 8 bytes must be defined, or one with three
or more identical bytes in sequence, the signature should be defined
as it would be stored on a compressed volume (ie: with tag bytes and
tuples in appropriate positions). Otherwise the only way to recognize
the signature will be through the `double-carve` processing option.
"""

# Command line argument defaults
options = {
    'images' : None,
    'ascii' : False,
    'chunk_size' : 512,
    'database' : False,
    'deep_carve' : False,
    'double_carve' : False,
    'metadata' : False,
    'keep_raw' : True,
    'no_carve' : False,
    'outdir' : "LaZy_NT_out",
    'unc_image' : False,
    'val_files' : False,
    'verbose' : 0
}
"""
(dict): Contains the current option settings for all program options.

### Keys:
* **images (list of str):** A list of fully qualified paths to each of the
image files to be processed.
* **ascii (bool):** Enables ASCII string extraction and raw ASCII carving.
* **chunk_size (int):** Indicates the chunk size to use while parsing the
image file.
* **database (bool):** Enables sqlite database output.
* **deep_carve (bool):** Must be enabled if either 'double carve' or 'ascii'
options are enabled.
* **double_carve (bool):** Enables double carving of the decompressed stream.
* **metadata (bool):** Enables post-processing of carved files to extract
metadata.
* **keep_raw (bool):** Enables preservation of intermediate raw data files when
'double carve' or 'ascii' are enabled.
* **no_carve (bool):** Disables carving to disk.
* **outdir (str):** Fully qualified path of the output directory.
* **unc_image (bool):** Disables compression detection for uncompressed images.
* **val_files (bool):** Enables post-processing file validation and deletion
of invalid files.
* **verbose (int):** Enables verbose output levels 1 through 3.
"""
# Output file handle placeholders (shared globals)
audit = None
"""(str): Filename of the audit log."""
sqldb = None
"""(str): Filename of the audit database, if one was created."""
ascii_raw_log = None
"""(str): Filename of the raw ASCII file log, if one was created."""
deep_raw_log = None
"""(str): Filename of the raw deep carving log, if one was created."""

class Signature(object):
    """
    Represent a file signature that should be carved if detected within
    the disk image file.
    """
    def __init__(self, file_type, signature,
                 stop_sig="", deep_flag='NoDupe', deep_list=None):
        """Instantiate a file signature representation."""
        self.file_type = file_type
        """(str): The extension that should be used for this file type."""
        self.signature = signature
        """
        (str): The header bytes that indicate the beginning of a file of
        this type.
        """
        self.stop_sig = stop_sig
        """
        (str): The footer bytes that indicate the end of a file of this type.
        """
        self.deep_flag = deep_flag
        """
        (str): Indicate whether files of this type should be deep carved.
        Allows four values:

        * **False** - Never deep carve files of this type.
        * **True** - Always deep carve files of this type.
        * **NoDupe** - Only deep carve files of this type if there is not
        another `vFile` of the same type currently being carved.
        * **List** - Only deep carve files of this type if there is not
        another `vFile` of any of the types listed in `deep_list`
        currently being carved.
        """
        self.deep_list = deep_list
        """
        (list of str): Provides a list of file types to be used by the
        `deep_flag` 'List' option.
        """

class StringTemplate(object):
    """
    Represent an ASCII string type, such as an email address or URL, that
    should be extracted if detected within the disk image file.
    """
    def __init__(self, string_type, body_regex, stop_regex,
                 start_regex="".join([r'[^\x30-\x39\x41-\x5A\x61-\x7A\x7F-',
                                      r'\xFF\x01-\x08\x0B\x0C\x0E-\x1F]'])):
        """Instantiate a string template representation."""
        self.type = string_type
        """
        (str): A specific name for this `LaZy_NT.config.StringTemplate` type,
        ie: 'Email' or 'URL'.
        """
        self.start = start_regex
        """
        (str): A regular expression containing the set of characters that are
        allowed to precede a `LaZy_NT.config.StringTemplate.body` match.
        Matches are ignored if a character from this set is not found
        immediately prior.
        """
        self.body = body_regex.replace('<self.start>', self.start)
        """
        (str): A regular expression defining the character pattern(s) which
        match this template type. If the pattern contains the substring
        '<self.start\>', this substring is replaced with the value of
        `LaZy_NT.config.StringTemplate.start`.
        """
        self.stop = stop_regex
        """
        (str): A regular expression containing the set of characters that are
        disallowed within the `LaZy_NT.config.StringTemplate.body` of this
        string type. Acts like a file's stop signature, to indicate the end of
        a string of this type.
        """

# Signatures are sorted by length for higher priority matching
signatures = [
    # --- 8 ---
    Signature('bat', '@echo of'),
    Signature('doc', chr(0xD0) + chr(0xCF) + chr(0x11) + chr(0xE0) +
              chr(0xA1) + chr(0xB1) + chr(0x1A) + chr(0xE1)),
    Signature('docx', 'PK' + chr(0x03) + chr(0x04) + chr(0x14) + chr(0x00) +
              chr(0x06) + chr(0x00),
              'PK' + chr(0x05) + chr(0x06) + chr(0x00) + chr(0x00) +
              chr(0x00) + chr(0x00),
              deep_flag='List', deep_list=['docx', 'zip']),
    Signature('png', chr(0x89) + 'PNG' + chr(0x0D) + chr(0x0A) +
              chr(0x1A) + chr(0x0A),
              'IEND' + chr(0xAE) + chr(0x42) + chr(0x60) + chr(0x82)),
    Signature('rar', 'Rar!' + chr(0x1A) + chr(0x07) + chr(0x01) + chr(0x00)),
    # --- 7 ---
    Signature('rar', 'Rar!' + chr(0x1A) + chr(0x07) + chr(0x00)),
    # --- 6 ---
    Signature('gif', 'GIF87a', chr(0x00) + chr(0x3B)),
    Signature('gif', 'GIF89a', chr(0x00) + chr(0x3B)),
    Signature('rtf', chr(0x7B) + chr(0x5C) + 'rtf1',
              chr(0x5C) + 'par' + chr(0x0A) + '}}'),
    Signature('xml', '<?xml ', deep_flag='List',
              deep_list=['xml', 'docx', 'zip']),
    # --- 5 ---
    Signature('html', '<html', '</html>'),
    # --- 4 ---
    Signature('class', chr(0xCA) + chr(0xFE) + chr(0xBA) + chr(0xBE)),
    Signature('pdf', '%PDF', deep_flag=True),
    Signature('ps', '%!PS'),
    Signature('psd', '8BPS'),
    Signature('tif', 'II*' + chr(0x00)),
    Signature('zip', 'P' + 'K' + chr(0x03) + chr(0x04),
              deep_flag='List', deep_list=['docx', 'zip']),
    # --- 3 ---
    Signature('jpg', chr(0xFF) + chr(0xd8) + chr(0xFF),
              chr(0xFF) + chr(0xD9), deep_flag=True),
    Signature('sh', '#!/', deep_flag=False),
    Signature('tif', 'I I', deep_flag=False),
    Signature('txt', chr(0xEF) + chr(0xBB) + chr(0xBF), deep_flag=False),
    # --- 2 ---
    Signature('bmp', 'BM', deep_flag=False)
]
"""
(list of `LaZy_NT.config.Signature`): These file signatures will be searched
for within the disk image file.
"""

templates = [
    # Email addresses. This regex was created through trial and
    # error based on RFC specifications.
    StringTemplate('Email', body_regex=r'[^@\x00-\x20\x7F-\xFF]+@' \
                   '[\x28\x29\x2D\x2E\x30-\x39\x41-\x5A\x61-\x7A]+\.' \
                   '[\x28\x29\x2D\x2E\x30-\x39\x41-\x5A\x61-\x7A]+',
                   stop_regex=r'[^\x21-\x7E]'),
    # URL-like sequences. This regex is a simplification of one created by
    # Matthew O'Riordan:  http://blog.mattheworiordan.com/post/13174566389/
    StringTemplate('URL', body_regex=r'((([A-Za-z]{3,6}:(?:\/\/))' \
                   '[A-Za-z0-9\.\-]+|(?:www\.)[A-Za-z0-9\.\-]+)' \
                   '((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)' \
                   '#?(?:[\.\!\/\\\w]*))?)',
                   stop_regex=r'[^\x2E-\x3A\x41-\x5A\x61-\x7A]'),
    # Telephone-like sequences. Created through trial and error.
    StringTemplate('Phone', body_regex=r'\(?([2-9][0-9]{2})\)?[-. ]?' \
                   '([0-9]{3})[-. ]?([0-9]{4})([-. xX]+[0-9]{1,6})?' \
                   '[^\x30-\x39]{2}',
                   stop_regex=r'[^\x20\x28\x29\x2D\x58\x78\x30-\x39]'),
    # SSN-like sequences. This regex is heavily based on one created by
    # Rion Williams:  http://rionscode.wordpress.com/2013/09/10/
    StringTemplate('SSN', body_regex=r'((?!219-09-9999|078-05-1120)' \
                   '(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4})' \
                   '[^\x2D\x30-\x39]|' + '<self.start>' + \
                   r'((?!219099999|078051120)(?!666|000|9\d{2})\d{3}(?!00)' \
                   '\d{2}(?!0{4})\d{4})[^\x2D\x30-\x39]',
                   stop_regex=r'[^\x2D\x30-\x39]'),
    # Credit card-like sequences. Heavily modified based on examples from:
    # http://www.regular-expressions.info/creditcard.html
    StringTemplate('CCN', body_regex=r'(?:4(?:[0-9][ -]*?){12}(?:(?:[0-9]' \
                   '[ -]*?){3})?|5[1-5](?:[0-9][ -]*?){14}|3[47](?:[0-9]' \
                   '[ -]*?){13}|3(?:0[0-5]|[68][0-9])(?:[0-9][ -]*?){11}|' \
                   '6(?:011|5[0-9]{2})(?:[0-9][ -]*?){12}|'
                   '(?:2131|1800|35\d{2})(?:[0-9][ -]*?){11})[^\x30-\x39]{2}',
                   stop_regex=r'[^\x20\x2D\x30-\x39]')
]
"""
(list of `LaZy_NT.config.StringTemplate`): These string templates will be
searched for within the disk image file.
"""

histogram = {
    'Email' : {},
    'URL' : {},
    'Phone' : {},
    'SSN' : {},
    'CCN' : {}
}
"""
(dict of (dict of int)): Contains the count of each ASCII string extracted
from the disk image file. Outer dict contains one key for each
`LaZy_NT.config.StringTemplate` type defined in `LaZy_NT.config.templates`,
(ie: 'Email', 'URL', etc.). Inner dict keys are created for each unique
`vString` `data` attribute, and the value is the occurence count of that
`vString`. (eg: histogram[Email][JohnDoe@gmail.com] might equal 3).
"""
