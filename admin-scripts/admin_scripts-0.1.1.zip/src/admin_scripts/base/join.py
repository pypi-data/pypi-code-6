#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Administration Scripts.
#
# Hive Administration Scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Administration Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Administration Scripts. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re
import os
import sys
import zlib
import time
import json
import struct
import getopt

import legacy

DEFAULT_COMPRESSION_LEVEL = 9
""" The default compression level """

def javascript_minify(string_value):
    """
    "Minifies" the given string value assuming it
    contains javascript code in it.
    The heuristics used in the minification should not
    change the normal behavior of the file.

    @type string_value: String
    @param string_value: The string containing the value
    to be minified.
    @rtype: String
    @return: The minified string value.
    """

    # creates a new string buffer with the given
    # string value (for the input) and then creates
    # new empty string buffer for the result
    string_buffer = legacy.StringIO(string_value)
    string_buffer_result = legacy.StringIO()

    # creates a new javascript minify object
    # and runs the minification
    javascript_minify = JavascriptMinify()
    javascript_minify.minify(string_buffer, string_buffer_result)

    # retrieves the string value (result) from the
    # string buffer
    string_value_result = string_buffer_result.getvalue()

    # in case the string value of result is valid and starts
    # with a newline character (need to strip)
    if string_value_result and string_value_result[0] == '\n':
        # removes the newline character from the string value
        string_value_result = string_value_result[1:]

    # returns the string value
    # for the result
    return string_value_result

def is_alpha(character):
    """
    Checks if the given character represents an alphabet
    letter.

    @rtype: bool
    @return: If the given character represents an alphabet
    letter.
    """

    return ((character >= "a" and character <= "z") or (character >= "0" and character <= "9") or
            (character >= "A" and character <= "Z") or character == "_" or character == "$" or character == "\\" or (character is not None and ord(character) > 126));

class JavascriptMinify:
    """
    Class used to minify javascript code.
    The minification is done using a classic
    parsing approach.
    """

    def _out_a(self):
        """
        Outputs the "first" value to the output
        file buffer.
        This method works like a flushing utility
        for the first value.
        """

        self.output_file.write(self.theA)

    def _out_b(self):
        self.output_file.write(self.theB)

    def _get(self):
        """
        return the next character from stdin. Watch out for lookahead. If
        the character is a control character, translate it to a space or
        linefeed.
        """

        # tries to retrieves the character
        # from the look ahead and then unsets
        # the look ahead
        character = self.look_ahead
        self.look_ahead = None

        # in case the look ahead character is not
        # found (need to read from the input file
        # buffer)
        if character == None:
            # reads a character from the input
            # file buffer
            character = self.input_file.read(1)

        # in case the character is a "normal" alpha
        # numeric character
        if character >= " " or character == "\n":
            # returns the character
            return character

        # in case not character is found
        # end of file is reached
        if character == "":
            # returns the end of string character
            return "\0"

        # in case the character is a carriage return
        # (windows newline present)
        if character == "\r":
            # returns "just" the normal
            # newline character
            return "\n"

        # as a "failover" return the space
        # character
        return " "

    def _peek(self):
        # retrieves the current item from
        # the input buffer
        self.look_ahead = self._get()

        # returns the look ahead character
        # as the "read" character
        return self.look_ahead

    def _next(self):
        """
        get the next character, excluding comments. peek() is used to see
        if a '/' is followed by a '/' or '*'.
        """

        # retrieves the current character
        # (removes the character from "input buffer")
        character = self._get()

        # in case the current character represents
        # a possible comment character (possible
        # line removal)
        if character == "/":
            # peeks the next character to be sure
            # that this is a comment
            next_character = self._peek()

            if next_character == "/":
                character = self._get()

                while character > "\n":
                    character = self._get()

                return character

            if next_character == "*":
                character = self._get()

                # iterates continuously
                while True:
                    character = self._get()

                    if character == "*":
                        if self._peek() == "/":
                            self._get()
                            return " "

                    if character == "\0":
                        # raises a runtime error
                        raise RuntimeError("unterminated comment")

        # returns the current character
        return character

    def _action(self, action):
        """
        do something! What you do is determined by the argument:
        1   Output A. Copy B to A. Get the next B.
        2   Copy B to A. Get the next B. (Delete A).
        3   Get the next B. (Delete B).
        action treats a string as a single character. Wow!
        action recognizes a regular expression if it is preceded by ( or , or =.
        """

        if action <= 1:
            self._out_a()

        if action <= 2:
            self.theA = self.theB
            if self.theA == "'" or self.theA == '"':
                while True:
                    self._out_a()
                    self.theA = self._get()
                    if self.theA == self.theB:
                        break
                    if self.theA <= '\n':
                        # raises a runtime error
                        raise RuntimeError("unterminated string literal")
                    if self.theA == '\\':
                        self._out_a()
                        self.theA = self._get()

        if action <= 3:
            self.theB = self._next()

            if self.theB == '/' and (self.theA == '(' or self.theA == ',' or
                self.theA == '=' or self.theA == ':' or
                self.theA == '[' or self.theA == '?' or
                self.theA == '!' or self.theA == '&' or
                self.theA == '|' or self.theA == ';' or
                self.theA == '{' or self.theA == '}' or
                self.theA == '\n'):
                self._out_a()
                self._out_b()

                # iterates continuously
                while True:
                    self.theA = self._get()
                    if self.theA == '/':
                        break
                    elif self.theA == '\\':
                        self._out_a()
                        self.theA = self._get()
                    elif self.theA <= '\n':
                        # raises a runtime error
                        raise RuntimeError("unterminated regular expression")
                    self._out_a()

                self.theB = self._next()


    def _jsmin(self):
        """Copy the input to the output, deleting the characters which are
           insignificant to JavaScript. Comments will be removed. Tabs will be
           replaced with spaces. Carriage returns will be replaced with linefeeds.
           Most spaces and linefeeds will be removed.
        """
        self.theA = '\n'
        self._action(3)

        while self.theA != '\0':
            if self.theA == ' ':
                if is_alpha(self.theB):
                    self._action(1)
                else:
                    self._action(2)
            elif self.theA == '\n':
                if self.theB in ['{', '[', '(', '+', '-']:
                    self._action(1)
                elif self.theB == ' ':
                    self._action(3)
                else:
                    if is_alpha(self.theB):
                        self._action(1)
                    else:
                        self._action(2)
            else:
                if self.theB == ' ':
                    if is_alpha(self.theA):
                        self._action(1)
                    else:
                        self._action(3)
                elif self.theB == '\n':
                    if self.theA in ['}', ']', ')', '+', '-', '"', '\'']:
                        self._action(1)
                    else:
                        if is_alpha(self.theA):
                            self._action(1)
                        else:
                            self._action(3)
                else:
                    self._action(1)

    def minify(self, input_file, output_file):
        # sets the file values
        self.input_file = input_file
        self.output_file = output_file

        #
        self.theA = '\n'
        self.theB = None
        self.look_ahead = None

        # runs the minification
        self._jsmin()

        # closes the input file
        self.input_file.close()




