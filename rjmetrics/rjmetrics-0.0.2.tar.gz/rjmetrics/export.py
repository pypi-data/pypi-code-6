
import sys
import StringIO
import zipfile
import requests


def get_table():
    # Trigger table export
    export_url = "https://api.rjmetrics.com/0.1/client/{0.client_id}/table/{0.table_id}/export".format(args)

    print >> sys.stderr, 'POST', export_url

    response = requests.post(export_url, data="",
                             headers={'X-RJM-API-Key': args.api_key})

    export_id = response.json()['export_id']

    # Fetch the exported table
    max_tries = 50
    while True:
        export_data_url = "https://api.rjmetrics.com/0.1/export/{0}".format(export_id)
        print >> sys.stderr, 'GET', export_data_url

        data_response = requests.get(export_data_url,
                                     headers={'X-RJM-API-Key': args.api_key})

        if data_response.ok:
            break
        else:
            print >> sys.stderr, data_response.status_code, data_response.text

        max_tries -= 1
        if max_tries < 0:
            print >> sys.stderr, "Error exporting table."
            exit(1)

    # Unzip exported table and write to stdout
    export_zip = zipfile.ZipFile(StringIO.StringIO(data_response.content), 'r')
    for filename in export_zip.namelist():
        print export_zip.read(filename)

    print >> sys.stderr, "Exported table."
