#!coding:utf-8
import os
import subprocess
import unittest
from simple_report.converter.abstract import FileConverter
from simple_report.interface import ISpreadsheetSection
from simple_report.report import SpreadsheetReport
from simple_report.xls.document import DocumentXLS
from simple_report.xls.section import MergeXLS, XLSImage
from core import insert_formulas, LOREM_IPSUM

__author__ = 'khalikov'


class TestWriteXLS(unittest.TestCase):
    """
    Тестируем правильность вывода для XSL
    """

    SUBDIR = 'linux'

    def setUp(self):
        assert self.SUBDIR
        self.src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'test_data', self.SUBDIR, 'xls', )
        self.dst_dir = self.src_dir

        self.test_files = dict([(path, os.path.join(self.src_dir, path))
                                for path in os.listdir(self.src_dir)
                                if path.startswith('test')])

    def test_left_down(self, report=None):
        if report is None:
            return
        for i in range(2):
            section1 = report.get_section('Section1')
            section1.flush({'section1': i}, oriented=ISpreadsheetSection.LEFT_DOWN)
            self.assertEqual(section1.sheet_data.cursor.row, (0, 2 * i + 2))
            self.assertEqual(section1.sheet_data.cursor.column, (2, 2 * i))

    def test_left_down2(self, report=None):
        if report is None:
            return
        for i in range(2):
            section3 = report.get_section('Section3')
            section3.flush({'section3': 100}, oriented=ISpreadsheetSection.LEFT_DOWN)
            self.assertEqual(section3.sheet_data.cursor.row, (0, 2 * i + 10))
            self.assertEqual(section3.sheet_data.cursor.column, (2, 2 * i + 8))

    def test_right_up(self, report=None):
        if report is None:
            return
        section1 = report.get_section('Section1')
        section1.flush({'section1': 2}, oriented=ISpreadsheetSection.RIGHT_UP)
        self.assertEqual(section1.sheet_data.cursor.row, (2, 2))
        self.assertEqual(section1.sheet_data.cursor.column, (4, 0))

    def test_vertical(self, report=None):
        if report is None:
            return
        for i in range(3):
            section2 = report.get_section('Section2')
            section2.flush({'section2': i}, oriented=ISpreadsheetSection.VERTICAL)
            self.assertEqual(section2.sheet_data.cursor.row,
                             (2, 2 * (i + 1) + 2))
            self.assertEqual(section2.sheet_data.cursor.column,
                             (4, 2 * (i + 1)))

    def test_horizontal(self, report=None):
        if report is None:
            return
        for i in range(3):
            section3 = report.get_section('Section3')
            section3.flush({'section3': i}, oriented=ISpreadsheetSection.HORIZONTAL)
            self.assertEqual(section3.sheet_data.cursor.row, (2, 8))
            self.assertEqual(section3.sheet_data.cursor.column,
                             (6 + 2 * i, 6))

    def test_report_write(self):

        src = self.test_files['test-report-output.xls']
        dst = os.path.join(self.dst_dir, 'res-report-output.xls')
        if os.path.exists(dst):
            os.remove(dst)

        report = SpreadsheetReport(src, wrapper=DocumentXLS,
                                   type=FileConverter.XLS)
        self.test_left_down(report)
        self.test_right_up(report)
        self.test_vertical(report)
        self.test_horizontal(report)
        self.test_left_down2(report)

        return report.build(dst)


