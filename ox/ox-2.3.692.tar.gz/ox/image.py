#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from __future__ import division

try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except:
    import Image
    import ImageDraw
    import ImageFont


ZONE_INDEX = []
for pixel_index in range(64):
    x, y = pixel_index % 8, int(pixel_index / 8)
    ZONE_INDEX.append(int(x / 2) + int(y / 4) * 4)
del x
del y

def drawText(image, position, text, font_file, font_size, color):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, font_size, encoding='unic')
    draw.text(position, text, fill=color, font=font)
    return draw.textsize(text, font=font)

def getHSL(rgb):
    rgb = [x / 255 for x in rgb]
    maximum = max(rgb)
    minimum = min(rgb)
    hsl = [0.0, 0.0, 0.0]
    hsl[2] = (maximum + minimum) / 2
    if maximum == minimum:
        hsl[0] = 0.0
        hsl[1] = 0.0
    else:
        if maximum == rgb[0]:
            hsl[0] = (60 * (rgb[1] - rgb[2]) / (maximum - minimum) + 360) % 360
        elif maximum == rgb[1]:
            hsl[0] = 60 * (rgb[2] - rgb[0]) / (maximum - minimum) + 120
        else:
            hsl[0] = 60 * (rgb[0] - rgb[1]) / (maximum - minimum) + 240
        if hsl[2] <= 0.5:
            hsl[1] = (maximum - minimum) / (2 * hsl[2])
        else:
            hsl[1] = (maximum - minimum) / (2 - 2 * hsl[2])
    return tuple(hsl)

def getImageHash(image_file, mode):
    image = Image.open(image_file).convert('RGB').resize((8, 8), Image.ANTIALIAS)
    image_hash = 0
    if mode == 'color':
        # divide the image into 8 zones:
        # 0 0 1 1 2 2 3 3
        # 0 0 1 1 2 2 3 3
        # 0 0 1 1 2 2 3 3
        # 0 0 1 1 2 2 3 3
        # 4 4 5 5 6 6 7 7
        # 4 4 5 5 6 6 7 7
        # 4 4 5 5 6 6 7 7
        # 4 4 5 5 6 6 7 7
        image_data = image.getdata()
        zone_values = [[] for i in range(8)]
        for pixel_index, pixel_value in enumerate(image_data):
            zone_values[ZONE_INDEX[pixel_index]].append(pixel_value)
        for zone_index, pixel_values in enumerate(zone_values):
            # get the mean for each color channel
            mean = [int(round(sum(x) / 8)) for x in zip(*pixel_values)]
            # store the mean color of each zone as an 8-bit value:
            # RRRGGGBB
            color_index = sum((
                int(mean[0] / 32) << 5,
                int(mean[1] / 32) << 2,
                int(mean[2] / 64)
            ))
            image_hash += color_index * pow(2, zone_index * 8)
    elif mode == 'shape':
        # pixels brighter than the mean register as 1,
        # pixels equal to or darker than the mean as 0
        image_data = image.convert('L').getdata()
        image_mean = sum(image_data) / 64
        for pixel_index, pixel_value in enumerate(image_data):
            if pixel_value > image_mean:
                image_hash += pow(2, pixel_index)
    image_hash = hex(image_hash)[2:].upper()
    if image_hash.endswith('L'):
        image_hash = image_hash[:-1]
    image_hash = '0' * (16 - len(image_hash)) + image_hash
    return image_hash

def getImageHeat(image_file):
    image = Image.open(image_file).convert('RGB').resize((16, 16), Image.ANTIALIAS)
    pixel = image.load()
    image_heat = 0
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            pixel_heat = []
            for y_ in range(max(y - 1, 0), min(y + 2, image.size[1])):
                for x_ in range(max(x - 1, 0), min(x + 2, image.size[0])):
                    if x != x_ or y != y_:
                        for c in range(3):
                            pixel_heat.append(abs(pixel[x, y][c] - pixel[x_, y_][c]))
            image_heat += sum(pixel_heat) / len(pixel_heat)
    return image_heat / 256

def getImageHSL(image_file):
    image = Image.open(image_file).convert('RGB').resize((1, 1), Image.ANTIALIAS)
    return getHSL(image.getpixel((0, 0)))

