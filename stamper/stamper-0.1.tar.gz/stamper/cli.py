import argparse


def build_args_parser():
    parser = argparse.ArgumentParser(
        description='stamps: show recorded times information')
    parser.add_argument('customer', action="store", nargs='?',
                        help='Show times only for this customer')
    parser.add_argument('filter', action="store", nargs='?',
                        help='Filter the times by date range')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Include detailed times information')
    parser.add_argument('-s', '--sum', action="store_true",
                        help='Include sum of times')
    parser.add_argument('-g', '--graph', action="store_true",
                        help='Generate a SVG graph')
    parser.add_argument('-t', '--timeline', action="store_true",
                        help='Show a timeline of recorded times')
    parser.add_argument('-d', '--delete', action="store", type=int,
                        help='Delete up to n recorded stamps')
    parser.add_argument('-i', '--import', action="store", dest="import_file",
                        help='Import stamps from the given file')
    return parser