def uniqify(all):
    """ borrowed from Tim Peters' algorithm on ASPN Cookbook """
    # REMEMBER! This will shuffle the order of the list
    u = {}
    for each in all:
        u[each]=1
    return u.keys()

def simplifyHexColours(text):
    """ Replace all colour declarations where pairs repeat.
    I.e. #FFFFFF => #FFF; #CCEEFF => #CEF
    and #EFEFEF, #EFCDI9 avoided """
    colour_replacements = {}
    all_hex_encodings = hex_colour.findall(text)

    for e in uniqify(all_hex_encodings):
        if e[1]==e[2] and e[3]==e[4] and e[5]==e[6]:
            colour_replacements[e] = '#'+e[1]+e[3]+e[5]

    for k, v in colour_replacements.items():
        text = text.replace(k, v)

    return text

# CSS
css_comments = re.compile(r'/\*.*?\*/', re.MULTILINE|re.DOTALL)
hex_colour = re.compile(r'#\w{2}\w{2}\w{2}')

def _css_slimmer(css):
    """ remove repeating whitespace ( \t\n) """

    #css = css_comments.sub('', css) # remove comments
    remove_next_comment = 1
    for css_comment in css_comments.findall(css):
        if css_comment[-3:]=='\*/':
            remove_next_comment=0
            continue
        if remove_next_comment:
            css = css.replace(css_comment, '')
        else:
            remove_next_comment = 1

    css = re.sub(r'\s\s+', ' ', css) # >= 2 whitespace becomes one whitespace
    css = re.sub(r'\s+\n', '', css) # no whitespace before end of line
    # Remove space before and after certain chars
    for char in ('{', '}', ':', ';', ','):
        css = re.sub(char+r'\s', char, css)
        css = re.sub(r'\s'+char, char, css)
    css = re.sub(r'\s+</',r'</', css) # no extraspace before </style>
    css = re.sub(r'}\s(#|\w)', r'}\1', css)
    css = re.sub(r';}', r'}', css) # no need for the ; before end of attributes
    css = re.sub(r'}//-->', r'}\n//-->', css)
    css = simplifyHexColours(css)

    # voice-family hack. The declation: '''voice-family: "\"}\""''' requires
    # that extra space between the ':' and the first '"' which _css_slimmer()
    # removed. Put it back (http://real.issuetrackerproduct.com/0168)
    css = re.sub(r'voice-family:"\\"}\\""', r'voice-family: "\\"}\\""', css)

    return css.strip()





