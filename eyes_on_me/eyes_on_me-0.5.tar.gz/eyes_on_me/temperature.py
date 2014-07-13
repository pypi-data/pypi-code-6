import subprocess
import re


kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)}


def color_temperature_to_rgb(kelvin):
    normalized_kelvin = int(kelvin) / 500 * 500
    if (normalized_kelvin < min(kelvin_table.keys())):
        return kelvin_table[min(kelvin_table.keys())]
    elif (normalized_kelvin > max(kelvin_table.keys())):
        return kelvin_table[max(kelvin_table.keys())]
    else:
        return kelvin_table[normalized_kelvin]


def normalized_rgb_to_color_temperature(nrgb):
    (nr, ng, nb) = nrgb

    def rgb_deviation(x):
        nx = normalize_rgb(x[1])
        d = (abs(nx[0] - nr) +
             abs(nx[1] - ng) + abs(nx[2] - nb))
        return d

    min_kelvins = min(kelvin_table.items(),
                      key=rgb_deviation)

    return min_kelvins[0]


def normalize_rgb(rgb):
    rgb = [float(x) for x in rgb]
    median = sum(rgb) / len(rgb)
    normalized_rgb = [x / median for x in rgb]
    return normalized_rgb


def set_temperature(kalvin):
    rgb = color_temperature_to_rgb(kalvin)

    # normalize around 1.0
    normalized_rgb = normalize_rgb(rgb)
    # set via xgamma
    (r, g, b) = normalized_rgb
    subprocess.check_call("xgamma -rgamma %s" % r, shell=True)
    subprocess.check_call("xgamma -ggamma %s" % g, shell=True)
    subprocess.check_call("xgamma -bgamma %s" % b, shell=True)


def get_temperature():
    # find
    out = subprocess.check_output("xgamma 2>&1", shell=True)
    reg = re.search(
        "->.+?Red.+?([0-9]+\.[0-9]+).+?Green.+?([0-9]+\.[0-9]+),.+?Blue.+?([0-9]+\.[0-9]+)",
        out)
    (nr, ng, nb) = (float(x) for x in reg.groups())
    # find nearest values
    return normalized_rgb_to_color_temperature((nr, ng, nb))
