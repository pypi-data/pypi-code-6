# -*- coding: utf-8 -*-

import csv

from django.utils.translation import ugettext as _

from openslides.utils import csv_ext

from .models import Category, Topic


def import_categories_and_topics(csvfile):
    """
    Performs the import of categories and topics from a csv file.
    """
    # Check encoding
    try:
        csvfile.read().decode('utf8')
    except UnicodeDecodeError:
        return_value = '', '', _('Import file has wrong character encoding, only UTF-8 is supported!')
    else:
        csvfile.seek(0)
        # Check dialect
        dialect = csv.Sniffer().sniff(csvfile.readline())
        dialect = csv_ext.patchup(dialect)
        csvfile.seek(0)
        # Parse CSV file
        topics = 0
        categories = 0
        for (line_no, line) in enumerate(csv.reader(csvfile, dialect=dialect)):
            if line_no == 0 or len(line) == 0:
                # Do not read the header line
                continue
            # Check and repair format
            if len(line) < 3:
                line.extend(['', ''])
            # Extract data
            title, submitter, category = line[:3]
            if not title:
                continue
            if category:
                category_object, created = Category.objects.get_or_create(name=category)
                if created:
                    categories += 1
            else:
                category_object = None
            Topic.objects.create(title=title, submitter=submitter, category=category_object)
            topics += 1
        success = _('%(categories)d categories and %(topics)d topics successfully imported.') % {'categories': categories, 'topics': topics}
        return_value = success, '', ''
    return return_value
