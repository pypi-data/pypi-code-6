"""
Abstracts database used by Captain Tractor projects.
Currently it is implemented using ElasticSearch, but this could be changed.
"""
import json
import requests  # TO-DO: change by async call


HOST = "http://0.0.0.0:9200"
INDEX = "twitter"
TYPE = "user"


class DatabaseException(Exception):
    "Wrap exceptions raised in tractor_common.database"
    pass


def store(doc_id, doc_body, host=HOST, index=INDEX, doc_type=TYPE):
    """
    Store an item defined by:
        doc_id: item id (integer or string)
        doc_body: item body (dict)

    The following parameters are optional and related to how the item will be
    stored in ElasticSearch:
        host: default is "http://0.0.0.0:9200"
        index: default is "twitter"
        doc_type: default is "user"
    """
    url = "{0}/{1}/{2}/{3}".format(host, index, doc_type, doc_id)
    body = json.dumps(doc_body)
    response = requests.put(url, data=body)
    if not response.status_code in [200, 201]:
        raise DatabaseException(response.text)


def retrieve(doc_id, host=HOST, index=INDEX, doc_type=TYPE):
    """
    Retrieve
        doc_id: item id (integer or string)

    The following parameters are optional and related to how the item will be
    retrieved from ElasticSearch:
        host: default is "http://0.0.0.0:9200"
        index: default is "twitter"
        doc_type: default is "user"
    """
    url = "{0}/{1}/{2}/{3}".format(host, index, doc_type, doc_id)
    response = requests.get(url)
    if not response.status_code == 200:
        raise DatabaseException(response.text)
    return response.json()["_source"]


def delete(doc_id, host=HOST, index=INDEX, doc_type=TYPE):
    """
    Remove:
        doc_id: item id (integer or string)

    The following parameters are optional and related to how the item will be
    identified and deleted ElasticSearch:
        host: default is "http://0.0.0.0:9200"
        index: default is "twitter"
        doc_type: default is "user"
    """
    url = "{0}/{1}/{2}/{3}".format(host, index, doc_type, doc_id)
    return requests.delete(url)


def delete_index(host=HOST, index=INDEX):
    """
    Deletes test index. Uses class attribute:
        index: name of the index to be deleted
    """
    url = "{0}/{1}/".format(host, index)
    requests.delete(url)
