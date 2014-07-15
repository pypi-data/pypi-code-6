from pywantickets.shipping import WanticketsDeliveryMethod
from pywantickets import WanticketsModel

class WanticketsCart(WanticketsModel):
    __slots__ = ('id')

    def __init__(self, wt_client=None):
        self._wt_client = wt_client
        self.items = []

    def add_item(self, ticket_id, quantity=1):
        assert not self._wt_client is None, \
            "Wantickets client not initialized"

        response = self._wt_client.add_item_to_cart(
            ticket_id=ticket_id,
            quantity=quantity,
            cart=self if len(self.items) > 0 else None,
        )

        if not response.success \
        or not "CartItems" in response.result \
        or len(response.result) == 0:
            return response

        self.update_cart_from_dict(response.result)

        return response

    def change_quantity(self):
        raise NotImplementedError()

    def remove_item(self, ticket_id):
        """ Removes a ticket from the cart """

        response = self._wt_client \
            .modify_item_quantity_or_delivery_method_type_in_cart(
                ticket_id=ticket_id,
                cart=self,
                quantity=0,
            )

        if not response.success:
            return response

        self.update_cart_from_dict(response.result)

        return response

    def update_cart_from_dict(self, result):
        self.currency_code = result.get("CurrencyCode")
        self.currency_html_symbol = result.get("CurrencyHTMLSymbol")
        self.fedex_shipping_fee = float(result.get("FedexShippingFee"))
        self.chosen_pickup_delivery_method_id \
            = int(result.get("ChosenPickupDeliveryMethodId"))
        self.pickup_fee = float(result.get("PickupFee"))
        self.chosen_regular_mailing_delivery_method_id \
            = int(result.get("ChosenRegularMailingDeliveryMethodId"))
        self.regular_mailing_fee = float(result.get("RegularMailingFee"))
        self.print_at_home_fee = float(result.get("PrintAtHomeFee"))
        self.will_call_fee = float(result.get("WillCallFee"))
        self.coupon_code_applied = result.get("CouponCodeApplied")
        self.coupon_code_value = float(result.get("CouponCodeValue"))
        self.grand_total = float(result.get("GrandTotal"))
        self.fedex_zip_code_estimation = result.get("ZipCodeForFedexShippingEstimation")
        self.fedex_country_estimation = result.get("CountryForFedexShippingEstimation")
        self.customer_ip = result.get("CustomerIP")
        self.aff_code = result.get("AddCode")
        self.chosen_shipping_fedex_delivery_method \
            = int(result.get("ChosenFedexShippingDeliveryMethodId"))

        self.available_shipping_fedex_delivery_methods = []
        for fdx_deliv in result.get("AvailableFedexShippingDeliveryMethods"):
            self.available_shipping_fedex_delivery_methods.append(
                WanticketsDeliveryMethod(
                    id=int(fdx_deliv.get("DeliveryMethodId")),
                    description=fdx_deliv.get("DeliveryMethodDescription"),
                    price=float(fdx_deliv.get("DeliveryMethodPrice")),
                )
            )

        self.available_pickup_delivery_methods = []
        for pick_deliv in result.get("AvailablePickupDeliveryMethods"):
            self.available_pickup_delivery_methods.append(
                WanticketsDeliveryMethod(
                    id=int(pick_deliv.get("DeliveryMethodId")),
                    description=pick_deliv.get("DeliveryMethodDescription"),
                    price=float(pick_deliv.get("DeliveryMethodPrice")),
                )
            )

        self.items = []
        for res in result["CartItems"]:
            self.items.append(parse_cart_item(res))

    def apply_coupon(self, coupon_code):
        response = self._wt_client.apply_coupon_code_to_cart(coupon_code, self)
        if not response.success:
            return response

        self.update_cart_from_dict(response.result)
        return response

    def get_api_model(self):
        return {
            'CartItems': getattr(self, 'items', []),
            'CurrencyCode': getattr(self, 'currency_code', 'USD'),
            'CurrencyHTMLSymbol': getattr(self, 'currency_html_symbol', '$'),
            'AvailableFedexShippingDeliveryMethods': \
                getattr(self, 'available_shipping_fedex_delivery_methods', []),
            'FedexShippingFee': getattr(self, 'fedex_shipping_fee', 0.00),
            'AvailablePickupDeliveryMethods': \
                getattr(self, 'available_pickup_delivery_methods', []),
            'ChosenPickupDeliveryMethodId': \
                getattr(self, 'chosen_pickup_delivery_method_id', 0),
            'PickupFee': getattr(self, 'pickup_fee', float(0.00)),
            'AvailableRegularMailingDeliveryMethods': \
                getattr(self, 'available_regular_mailing_delivery_methods', []),
            'ChosenFedexShippingDeliveryMethodId': \
                getattr(self, 'chosen_shipping_fedex_delivery_method', 0),
            'ChosenRegularMailingDeliveryMethodId': \
                getattr(self, 'chosen_regular_mailing_delivery_method_id', 0),
            'RegularMailingFee': getattr(self, 'regular_mailing_fee', 0.00),
            'PrintAtHomeFee': getattr(self, 'print_at_home_fee', 0.00),
            'WillCallFee': getattr(self, 'will_call_fee', 0.00),
            'CouponCodeApplied': getattr(self, 'coupon_code_applied', None),
            'CouponCodeValue': getattr(self, 'coupon_code_value', float(0.00)),
            'CartItems': getattr(self, 'items', []),
            'GrandTotal': getattr(self, 'grand_total', float(0.00)),
            'ZipCodeForFedexShippingEstimation': \
                getattr(self, 'fedex_zip_code_estimation', ''),
            'CountryForFedexShippingEstimation': \
                getattr(self, 'fedex_country_estimation', ''),
            'CustomerIP': getattr(self, 'customer_ip', None),
            'TrackingCode': getattr(self, 'tracking_code', None),
            'AffCode': getattr(self, 'aff_code', None),
        }


