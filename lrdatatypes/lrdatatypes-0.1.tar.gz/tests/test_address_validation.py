import unittest

from copy import deepcopy
from datatypes import address_validator
from datatypes.core import DataDoesNotMatchSchemaException
from datatypes.core import unicoded

class TestAddressValidation(unittest.TestCase):

    def setUp(self):

        self.address_with_mandatory_fields = unicoded({
            "full_address" : "8 Acacia Avenue, Bootata, AL3 5PU",
            "house_no" : "8",
            "street_name" : "Acacia Avenue",
            "town" : "Bootata",
            "postal_county" : "",
            "region_name" : "Smotania",
            "postcode" : "AL3 5PU",
            "country" : "Wales"
        })

        self.no_full_address = unicoded({
            "house_no" : "8",
            "street_name" : "Acacia Avenue",
            "town" : "Bootata",
            "postal_county" : "",
            "region_name" : "Smotania",
            "postcode" : "AL3 5PU",
            "country": "Wales"
        })

        self.without_all_additional_fields = unicoded({
            "full_address" : "8 Acacia Avenue, Bootata, AL3 5PU"
        })

        self.address_with_empty_postcode = unicoded({
            "full_address" : "8 Acacia Avenue, Bootata, AL3 5PU",
            "house_no" : "8",
            "street_name" : "Acacia Avenue",
            "town" : "Bootata",
            "postal_county" : "",
            "region_name" : "Smotania",
            "postcode" : "",
            "country" : "Wales"
        })



    def test_address_with_no_full_address_fails_validation(self):
        self.assertRaises(DataDoesNotMatchSchemaException, address_validator.validate, self.no_full_address)

    def test_address_without_additional_fields_fails_validation(self):
        self.assertRaises(DataDoesNotMatchSchemaException, address_validator.validate, self.without_all_additional_fields)

    def test_address_with_whitespace_full_address_fails_validation(self):
        address_with_whitespace_full_address = deepcopy(self.address_with_mandatory_fields )
        address_with_whitespace_full_address["full_address"] = "    \t \n  "
        self.assertRaises(DataDoesNotMatchSchemaException, address_validator.validate, address_with_whitespace_full_address)

    def test_can_validate_address_with_required_mandatory_fields(self):
        try:
            address_validator.validate(self.address_with_mandatory_fields)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate address: " + repr(e))

    def test_can_detect_correct_number_of_missing_fields_from_exception(self):
        try:
            address_validator.validate({})
        except DataDoesNotMatchSchemaException as exception:
            print repr(exception.field_errors)
            self.assertEquals(len(exception.field_errors), 8)  # we have eight required fields

    def test_can_validate_address_with_empty_postcode(self):
        try:
            address_validator.validate(self.address_with_empty_postcode)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate address: " + repr(e))
