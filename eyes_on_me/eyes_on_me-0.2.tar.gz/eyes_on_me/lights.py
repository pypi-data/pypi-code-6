from eyes_on_me.config import config
import eyes_on_me.backlight
import eyes_on_me.temperature
import eyes_on_me.timed_strategy
import logging
import eyes_on_me.webcam_strategy


def choose_strategy():
    strategies = {
        'timed': eyes_on_me.timed_strategy.TimedStrategy,
        'webcam': eyes_on_me.webcam_strategy.WebcamStrategy
    }

    return strategies[config['strategy']]()


def get_backlight_for_light(light):
    backlights = [(0.0, config['backlight']['min']),
                  (0.5, config['backlight']['normal']),
                  (1.0, config['backlight']['max'])]
    # find closer values
    sorted_bl = sorted(backlights, key=lambda l: abs(light - l[0]))
    left_bl = sorted_bl[0]
    right_bl = sorted_bl[1]

    # calculate average
    left_delta = light - left_bl[0]
    right_delta = right_bl[0] - light
    overall_delta = right_bl[0] - left_bl[0]
    # TODO: zero division
    return (left_bl[1] * right_delta +
            right_bl[1] * left_delta) / overall_delta


def tune_backlight(light):
    backlight = get_backlight_for_light(light)
    logging.info("setting up backlight to %s", backlight)
    eyes_on_me.backlight.set_backlight(backlight)


def get_temperature_for_light(light):
    temperatures = [(0.0, config['wb_balance']['min']),
                    (0.5, config['wb_balance']['normal']),
                    (1.0, config['wb_balance']['max'])]
    # find closer ones
    sorted_temps = sorted(temperatures, key=lambda t: abs(light - t[0]))
    left_t = sorted_temps[0]
    right_t = sorted_temps[1]
    # calculate average
    left_delta = light - left_t[0]
    right_delta = right_t[0] - light
    overall_delta = right_t[0] - left_t[0]

    return (left_t[1] * right_delta +
            right_t[1] * left_delta) / overall_delta


def tune_wb(light):
    temperature = get_temperature_for_light(light)
    logging.info("setting up wb temperature to %s", temperature)
    eyes_on_me.temperature.set_temperature(temperature)


def tune_lights():
    strategy = choose_strategy()
    current_light = strategy.get_lightning()

    # set backlight
    tune_backlight(current_light)
    logging.info("current light is %s", current_light)
    # tune wb
    tune_wb(current_light)
