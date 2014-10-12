import unicodecsv
from kvtags.models import *


def import_tags_csv(csv_file):
    """Imports tags from a csv file to the database.

    A file instance must be provided as an argument.
    File must be opened beforehand.

    The first row is for tag key.
    The second row is for keys of key-value pairs
    Subsequent rows are values of key-value pairs.

    :param csv_file: opened csv file instance
    """
    reader = unicodecsv.reader(csv_file, encoding='utf-8')
    tag_key = reader.next()[0]
    keys = reader.next()

    for row in reader:
        tag = None
        news = []

        for index, value in enumerate(row):
            if tag is None:
                try:
                    key_value = KeyValue.objects.get(key=keys[index], value=value, tag__key=tag_key)
                    tag = key_value.tag
                except KeyValue.DoesNotExist:
                    obj = KeyValue(key=keys[index], value=value)
                    news.append(obj)
            else:
                KeyValue.objects.get_or_create(tag=tag, key=keys[index], value=value)

        if tag is None:
            tag = Tag.objects.create(key=tag_key)

        for new in news:
            new.tag = tag
            new.save()
