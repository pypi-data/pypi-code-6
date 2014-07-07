from .util import get_cached


BASE_URL = "https://gemstore-fra-live.ncplatform.net/"


def search(**params):
    """Search for items in the Gem Store.

    :param text: Search in item names.
    :param category: Search by item category. Valid categories are: decorative,
           consumable, convenience, boosts, minipets and account.
    :param discounted: Search for discounted items.
    :param count: Number of items to return. Defaults to 10.
    :param offset: Offset. Defaults to 1.

    """
    response = get_cached(BASE_URL + "ws/search.json", False, params=params)
    return response["items"]


def history():
    """Return items previously bought from the Gem Store.

    """
    response = get_cached(BASE_URL + "ws/history.json", False)
    return response["items"]