USAGE_MESSAGE="join-files-python path [-r] [-w exclusion_1, exclusion_2, ...] [-c configuration_file]"
""" The usage message """

RELATIVE_BASE_PATH = "/.."
""" The relative base path """

LONG_PATH_PREFIX = "\\\\?\\".decode("utf-8")
""" The windows long path prefix """

NT_PLATFORM_VALUE = "nt"
""" The nt platform value """

DOS_PLATFORM_VALUE = "dos"
""" The dos platform value """

WINDOWS_PLATFORMS_VALUE = (
    NT_PLATFORM_VALUE,
    DOS_PLATFORM_VALUE
)
""" The windows platform value """

def normalize_path(path):
    """
    Normalizes the given path, using the characteristics
    of the current environment.
    In windows this function adds support for long path names.

    @type path: String
    @param path: The path to be normalized.
    @rtype: String
    @return: The normalized path.
    """

    # retrieves the current os name
    os_name = os.name

    # in case the current operative system is windows based and
    # the normalized path does start with the long path prefix it
    # must be removed to allow a "normal" path normalization
    if os_name in WINDOWS_PLATFORMS_VALUE and path.startswith(LONG_PATH_PREFIX):
        # removes the long path prefix from the path
        path = path[4:]

    # checks if the path is absolute
    is_absolute_path = os.path.isabs(path)

    # in case the path is not absolute (creates problem in windows
    # long path support)
    if os_name in WINDOWS_PLATFORMS_VALUE and not is_absolute_path:
        # converts the path to absolute
        path = os.path.abspath(path)

    # normalizes the path
    normalized_path = os.path.normpath(path)

    # in case the current operative system is windows based and
    # the normalized path does not start with the long path prefix
    if os_name in WINDOWS_PLATFORMS_VALUE and not normalized_path.startswith(LONG_PATH_PREFIX):
        # creates the path in the windows mode, adds
        # the support for long path names with the prefix token
        normalized_path = LONG_PATH_PREFIX + normalized_path

    # returns the normalized path
    return normalized_path

def join_files(file_path):
    """
    Removes the extra spaces or tabs in every line of the
    file contents.
    The extra argument defines if the newline format used
    should be the windows mode (carriage return and newline).

    @type file_path: String
    @param file_path: The path to the file to have the trailing
    spaces removed.
    """

    # normalizes the file path
    file_path_normalized = normalize_path(file_path)

    # opens the file for reading and then reads the
    # complete set of data contained in it
    file = open(file_path_normalized, "rb")
    try: file_contents = file.read()
    finally: file.close()

    # uses the default encoding for json to decode
    # the complete set of contents in the file
    file_contents = file_contents.decode("utf-8")

    # loads the file contents, retrieving the
    # map of files to be created from joining
    files_map = json.loads(file_contents)

    # retrieves the directory path from the normalized
    # file path (for context resolution)
    directory_path = os.path.dirname(file_path_normalized)

    # tries to retrieve the target directories
    target_directories = files_map.get("_target_directories", None)

    # in case the target directories are
    # successfully retrieved
    if target_directories:
        # removes the target directories from
        # the files map (avoids collision)
        del files_map["_target_directories"]
    # otherwise the target directories to be
    # used are the default ones
    else:
        # sets the default target directories
        target_directories = (".",)

    # iterates over all the files (composition of joined files)
    # from the files map
    for file_key, file_value in files_map.items():
        # creates the string buffer for temporary
        # file holding, this is bytes based
        string_buffer = legacy.BytesIO()

        # retrieves the current value attributes
        # (setting default values)
        files = file_value.get("files", [])
        minify = file_value.get("minify", None)
        compress = file_value.get("compress", None)

        # sets the is first flag
        is_first = True

        # iterates over all the files,
        # to be joined
        for file in files:
            # in case it's the first file
            # no need to write the separator
            if is_first: is_first = False
            # otherwise the separator must
            # be written
            else: string_buffer.write(b"\r\n")

            # retrieves the complete file path by joining the
            # directory path and the current "file"
            file_path = os.path.join(directory_path, file)
            file_path = os.path.abspath(file_path)

            # in case the file does not exists, raises an
            # error indicating that there was an error
            if not os.path.exists(file_path):
                raise RuntimeError("the file path does not exist for file '%s'" % file)

            # opens the current file for reading
            # in binary format and reads the complete
            # set of contents into the current buffer
            _file = open(file_path, "rb")
            try: file_contents = _file.read()
            finally: _file.close()

            # writes the file contents into the string
            # buffer, appending the contents to the same file
            string_buffer.write(file_contents)

        # retrieves the string value from the buffer, this is
        # a binary (byte based) string and should be used with
        # the proper care to avoid unwanted results
        string_value = string_buffer.getvalue()

        # minifies and compresses the string value
        string_value = minify == "javascript" and javascript_minify(string_value) or string_value
        string_value = minify == "css" and _css_slimmer(string_value) or string_value
        string_value = compress == "gzip" and gzip_contents(string_value) or string_value

        # iterates over all the target directories for
        # to write the contents
        for target_directory in target_directories:
            # "calculates" the (current) base file path
            base_file_directory = os.path.join(directory_path, target_directory)
            base_file_directory = os.path.abspath(base_file_directory)
            base_file_path = os.path.join(base_file_directory, file_key)

            # in case the base file directory does not exists
            # it must be created
            if not os.path.exists(base_file_directory):
                # creates the base file directory
                os.makedirs(base_file_directory)

            # opens the base file for writing in binary
            base_file = open(base_file_path, "wb")

            try:
                # writes the final string value (after minification
                # and compression) to the base file
                base_file.write(string_value)
            finally:
                # closes the base file
                base_file.close()

