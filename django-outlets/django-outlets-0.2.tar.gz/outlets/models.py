"""Models for the outlets app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class Outlet(models.Model):
    """
    Holds the information about one outlet store.

    :name: Name of the store.
    :country: The OutletCountry instance of the country, this outlet is in.
    :city: Name of the city.
    :street: Street address.
    :postal_code: The postal code.
    :phone: A phone number of the store.
    :position: The default ordering of the outlet.
    :lat: The latitude of the shop. Required for google maps integration.
    :lon: The longitude of the shop. Required for google maps integration.

    """
    name = models.CharField(verbose_name=_('Name'), max_length=128)
    country = models.ForeignKey('outlets.OutletCountry',
                                verbose_name=_('Country'))
    city = models.CharField(verbose_name=_('City'), max_length=128)
    street = models.CharField(verbose_name=_('Street'), max_length=128)
    postal_code = models.CharField(verbose_name=_('Postal code'),
                                   max_length=10)
    phone = PhoneNumberField(verbose_name=_('Phone'), blank=True, null=True)
    position = models.PositiveIntegerField(verbose_name=_('Position'),
                                           default=1)
    # TODO Maybe make good lat/lon field with proper validation and put to libs
    lat = models.CharField(verbose_name=_('Lat'), max_length=64, blank=True)
    lon = models.CharField(verbose_name=_('Lon'), max_length=64, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('position', 'name')


class OutletCountry(models.Model):
    """
    A country, where the outlet resides.

    :name: The name of the country.
    :slug: A unique slug. E.g. the lowercase name.
    :position: The default ordering of the country.

    """
    name = models.CharField(verbose_name=_('Name'), max_length=128)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=64, unique=True)
    position = models.PositiveIntegerField(verbose_name=_('Position'),
                                           default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('position', 'name')
