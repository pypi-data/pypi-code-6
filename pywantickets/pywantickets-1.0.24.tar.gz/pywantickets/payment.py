from pywantickets import WanticketsModel
from pywantickets.customer import parse_customer
from pywantickets.shipping import parse_address
from pywantickets.cart import parse_cart_item


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


class WanticketsOrderItem(WanticketsModel):
    __slots__ = ('id', 'name', 'event_id', 'event_name',
                 'quantity', 'price', 'handling_fee',
                 'pickup_first_name', 'pickup_last_name',
                 'delivery_method', 'total', 'venue',
                 'barcodes')

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self._wt_client = None

def parse_order(data):
    return WanticketsOrder(
        id=int(data.get("OrderId")),
        is_cancelled=data.get("IsCancelled"),
        date=data.get("OrderDate"),
        guid=data.get("GUID"),
        currency_code=data.get("CurrencyCode"),
        currency_html_symbol=data.get("CurrencyHTMLSymbol"),
        chosen_fedex_shipping_delivery_description\
            =data.get("ChosenFedexShippingDeliveryDescription"),
        chosen_fedex_shipping_delivery_method_id\
            =int(data.get("ChosenFedexShippingDeliveryMethodId")),
        fedex_shipping_fee=float(data.get("FedexShippingFee")),
        chosen_pickup_delivery_description\
            =data.get("ChosenPickupDeliveryDescription"),
        chosen_pickup_delivery_method_id\
            =data.get("ChosenPickupDeliveryMethodId"),
        pickup_fee=data.get('pickup_fee'),
        chosen_regular_mailing_delivery_description\
            =data.get("ChosenRegularMailingDeliveryDescription"),
        chosen_regular_mailing_delivery_method_id\
            =int(data.get("ChosenRegularMailingDeliveryMethodId")),
        regular_mailing_fee=float(data.get("RegularMailingFee")),
        print_at_home_fee=float(data.get("PrintAtHomeFee")),
        will_call_fee=float(data.get("WillCallFee")),
        grand_total=float(data.get('GrandTotal', 0)),
        customer=parse_customer(data.get('Customer')),
        address=parse_address(data.get('Address')),
        items=[parse_order_item(item) for item in data.get('OrderItems')],
        # customer=Wantickets
    )

def parse_order_item(data):
    return WanticketsOrderItem(
        id=data.get('TicketItemId'),
        name=data.get('TicketName'),
        event_id=data.get('EventId'),
        event_name=data.get('EventName'),
        quantity=data.get('PurchaseQty', 0),
        price=data.get('TicketPrice', float(0)),
        handling_fee=data.get('TicketHandlingFee', float(0)),
        pickup_first_name=data.get('TicketPickupFirstName'),
        pickup_last_name=data.get('TicketPickupLastName'),
        delivery_method=data.get('SelectedDeliveryMethodType'),
        total=data.get('LineItemTotal', 0),
        venue=data.get('VenueName'),
        barcodes=[a_code for a_code in data.get('BarCodes')],
    )
