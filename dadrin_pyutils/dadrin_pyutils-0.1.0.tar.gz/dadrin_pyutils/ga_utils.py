"""
Utilities for the python Google Analytics API client
"""
__author__ = 'Lluis Canet'

import argparse
import logging
import httplib2
import os
import pandas as pd

from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from pandas import DataFrame


def get_all_df_stats(service, view_id, keys, start_dt, end_dt, ga_dimensions='ga:pagePath,ga:source'):
    """
    Get all available results by iterating through GA API and append all results to a data frame
    service: The service object built by the Google API Python client library.

    Args
    view_id: str The View ID form which to retrieve data.
    start_dt: str with reporting start date, format YYYY-MM-DD
    start_dt: str with reporting end date, format YYYY-MM-DD
    """

    all_df_stats = [resp_to_dataframe(response, keys) for response in
                    get_page_stats(service, view_id, start_dt, end_dt, ga_dimensions) if response is not None]
    if all(v is None for v in all_df_stats):
        return None
    df_stats = DataFrame(pd.concat(all_df_stats))
    logging.info('Obtained raw items %d' % (len(df_stats)))
    return df_stats


def get_page_stats(service, view_id, start_dt, end_dt, ga_dimensions):
    """Returns a generator for metrics associated with pagaPath.

    Args:
    service: The service object built by the Google API Python client library.
    view_id: str The View ID form which to retrieve data.
    start_dt: str with reporting start date, format YYYY-MM-DD
    start_dt: str with reporting end date, format YYYY-MM-DD
    """
    ga_metrics = 'ga:users,' \
                 'ga:newUsers,' \
                 'ga:sessions,' \
                 'ga:bounces,' \
                 'ga:sessionDuration,' \
                 'ga:pageviews,' \
                 'ga:timeOnPage,' \
                 'ga:socialInteractions,' \
                 'ga:uniqueSocialInteractions'

    next_item = 1
    total_res = 100
    while next_item < total_res:
        response = get_api_query(service, view_id, start_dt, end_dt,
                                 ga_metrics, ga_dimensions, str(next_item), ga_sort='-ga:pageviews')
        items = response['itemsPerPage']
        total_res = response['totalResults']
        yield response
        next_item = next_item + items


def resp_to_dataframe(api_response, keys):
    """
    Create a data frame from the contents of a response from GA
    """
    col_names = [elem['name'].split(':')[1] for elem in api_response['columnHeaders']]
    if 'rows' in api_response:
        df = DataFrame(api_response['rows'], columns=col_names)
        df.set_index(keys, inplace=True)
        df = df.convert_objects(convert_numeric=True)
        df.reset_index(inplace=True)
        return df
    return None


def get_api_query(service, view_id, start_dt, end_dt, ga_metrics, ga_dimensions, index, ga_sort):
    """
    Generic wrapper around Google API query Engine
    """
    try:
        response = service.data().ga().get(
            ids=view_id,
            start_date=start_dt,
            end_date=end_dt,
            metrics=ga_metrics,
            dimensions=ga_dimensions,
            sort=ga_sort,
            start_index=index).execute()
    except TypeError, error:
        # Handle errors in constructing a query.
        logging.error('There was an error in constructing your query : %s' % error)

    except HttpError, error:
        # Handle API errors.
        logging.error('Arg, there was an API error : %s : %s' %
                      (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        logging.error('The credentials have been revoked or expired, please re-run '
                      'the application to re-authorize')
    return response

def get_view_ids(service, account_name):
    """Returns a map between webproperty Ids and ViewIds.

    Args:
    service: The service object built by the Google API Python client library.
    account_name: str with name of the account to retrieve web properties
    """
    accounts = service.management().accounts().list().execute()

    for item in accounts.get('items'):
        if item['name'] == account_name:
            hubs_account_id = item.get('id')
            break

    webproperties = service.management().webproperties().list(accountId=hubs_account_id).execute()

    views_dict = {webproperty['id']: 'ga:'+webproperty['defaultProfileId'] for webproperty in webproperties['items']}
    return views_dict



def auth_offline(name, version, doc, filename, scope=None):
    """A common authentication routine for Google API.
  Based on the code from 'jcgregorio@google.com (Joe Gregorio)' from apiclient import sample_tools

  The credentials are stored in a file named apiname.dat, and the
  client_secrets.json file is stored in the same directory as the application
  main file.

  This authentication method requests the user to authorize for permanent offline access
  so that authentication is no longer required when running the code on a server application.

  Args:
    argv: list of string, the command-line parameters of the application.
    name: string, name of the API.
    version: string, version of the API.
    doc: string, description of the application. Usually set to __doc__.
    file: string, filename of the application. Usually set to __file__.
    parents: list of argparse.ArgumentParser, additional command-line flags.
    scope: string, The OAuth scope used.

  Returns:
    A tuple of (service, flags), where service is the service object and flags
    is the parsed command-line flags.
  """
    argparser = argparse.ArgumentParser(add_help=False)
    parents = [argparser]
    if scope is None:
        scope = 'https://www.googleapis.com/auth/' + name

    # Parser command-line arguments.
    parent_parsers = [tools.argparser]
    parent_parsers.extend(parents)
    parser = argparse.ArgumentParser(
        description=doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)
    flags = parser.parse_args()

    # Name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret, which are found
    # on the API Access tab on the Google APIs
    # Console <http://code.google.com/apis/console>.
    client_secrets = os.path.join(os.path.dirname(filename),
                                  'config/client_secrets.json')

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(client_secrets,
                                          scope=scope,
                                          message=tools.message_if_missing(client_secrets))

    #Force approval to grant offline access
    flow.params['approval_prompt'] = 'force'

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Construct a service object via the discovery service.
    service = discovery.build(name, version, http=http)
    return service