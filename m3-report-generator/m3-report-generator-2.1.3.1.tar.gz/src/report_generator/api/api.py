#coding: utf-8

from report_generator.report_builder.builder import ReportBuilder

def build_report(report_key, result_format, params):
    """
    Построение отчета по ключу и параметрам
    :param report_key: ключ отчета
    :param result_format: формат результата
    :param params: параметры отчета
    """

    assert report_key
    assert result_format

    rb = ReportBuilder(report_key=report_key, params=params,
                                                result_format=result_format)
    file_name = rb.build()
    return file_name
