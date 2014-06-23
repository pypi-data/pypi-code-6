import requests
import json
import time
import urllib
import pywantickets.utils as wt_utils
from pywantickets.response import WanticketsResponse
from pywantickets.event import WanticketsEvent
from pywantickets.ticket import WanticketsTicket
from pywantickets.promoter import WanticketsPromoter
from pywantickets.image import WanticketsImage
from pywantickets.artist import WanticketsArtist
from pywantickets.facebook import WanticketsFacebook
from pywantickets.cart import WanticketsCart
from pywantickets.customer import WanticketsCustomer
from pywantickets.shipping import \
    WanticketsAddress, \
    WanticketsDeliveryMethod, \
    WanticketsState
from pywantickets.payment import WanticketsOrder
from datetime import datetime


def parse_wt_dtime(string):
    return datetime.strptime(string, '"%Y-%m-%dT%H:%M:%SZ"')

class WanticketsClient(object):
    def do_request(self):
        raise NotImplementedError()


class WanticketsSearchClient(WanticketsClient):
    api_url="http://www.wantickets.com/Services/Search.ashx"

    def ping(self):
        """ Check if server is working, returns
        a success=true"""
        return self.do_request("validateServer")

    def do_request(self, command=None, params=None, request_token_name=None):
        """ Do an standard request given a command
        and its parameters """

        data = { "command": command }

        if not params is None:
            for p in params:
                data[p] = params[p]

        payload = json.dumps({"SearchAPIRequest": data})

        http_response = requests.post(
            self.api_url,
            data=payload,
            timeout=5,
            headers={
                'content-type': 'application/json',
                'content-length': len(payload)
            }
        )

        json_response = json.loads(http_response.text)["searchAPIResponse"]
        response = WanticketsResponse()
        response.success = True if json_response['success'] else False
        response.result = json_response['results']
        response.message = json_response['message']

        return response

    def get_event_list(self, promoter_id=None):
        params = {}

        if not promoter_id is None:
            params["promoterId"] = int(promoter_id)

        response = self.do_request("getEventList", params=params)

        return response

    def get_event_details(self, ids, last_modified_date=None,
                          only_text_description=False, affiliate_code=None):
        """ Given a list of event ID's, a last modified time
        or an affiliate code, a detailed list of events will be returned"""

        params = {
            "eventIdList": ids,
        }

        return self.do_request("getEventDetails", params)

    def get_events(self, promoter_id=None, ids=None):
        """ Determine wether use getEventList or getEventDetails.
        If ids are given, getEventDetails will be called.
        Otherwise getEventList is used by default"""

        events = []

        if not ids is None:
            """ getEventDetails """

            response = self.get_event_details(ids)
            if response.success:
                for ev in response.result["eventDetails"]:
                    event = WanticketsEvent(
                        id=ev["eventId"],
                        name=ev["eventName"],
                        url=ev["eventURL"],
                        start_date=parse_wt_dtime(ev["eventStartDateTime"]),
                        end_date=parse_wt_dtime(ev["eventEndDateTime"]),
                        sales_cutoff_date=ev["eventSalesCutoffDateTime"],
                        sales_start_date=ev["eventSalesStartDateTime"],
                        last_modified_date=ev["lastModifiedDate"],
                        promoter_id=ev["promoterId"],
                        presented_by=ev["presentedBy"],
                        ages=ev["eventAges"],
                        description=ev["eventDescription"],
                        venue_name=ev["venueName"],
                        venue_address1=ev["venueAddress1"],
                        venue_address2=ev["venueAddress2"],
                        venue_city=ev["venueCity"],
                        venue_state=ev["venueState"],
                        venue_postal_code=ev["venuePostalCode"],
                        venue_country=ev["venueCountry"],
                        venue_timezone=ev["venueTimeZone"],
                        is_available=ev["availableForPurchase"],
                        artists=[
                            WanticketsArtist(
                                id=artist["artistId"],
                                name=artist["artistName"]
                            ) for artist in ev["artists"]
                        ],
                    )

                    events.append(event)

        else:
            """ getEventList """
            response = self.get_event_list(promoter_id=promoter_id)
            if response.success:
                for ev in response.result["events"]:
                    event = WanticketsEvent()
                    event.id = ev["eventId"]
                    event.name = ev["eventName"]
                    event.start_date = ev["eventStartDateTime"]
                    event.url = ev["eventURL"]
                    event.venue_name = ev["venueName"]
                    event.venue_city = ev["venueCity"]
                    event.venue_state = ev["venueState"]
                    event.images = []
                    # TODO: images

                    if "images" in ev:
                        for img in ev["images"]:
                            image = WanticketsImage(url=img["imageURL"], type=img["imageType"])
                            event.images.append(image)

                    events.append(event)

        return events


