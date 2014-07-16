from mws import *

MWS_ACCESS_KEY = 'AKIAJNVV6YPWB7LJ2WZA'
MWS_SECRET_KEY = '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'
MARKETPLACE_ID = 'ATVPDKIKX0DER'
ACCOUNT_ID = 'A1W3ZPM592JAN3'

SINGLE_ASIN = ['B00936AC6Y']
MULTIPLE_ASINS = ['B00936AC6Y', 'B00BMA8TAK', 'B0092TV45A']


amazon_mws_products_api = Products(
    access_key=MWS_ACCESS_KEY,
    secret_key=MWS_SECRET_KEY,
    account_id=ACCOUNT_ID,
    region='RE'
)

def get_children_from_asins(asins):
    response = amazon_mws_products_api.get_matching_product(
        marketplaceid=MARKETPLACE_ID,
        asins=asins
    )
    return response

single_response = get_children_from_asins(SINGLE_ASIN)
multiple_response = get_children_from_asins(MULTIPLE_ASINS)
