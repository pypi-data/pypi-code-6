#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json
import requests
import click
from xlwt import Workbook, XFStyle, Style, Font, Pattern, Borders

XLS_COLORS = [
    'gray_ega', 'dark_green', 'indigo',
    'gold', 'blue_grey', 'dark_green_ega',
    'lavender', 'yellow', 'purple_ega',
    'olive_ega', 'olive_green', 'light_yellow',
    'pale_blue', 'violet', 'dark_red_ega',
    'cyan_ega', 'dark_blue', 'blue_gray',
    'magenta_ega', 'lime', 'blue', 'grey40',
    'pink', 'grey25', 'rose', 'white', 'black',
    'silver_ega', 'gray50', 'periwinkle',
    'magenta_ega', 'lime', 'blue', 'grey40',
    'pink', 'grey25', 'rose', 'white', 'black',
    'silver_ega', 'gray50', 'periwinkle',
    'sea_green', 'orange', 'red', 'grey80',
    'dark_teal', 'brown', 'ivory', 'bright_green',
    'ocean_blue', 'dark_blue_ega', 'dark_yellow',
    'light_turquoise', 'light_blue', 'dark_purple',
    'ice_blue', 'light_orange', 'grey50', 'grey_ega',
    'tan', 'sky_blue', 'gray25', 'gray40', 'coral',
    'light_green', 'aqua', 'dark_red', 'gray80',
    'green', 'teal_ega', 'teal', 'plum', 'turquoise'
]


class Json2Xls(object):

    def __init__(self, filename, url_or_json, method='get',
                 params=None, data=None, headers=None,
                 sheet_name='sheet0', title_color='lime', font_name='Arial'):
        self.sheet_name = sheet_name
        self.filename = filename
        self.url_or_json = url_or_json
        self.method = method
        self.params = params
        self.data = data
        self.headers = headers
        self.title_color = title_color

        self.__check_color()
        self.__check_file_suffix()

        self.book = Workbook(encoding='utf-8')
        self.sheet = self.book.add_sheet(self.sheet_name)

        self.title_start_col = 0
        self.title_start_row = 0

        self.font = Font()
        self.font.name = font_name
        self.font.bold = True

        self.borders = Borders()
        self.borders.left = 1
        self.borders.right = 1
        self.borders.top = 1
        self.borders.bottom = 1

        self.pattern = Pattern()
        self.pattern.pattern = Pattern.SOLID_PATTERN
        self.pattern.pattern_fore_colour = Style.colour_map[self.title_color]

        self.title_style = XFStyle()
        self.title_style.font = self.font
        self.title_style.borders = self.borders
        self.title_style.pattern = self.pattern

        self.__make()

    def __parse_dict_depth(self, d, depth=0):
        if not isinstance(d, dict) or not d:
            return depth
        return max(self.__parse_dict_depth(v, depth + 1)
                   for k, v in d.iteritems())

    def __check_color(self):
        if self.title_color not in XLS_COLORS:
            raise Exception('your color is not supported')

    def __check_file_suffix(self):
        suffix = self.filename.split('.')[-1]
        if '.' not in self.filename:
            self.filename += '.xls'
        elif suffix not in ['xls', 'xlsx']:
            raise Exception('filename format must be .xls/.xlsx')

    def __check_dict_deep(self, d):
        depth = self.__parse_dict_depth(d)
        if depth > 1:
            raise Exception("dict is too deep")

    def __get_json(self):
        data = None
        try:
            data = json.loads(self.url_or_json)
        except:
            try:
                if self.method.lower() == 'get':
                    resp = requests.get(self.url_or_json,
                                        params=self.params,
                                        headers=self.headers)
                    data = resp.json()
                else:
                    resp = requests.post(self.url_or_json,
                                         data=self.data, headers=self.headers)
                    data = resp.json()
            except Exception as e:
                print e
        return data

    def __fill_title(self, data):
        self.__check_dict_deep(data)
        for index, key in enumerate(data.keys()):
            self.sheet.row(self.title_start_row).write(index,
                                                       key, self.title_style)
        self.title_start_row += 1

    def __fill_data(self, data):
        self.__check_dict_deep(data)
        for index, value in enumerate(data.values()):
            self.sheet.row(self.title_start_row).write(index, str(value))

        self.title_start_row += 1

    def __make(self):
        data = self.__get_json()
        if not isinstance(data, (dict, list)):
            raise Exception('bad json format')
        if isinstance(data, dict):
            data = [data]

        self.__fill_title(data[0])
        for d in data:
            self.__fill_data(d)
        self.book.save(self.filename)


@click.command()
@click.argument('filename')
@click.argument('source')
@click.option('--method', '-m', default='get')
@click.option('--params', '-p', default=None)
@click.option('--data', '-d', default=None)
@click.option('--headers', '-h', default=None)
@click.option('--sheet', '-s', default='sheet0')
@click.option('--color', '-c', default='lime')
@click.option('--font', '-f', default='Arial')
def make(filename, source, method, params, data, headers, sheet, color, font):
    Json2Xls(filename, source, method=method, params=params,
             data=data, headers=headers, sheet_name=sheet,
             title_color=color, font_name=font)

if __name__ == '__main__':
    make()
