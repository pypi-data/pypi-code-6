#!/usr/bin/env python
import docopt
doc = """
usage: teuthology-schedule-suite -h
       teuthology-schedule-suite -s suite -c ceph -k kernel [options]

Options:
    -s <suite>, --suite <suite>           Suite
    -c <branch>, --ceph <branch>          Ceph branch
    -k <branch>, --kernel <branch>        Kernel branch
    -e <email>, --email <email>           E-Mail address
                                          [default: ceph-qa@ceph.com]
    -f <flavor>, --flavor <flavor>        Kernel flavor
                                          ('basic', 'gcov', 'notcmalloc')
                                          [default: basic]
    -t <branch>, --teuthology <branch>    teuthology branch
    -m <type>, --machine-type <type>      Machine type
                                          [default: plana]
    -d <distro>, --distro <distro>        Distribution
                                          [default: ubuntu]
    -p <priority>, --priority <priority>  Scheduling priority
"""


def main():
    args = docopt.docopt(doc)
    print args

if __name__ == "__main__":
    main()
