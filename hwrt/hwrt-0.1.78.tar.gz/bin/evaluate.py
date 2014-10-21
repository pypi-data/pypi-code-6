#!/usr/bin/env python

"""Evaluate data."""

import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import yaml
import json
# mine
import hwrt.utils as utils


def main(model_folder):
    recording = sys.stdin.readline()
    raw_data_json = json.dumps(yaml.load(recording))
    logging.info(recording)
    logging.info("Start evaluation...")
    print(utils.evaluate_model(raw_data_json, model_folder))


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with a info.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=utils.default_model())
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.model)
