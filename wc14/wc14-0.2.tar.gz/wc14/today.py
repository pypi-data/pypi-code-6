__author__ = "Alok Kumar"

import click 
import datetime
import dateutil.tz
import dateutil.parser
import colorama
import humanize
import requests
import json

FUTURE = "future"
NOW = "now"
PAST = "past"
SCREEN_WIDTH = 68

def prettify(match):
    diff = (datetime.datetime.now(tz=dateutil.tz.tzlocal()) - dateutil.parser.parse(match['datetime']))
    seconds = diff.total_seconds()
    if seconds > 0:
        if seconds > 60 * 90:
            status = PAST
        else:
            status = NOW
    else:
        status = FUTURE
        
    if status in [PAST, NOW]:
        color = colorama.Style.BRIGHT + colorama.Fore.GREEN
    else:
        color = colorama.Style.NORMAL + colorama.Fore.WHITE
        
    home = match['home_team']
    away = match['away_team']
    if status == NOW:
        minute = int(seconds / 60)
        match_status = "Being played now: %s minutes gone" % minute
    elif status == PAST:
        if match['winner'] == 'Draw':
            result = 'Draw'
        else:
            result = "%s won" % (match['winner'])
        match_status = "Played %s. %s" % (humanize.naturaltime(diff), result)
    else:
        match_status = "Will be played %s at %s" % (
            humanize.naturaltime(diff), dateutil.parser.parse(match['datetime']).astimezone(dateutil.tz.tzlocal()).strftime("%H:%M %p")
        ) 
        
    if status == NOW:
        match_percentage = int(seconds / 60 / 90 * 100)
    elif status == FUTURE:
        match_percentage = 0
    else:
        match_percentage = 100
    
    return """
    {} {:<30} {} - {} {:>30}
    {}
    \xE2\x9A\xBD  {}
    """.format(
        color,
        home['country'],
        home['goals'],
        away['goals'],
        away['country'],
        progress_bar(match_percentage),
        colorama.Fore.WHITE + match_status
    )


def progress_bar(percentage, separator="o", character="-"):
    """
    Creates a progress bar by given percentage value
    """
    filled = colorama.Fore.GREEN + colorama.Style.BRIGHT
    empty = colorama.Fore.WHITE + colorama.Style.BRIGHT

    if percentage == 100:
        return filled + character * SCREEN_WIDTH

    if percentage == 0:
        return empty + character * SCREEN_WIDTH

    completed = int((SCREEN_WIDTH / 100.0) * percentage)

    return (filled + (character * (completed - 1)) +
            separator +
            empty + (character * (SCREEN_WIDTH - completed)))
    

@click.command()
def today():
    url = "http://worldcup.sfg.io/matches/today"
    response = requests.get(url)
    matches = json.loads(response.text)
    for match in matches:
        print prettify(match)


@click.command()
def tomorrow():
    url = "http://worldcup.sfg.io/matches/tomorrow/"
    response = requests.get(url)
    matches = json.loads(response.text)
    for match in matches:
        print prettify(match)