from pywantickets import WanticketsModel
from pywantickets.utils import parse_wt_dtime
from pywantickets.artist import WanticketsArtist


class WanticketsEvent(WanticketsModel):

    def __init__(self, **kwargs):
        for p in kwargs:
            setattr(self, p, kwargs[p])

	def get_tickets(self):
		""" Returns tickets list of current event """
		if not self._wt_client is None:
			response = self._wt_client.get_ticket_list(events=[str(self.id)])
			return response.ticket_list

	def set_wt_client(self, wt_client):
		self._wt_client = wt_client

def parse_search_event(data):
	return WanticketsEvent(
        id=data["eventId"],
        name=data["eventName"],
        url=data["eventURL"],
        start_date=parse_wt_dtime(data["eventStartDateTime"]),
        end_date=parse_wt_dtime(data["eventEndDateTime"]),
        sales_cutoff_date=parse_wt_dtime(data["eventSalesCutoffDateTime"]),
        sales_start_date=parse_wt_dtime(data["eventSalesStartDateTime"]),
        last_modified_date=parse_wt_dtime(data["lastModifiedDate"]),
        promoter_id=data["promoterId"],
        presented_by=data["presentedBy"],
        ages=data["eventAges"],
        description=data["eventDescription"],
        venue_name=data["venueName"],
        venue_address1=data["venueAddress1"],
        venue_address2=data["venueAddress2"],
        venue_city=data["venueCity"],
        venue_state=data["venueState"],
        venue_postal_code=data["venuePostalCode"],
        venue_country=data["venueCountry"],
        venue_timezone=data["venueTimeZone"],
        is_available=data["availableForPurchase"],
        artists=[
            WanticketsArtist(
                id=artist["artistId"],
                name=artist["artistName"]
            ) for artist in data["artists"]
        ],
    )
