#!/usr/bin/env python

"""Evaluate data."""

import logging
import sys
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.DEBUG,
                    stream=sys.stdout)
import yaml
import json
import os
import csv
# mine
import hwrt.utils as utils


def main(model_folder, output_format):
    recording = sys.stdin.readline()
    raw_data_json = json.dumps(yaml.load(recording))
    logging.info(recording)
    logging.info("Start evaluation...")
    evaluation_file = utils.evaluate_model(raw_data_json, model_folder)
    PROJECT_ROOT = utils.get_project_root()
    with open(os.path.join(model_folder, "info.yml")) as ymlfile:
            model_description = yaml.load(ymlfile)
    translation_csv = os.path.join(PROJECT_ROOT,
                                   model_description["data-source"],
                                   "index2formula_id.csv")
    index2latex = {}
    with open(translation_csv) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            index2latex[int(row['index'])] = row['latex']
    with open(evaluation_file) as f:
        content = f.read()
    probabilities = map(float, content.split(" "))
    for index, probability in enumerate(probabilities):
        print("%s: %0.4f" % (index2latex[index], probability))


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
    parser.add_argument("--output-format",
                        dest="output_format",
                        help="in which format should the output be",
                        choices=["csv", "human-readable"],
                        default="human-readable")
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args.model, args.output_format)
