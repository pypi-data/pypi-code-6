# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from production import ProductionReport


def register():
    Pool.register(
        ProductionReport,
        module='production_report', type_='report'
    )