def getRGB(hsl):
    hsl = list(hsl)
    hsl[0] /= 360
    rgb = [0, 0, 0]
    if hsl[1] == 0:
        rgb = [hsl[2], hsl[2], hsl[2]]
    else:
        if hsl[2] < 1/2:
            v2 = hsl[2] * (1 + hsl[1])
        else:
            v2 = hsl[1] + hsl[2] - (hsl[1] * hsl[2])
        v1 = 2 * hsl[2] - v2
        for i in range(3):
            v3 = hsl[0] + (1 - i) * 1/3;
            if v3 < 0:
                v3 += 1
            elif v3 > 1:
                v3 -= 1
            if v3 < 1/6:
                rgb[i] = v1 + ((v2 - v1) * 6 * v3)
            elif v3 < 1/2:
                rgb[i] = v2
            elif v3 < 2/3:
                rgb[i] = v1 + ((v2 - v1) * 6 * (2/3 - v3))
            else:
                rgb[i] = v1
    return tuple([int(x * 255) for x in rgb])

def getTextSize(image, text, font_file, font_size):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, font_size, encoding='unic')
    return draw.textsize(text, font=font)

def wrapText(text, max_width, max_lines, font_file, font_size):
    # wraps text to max_width and max_lines
    def get_min_width():
        # returns the width of the longest non-hyphenated word
        min_width = 0
        for word in words:
            width = get_width(word)
            if width <= max_width and width > min_width:
                min_width = width
        return min_width
    def get_width(string):
        return draw.textsize(string, font=font)[0]
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, font_size, encoding='unic')
    ellipsis = '…'.decode('utf-8')
    separators = ['-', '+', '/', ':']
    if get_width(text) <= max_width:
        # text fits in one line
        lines = [text]
    else:
        lines = ['']
        words = []
        spaces = []
        test_words = text.split(' ')
        for word in test_words:
            if get_width(word) <= max_width:
                # word fits in one line
                words.append(word)
                spaces.append(' ')
            else:
                # word does not fit in one line
                position = 0
                test_word = word
                for separator in separators:
                    test_word = test_word.replace(separator, ' ')
                parts = test_word.split(' ')
                for i, part in enumerate(parts):
                    words.append(part)
                    if i < len(parts) - 1:
                        position += len(part) + 1
                        spaces.append(word[position - 1])
                    else:
                        spaces.append(' ')
        if max_lines:
            # test if the same number of lines can be achieved with shorter
            # lines, without hyphenating words that are not yet hyphenated
            best_lines = len(wrapText(text, max_width, 0, font_file, font_size))
            test_lines = best_lines
            min_width = get_min_width()
            while test_lines == best_lines and max_width >= min_width:
                max_width -= 1
                test_lines = len(wrapText(text, max_width, 0, font_file, font_size))
            max_width += 1
        for i, word in enumerate(words):
            line = len(lines) - 1
            word_width = get_width(word)
            if word_width <= max_width:
                # word fits in one line
                test = (lines[line] + word + spaces[i]).strip()
                if get_width(test) <= max_width:
                    # word fits in current line
                    lines[line] = test + (' ' if spaces[i] == ' ' else '')
                elif max_lines == 0 or line < max_lines - 1:
                    # word fits in next line
                    lines.append(word + spaces[i])
                else:
                    # word does not fit in last line
                    test = lines[line].strip() + ellipsis
                    if get_width(test) <= max_width:
                        # ellipsis fits in last line
                        lines[line] = test
                    else:
                        # ellipsis does not fit in last line
                        test_words = lines[line].split(' ')
                        while get_width(test) > max_width:
                            test_words.pop()
                            test = ' '.join(test_words) + ellipsis
                        if test == ellipsis:
                            # ellipsis does not fit after first word of last line
                            test = lines[line][:-1] + ellipsis
                            while get_width(test) > max_width:
                                test = test[:-2] + ellipsis
                        lines[line] = test
                    break
            else:
                # word does not fit in one line
                chars = list(word)
                for char in chars:
                    line = len(lines) - 1
                    test = (lines[line] + char + '-').strip()
                    if get_width(test) <= max_width:
                        # char fits in current line
                        lines[line] = test[:-1]
                    elif max_lines == 0 or line < max_lines - 1:
                        # char fits in next line
                        if test[-3] == ' ':
                            lines[line] = test[:-3]
                        else:
                            lines[line] = test[:-2] + '-'
                        lines.append(char)
                    else:
                        # char does not fit in last line
                        test = lines[line] + char + ellipsis
                        while get_width(test) > max_width:
                            test = test[:-2] + ellipsis
                        lines[line] = test
                lines[line] += ' '
    return lines
