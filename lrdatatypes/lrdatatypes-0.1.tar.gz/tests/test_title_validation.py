# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from datatypes.exceptions import DataDoesNotMatchSchemaException

from datatypes import title_validator
from datatypes.core import unicoded

dumb_entry = unicoded({
    "template" : "some text",
    "full_text" : "some text",
    "fields" : {
            "field_name_1": "something",
            "field_name_2": {"some": "other thing"}
    },
    "deeds" : [],
    "notes" : [],
    "extra_field_to_ignore" : "should not cause validation failure"
})

proprietorship = unicoded({
        "template" : "example text",
        "full_text" : "example text",
        "fields" : {"proprietors": [
                {   "name": {
                        "title" : "Balarot",
                        "full_name" : "Cheesoir",
                        "decoration" : "Elegant",
                        "extra_field_to_ignore" : "should not cause validation failure"
                    },
                    "addresses": [{
                        "full_address" : "8 Acacia Avenue, Bootata, AL35PU",
                        "house_no" : "8",
                        "street_name" : "Acacia Avenue",
                        "town" : "Bootata",
                        "postal_county" : "",
                        "region_name" : "Smotania",
                        "postcode" : "AL3 5PU",
                        "country" : "Wales",
                        "something": "random which should not matter"
                    }]
                }
            ]
        },
        "deeds" : [],
        "notes": []
})

property_description = unicoded({
        "template" : "example text",
        "full_text" : "example text",
        "fields" : {"addresses": [{
                    "full_address" : "8 Acacia Avenue, Bootata, AL35PU",
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


simple_title = unicoded({
    "title_number": "TEST123456789",
    "class_of_title": "Absolute",
    "tenure": "Freehold",
    "edition_date": "20-12-2013",
    "proprietorship": proprietorship,
    "property_description": property_description,
    "price_paid": dumb_entry,
    "provisions": [],
    "easements":[],
    "restrictive_covenants" : [],
    "restrictions" : [],
    "bankruptcy" : [],
    "h_schedule": dumb_entry,
    "charges" : [],
    "other" : []
})

class TestTitleValidation(unittest.TestCase):
    def test_can_validate_valid_title(self):
        try:
            title_validator.validate(simple_title)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate title: " + repr(e))

    def test_can_validate_title_without_optional_fields(self):
        for field in ["price_paid", "h_schedule"]:
            title = deepcopy(simple_title)
            del title[field]
            try:
                title_validator.validate(simple_title)
            except DataDoesNotMatchSchemaException as e:
                self.fail("Could not validate title: " + repr(e))

    def test_cannot_validate_title_without_required_field(self):
        for field in ["class_of_title", "tenure", "title_number", "proprietorship", "property_description", "provisions", "easements", "restrictive_covenants", "restrictions", "bankruptcy", "charges", "other"]:
            bad_title = deepcopy(simple_title)
            del bad_title[field]
            self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "%s is a required field" % field, title_validator.validate, bad_title)

    def test_cannot_validate_title_for_required_string_fields_that_are_empty(self):
        for field in ["class_of_title", "tenure", "title_number"]:
            bad_title = deepcopy(simple_title)
            bad_title[field] = ""
            self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "%s is a required field, must not be an empty string" % field, title_validator.validate, bad_title)

    def test_cannot_validate_title_for_entry_fields_that_are_empty(self):
        for field in ["property_description", "h_schedule","price_paid"]:
            bad_title = deepcopy(simple_title)
            bad_title[field] = {} # replace dumb entry with empty object
            self.assertRaises(DataDoesNotMatchSchemaException,  title_validator.validate, bad_title)

    def test_cannot_validate_title_if_no_addresses_in_property_description(self):
        bad_title = deepcopy(simple_title)
        bad_title["property_description"]["fields"]["addresses"] = [] # replace address entry with empty list
        self.assertRaises(DataDoesNotMatchSchemaException,  title_validator.validate, bad_title)

    def test_cannot_validate_title_if_addresses_in_property_description_invalid(self):
        bad_title = deepcopy(simple_title)
        bad_title["property_description"]["fields"]["addresses"][0]["full_address"] = " "
        self.assertRaises(DataDoesNotMatchSchemaException, title_validator.validate, bad_title)

    def test_cannot_validate_title_if_addresses_in_proprietorship_invalid(self):
        bad_title = deepcopy(simple_title)
        bad_title["proprietorship"]["fields"]["proprietors"][0]["addresses"][0]["full_address"] = " "
        self.assertRaises(DataDoesNotMatchSchemaException,  title_validator.validate, bad_title)

    def test_cannot_validate_title_if_no_addresses_in_proprietorship(self):
        bad_title = deepcopy(simple_title)
        bad_title["proprietorship"]["fields"]["proprietors"][0]["addresses"] = [] # replace address entry with empty list
        self.assertRaises(DataDoesNotMatchSchemaException,  title_validator.validate, bad_title)
