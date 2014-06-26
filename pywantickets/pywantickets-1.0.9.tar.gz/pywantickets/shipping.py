from pywantickets import WanticketsModel


class WanticketsDeliveryMethod(WanticketsModel):
    def __init__(self, **kwargs):
        super(WanticketsDeliveryMethod, self).__init__()
        for p in kwargs:
            setattr(self, p, kwargs[p]) 
            
    def get_api_model(self):
    	return {
    		'DeliveryMethodId': getattr(self, 'id', None),
    		'DeliveryMethodDescription': getattr(self, 'description', ''),
    		'DeliveryMethodPrice': getattr(self, 'price', 0.00),
    	}

class WanticketsAddress(WanticketsModel):
    __slots__ = ('fist_name', 'last_name', 'addresss',
                 'address2', 'city', 'state', 'zip',
                 'country', 'phone')
    
    def __init__(self, **kwargs):
        for p in kwargs:
            setattr(self, p, kwargs[p])

    def get_api_model(self):
        return {
            'FirstName': getattr(self, 'first_name', ''),
            'LastName': getattr(self, 'last_name', ''),
            'Address1': getattr(self, 'address1', ''),
            'Address2': getattr(self, 'address2', ''),
            'City': getattr(self, 'city', ''),
            'StateId': getattr(self, 'state', 'TN'),
            'Zip': getattr(self, 'zip', '00000'),
            'Country': getattr(self, 'coountry', 'United States'),
            'Phone': getattr(self, 'phone', ''),
        }

class WanticketsState(WanticketsModel):
    __slots__ = ('id', 'description', 'country')

    def __init__(self, **kwargs):
        for p in kwargs:
            setattr(self, p, kwargs[p])