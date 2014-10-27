import unittest
from copy import deepcopy

from datatypes.exceptions import DataDoesNotMatchSchemaException

from datatypes import property_description_validator
from datatypes.core import unicoded

property_description = unicoded({
        "template" : "example text",
        "full_text" : "example text",
        "fields" : {"addresses": [{
                    "full_address" : "8 Acacia Avenue, Bootata, AL3 5PU",
                    "house_no" : "8",
                    "street_name" : "Acacia Avenue",
                    "town" : "Bootata",
                    "postal_county" : "",
                    "region_name" : "Smotania",
                    "postcode" : "AL3 5PU",
                    "country" : "Wales",
                    "something": "random which should not matter"
                }]
        },
        "deeds" : [],
        "notes": []
})


class TestPropertyDescriptionValidation(unittest.TestCase):

    def test_can_validate_valid_property_description(self):
        try:
            property_description_validator.validate(property_description)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate entry: " + repr(e))


    def test_cannot_validate_property_description_without_addresses(self):
        invalid_property_description = deepcopy(property_description)
        invalid_property_description["fields"]["addresses"] = []
        try:
            property_description_validator.validate(invalid_property_description)
        except DataDoesNotMatchSchemaException as e:
            error = e.field_errors.get("fields.addresses")
            self.assertIsNotNone(error)
            self.assertEqual("addresses are required and there must be at least 1", error)

    def test_cannot_validate_property_description_with_invalid_addresses(self):
        invalid_property_description = deepcopy(property_description)
        invalid_property_description["fields"]["addresses"][0]["full_address"] = ""
        self.assertRaises(DataDoesNotMatchSchemaException, property_description_validator.validate, invalid_property_description)
