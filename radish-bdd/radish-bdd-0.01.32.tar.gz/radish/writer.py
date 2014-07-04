# -*- coding: utf-8 -*-

import sys

from radish.colorful import colorful
from radish.config import Config
from radish.hookregistry import after, before


@before.each_feature
def print_before_feature(feature):
    if not feature.is_dry_run():
        sys.stdout.write(feature.get_representation())
        sys.stdout.flush()


@before.each_scenario
def print_before_scenario(scenario):
    if not scenario.is_dry_run():
        sys.stdout.write(scenario.get_representation(ran=False))
        sys.stdout.flush()


@after.each_scenario
def print_after_scenario(scenario):
    if not scenario.is_dry_run():
        sys.stdout.write(scenario.get_representation(ran=True))
        sys.stdout.flush()


@before.each_step
def print_before_step(step):
    if not step.is_dry_run():
        sys.stdout.write(step.get_representation(ran=False))
        sys.stdout.flush()


@after.each_step
def print_after_step(step):
    if not step.is_dry_run():
        sys.stdout.write(step.get_representation(ran=True))
        sys.stdout.flush()


@after.all
def print_after_all(endResult):
    if not Config().dry_run:
        white = colorful.bold_white
        green = colorful.bold_green
        red = colorful.bold_red
        cyan = colorful.cyan

        feature_text = green(str(endResult.get_passed_features()) + " passed")
        if endResult.get_failed_features() > 0:
            feature_text += white(", ") + red(str(endResult.get_failed_features()) + " failed")
        if endResult.get_skipped_features() > 0:
            feature_text += white(", ") + cyan(str(endResult.get_skipped_features()) + " skipped")

        scenario_text = green(str(endResult.get_passed_scenarios()) + " passed")
        if endResult.get_failed_scenarios() > 0:
            scenario_text += white(", ") + red(str(endResult.get_failed_scenarios()) + " failed")
        if endResult.get_skipped_scenarios() > 0:
            scenario_text += white(", ") + cyan(str(endResult.get_skipped_scenarios()) + " skipped")

        step_text = green(str(endResult.get_passed_steps()) + " passed")
        if endResult.get_failed_steps() > 0:
            step_text += white(", ") + red(str(endResult.get_failed_steps()) + " failed")
        if endResult.get_skipped_steps() > 0:
            step_text += white(", ") + cyan(str(endResult.get_skipped_steps()) + " skipped")

        colorful.out.bold_white(str(endResult.get_total_features()) + " features (%s" % (feature_text) + white(")"))
        colorful.out.bold_white(str(endResult.get_total_scenarios()) + " scenarios (%s" % (scenario_text) + white(")"))
        colorful.out.bold_white(str(endResult.get_total_steps()) + " steps (%s" % (step_text) + white(")"))

        sys.stdout.write(colorful.cyan("Run %s finished" % Config().marker))
        if not Config().no_duration:
            duration = sum([f.get_duration() for f in endResult.get_features()])
            sys.stdout.write(colorful.cyan(" within %d:%02d minutes" % (duration / 60, float(duration) % 60.0)))
        sys.stdout.write("\n")
        sys.stdout.flush()