class WanticketsCartItem(WanticketsModel):
    __slots__ = ('id', 'name', 'id_event', 'event_name',
                 'quantity', 'max_quantity', 'min_quantity',
                 'price', 'handling_fee', 'first_name',
                 'last_name', 'delivery_methods', 'delivery_method',
                 'total', 'pickup_first_name', 'pickup_last_name',
                 )

    def __init__(self, **kwargs):
        for p in kwargs:
            setattr(self, p, kwargs[p])

    def get_api_model(self):
        return {
            'TicketItemId': getattr(self, 'id', 0),
            'TicketName': getattr(self, 'name', ''),
            'EventId': getattr(self, 'id_event', ''),
            'EventName': getattr(self, 'event_name', ''),
            'PurchaseQty': getattr(self,'quantity', 1),
            'MinimumPurchaseQty': getattr(self, 'min_quantity', 1),
            'MaximumPurchaseQty': getattr(self, 'max_quantity', 0),
            'TicketPrice': getattr(self, 'price', float(0)),
            'TicketHandlingFee': self.handling_fee,
            'TicketPickupFirstName': getattr(self, 'pickup_first_name', None),
            'AvailableDeliveryMethodTypes': \
                getattr(self, 'delivery_methods', []),
            'SelectedDeliveryMethodType': getattr(self, 'delivery_method', ''),
            'LineItemTotal': getattr(self, 'total', float(0)),
        }

def parse_cart_item(data):
    return WanticketsCartItem(
        id=data.get("TicketItemId", 0),
        name=data.get("TicketName", ''),
        id_event=data.get("EventId", 0),
        event_name=data.get("EventName", ''),
        quantity=data.get("PurchaseQty", 1),
        max_quantity=data.get("MaximumPurchaseQty", 0),
        min_quantity=data.get("MinimumPurchaseQty", 1),
        price=data.get("TicketPrice", float(0)),
        handling_fee=data.get("TicketHandlingFee", float(0)),
        first_name=data.get("TicketPickupFirstName", ''),
        last_name=data.get("TicketPickupLastName", ''),
        delivery_methods=data.get("AvailableDeliveryMethodTypes", []),
        delivery_method=data.get("SelectedDeliveryMethodType", ''),
        total=data.get("LineItemTotal", float(0)),
    )
