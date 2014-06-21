# -*- coding: utf-8 -*-
from models import *

from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from product.models import Product, Category



class CMSSatchmoProductPlugin(CMSPluginBase):
	"""Main product plugin for Django CMS"""
	module = 'Satchmo Shop'
	model = SatchmoProductPlugin
	name = _('Product detail')
	render_template = 'cmsplugin_satchmo/product.html'
	raw_id_fields = ('product',)
	fields = ['product', 'title', 'style',]

	def render(self, context, instance, placeholder):
		context.update({
			'instance': instance,
			'placeholder': placeholder,
		})
		return context
plugin_pool.register_plugin(CMSSatchmoProductPlugin)


class CMSSatchmoProductsListingPlugin(CMSPluginBase):
	"""Main plugin for product listing in Django CMS"""
	module = 'Satchmo Shop'
	model = SatchmoProductsListPlugin
	name = _('Products listing')
	render_template = 'cmsplugin_satchmo/products_listing.html'
	fields = ['list_type', 'number', 'site', 'title', 'style',]

	def render(self, context, instance, placeholder):
		products = Product.objects.active().filter(site=instance.site)

		if instance.list_type == RECENT_PRODUCTS_CHOICE_ID:
			products = products.order_by('-date_added', '-id')
		elif instance.list_type == BESTSELLERS_CHOICE_ID:
			products = products.order_by('-total_sold')
		elif instance.list_type == FEATURED_PRODUCTS_CHOICE_ID:
			products = products.filter(featured=True).order_by('?')
		else:
			raise ValueError('(cmsplugin_satchmo) List type is not defined in PRODUCTS_LISTING_CHOICES!')

		products = products[:instance.number]
		for product in products:
			product.get_absolute_url = instance.create_absolute_url(product)

		context.update({
			'products': products,
			'instance': instance,
			'placeholder': placeholder,
		})
		return context
plugin_pool.register_plugin(CMSSatchmoProductsListingPlugin)



class CMSSatchmoCategoryPlugin(CMSPluginBase):
	"""Main category plugin for Django CMS"""
	module = 'Satchmo Shop'
	model = SatchmoCategoryPlugin
	name = _('Category detail')
	render_template = 'cmsplugin_satchmo/category.html'
	raw_id_fields = ('category',)
	fields = ['category', 'title', 'style',]

	def render(self, context, instance, placeholder):
		context.update({
			'instance': instance,
			'placeholder': placeholder,
		})
		return context
plugin_pool.register_plugin(CMSSatchmoCategoryPlugin)



class CMSSatchmoCategoriesListPlugin(CMSPluginBase):
	"""Main plugin for categories listing in Django CMS"""
	module = 'Satchmo Shop'
	model = SatchmoCategoriesListPlugin
	name = _('Categories listing')
	render_template = 'cmsplugin_satchmo/categories_listing.html'
	fields = ['main_category', 'site', 'title', 'style',]

	def render(self, context, instance, placeholder):
		categories = Category.objects.active().filter(site=instance.site)

		if instance.main_category:
			categories = categories.filter(parent=instance.main_category)
		
		categories = categories.order_by('ordering')

		for category in categories:
			category.get_absolute_url = instance.create_absolute_url(category)
			
		context.update({
			'categories': categories,
			'instance': instance,
			'placeholder': placeholder,
		})
		return context
plugin_pool.register_plugin(CMSSatchmoCategoriesListPlugin)


