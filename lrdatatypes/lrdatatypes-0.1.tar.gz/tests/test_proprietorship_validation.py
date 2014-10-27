import unittest
from copy import deepcopy

from datatypes.exceptions import DataDoesNotMatchSchemaException

from datatypes import proprietorship_validator
from datatypes.core import unicoded

proprietorship = unicoded({
        "template" : "example text",
        "full_text" : "example text",
        "fields" : {"proprietors": [
                {   "name": {
                        "title" : "Balarot",
                        "full_name" : "Cheesoir",
                        "decoration" : "Elegant"
                    },
                    "addresses": [{
                     "full_address":"27 Baytree Road, Weston-super-Mare SO3 4NE",
                     "house_no":"27",
                     "street_name":"Baytree Road",
                     "town":"Weston-super-Mare",
                     "postal_county":"",
                     "region_name":"",
                     "country":"",
                     "postcode":"SO3 4NE",
                     "local_name":"",
                     "dx_number":"",

                    }]
                }
            ]
        },
        "deeds" : [],
        "notes": []
})

proprietorship_without_addressess = unicoded({
        "template" : "example text",
        "full_text" : "example text",
        "fields" : {"proprietors": [
                {   "name": {
                        "title" : "Balarot",
                        "full_name" : "Cheesoir",
                        "decoration" : "Elegant"
                    },
                    "addresses": []
                }
            ]
        },
        "deeds" : [],
        "notes": []
})

class TestProprietorshipValidation(unittest.TestCase):

    def test_can_validate_valid_proprietorship(self):
        try:
            proprietorship_validator.validate(proprietorship)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate entry: " + repr(e))

    def test_can_validate_valid_proprietorship_with_extra_fields_in_proprietor(self):
        test_proprietorship = deepcopy(proprietorship)
        test_proprietorship["fields"]["proprietors"][0]["name"]["something"] = "random"
        try:
            proprietorship_validator.validate(test_proprietorship)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate entry: " + repr(e))

    def test_cannot_validate_proprietorship_without_proprietors(self):
        invalid_proprietorship = deepcopy(proprietorship)
        del invalid_proprietorship["fields"]["proprietors"]
        try:
            proprietorship_validator.validate(invalid_proprietorship)
        except DataDoesNotMatchSchemaException as e:
            error = e.field_errors.get("fields.proprietors")
            self.assertIsNotNone(error)
            self.assertEqual("proprietors are required and there must be at least 1", error)

    def test_cannot_validate_proprietorship_with_empty_proprietors(self):
        invalid_proprietorship = deepcopy(proprietorship)
        invalid_proprietorship["fields"]["proprietors"] = []
        try:
            proprietorship_validator.validate(invalid_proprietorship)
        except DataDoesNotMatchSchemaException as e:
            error = e.field_errors.get("fields.proprietors")
            self.assertIsNotNone(error)
            self.assertEqual("proprietors are required and there must be at least 1", error)

    def test_cannot_validate_proprietorship_without_name(self):
        invalid_proprietorship = deepcopy(proprietorship)
        del invalid_proprietorship["fields"]["proprietors"][0]["name"] #ouch
        try:
            proprietorship_validator.validate(invalid_proprietorship)
        except DataDoesNotMatchSchemaException as e:
            errors = e.field_errors.get("fields.proprietors.name")
            self.assertIsNotNone(errors)
            self.assertEquals(errors, "proprietors name is required")


    def test_cannot_validate_proprietorship_without_address(self):
        try:
            proprietorship_validator.validate(proprietorship_without_addressess)
        except DataDoesNotMatchSchemaException as e:
            errors = e.field_errors.get("fields.proprietors.addresses")
            self.assertIsNotNone(errors)
            self.assertEquals(errors, "proprietors addresses are required")
