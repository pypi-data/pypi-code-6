"""Tests for the models of the outlets app."""
from django.test import TestCase
from django.utils.timezone import now, timedelta

from . import factories
from .. import models


class OutletManagerTestCase(TestCase):
    """Tests for the ``OutletManager`` custom manager."""
    longMessage = True

    def setUp(self):
        future_date = now() + timedelta(days=7)
        past_date = now() - timedelta(days=7)

        self.past_outlet = factories.OutletFactory(
            start_date=past_date, end_date=past_date)
        self.active_outlet = factories.OutletFactory(
            start_date=past_date, end_date=future_date)
        self.future_outlet = factories.OutletFactory(
            start_date=future_date, end_date=future_date)
        self.no_date_outlet = factories.OutletFactory()
        self.no_start_outlet = factories.OutletFactory(start_date=past_date)
        self.no_end_outlet = factories.OutletFactory(end_date=future_date)
        self.ended_in_past_outlet = factories.OutletFactory(
            end_date=past_date)
        self.starts_in_future_outlet = factories.OutletFactory(
            start_date=future_date)

    def test_manager(self):
        self.assertEqual(models.Outlet.objects.active().count(), 4, msg=(
            'Should return the correct amount of active outlets.'))
        self.assertEqual(models.Outlet.objects.future().count(), 6, msg=(
            'Should return the correct amount of future outlets.'))


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
