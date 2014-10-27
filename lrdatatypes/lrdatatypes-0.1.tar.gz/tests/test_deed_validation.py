import unittest
from copy import deepcopy

from datatypes.exceptions import DataDoesNotMatchSchemaException

from datatypes import deed_validator
from datatypes.core import unicoded

proprietors = unicoded([ { "title" : "Mrs",
            "full_name": "Bootata Smick",
            "decoration": ""
        },
        {   "title" : "Mr",
            "full_name": "Mishmisha Okasha",
            "decoration": "",
            "an_extra_field": "to be ignored"
        }
])

deed =  unicoded({
   "type":"Conveyance",
   "date":"2014-02-01",
   "parties":[
      [
         {
            "title":"",
            "decoration":"",
            "first_name":"",
            "last_name":"Bishop",
            "non_private_individual_name":"",
            "full_name":"Paul Bishop",
            "country_incorporation":"",
            "company_registration_number":"",
            "name_information":"",
            "occupation":"",
            "name_supplementary":"",
            "trading_name":"",
            "trust_type":"",
            "name_category":"",
            "charity_name":"",
            "local_authority_area":"",
            "alias_names":[

            ]
         }
      ],
      [
         {
            "title":"",
            "decoration":"",
            "first_name":"",
            "last_name":"Smith",
            "non_private_individual_name":"",
            "full_name":"James Smith",
            "country_incorporation":"",
            "company_registration_number":"",
            "name_information":"",
            "occupation":"",
            "name_supplementary":"",
            "trading_name":"",
            "trust_type":"",
            "name_category":"",
            "charity_name":"",
            "local_authority_area":"",
            "alias_names":[

            ]
         }
      ]
   ],
   "rentcharge_amount":"",
   "payment_detail":"",
   "lease_term":""
})

deed_no_parties =  unicoded({
   "type":"Conveyance",
   "date":"2014-02-01",
   "parties":[],
   "rentcharge_amount":"",
   "payment_detail":"",
   "lease_term":""
})

class TestDeedValidation(unittest.TestCase):

    def test_can_validate_valid_deed(self):
        try:
            deed_validator.validate(deed)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate deed: " + repr(e))

    def test_can_validate_valid_deed_with_no_parties(self):
        try:
            deed_validator.validate(deed_no_parties)
        except DataDoesNotMatchSchemaException as e:
            self.fail("Could not validate deed: " + repr(e))


    def test_does_not_validate_deed_without_type(self):
        invalid_deed = deepcopy(deed)
        del invalid_deed["type"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "type is a required field", deed_validator.validate, invalid_deed)

    def test_does_not_validate_deed_without_date(self):
        invalid_deed = deepcopy(deed)
        del invalid_deed["date"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "date is a required field", deed_validator.validate, invalid_deed)

    def test_does_not_validate_deed_without_parties(self):
        invalid_deed = deepcopy(deed)
        del invalid_deed["parties"]
        self.assertRaisesRegexp(DataDoesNotMatchSchemaException, "parties is a required field", deed_validator.validate, invalid_deed)
