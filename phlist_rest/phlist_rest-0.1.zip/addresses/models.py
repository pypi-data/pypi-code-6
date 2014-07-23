from django.db import models
from django.template.defaultfilters import slugify


def generate_city_slug(city_name, province_name):
    s = u'{!s}, {!s}'.format(city_name, province_name)
    return slugify(s)


class Province(models.Model):
    ISLAND_GROUP_CHOICES = [
        ('LUZON', 'Luzon'),
        ('VISAYAS', 'Visayas'),
        ('MINDANAO', 'Mindanao'),
    ]
    class Meta:
        ordering = ['country', 'name']
    name = models.CharField('Province', unique=True, max_length=50)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    island_group = models.CharField('Island Group', choices=ISLAND_GROUP_CHOICES, max_length=10)
    country = models.CharField('Country', max_length=20, default='Philippines')

    def __unicode__(self):
        return u'{!s}, {!s}, {!s}'.format(self.name, self.island_group, self.country)

    def save(self):
        #Only set the slug when the object is created.
        self.name = self.name.strip()
        if not self.id:
            self.slug = slugify(self.name)
        super(Province, self).save()


class City(models.Model):
    class Meta:
        ordering = ['province', 'name']
        verbose_name_plural = 'Cities'
    name = models.CharField('Municipality/City', max_length=50)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    province = models.ForeignKey(Province, to_field='slug')   

    def __unicode__(self):
        return u'{!s}, {!s}'.format(self.name, self.province.name)

    # override models save method:
    def save(self):
        #Only set the slug when the object is created.
        self.name = self.name.strip()
        if not self.id:
            self.slug = generate_city_slug(self.name, self.province.name)
        super(City, self).save()


class FullAddress(models.Model):
    building = models.CharField(max_length=100, blank=True)
    house_number = models.CharField(max_length=50, blank=True)
    street_name = models.CharField(max_length=100, blank=True)
    barangay = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.ForeignKey(City, to_field='slug')
