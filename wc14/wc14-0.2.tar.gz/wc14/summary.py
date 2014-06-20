# -*- coding: utf-8 -*-
__author__ = "Alok Bhan"

import colorama
import click
import json
import requests


def group_prettify(group):
    empty = colorama.Fore.WHITE + colorama.Style.BRIGHT
    
        
    print '''{}
    {} {:^30} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5}
    {}
    '''.format(empty + " " * 4  + "-" * 95, "", "Group %s" % chr(64 + group[0]["group_id"]), 
               "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts", empty + "-" * 95)
    for team in group:
        if team['knocked_out']:
            color = colorama.Fore.RED
        else:
            color = colorama.Fore.WHITE
        print '''{} {:<30} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} | {:^5} {}
        '''.format(color + " " * 4,
                team['country'] + "  (" + team['fifa_code'] + ")", team['wins'] + (team['draws'] + team['losses']),
                team['wins'], team['draws'], team['losses'],
                team['goals_for'], team['goals_against'], (team['goals_for'] - team['goals_against']),
                (3 * team['wins'] + 1 * team['draws']), colorama.Fore.WHITE)
    print 


COUNTRY_TO_ID_MAP = {
    "1": ["BRA", "MEX", "CRO", "CMR"],
    "2": ["CHI", "NED", "AUS", "ESP"],
    "3": ["COL", "CIV", "GRE", "JPN"],
    "4": ["ITA", "CRC", "ENG", "URU"],
    "5": ["SUI", "FRA", "HON", "ECU"],
    "6": ["ARG", "IRN", "NGA", "BIH"],
    "7": ["USA", "GER", "GHA", "POR"],
    "8": ["BEL", "RUS", "KOR", "ALG"]
}

def _sorted_group(group):
    return sorted(group, key=lambda k: (3 * k["wins"] + 1 * k["draws"], k["goals_for"] - k["goals_against"]), reverse=True)

@click.command()
@click.option('--country-code', default="all")
def summary(country_code):
    results = json.loads(requests.get("http://worldcup.sfg.io/group_results").text)
#     results = group_results
    if country_code == "all":
        for x in range(1, 9):
            group_prettify(
                _sorted_group([result for result in results if result["group_id"] == x])
            )
    else:
        country_id = [int(k) for k,v in COUNTRY_TO_ID_MAP.items() if country_code in v][0]        
        group_prettify(
            _sorted_group([result for result in results if result["group_id"] == country_id])
        )
