from pywantickets import WanticketsModel


class WanticketsCreditCard(WanticketsModel):
	__slots__ = ('first_name', 'last_name', 'number',
				 'cvv', 'expires_month', 'expires_year',
				 'zip')

	def get_api_model(self):
		return {
			"CreditCardFirstName": self.first_name,
			"CreditCardLastName": self.last_name,
			"CreditCardNumber": self.number,
			"CVV": self.cvv,
			"ExpireMonth": self.expires_month,
			"ExpireYear": self.expires_year,
			# "BillingZip": getattr(self, 'zip', '00000'),
		}

	