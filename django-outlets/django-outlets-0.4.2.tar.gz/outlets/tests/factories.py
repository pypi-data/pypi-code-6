"""Factories for the outlets app."""
from django.utils.text import slugify

import factory

from .. import models


class OutletFactory(factory.DjangoModelFactory):
    """Factory for the ``Outlet`` model."""
    FACTORY_FOR = models.Outlet

    name = factory.Sequence(lambda n: u'name {0}'.format(n))
    country = factory.SubFactory(
        'outlets.tests.factories.OutletCountryFactory')
    city = factory.Sequence(lambda n: u'city {0}'.format(n))
    street = factory.Sequence(lambda n: u'street {0}'.format(n))
    postal_code = factory.Sequence(lambda n: u'555{0}'.format(n))


class OutletCountryFactory(factory.DjangoModelFactory):
    """Factory for the ``OutletCountry`` model."""
    FACTORY_FOR = models.OutletCountry

    name = factory.Sequence(lambda n: u'name {0}'.format(n))
    slug = factory.LazyAttribute(lambda oc: slugify(oc.name))
