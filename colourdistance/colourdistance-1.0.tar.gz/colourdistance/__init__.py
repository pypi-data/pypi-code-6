"""
Colour extraction routines
"""

try:
    from colourdistance import closest_by_palette, colour_distance
except ImportError:
    from math import sqrt

    def colour_distance(e1, e2):
        rmean = (e1[0] + e2[0]) / 2
        r = e1[0] - e2[0]
        g = e1[1] - e2[1]
        b = e1[2] - e2[2]

        return sqrt((((512 + rmean) * r * r) >> 8) +
                    4 * g * g +
                    (((767 - rmean) * b * b) >> 8))

    def closest_by_palette(colour, palette):
        min_distance = 2 << 31
        replacement = None
        i = 0
        for target in palette:

            distance = colour_distance(colour, target)

            if distance < min_distance:
                min_distance = distance
                replacement = i
            i += 1

        return replacement
