# -*- coding: utf-8 -*-

from .utils import not_implemented


class ConversionsMixin(object):
    @staticmethod
    def bool_to_yes_or_no(boolean):
        """
        :param boolean:
        :return: YES if True NO if False
        """
        return 'YES' if boolean else 'NO'

    @staticmethod
    def bool_to_1_or_0(boolean):
        """
        :param boolean:
        :return: 1 if True 0 if False
        """
        return 1 if boolean else 0

    @staticmethod
    def convert__expiration_date(datetime):
        """
        :param datetime:
        :return: A string formatted "%m%y"
        """
        return datetime.strftime("%m%y")

    convert__upsell_count = bool_to_1_or_0
    convert__billing_same_as_shipping = bool_to_yes_or_no
    convert__cascade_enabled = bool_to_1_or_0
    convert__save_customer = bool_to_1_or_0


class FieldsMixin(object):
    unconverted_field_labels = not_implemented
    schema = not_implemented
    endpoint = not_implemented
    error = not_implemented
    username = not_implemented
    password = not_implemented
    host = not_implemented

    def parse_response(self, response):
        raise NotImplementedError