def gzip_contents(contents_string, file_name = None):
    """
    Compresses the given contents using the deflate compression
    algorithm and encapsulating it into the gzip file format.

    @type contents_string: String
    @param contents_string: A string containing the contents
    to be compressed.
    @type file_name: String
    @param file_name: The name to be set to the file in the
    generated compressed buffer.
    @rtype: String
    @return: The string containing the compressed buffer.
    """

    # creates a new string buffer
    string_buffer = legacy.StringIO()

    # writes the magic header and then writes the
    # compression method as part of binary header
    string_buffer.write("\x1f\x8b")
    string_buffer.write("\x08")

    # writes the flag values
    file_name and string_buffer.write("\x08") or string_buffer.write("\x00")

    # writes the timestamp value
    string_buffer.write(struct.pack("<L", legacy.LONG(time.time())))

    # writes some extra heading values
    # (includes operating system)
    string_buffer.write("\x02")
    string_buffer.write("\xff")

    # writes the file name
    file_name and string_buffer.write(file_name + "\0")

    # compresses the contents with the zlib
    contents_string_compressed = zlib.compress(contents_string, DEFAULT_COMPRESSION_LEVEL)

    # writes the the contents string compressed into the string buffer
    string_buffer.write(contents_string_compressed[2:-4])

    # computes the contents string crc 32
    # and convert it to unsigned number
    contents_string_crc32 = zlib.crc32(contents_string)
    contents_string_crc32_unsigned = _unsigned(contents_string_crc32)

    # writes the crc 32 lower values
    string_buffer.write(struct.pack("<L", contents_string_crc32_unsigned))

    # retrieves the contents string size
    # and the writes the size lower values
    contents_string_length = len(contents_string)
    contents_string_length_unsigned = _unsigned(contents_string_length)
    string_buffer.write(struct.pack("<L", contents_string_length_unsigned))

    # retrieves the string value from the string buffer
    string_value = string_buffer.getvalue()

    # returns the string value
    return string_value

def _unsigned(number):
    """
    Converts the given number to unsigned assuming
    a 32 bit value.

    @type number: int
    @param number: The number to be converted to unsigned.
    @rtype: int
    @return: The given number converted to unsigned.
    """

    # in case the number is positive or zero
    # (no need to convert)
    if number >= 0:
        # returns the immediately with
        # the current number value
        return number

    # runs the modulus in the number
    # to convert it to unsigned
    return number + 4294967296

def join_files_walker(arguments, directory_name, names):
    """
    Walker method to be used by the path walker for the joining of the files.

    @type arguments: Tuple
    @param arguments: The arguments tuple sent by the walker method.
    @type directory_name: String
    @param directory_name: The name of the current directory in the walk.
    @type names: List
    @param names: The list of names in the current directory.
    """

    # unpacks the arguments tuple
    file_exclusion, = arguments

    # removes the complete set of names that are meant to be excluded from the
    # current set names to be visit (avoid visiting them)
    for exclusion in file_exclusion:
        if not exclusion in names: continue
        names.remove(exclusion)

    # retrieves the valid names for the names list (removes directory entries)
    valid_complete_names = [directory_name + "/" + name for name in names
        if not os.path.isdir(directory_name + "/" + name)]

    # filters the names with non valid file extensions so that only the
    # ones that contain the join extension are used
    valid_complete_names = [os.path.normpath(name) for name in valid_complete_names
        if len(name.split(".")) > 1 and name.split(".")[-2] == "join"
        and name.split(".")[-1] == "json"]

    # iterates over all the valid complete names with extension filter
    for valid_complete_name in valid_complete_names:
        # print a message
        print("Joining files defined in file: %s" % valid_complete_name)

        # joins the files for the (path) name
        join_files(valid_complete_name)

