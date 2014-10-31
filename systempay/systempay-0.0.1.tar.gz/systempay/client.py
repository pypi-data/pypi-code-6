import pytz
import hashlib
import suds.client

from .utils import get_factory_data, get_formatted_value, RESPONSE_SIGNATURE_KEYS


PRODUCTION = 'PRODUCTION'
TEST = 'TEST'


class SystempayMixin(object):
    """
    Systempay mixin for signature calculation and datetime operations
    """
    def __init__(self, shop_id, certificate, context, tz):
        """
        Creates a Systempay mixin instance

        :param shop_id: The merchant shop ID
        :type shop_id: str or int
        :param certificate: The merchant certificate
        :type certificate: str or int
        :param context: The context to use (production or test)
        :type context: str
        :param tz: The timezone to use in the fomat like 'Europe/Paris'
        :type tz: str
        """
        assert context in [PRODUCTION, TEST], "Invalid context"

        self.shop_id = shop_id
        self.certificate = certificate
        self.context = context
        self.tz = pytz.timezone(tz)

    def get_signature(self, factory, keys=None, excludes=None):
        """
        Returns the factory signature

        :param factory: The source Factory object
        :type factory: `suds.client.Factory`
        :param keys: Explicit list of keys to use for signature calculation. If None,
        uses all the fields from the Factory.
        :type keys: list
        :param excludes: A list of fields to exclude for signature calculation
        :type excludes: list
        :returns: The SHA1 of the factory signature
        :rtype: str
        """
        sha = hashlib.sha1()
        factory_data = get_factory_data(factory, keys, excludes)

        # Create signature string
        signature = '+'.join(
            get_formatted_value(v) for v in list(zip(*factory_data))[1])

        # Append certificate
        signature += '+' + str(self.certificate)

        # Return signature string sha1
        sha.update(signature.encode())
        return sha.hexdigest()

    def format_and_get_signature(self, factory, keys=None, excludes=None):
        """
        Formats the factory by setting shopId and ctxMode fields if they exists
        and returns the computed signature

        :param factory: The source Factory object
        :type factory: `suds.client.Factory`
        :param keys: Explicit list of keys to use for signature calculation. If None,
        uses all the fields from the Factory.
        :type keys: list
        :param excludes: A list of fields to exclude for signature calculation
        :type excludes: list
        :returns: The SHA1 of the factory signature
        :rtype: str
        """
        if hasattr(factory, 'shopId'):
            factory.shopId = str(self.shop_id)

        if hasattr(factory, 'ctxMode'):
            factory.ctxMode = self.context

        return self.get_signature(factory, keys, excludes)

    def __get_localized_datetime_format(self, dt, tz):
        """
        Returns the RFC 3339 datetime format using the given timezone

        :param dt: The datetime object to convert
        :type dt: `datetime.datetime`
        :param tz: The timezone to use for converting datetime object
        :type tz: `pytz.DstTzInfo`
        :returns: The formatted datetime in format like '2014-12-30T10:00:00+01:00'
        :rtype: str
        """
        tz_aware = tz.localize(dt).replace(microsecond=0)
        return tz_aware.isoformat()

    def get_local_datetime_format(self, dt):
        """
        Returns the RFC 3339 datetime format using the local timezone

        :param dt: The datetime object to convert
        :type dt: `datetime.datetime`
        :returns: The formatted datetime in format like '2014-12-30T10:00:00+01:00'
        :rtype: str
        """
        return self.__get_localized_datetime_format(dt, self.tz)

    def get_utc_datetime_format(self, dt):
        """
        Returns the RFC 3339 datetime format using UTC timezone

        :param dt: The datetime object to convert
        :type dt: `datetime.datetime`
        :returns: The formatted datetime in format like '2014-12-30T10:00:00+00:00'
        :rtype: str
        """
        return self.__get_localized_datetime_format(dt, pytz.utc)

    def response_is_valid(self, response):
        """
        Returns whether the response is a valid one by checking
        its signature

        :param response: The suds client response to check
        :type response: `suds.sudsobject.identResponse`
        :returns: Whether the response is valid or not
        :rtype: bool
        """
        response_signature = getattr(response, 'signature', None)
        computed_signature = self.get_signature(
            response, keys=RESPONSE_SIGNATURE_KEYS)

        return computed_signature == response_signature


class Client(SystempayMixin, suds.client.Client):
    """
    Systempay API Client extending suds Client
    """
    def __init__(self, url, shop_id, certificate, context, tz, **kwargs):
        """
        Creates a Systempay Client instance

        :param url: The API endpoint url
        :type url: str
        :param shop_id: The merchant shop ID
        :type shop_id: str or int
        :param certificate: The merchant certificate
        :type certificate: str or int
        :param context: The context to use (production or test)
        :type context: str
        :param tz: The timezone to use in the fomat like 'Europe/Paris'
        :type tz: str
        """
        SystempayMixin.__init__(self, shop_id, certificate, context, tz)
        suds.client.Client.__init__(self, url, **kwargs)