class WanticketsPurchaseClient(WanticketsClient):
    api_url = "https://www.wantickets.com/Services/Purchase.ashx"
    auth_grant = None
    access_token = None
    auth_expires_on = 0

    def __init__(self, username=None, password=None):
        super(WanticketsPurchaseClient, self).__init__()
        self.username = username
        self.password = password

    def get_access_token(self):
        if time.time() > self.auth_expires_on:
            response = self.do_request("AuthorizationRequest", {
                "UserName": self.username,
                "Password": self.password
            })
            if response.success:
                self.auth_grant = response.result

                response = self.do_request("AccessTokenRequest", {
                    "AUTH_GRANT": self.auth_grant,
                    "AuthenticationCode": "TestAuthCode"
                })
                if response.success:
                    self.access_token = response.result
                    self.auth_expires_on = time.time() + 60*60*2


        return self.access_token


    def do_request(self, command, params=None):
        data = {}

        if command != "AuthorizationRequest" \
        and command != "AccessTokenRequest":
            data["ACCESS_TOKEN"] = self.get_access_token()

        if not params is None:
            for p in params:
                data[p] = params[p]

        http_response = requests.post(self.api_url,
            data={"jsonRequest": wt_utils.to_json({command: data})},
            timeout=5
        )

        response_data = json.loads(http_response.text)["PurchaseAPIResponse"]

        response = WanticketsResponse()
        response.success = True \
            if "IsSuccess" and response_data["IsSuccess"] else False
        response.result = response_data["Result"]
        response.result2 = response_data["Result2"]
        response.message = response_data["ErrorMessage"]

        if command == 'SubmitOrderRequest':
            with open("monda.json", 'wb') as monda:
                monda.write(wt_utils.to_json(data))

        return response

    def authorization(self):
        response = self.do_request("AuthorizationRequest", {
            "UserName": self.username,
            "Password": self.password
        })

        return response

    def get_event_info(self, event):
        return self.do_request("GetEventInfoRequest", {"EventId": int(event)})

    def get_event(self, event_id):
        event = None
        response = self.get_event_info(event_id)
        if response.success:
            pevent = response.result
            event = WanticketsEvent()
            event.id = pevent["EventId"]
            event.name = pevent["EventName"]
            event.currency = pevent["CurrencyCode"]
            event.currency_symbol = pevent["CurrencyHTMLSymbol"]
            event.time_zone = pevent["TimeZone"]
            event.start_date = pevent["EventStartDate"]
            event.end_date = pevent["EventEndDate"]
            event.display_date = pevent["CustomDisplayDate"]
            event.sales_cutoff_date = pevent["SalesCutoffDate"]
            event.utc_sales_cutoff_date = pevent["UTCSalesCutoffDate"]
            event.logo = pevent["EventLogo"]
            event.flyer = pevent["EventFlyer"]
            event.featured_header_image = pevent["FeaturedHeaderImage"]
            # Promoter 
            event.promoter = WanticketsPromoter(
                id=response.result["PromoterId"],
                name=response.result["PromoterName"]
            )
            event.venue_id = pevent["VenueId"]
            event.venue_name = pevent["VenueName"]
            event.venue_address = pevent["VenueAddress"]
            event.venue_city = pevent["VenueCity"]
            event.venue_state = pevent["VenueState"]
            event.venue_zip = pevent["VenueZip"]
            event.venue_phone = pevent["VenuePhone"]
            event.party_type = pevent["PartyType"]
            event.music_type = pevent["MusicType"]
            event.dress_code = pevent["DressCode"]
            event.age_limit = pevent["AgeLimit"]
            event.description = pevent["Description"]
            event.tickets = []
            event.artist=[]
            event.facebook=None

            #Artists
            if "Artists" in response.result:
                for ar in pevent["Artists"]:
                    artist=WanticketsArtist()
                    artist.id=int(ar["ArtistId"])
                    artist.name=ar["ArtistName"]
                    artist.thumbNail=ar["ArtistThumbNail"]
                    artist.bio=ar["Bio"]
                    event.artist.append(artist)

            #Facebook discount share
            if "FacebookDiscountOffer" in response.result and not pevent ["FacebookDiscountOffer"] is None:
                fd = pevent["FacebookDiscountOffer"]
                facebook=WanticketsFacebook()
                facebook.url=fd["FacebookRedirectURL"]
                facebook.discount=fd["DiscountValue"]
                facebook.type=fd["RedemptionType"]
                facebook.maxdiscount=fd["MaxTicketPerDiscount"]
                event.facebook = facebook

            # Tickets
            if "Tickets" in response.result:
                for tk in pevent["Tickets"]:
                    ticket = WanticketsTicket()
                    ticket.id = int(tk["TicketItemId"])
                    ticket.name = tk["TicketName"]
                    ticket.description = tk["TicketDescription"]
                    ticket.price = tk["TicketPrice"]
                    ticket.handling_fee = float(tk["TicketHandlingFee"])
                    ticket.quantity = int(tk["Quantity"])
                    ticket.minimum_purchase_quantity = int(tk["MinimumPurchaseQty"])
                    ticket.maximum_purchase_quantity = int(tk["MaximumPurchaseQty"])
                    ticket.is_soldout = tk["IsSoldout"]
                    ticket.soldout_message = tk["SoldOutMessage"]
                    ticket.is_coupon_required = tk["IsCouponCodeRequired"]
                    event.tickets.append(ticket)

        return event

    def add_item_to_cart(self, ticket_id=None, quantity=1, cart=None):
        response = self.do_request("AddItemToCartRequest", params={
            "TicketItemId": int(ticket_id),
            "Qty": quantity,
            "CurrentCart": cart
        })

        return response

    def create_cart(self):
        cart = WanticketsCart(wt_client=self)
        return cart

    def create_customer(self, **kwargs):
        customer = WanticketsCustomer(**kwargs)
        return customer

    def encrypt_credit_card(self, number=None):
        assert not number is None, "Credit card number not provided"
        return self.do_request("EncryptCreditCardRequest", params={
            "UnencryptedString": str(number)
        })

    def submit_order(self, guid=None, test_mode=True, customer=None,
                     credit_card=None, address=None, cart=None):
        response = self.do_request("SubmitOrderRequest", params={
            "GUID": guid,
            "ForPreviewOnly": test_mode,
            "Customer": customer,
            "CreditCard": credit_card,
            "Address": address,
            "CurrentCart": cart,
        })

        response.order = None

        if not response.success:
            return response

        result = response.result[0]
        order = WanticketsOrder(
            id=result.get("OrderId"),
            is_cancelled=result.get("IsCancelled"),
            date=result.get("OrderDate"),
            guid=result.get("GUID"),
            currency_code=result.get("CurrencyCode"),
            currency_html_symbol=result.get("CurrencyHTMLSymbol"),
            chosen_fedex_shipping_delivery_description\
                =result.get("ChosenFedexShippingDeliveryDescription"),
            chosen_fedex_shipping_delivery_method_id\
                =int(result.get("ChosenFedexShippingDeliveryMethodId")),
            fedex_shipping_fee=float(result.get("FedexShippingFee")),
            chosen_pickup_delivery_description\
                =result.get("ChosenPickupDeliveryDescription"),
            chosen_pickup_delivery_method_id\
                =result.get("ChosenPickupDeliveryMethodId"),
            pickup_fee=result.get('pickup_fee'),
            chosen_regular_mailing_delivery_description\
                =result.get("ChosenRegularMailingDeliveryDescription"),
            chosen_regular_mailing_delivery_method_id\
                =int(result.get("ChosenRegularMailingDeliveryMethodId")),
            regular_mailing_fee=float(result.get("RegularMailingFee")),
            print_at_home_fee=float(result.get("PrintAtHomeFee")),
            will_call_fee=float(result.get("WillCallFee")),
            # customer=Wantickets
        )
        response.order = order

        return response

    def get_available_state(self):
        return self.do_request("GetAvailableStateRequest")

    def get_states(self):
        response = self.get_available_state()
        states = []
        if response.success:
            for astate in response.result:
                states.append(WanticketsState(
                    id=astate.get("StateId"),
                    description=astate.get("StateDescription"),
                    country=astate.get("Country"),
                ))
        return states

    def get_available_country(self):
        return self.do_request("GetAvailableCountryRequest")

    def apply_coupon_code_to_cart(self, coupon_code=None, cart=None):
        response = self.do_request("ApplyCouponCodeToCartRequest", params={
            "CouponCode": coupon_code,
            "CurrentCart": cart,
        })

        return response

    def get_countries(self):
        response = self.get_available_country()
        if response.success:
            countries = response.result
        else:
            countries = []
        return countries

    def login_customer(self, email=None, password=None):
        response = self.do_request("CustomerLoginRequest", params={
            "Email": email,
            "Password": password,
        })

        if response.success:
            result = response.result2
            customer = WanticketsCustomer(
                email=result["Email"],
                first_name=result["FirstName"],
                last_name=result["LastName"],
                id_customer=result["CustomerId"],
            )

            if "AddressesOnRecord" in result:
                for raddr in result["AddressesOnRecord"]:
                    address = WanticketsAddres(
                        first_name=raddr["FirstName"],
                        last_name=raddr["LastName"],
                        address1=raddr["Address1"],
                        address2=raddr["Address2"],
                        city=raddr["City"],
                        state=raddr["State"]
                    )
                    customer.addresses.append(address)

                response.customer = customer
            else:
                response.customer = None
        else:
            pass

        return response

    def modify_item_quantity_or_delivery_method_type_in_cart(
        self, ticket_id, quantity=None,
        delivery_method="", cart=None
    ):
        params = {
            "CurrentCart": cart,
            "DeliveryMethodType": delivery_method,
        }

        if not ticket_id is None:
            params["TicketItemId"] = ticket_id

        if not quantity is None:
            params["Qty"] = quantity

        response = self.do_request(
            "ModifyItemQuantityOrDeliveryMethodTypeInCartRequest",
            params=params
        )

        return response


