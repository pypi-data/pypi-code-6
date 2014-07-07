import re
import json

import gw2api
from .util import get_cached


BASE_URL = "https://tradingpost-fra-live.ncplatform.net/"
RARITY = {
    "basic": 1,
    "fine": 2,
    "masterwork": 3,
    "rare": 4,
    "exotic": 5,
    "ascended": 6,
    "legendary": 7,
}
TYPES = {
    "Armor": {
        "id": 0,
        "All": 0,
        "Aquatic Helm": 4,
        "Boots": 5,
        "Coat": 0,
        "Gloves": 2,
        "Helm": 3,
        "Leggings": 1,
        "Shoulders": 6,
    },
    "Bag": {
        "id": 2,
    },
    "Consumable": {
        "id": 3,
        "All": 0,
        "Food": 3,
        "Generic": 4,
        "Transmutation": 8,
        "Unlock": 9,
    },
    "Container": {
        "id": 4,
        "All": 0,
        "Default": 0,
        "Gift Box": 1,
    },
    "Crafting Material": {
        "id": 5,
    },
    "Gathering": {
        "id": 6,
        "All": 0,
        "Foraging": 0,
        "Logging": 1,
        "Mining": 2,
    },
    "Gizmo": {
        "id": 7,
        "All": 0,
        "Default": 0,
        "Salvage": 2,
    },
    "Mini": {
        "id": 11,
    },
    "Tool": {
        "id": 13,
        "All": 0,
        "Crafting": 0,
        "Salvage": 2,
    },
    "Trinket": {
        "id": 15,
        "All": 0,
        "Accessory": 0,
        "Amulet": 1,
        "Ring": 2,
    },
    "Trophy": {
        "id": 16,
    },
    "Upgrade Component": {
        "id": 17,
        "All": 0,
        "Accessory": 0,
        "Armor": 2,
        "Weapon": 3,
    },
    "Weapon": {
        "id": 18,
        "All": 0,
        "Axe": 4,
        "Dagger": 5,
        "Focus": 13,
        "Greatsword": 6,
        "Hammer": 1,
        "Harpoon Gun": 20,
        "Longbow": 2,
        "Mace": 7,
        "Pistol": 8,
        "Rifle": 10,
        "Scepter": 11,
        "Shield": 16,
        "Short Bow": 3,
        "Spear": 19,
        "Staff": 12,
        "Sword": 0,
        "Torch": 14,
        "Toy": 22,
        "Trident": 21,
        "Warhorn": 15,
    },
}


def set_session_key(session_key):
    gw2api.session.cookies.set("s", session_key, domain=".ncplatform.net")


def get_market_data():
    market_data = {}
    r = gw2api.session.get(BASE_URL)
    for match in re.finditer(r"^\s*GW2\.(\w+) = (.*)$", r.text, re.MULTILINE):
        key, value = match.groups()
        if value.endswith(";"):
            value = value[:-1]
        market_data[key] = json.loads(value)
    return market_data


def search_by_id(*args, **kwargs):
    """Search for items on the trading post by item id. If one Id is passed,
    the result is a dictionary. If multiple Ids are passed, the result is a
    list if dictionaries.

    >>> search_by_id(12144).get('name')
    'Snow Truffle'
    >>> rings = search_by_id(38156, 38157, 38158)
    >>> [ring['name'] for ring in rings]
    ['Snowflake Copper Ring', 'Snowflake Silver Ring', 'Snowflake Gold Ring']

    """
    ids = []
    for arg in args:
        if isinstance(arg, (tuple, list)):
            ids.extend(arg)
        else:
            ids.append(arg)

    if not ids:
        raise ValueError("specify one or more item ids")

    kwargs.setdefault("single", len(ids) == 1)
    id_str = ",".join([str(id) for id in ids])
    return search(ids=id_str, **kwargs)


def search(raw=False, single=False, **params):
    """Search for items on the trading post.

    :param raw: Normally, only the search results are returned. Set this to
           true if you want the whole response body.
    :param single: If single is true, only the first result is returned.

    All other parameters are passed as query parameters to the trading post.
    Known parameters:

    :param text: Text to search for.
    :param ids: Comma-separated list of item ids to search for. **Other search
           parameters will be ignored.**
    :param levelmin: Minimum item level. Defaults to 0.
    :param levelmax: Maximum item level. Defaults to 80.
    :param count: Number of items to return. Defaults to 10.
    :param offset: Offset. Defaults to 1.
    :param removeunavailable: If true, do not report items that currently have
           no listings.
    :param rarity: Find items by quality. The value is specified as an integer.
    :param type: Find items by type. The value is specified as an integer.
    :param subtype: Find items by type and subtype. The value is specified as
           an integer.
    :param orderby: Order results by a specific field. Possible values are
           'name', 'level', 'price', 'rarity' and 'count'. Defaults to 'name'.
    :param sortdescending: Order results in descending order instead of
           ascending


    """
    data = get_cached(BASE_URL + "ws/search.json", False, params=params)
    if raw:
        return data

    results = data["results"]

    if single:
        assert len(results) <= 1
        return results[0] if results else None

    return results


def listings(item_id, type=None):
    """Get buy and or sell listings for an item. Returns the first 20 listings.

    :param item_id: The item to retrieve listings for.
    :param type: Listing type. Can be 'buys' or 'sells'. If not specified, both
           types of listing are returned.

    """
    params = {"id": item_id, "type": type} if type else {"id": item_id}
    data = get_cached(BASE_URL + "ws/listings.json", False,
                      params=params)
    return data["listings"][type] if type else data["listings"]


def trends():
    """Get information about current trends (as shown on the main page of the
    Black Lion Trading Company). May or may not be up to date.

    Returns a tuple (order, items). The order dictionary contains lists of
    item ids corresponding to the top valued, supplied, demanded and traded
    items. The items dictionary contains details about the items listed in
    the order dictionary.

    """
    data = get_cached(BASE_URL + "ws/trends.json", False)
    items = data["items"]
    return items.pop("order"), items


def transactions(type="buy", time="now", offset=1):
    """Display transactions for the user.

    :param type: Type of transactions. Can be 'buy' or 'sell'.
    :param time: Current transactions ('now') or historical ('past').
    :param offset: Offset. Defaults to 1.

    """
    params = {"type": type, "time": time, "offset": offset}
    data = get_cached(BASE_URL + "ws/me.json", False, params=params)
    return data["listings"]


def _buy(item_id, payload):
    url = BASE_URL + "ws/item/%s/buy" % item_id
    r = gw2api.session.post(url, data=payload)
    r.raise_for_status()
    return r.json()


def buy(item_id, tuples, char_id):
    """Buy an item.

    :param item_id: The id of the item to buy.
    :param tuples: A list of tuples (count, price) taken from the sell
           listings for the item.
    :param char_id: The GUID of the character executing the transaction.

    """
    payload = [("charid", char_id)]
    for tuple in tuples:
        payload.append(("tuples", "%s,%s" % tuple))

    return _buy(item_id, payload)


def buy_offer(item_id, count, price, char_id):
    """Place a buy offer.

    :param item_id: The id of the item to buy.
    :param count: The number of items to buy.
    :param price: The price at which to buy the items (unit price).
    :param char_id: The GUID of the character executing the transaction.

    """
    payload = {"count": count, "price": price, "charid": char_id}
    return _buy(item_id, payload)