def join_files_recursive(directory_path, file_exclusion):
    """
    Joins the files in recursive mode.
    All the options are arguments to be passed to the
    walker function.

    @type directory_path: String
    @param directory_path: The path to the (entry point) directory.
    @type file_exclusion: List
    @param file_exclusion: The list of file exclusion to be used.
    """

    legacy.walk(directory_path, join_files_walker, (file_exclusion,))

def _retrieve_configurations(recursive, file_exclusion, configuration_file_path):
    """
    Retrieves the configuration maps for the given arguments.

    @type recursive: bool
    @param recursive: If the removing should be recursive.
    @type file_exclsuion:
    @type file_exclusion: List
    @param file_exclusion: The list of file extensions to be excluded.
    @type configuration_file_path: String
    @param configuration_file_path: The path to the configuration file.
    """

    # in case the configuration file path is defined
    if configuration_file_path:
        # creates the base path from the file paths
        base_path = os.path.dirname(os.path.realpath(__file__)) + RELATIVE_BASE_PATH

        # retrieves the real base path
        real_base_path = os.path.realpath(base_path)

        # retrieves the configuration directory from the configuration
        # file path (the directory is going to be used to include the module)
        configuration_directory_path = os.path.dirname(configuration_file_path)

        # in case the configuration directory path is not an absolute path
        if not os.path.isabs(configuration_directory_path):
            # creates the (complete) configuration directory path prepending the manager path
            configuration_directory_path = real_base_path + "/" + configuration_directory_path

        # in case the configuration directory path is valid inserts it into the system path
        configuration_directory_path and sys.path.insert(0, configuration_directory_path)

        # retrieves the configuration file base path from the configuration file path
        configuration_file_base_path = os.path.basename(configuration_file_path)

        # retrieves the configuration module name and the configuration module extension by splitting the
        # configuration base path into base name and extension
        configuration_module_name, _configuration_module_extension = os.path.splitext(configuration_file_base_path)

        # imports the configuration module
        configuration = __import__(configuration_module_name)

        # retrieves the configurations from the configuration module
        configurations = configuration.configurations
    else:
        # creates the base configuration map
        base_configuration = {}

        # sets the base configuration map attributes
        base_configuration["recursive"] = recursive
        base_configuration["file_exclusion"] = file_exclusion

        # creates the configurations tuple with the base configurations
        configurations = (
            base_configuration,
        )

    # returns the configurations tuple
    return configurations

def main():
    """
    Main function used for the joining files.
    """

    # in case the number of arguments
    # is not sufficient
    if len(sys.argv) < 2:
        # prints a message
        print("Invalid number of arguments")

        # prints the usage message
        print("Usage: " + USAGE_MESSAGE)

        # exits the system in error
        sys.exit(2)

    # sets the default values for the parameters
    path = sys.argv[1]
    recursive = False
    file_exclusion = None
    configuration_file_path = None

    try:
        options, _arguments = getopt.getopt(sys.argv[2:], "rc:", [])
    except getopt.GetoptError:
        # prints a series of messages about the
        # correct usage of the command line
        print("Invalid number of arguments")
        print("Usage: " + USAGE_MESSAGE)

        # exits the system in error
        sys.exit(2)

    # iterates over all the options, retrieving the option
    # and the value for each
    for option, value in options:
        if option == "-r":
            recursive = True
        elif option == "-w":
            file_exclusion = [value.strip() for value in value.split(",")]
        elif option == "-c":
            configuration_file_path = value

    # retrieves the configurations from the command line arguments
    configurations = _retrieve_configurations(
        recursive,
        file_exclusion,
        configuration_file_path
    )

    # iterates over all the configurations, executing them
    for configuration in configurations:
        # retrieves the configuration values
        recursive = configuration["recursive"]
        file_exclusion = configuration["file_exclusion"]

        # in case the recursive flag is set, joins the files in
        # recursive mode (multiple files)
        if recursive: join_files_recursive(path, file_exclusion)
        # otherwise it's a "normal" iteration and joins the
        # files (for only one file)
        else: join_files(path)

if __name__ == "__main__":
    main()
