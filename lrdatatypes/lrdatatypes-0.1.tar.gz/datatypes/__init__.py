from datatypes.validators.iso_country_code_validator import IsoCountryCode
from datatypes.validators.ogc_urn_validator import OgcUrn
from datatypes.validators.postcode_validator import Postcode
from datatypes.validators.price_validator import Price
from datatypes.validators.address_validator import Address
from datatypes.validators.title_validator import Title
from datatypes.validators.entry_validator import Entry
from datatypes.validators.deed_validator import Deed
from datatypes.validators.proprietor_validator import Proprietor
from datatypes.validators.proprietorship_validator import Proprietorship
from datatypes.validators.property_description_validator import PropertyDescription

price_validator = Price()
address_validator = Address()
postcode_validator = Postcode()
country_code_validator = IsoCountryCode()
ogc_urn_validator = OgcUrn()
title_validator = Title()
entry_validator = Entry()
deed_validator = Deed()
proprietor_validator = Proprietor()
proprietorship_validator = Proprietorship()
property_description_validator = PropertyDescription()

from datatypes.validators.geo_json_validator import GeoJson, GeoJsonString

geo_json_validator = GeoJson()
geo_json_string_validator = GeoJsonString()

from datatypes.validators.system_of_record_request_validator import SystemOfRecordRequestValidator

system_of_record_request_validator = SystemOfRecordRequestValidator()

from datatypes.validators.system_of_record_chain_message_validator import SystemOfRecordChainMessageValidator

system_of_record_chain_message_validator = SystemOfRecordChainMessageValidator()
