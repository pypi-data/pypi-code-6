#coding: utf-8

# Для удобства разработчиков вынес форматы выходных файлов сюда.
from report_generator.report_builder.enums import (DocumentResultFileTypes,
                                                   TableDocumentResultFileTypes)

# Функция, которая позволяет строить отчет.
from report_generator.api.api import build_report