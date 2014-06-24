from pywantickets import WanticketsModel


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
