import sys
import shlex
import insert_tags
import os
import fnmatch
import logging

from detektor.libs.defgetter import defgetter

DEBUG = 1
logger = logging.getLogger(__name__)

#########################################################
######### STUFF THAT SHOULD BE DONE ON IMPORT ###########
#########################################################

default_data_directory = os.path.join(
    os.path.dirname(__file__), 'default_data_directory')
datadir = os.environ.get('DETEKTOR_DATA_DIRECTORY', default_data_directory)

# get info about supported languages
with open(os.path.join(datadir, "supported_languages.dat"), 'r') as supported_languages_file:
    languages = []
    for line in supported_languages_file:
        languages.append(line.replace('\n', '').split())

logger.debug('LANGUAGES: {}'.format(languages))


# Get keywords and operators for the supported languages

# Make dictionaries for saving operators for each language
operators = {}
keywords = {}

logger.debug('Languages: {}'.format(languages))

for lang in languages:
    # put an empty list in dictionaries
    keywords[lang[0]] = []
    operators[lang[0]] = []
    keyws = ''
    ops = ''
    try:
        language_definition_file = open(os.path.join(datadir, lang[2]), 'r')
    except IOError:
        raise SystemExit('Could not open {} {}'.format(datadir, lang[2]))
    else:
        language_definition_file.readline()  # read past the tag 'KEYWORDS:'
        while language_definition_file:
            line = language_definition_file.readline()
            if fnmatch.fnmatch(line, 'OPERATORS:*'):
                break
            keyws += " " + line
        keywords[lang[0]] = keyws.split()
        line = language_definition_file.readline()
        while line:
            ops = ops + " " + line
            line = language_definition_file.readline()
        operators[lang[0]] = ops.split()
        language_definition_file.close()

logger.debug('KEYWORDS: {}'.format(keywords))
logger.debug('OPERATORS: {}'.format(operators))


############ Add multicharacter operators to wordchars ################
def add_multichars(lexer):
    # If e.g '**' is found, this is wanted,
    # not the one-charachter operator '*'
    for lang, op_list in operators.iteritems():
        for op in op_list:
            if len(op) > 1:
                lexer.wordchars += op


########################### The Parser Class #########################
class Parser:
    """This class performes the necessary tasks for getting data to use
    for comparing assignments.
    """
    keywords = {}

    def __init__(self, language, filehandler):

        # run get_defs to insert mark where end of functions is
        new_filehandler = insert_tags.add_enddef(language, filehandler)

        #filereader = open(new_file, 'r')
        self.lexer = shlex.shlex(new_filehandler)
        add_multichars(self.lexer)

        # initialize a dictionary for counting occurences of keywords
        self.cur_lang_keywords = {}
        for kw in keywords[language]:
            self.cur_lang_keywords[kw] = 0
        self.cur_lang_operators = {}
        for op in operators[language]:
            self.cur_lang_operators[op] = 0

    def make_string(self, dict):
        """Makes strings from dictionaries of keywords or operators.
        If a language has two keywords, 'if' and 'for', and an
        assignment has 2 occurences of 'if', but no occurence of 'for',
        the string made is '_0_2' where the first number represents number
        of 'for', since 'for' comes before 'if' alphabetically.
        """
        tmp_list = []
        representing_string = ""
        for key in dict.keys():
            tmp_list.append(key)
        # the list must be sorted to make a string that can be used
        # for comparing number of each keyword/operator used.
        tmp_list.sort()
        for k in tmp_list:
            representing_string += ("_" + str(dict[k]))
        return representing_string

    def parse_file(self):
        """The method that analyzes a file, and generates datastructures
        that can be used for comparing assignments."""
        num_kw = 0
        num_op = 0
        bigs = ""
        curtok = self.lexer.get_token()
        while curtok:
            if curtok in self.cur_lang_keywords:
                bigs += curtok
                num_kw += 1
                self.cur_lang_keywords[curtok] += 1
            elif curtok in self.cur_lang_operators:
                bigs += curtok
                self.cur_lang_operators[curtok] += 1
                num_op += 1
            # 'enddef' is added so that end of functions can be found
            elif curtok == "enddef":
                bigs += curtok
            try:
                curtok = self.lexer.get_token()
            except ValueError:
                curtok = None
        s1 = self.make_string(self.cur_lang_keywords)
        s2 = self.make_string(self.cur_lang_operators)
        return s1, s2, bigs, hash(bigs), num_kw, num_op

    def get_code_signature(self):
        kwh, oph, bigstring, bigstringhash, num_kw, num_op = self.parse_file()
        list_of_functions = defgetter('python', bigstring)
        return {
            'keywordstring': kwh,
            'operatorstring': oph,
            'bigstring': bigstring,
            'bigstringhash': bigstringhash,
            'number_of_keywords': num_kw,
            'number_of_operators': num_op,
            'list_of_functions': list_of_functions,
        }

    def report_results(self, bigs):
        """ For debugging only """
        print 'The big string:\n', bigs
        print 'Keywords:'
        for key in self.cur_lang_keywords.keys():
            num = self.cur_lang_keywords[key]
            if num > 0:
                print '  ', num, ' \'' + key + '\'.'
        print 'Operators:'
        for key in self.cur_lang_operators.keys():
            num = self.cur_lang_operators[key]
            if num > 0:
                print '  ', num, ' \'' + key + '\'.'

####################### The Parser Class End #########################