class TestReportFormatXLS(unittest.TestCase):
    """
    Тест на работоспособность отчета формата XLS
    """

    SUBDIR = 'linux'

    def setUp(self):
        assert self.SUBDIR
        self.src_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_data',
            self.SUBDIR,
            'xls'
        )
        self.dst_dir = self.src_dir

        self.test_files = dict([(path, os.path.join(self.src_dir, path))
                                for path in os.listdir(self.src_dir)
                                if path.startswith('test')])

    def test_spreadsheet_with_flag(self):
        """
        Тест на использование класса SpreadsheetReport с переданным в
        конструктор wrapper-ом.
        """

        src = self.test_files['test_xls.xls']
        dst = os.path.join(self.dst_dir, 'res-test_xls.xls')
        if os.path.exists(dst):
            os.remove(dst)

        report = SpreadsheetReport(src, wrapper=DocumentXLS,
                                   type=FileConverter.XLS)

        section1 = report.get_section('Section1')
        section1.flush({'tag1': 1})

        report.workbook.active_sheet = 1

        section2 = report.get_section('Section2')
        for i in range(10):
            section2.flush({'tag2': i})

        for i in range(10):
            section2.flush({'tag2': str(10)}, oriented=ISpreadsheetSection.HORIZONTAL)

        return report.build(dst)

    def test_with_merge(self):
        """
        Конструкция with merge для обьединения ячеек вывода
        """

        src = self.test_files['test_merge.xls']
        dst = os.path.join(self.dst_dir, 'res-merge.xls')
        if os.path.exists(dst):
            os.remove(dst)

        report = SpreadsheetReport(src, wrapper=DocumentXLS,
                                   type=FileConverter.XLS)

        s1 = report.get_section('s1')
        s2 = report.get_section('s2')
        s3 = report.get_section('s3')
        s4 = report.get_section('s4')
        s5 = report.get_section('s5')

        s5.flush({'p5': 1}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 2}, oriented=ISpreadsheetSection.VERTICAL)
        s5.flush({'p5': 3}, oriented=ISpreadsheetSection.HORIZONTAL)

        m1 = MergeXLS(s1, s2, {'p1': 1},
                      oriented=ISpreadsheetSection.HORIZONTAL)
        with m1:
            m2 = MergeXLS(s2, s3, {'p21': 1, 'p22': 21},
                          oriented=ISpreadsheetSection.HORIZONTAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1},
                              oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    for i in range(2, 4):
                        s4.flush({'p4': i},
                                 oriented=ISpreadsheetSection.VERTICAL)

                m3_exp = (m3._begin_merge_col == 9
                          and m3._end_merge_col == 9
                          and m3.begin_row_merge == 3
                          and m3.end_row_merge == 5)
                self.assertEqual(m3_exp, True)

                m3 = MergeXLS(s3, s4, {'p3': 2},
                              oriented=ISpreadsheetSection.HIERARCHICAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

            m2 = MergeXLS(s2, s3, {'p21': 2, 'p22': 21},
                          oriented=ISpreadsheetSection.HIERARCHICAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1},
                              oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1}, oriented=ISpreadsheetSection.RIGHT)
                    s4.flush({'p4': 2}, oriented=ISpreadsheetSection.VERTICAL)

        m1_exp = (m1._begin_merge_col == 6 and m1._end_merge_col == 6
                  and m1.begin_row_merge == 3 and m1.end_row_merge == 9)
        self.assertEqual(m1_exp, True)

        m1 = MergeXLS(s1, s2, {'p1': 2},
                      oriented=ISpreadsheetSection.HIERARCHICAL)
        with m1:
            m2 = MergeXLS(s2, s3, {'p21': 1, 'p22': 21},
                          oriented=ISpreadsheetSection.HORIZONTAL)
            with m2:
                m3 = MergeXLS(s3, s4, {'p3': 1},
                              oriented=ISpreadsheetSection.HORIZONTAL)
                with m3:
                    s4.flush({'p4': 1},
                             oriented=ISpreadsheetSection.HORIZONTAL)

        return report.build(dst)

    def test_xls_formula_generation(self):
        """
        Генерация формул в xls
        """
        src = self.test_files['test-formula_generation.xls']
        dst = os.path.join(self.dst_dir, 'res-formula_generation.xls')
        if os.path.exists(dst):
            os.remove(dst)

        report = SpreadsheetReport(src, wrapper=DocumentXLS,
                                   type=FileConverter.XLS)

        row_insert_formula_section = report.get_section('row_insert_formula')
        check_insert_formula_section = report.get_section(
            'check_insert_formula'
        )

        insert_formulas(row_insert_formula_section,
                        check_insert_formula_section)
        report.build(dst)
        check_file = " Please, check output file %s with table proc." % dst
        if os.name == 'posix':
            openoffice = '/usr/bin/openoffice'
            libreoffice = '/usr/bin/libreoffice'
            office = None
            if os.path.exists(libreoffice):
                office = libreoffice
            elif os.path.exists(openoffice):
                office = openoffice
            assert office, ("Didn't found neither openoffice nor libreoffice" +
                            check_file)
            subprocess.call([office, dst])
        elif os.name == 'nt':
            subprocess.call(['EXCEL.exe', dst])
        # elif os.name == 'mac':
        else:
            raise Exception("Can't check xls formula generation.")

    def test_xls_image_insertion(self):
        """
        Вставка изображений
        """
        src = self.test_files['test_insert_image.xls']
        src_image1 = self.test_files['test_image1.bmp']
        src_image2 = self.test_files['test_image2.bmp']
        dst = os.path.join(self.dst_dir, 'res-insert_image.xls')
        if os.path.exists(dst):
            os.remove(dst)

        report = SpreadsheetReport(src, wrapper=DocumentXLS,
                                   type=FileConverter.XLS)

        row_section = report.get_section('row')
        row_section.flush({
            'image1': XLSImage(src_image1)
        })
        row_section.flush({
            'image2': XLSImage(src_image2)
        })
        row_section.flush({
            'image1': XLSImage(src_image2),
            'image2': XLSImage(src_image1)
        })
        report.build(dst)

    def test_rows_height(self):
        """
        Тест на выставление высоты строк
        """
        src = self.test_files['test_rows_height.xls']
        dst = os.path.join(self.dst_dir, 'res-rows-height.xls')

        if os.path.exists(dst):
            os.remove(dst)
        report = SpreadsheetReport(
            src,
            wrapper=DocumentXLS,
            type=FileConverter.XLS
        )
        report.get_section('row1').flush({
            't1': LOREM_IPSUM[:20],
            't2': u'. '.join([
                u'Проверка на автоподбор высоты',
                LOREM_IPSUM
            ])
        })

        report.get_section('row2').flush({
            't1': LOREM_IPSUM[:20],
            't2': u'. '.join([
                u'Проверка на высоту строки, взятую из шаблона',
                LOREM_IPSUM
            ])
        })
        report.build(dst)

    def test_styles(self):
        """
        Тест на сохранение стилей ячеек
        """
        src = self.test_files['test_styles.xls']
        dst = os.path.join(self.dst_dir, 'res-styles.xls')

        if os.path.exists(dst):
            os.remove(dst)
        report = SpreadsheetReport(
            src,
            wrapper=DocumentXLS,
            type=FileConverter.XLS
        )
        report.get_section('header').flush({
            'test': LOREM_IPSUM[:20],
        })
        report.build(dst)
        #active_sheet = report.workbook.active_sheet
        #wtsheet = active_sheet.writer.wtsheet

if __name__ == '__main__':
    unittest.main()