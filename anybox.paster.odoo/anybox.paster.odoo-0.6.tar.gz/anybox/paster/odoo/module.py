from paste.script.templates import Template
import datetime
import os
import ConfigParser
import re


def get_conf(conffile, section, option):
    author = ""
    author_email = ""
    val = ""
    p = ConfigParser.RawConfigParser()
    try:
        p.read([conffile])
        for o, v in p.items(section):
            if o == option:
                val = v
        if val:
            regex = re.compile('(.*) <(.*)>')
            author, author_email = regex.findall(val)[0]
    except Exception, e:
        print e

    return author, author_email


def git_conf(conffile, section, option):
    for line in open(conffile).readlines():
        if line.strip() == '[%s]' % section:
            user_section = True
        if user_section and line.split('=', 1)[0].strip() == option:
            return line.split('=', 1)[1].strip()


class Module(Template):
    summary = 'Template for creating an Odoo python file'
    required_templates = []
    _template_dir = 'templates/module'
    use_cheetah = True

    def pre(self, command, output_dir, vars):
        gitfile = os.path.expanduser("~/.gitconfig")
        hgfile = os.path.expanduser("~/.hgrc")
        bzrfile = os.path.expanduser("~/.bazaar/bazaar.conf")
        if os.path.exists(gitfile):
            author = git_conf(gitfile, 'user', 'name')
            author_email = git_conf(gitfile, 'user', 'email')
        elif os.path.exists(hgfile):
            author, author_email = get_conf(hgfile, 'ui', 'username')
        elif os.path.exists(bzrfile):
            author, author_email = get_conf(bzrfile, 'DEFAULT', 'email')

        loopvars = [
            ('description', 'Small description', ''),
            ('author', 'Author name', author),
            ('author_email', 'Author email', author_email),
            ('name', 'Module Name', vars['project'].replace('_', ' ')),
            ('version', 'Module version', '0.1'),
            ('category', 'Module category',  'Uncategorized'),
            ('company', 'Author Company', "Anybox"),
            ('website', 'Website', "http://anybox.fr"),
            ('depends', 'List of Odoo module dependencies (separated by ,)', "base"),
            ('app', 'Is the module an application? (True/False)', "False"),
        ]
        counter = 0
        vars['year'] = str(datetime.date.today().year)
        while counter < len(loopvars):
            field, question, default = loopvars[counter]
            if field in ('application',):
                question = command.challenge(question + ' :', default, True)
                if question not in ('True', 'False'):
                    continue
            else:
                question = command.challenge('Please Enter ' + question + ' :', default, True)
            if question != '':
                if field == 'depends':
                    question = ','.join(["'" + x.strip() + "'" for x in question.split(',')])
                vars[field] = question
                counter += 1
