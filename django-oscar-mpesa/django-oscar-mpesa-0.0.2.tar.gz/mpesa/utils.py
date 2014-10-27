FIELD_TO_QUERY_PARAMETER_MAPPING = {
        "ipn_id": "id",
        "origin": "orig",
        "destination": "dest",
        "recieved_at": "tstamp",
        "message": "text",
        "reference_number": "mpesa_code",
        "subscriber_phone_number": "mpesa_msisdn",
        "subscriber_name": "mpesa_sender",
        "amount": "mpesa_amt",
        "account": "mpesa_acc",

        "paybill_number": "business_number",
        "customer_id": "customer_id"
    }

def parse_ipn_data(raw_data):
    """
        This method maps the data received from MPESA's IPN 
        to format that can be used
        by the transaction model

        missing data will be handled by the form
    """
    parsed_data = {}
    for field, param in FIELD_TO_QUERY_PARAMETER_MAPPING.items():
        parsed_data[field] = raw_data.get(param)

    parsed_data["transaction_date"] = raw_data.get("mpesa_trx_date")
    parsed_data["transaction_time"] = raw_data.get("mpesa_trx_time")

    return parsed_data