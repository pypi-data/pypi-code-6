from django.db import models
from django.utils.translation import ugettext_lazy as _

CURRENCIES = (
	('CAD', 'CANADIAN DOLLAR'),
	('USD', 'UNITED STATES DOLLAR'),
	('GBP', 'GREAT BRITAIN POUND STERLING'),
	('NGN', 'NIGERIAN NAIRA')
)

class Tax(models.Model):
	# Saves a tax object after the tax has
	# been calculated based on the predefined
	# taxes available in the tax dictionary
	amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
	timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
	currency = models.CharField(_('Currency'), max_length=3, choices=CURRENCIES)

	def __unicode__(self):
		# Identifies a particular collected tax by
		# a friendly string representation
		return 'Tax of %(amount)s paid on %(date)s' % {'amount': self.amount,
													   'date': self.timestamp.strftime('%m/%d/%y')}

class CanadianTax(models.Model):
	# Due to the peculiar nature of Canadian
	# taxes, we need to be able to keep track
	# of the composition of the tax levied
	base = models.OneToOneField(Tax, verbose_name=_('base'), related_name=_('ca_tax'))
	gst = models.DecimalField(_('GST'), null=True, blank=True,
							  decimal_places=2, max_digits=10)
	hst = models.DecimalField(_('HST'), null=True, blank=True,
							  decimal_places=2, max_digits=10)
	pst = models.DecimalField(_('PST'), null=True, blank=True,
							  decimal_places=2, max_digits=10)
