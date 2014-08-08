"""
The RAD record format defines what a flat record should look like. It's
an unifying format that is used through out the application.

This record is passed around the different components of the application
to keep a consistent data format. Also it is a good model for other people
in the team looking for data. It gives our data collection some backbone.

For example a scraper is ran, it returns a list of "RadRecord"s, some
middleware takes these records and calls a function that accepts "RadRecord"s
and creates and saves database records from them. That way the scraper doesn't
know about the database and the database models aren't structured around the
scrapers.

Use the rad_record function to create new records. It allows you to create
objects without specifying all of the fields.

>>> r = rad_record('Some Hospital')
>>> r.city is None # True
>>> r2 = rad_record('Other Hospital', city='Chicago', state='Illinois')
>>> r2.city is None # False

The rad_record function will return an instance of RadRecord.

>>> r3 = rad_record('Vida Sida')
>>> r3.is_valid() # True
>>> r4 = rad_record(None)
>>> r4.is_valid() # False

For now all record needs to be valid is a name. In the future
more restrictions might arise. Before being saved to a database or
something similar should be valid.

"""

from collections import namedtuple


"""
A record contains the following fields.
The procedure type and category name are
optional. They are transformed by middleware
into relationships at the database.

The one field that is completely necessary is
`name`. This might be an institutions name, or
a doctor to name some examples.

Underneath the hood a RadRecord is a Python named
tuple, read it's documentation if you aren't familiar
with it. It is a very nice and slick data structure.

"""
RadRecord = namedtuple('RadRecord',
                       ('name',
                        'street',
                        'city',
                        'state',
                        'country',
                        'zipcode',
                        'email',
                        'phone',
                        'fax',
                        'url',
                        'description',
                        'source',
                        'category_name',
                        'procedure_type',
                        'visible'))


def is_valid(record):
    """
    A function to help validate RadRecords.
    A RadRecord name's should not be None.
    In the future we might impose more
    constraints

    :param record:
    :return:
    """
    return record.name is not None

# Give every RadRecord a method to help with validation.
RadRecord.is_valid = is_valid


def rad_record(name, street=None, city=None, state=None, country=None,
               zipcode=None, email=None, phone=None, fax=None, url=None,
               description=None, source=None, category_name=None,
               procedure_type=None, visible=True):
    """
    Convenience method to create RadRecords with optional fields.
    Use this instead of the class constructor so you don't have to
    specify the all the fields.

    """
    return RadRecord(name, street, city, state, country, zipcode, email, phone,
                     fax, url, description, source, category_name, procedure_type,
                     visible)
