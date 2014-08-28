import docopt

import teuthology.config
import teuthology.query

doc = """
usage: teuthology-query [-h]
       teuthology-query list running jobs

Query teuthology's reporting service

optional arguments:
  -h, --help            show this help message and exit
""".format(archive_base=teuthology.config.config.archive_base)


def main():
    args = docopt.docopt(doc)
    teuthology.query.main(args)
