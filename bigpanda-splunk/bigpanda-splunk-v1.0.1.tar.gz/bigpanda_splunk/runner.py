#!/usr/bin/python

from bigpanda_splunk import LOG, read_config, setup_logging
import sys
import json
import urllib2
import time

def alert(args):
    """
    BigPanda Splunk Alert Script

    Triggered by Splunk
    """
    setup_logging()
    number_of_events = args[1]
    search_terms = args[2]
    query_string = args[3]
    report_name = args[4]
    LOG.info("Started '%s'", report_name)
    trigger = args[5]
    link = args[6]
    results_file = args[8]
    timestamp = int(time.time())

    config = read_config()

    payload = {
        "app_key": config['app_key'],
        "status": "critical",
        "number_of_events": number_of_events,
        "primary_property": "report_name",
        "secondary_property": "trigger",
        "search_terms": search_terms,
        "query_string": query_string,
        "report_name": report_name,
        "trigger": trigger,
        "link": link,
        "results_file": results_file,
        "timestamp": timestamp,
        "incident_identifier": report_name + '_' + str(timestamp)
        }
    send_alert(payload, config)


def send_alert(data, config):
    """
    Send Alert to the BigPanda REST Alert API
    """
    LOG.info("Sending")
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer %s' % config['token']
        }

    url = "%s%s" % (config['api_server'], config['post_path'])
    try:
        req = urllib2.Request(url, json.dumps(data), headers)
        response = urllib2.urlopen(req)
        if response.code >= 400:
            error_message = 'HTTP Error code: %s.' % response.code
            text = response.read()
            if text:
                error_message += 'Message: %s.' % text
            LOG.error("%s", error_message)
    except Exception as error:
        return LOG.error("%s", error)

    LOG.info("Sent")

def send_test_alert():
    """
    Send a test alert to the BigPanda REST Alert API
    """
    LOG.info("Sending Test Alert..")
    config = read_config()
    timestamp = int(time.time())
    try:
        payload = {
            "app_key": config['app_key'],
            "status": "warning",
            "number_of_events": 1,
            "primary_property": "report_name",
            "secondary_property": "trigger",
            "search_terms": "test_search_terms",
            "query_string": "test_query_string",
            "report_name": "test_report",
            "trigger": "test_trigger",
            "link": "test_link",
            "results_file": "test_results_file",
            "timestamp": timestamp,
            "incident_identifier": 'test_report_' + str(timestamp)
        }
        send_alert(payload, config)
    except Exception as error:
        return error
    LOG.info("Test Alert Sent.")
