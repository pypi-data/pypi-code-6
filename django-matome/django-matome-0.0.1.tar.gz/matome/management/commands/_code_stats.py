# -*- coding: utf-8 -*-

import os
import re


class CodeStats(object):

    def __init__(self, name):
        self.name = name
        self.files = 1
        self.lines = 0
        self.code_lines = 0
        self.classes = 0
        self.methods = 0


class CategoryStats(object):

    def __init__(self, name):
        self.name = name
        self.files = 0
        self.lines = 0
        self.code_lines = 0
        self.classes = 0
        self.methods = 0

    def add(self, stats):
        if isinstance(stats, (CodeStats, CategoryStats)):
            self.lines += stats.lines
            self.code_lines += stats.code_lines
            self.classes += stats.classes
            self.methods += stats.methods
            self.files += stats.files
        else:
            AttributeError('argument must be an instance of CodeStats')


class SourceCodeInspector(object):

    REGEXES = {
        'py': {
            'line_comment': re.compile('^\s*#'),
            'class': re.compile('\s*class\s+[_A-Z]'),
            'method': re.compile('\s*def\s+[_a-z]'),
        },
        'js': {
            'line_comment': re.compile(r'^\s*//'),
            'begin_block_comment': re.compile(r'^\s*/\*'),
            'end_block_comment': re.compile(r'\*/'),
            'method': re.compile('function(\s+[_a-zA-Z][\da-zA-Z]*)?\s*\('),
        },
        'coffee': {
            'line_comment': re.compile('^\s*#'),
            'begin_block_comment': re.compile('^\s*###'),
            'end_block_comment': re.compile('^\s*###'),
            'class': re.compile('^\s*class\s+[_A-Z]'),
            'method': re.compile('[-=]>'),
        }
    }

    def __init__(self, file_path):
        self.file_path = file_path

    def inspect(self):
        stats = CodeStats(self.file_path)
        regexes = SourceCodeInspector.REGEXES
        file_type = re.sub(re.compile("\A\."), '', os.path.splitext(self.file_path)[-1]).lower()
        empty_line_pattern = re.compile('^\s*$')
        with open(self.file_path) as f:
            if file_type in regexes:
                patterns = regexes[file_type]
            else:
                patterns = {}

            comment_started = False
            for line in f.readlines():
                stats.lines += 1
                if comment_started:
                    if 'end_block_comment' in patterns and patterns['end_block_comment'].match(line):
                        comment_started = False
                    continue
                else:
                    if 'begin_block_comment' in patterns and patterns['begin_block_comment'].match(line):
                        comment_started = True
                        continue

                if 'class' in patterns and patterns['class'].match(line):
                    stats.classes += 1

                if 'method' in patterns and patterns['method'].match(line):
                    stats.methods += 1

                if not empty_line_pattern.match(line) and 'line_comment' not in patterns or not patterns['line_comment'].match(line):
                    stats.code_lines += 1
        return stats


class Summarizer(object):

    @staticmethod
    def summarize(category_name, file_paths, regex=re.compile('.*\.(py|js|coffee)$')):
        category_stats = CategoryStats(category_name)
        for path in file_paths:
            if regex.match(path):
                stats = SourceCodeInspector(path).inspect()
                category_stats.add(stats)

        return category_stats


class SummaryPresenter(object):

    HEADER =   "| Name                 |  FILES  |  Lines  |   LOC   | Classes | Methods |   M/C   |  LOC/M  |"

    SPLITTER = "+----------------------+---------+---------+---------+---------+---------+---------+---------+"


    @staticmethod
    def summarize(targets):
        if not isinstance(targets, dict):
            raise AttributeError('target must be an instance of dict')
        represents = []
        represents.append(SummaryPresenter.SPLITTER)
        represents.append(SummaryPresenter.HEADER)
        represents.append(SummaryPresenter.SPLITTER)
        total_stats = CategoryStats('Total')
        for category_name in targets:
            category_files = targets[category_name]
            category_stats = Summarizer.summarize(category_name, category_files)
            stats_line = StatsPresenter(category_stats).represent
            represents.append(stats_line)
            total_stats.add(category_stats)
        represents.append(SummaryPresenter.SPLITTER)
        total_stats_line = StatsPresenter(total_stats).represent
        represents.append(total_stats_line)
        represents.append(SummaryPresenter.SPLITTER)
        return "\n".join(represents)


class StatsPresenter(object):

    def __init__(self, stats):
        self.stats = stats

    @property
    def represent(self):
        m_over_c = (float(self.stats.methods) / self.stats.classes) if self.stats.classes != 0 else 0.0
        loc_over_m = (float(self.stats.code_lines) / self.stats.methods) - 2 if self.stats.methods != 0 else 0.0

        line_format = "".join([
            "| {name:20} ",
            "| {files:7} ",
            "| {lines:7} ",
            "| {code_lines:7} ",
            "| {classes:7} ",
            "| {methods:7} ",
            "| {m_over_c:7.1f} ",
            "| {loc_over_m:7.1f} |"
        ])

        return line_format.format(
            name=self.stats.name,
            files=self.stats.files,
            lines=self.stats.lines,
            code_lines=self.stats.code_lines,
            classes=self.stats.classes,
            methods=self.stats.methods,
            m_over_c=m_over_c,
            loc_over_m=loc_over_m
        )