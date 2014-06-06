"""Tests for the models of the outlets app."""
from django.test import TestCase

from . import factories


class OutletTestCase(TestCase):
    """Tests for the ``Outlet`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``Outlet`` model."""
        outlet = factories.OutletFactory()
        self.assertTrue(outlet.pk)


class OutletCountryTestCase(TestCase):
    """Tests for the ``OutletCountry`` model class."""
    longMessage = True

    def test_instantiation(self):
        """Test instantiation of the ``OutletCountry`` model."""
        outletcountry = factories.OutletCountryFactory()
        self.assertTrue(outletcountry.pk)
