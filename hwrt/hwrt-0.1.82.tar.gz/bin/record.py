#!/usr/bin/env python

import logging
import sys
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.DEBUG,
                    stream=sys.stdout)
import datetime
import json
# GUI
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
# mine
import hwrt.utils as utils


def unix_time():
    return int(datetime.datetime.now().strftime("%s"))


recording = []
last_stroke = []


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        global recording, last_stroke
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
            if len(last_stroke) > 0:
                recording.append(last_stroke)
                last_stroke = []
            point = {"x": touch.x, "y": -touch.y, "time": unix_time()}
            last_stroke.append(point)

    def on_touch_move(self, touch):
        global last_stroke
        touch.ud['line'].points += [touch.x, touch.y]
        point = {"x": touch.x, "y": -touch.y, "time": unix_time()}
        last_stroke.append(point)


class MyPaintApp(App):

    def build(self):
        return MyPaintWidget()


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


if __name__ == '__main__':
    args = get_parser().parse_args()
    MyPaintApp().run()
    recording.append(last_stroke)
    last_stroke = []
    print(recording)
    raw_data_json = json.dumps(recording)
    logging.info(recording)
    logging.info("Start evaluation...")
    results = utils.classify_single_recording(raw_data_json, args.model)
    for latex, probability in results:
        print("{0:15s} {1:5f}".format(latex, probability))
