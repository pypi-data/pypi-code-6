# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin

from product.models import Product, Category



RECENT_PRODUCTS_CHOICE_ID = 1
BESTSELLERS_CHOICE_ID = 2
FEATURED_PRODUCTS_CHOICE_ID = 3

PRODUCTS_LISTING_CHOICES = (
	(RECENT_PRODUCTS_CHOICE_ID, _(u'recent products'),),
	(BESTSELLERS_CHOICE_ID, _(u'bestsellers'),),
	(FEATURED_PRODUCTS_CHOICE_ID, _(u'featured products'),),
)

class SatchmoSiteSetting(models.Model):
	"""Because every Satchmo site can use different settings for SHOP_BASE, PRODUCT_SLUG and CATEGORY_SLUG
	the system must know the right variables for every site otherwise we can't create the right 'absolute_url'
	for the site specific product/category"""
	site = models.OneToOneField(Site, related_name='satchmo_sites', verbose_name=_(u'site'))
	shop_base = models.CharField(_(u'shop base slug'), max_length=50, help_text=_(u'E.g. if in your SATCHMO_SETTINGS is defined SHOP_BASE as "/shop/" fill "/shop/" here.'))
	product_slug = models.SlugField(_(u'product slug'), max_length=50, help_text=_(u'E.g. if in your SATCHMO_SETTINGS is defined PRODUCT_SLUG as "products" fill "products" here.'))
	category_slug = models.SlugField(_(u'category slug'), max_length=50, help_text=_(u'E.g. if in your SATCHMO_SETTINGS is defined CATEGORY_SLUG as "category" fill "category" here.'))

	def __unicode__(self):
		return self.site.name
	
	def get_site_url(self, site):
		current_site = Site.objects.get_current()
		if site == current_site:
			return ''
		else:
			return '//%s' % site.domain

	def get_product_url(self, product):
		site_url = self.get_site_url(product.site)
		return '%s%s%s/%s/' % (site_url, self.shop_base, self.product_slug, product.slug)

	def get_category_url(self, category):
		site_url = self.get_site_url(category.site)
		slug_list = [cat.slug for cat in category.parents()]
		if slug_list:
			slug_list = "/".join(slug_list) + "/"
		else:
			slug_list = ""
		return '%s%s%s/%s%s/' % (site_url, self.shop_base, self.category_slug, slug_list, category.slug)

	def product_url_path(self):
		return u'%s%s/<%s>' % (self.shop_base, self.product_slug, _(u'product'))
	product_url_path.short_description = _(u'product\'s path')

	def category_url_path(self):
		return u'%s%s/<%s>' % (self.shop_base, self.category_slug, _(u'category'))
	category_url_path.short_description = _(u'category\'s path')

	class Meta:
		verbose_name = _(u'CMS plugin Satchmo Setting')
		verbose_name_plural = _(u'CMS plugin Satchmo Settings')
	


class CommonSatchmoPlugin(CMSPlugin):
	"""Only wrapper for DRY reasons"""
	title = models.CharField(_(u'title'), max_length=200, blank=True, help_text=_(u'Alternative text'))
	style = models.CharField(_(u'class'), max_length=100, blank=True, help_text=_(u'Name of CSS class for template cusomization'))

	class Meta:
		abstract = True



class SatchmoProductPlugin(CommonSatchmoPlugin):
	"""Model for the plugin for inlining a satchmo product"""
	product = models.ForeignKey(Product, verbose_name=_(u'product'), limit_choices_to={'active': True})

	def get_absolute_url(self):
		satchmo_site_setting = SatchmoSiteSetting.objects.get(site=self.product.site)
		return satchmo_site_setting.get_product_url(self.product)



class SatchmoProductsListPlugin(CommonSatchmoPlugin):
	"""Model for the plugin of product listing"""
	list_type = models.PositiveSmallIntegerField(_(u'kind of list'), choices=PRODUCTS_LISTING_CHOICES)
	number = models.PositiveSmallIntegerField(_(u'number'), default=5)
	site = models.ForeignKey(Site, verbose_name=_(u'products list from site'))
	
	def create_absolute_url(self, product):
		satchmo_site_setting = SatchmoSiteSetting.objects.get(site=self.site)
		return satchmo_site_setting.get_product_url(product)



class SatchmoCategoryPlugin(CommonSatchmoPlugin):
	"""Model for the plugin of category detail"""
	category = models.ForeignKey(Category, verbose_name=_(u'category'), limit_choices_to={'is_active': True})

	def get_absolute_url(self):
		satchmo_site_setting = SatchmoSiteSetting.objects.get(site=self.category.site)
		return satchmo_site_setting.get_category_url(self.category)



class SatchmoCategoriesListPlugin(CommonSatchmoPlugin):
	main_category = models.ForeignKey(Category, verbose_name=_(u'main category'), limit_choices_to={'is_active': True}, blank=True, null=True,
		help_text=_(u'Leave blank for listing root categories or select main category for listing their child categries.')
	)
	site = models.ForeignKey(Site, verbose_name=_(u'categories list from site'))

	def create_absolute_url(self, category):
		satchmo_site_setting = SatchmoSiteSetting.objects.get(site=self.site)
		return satchmo_site_setting.get_category_url(category)

