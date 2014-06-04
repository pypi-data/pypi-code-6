from pywantickets import WanticketsModel

class WanticketsCustomer(WanticketsModel):
    __slots__ = ('email', 'password', 'first_name', 'last_name',
                 'customer_login', 'id_customer', 'addresses')
    
    def __init__(self, **kwargs):
        for p in kwargs:
            setattr(self, p, kwargs[p])
        if not hasattr(self, "addresses"):
            self.addresses = []

    def get_api_model(self):
        return {
            'Email': self.email,
            'Password': self.password,
            'FirstName': self.first_name,
            'LastName': self.last_name,
        }



