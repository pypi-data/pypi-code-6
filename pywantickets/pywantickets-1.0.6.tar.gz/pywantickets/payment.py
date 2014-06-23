from pywantickets import WanticketsModel


class WanticketsOrder(WanticketsModel):
	__slots__ = ('id', 'is_cancelled', 'date', 'guid',
				 'currency_code', 'currency_html_symbol',
				 'chosen_fedex_shipping_delivery_description',
				 'chosen_fedex_shipping_delivery_method_id',
				 'fedex_shipping_fee',
				 'chosen_pickup_delivery_description',
				 'chosen_pickup_delivery_method_id',
				 'pickup_fee', 'chosen_regular_mailing_delivery_description',
				 'chosen_regular_mailing_delivery_method_id',
				 'regular_mailing_fee', 'print_at_home_fee',
				 'will_call_fee', 'customer', 'address',
				 'credit_card_first_name', 'credit_card_last_name',
				 'credit_card_last_four_digits', 'coupon_code_applied',
				 'coupon_code_value', 'items', 'grand_total')

	def __init__(self, **kwargs):
		for k in kwargs:
			setattr(self, k, kwargs[k])

		self._wt_client = None

	def set_wt_client(self, client):
		self._wt_client = client




