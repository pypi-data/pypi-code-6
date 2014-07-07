from .util import get_cached


BASE_URL = "https://exchange-fra-live.ncplatform.net/"


def trends(type="ReceivingCoins"):
    """Get hourly exchange rate trend data for the last five days.

    :param type: The exchange rate to retrieve. Can be ReceivingCoins (trading
           gems for gold) or ReceivingGems (trading gold for gems).

    The returned dictionary contains the 5 day average, low and high points,
    and a list of sample points (sampled roughly each half hour).

    """
    params = {"type": type}
    return get_cached(BASE_URL + "ws/trends.json", False, params=params)


def coins_to_gems(coins):
    """Calculate conversion from coins to gems.

    :param coins: Amount of coins to convert to gems.
    :return: A tuple (coins_per_gem, gems)

    """
    params = {"coins": coins}
    response = get_cached(BASE_URL + "ws/rates.json", False, params=params)
    result = response["results"]["gems"]
    return int(result["coins_per_gem"]), int(result["quantity"])


def gems_to_coins(gems):
    """Calculate conversion from gems to coins.

    :param gems: Amount of gems to convert to coins.
    :return: A tuple (coins_per_gem, coins)

    """
    params = {"gems": gems}
    response = get_cached(BASE_URL + "ws/rates.json", False, params=params)
    result = response["results"]["coins"]
    return int(result["coins_per_gem"]), int(result["quantity"])
