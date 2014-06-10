#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
sundowner.py

Webservice to provide sunrise and sunset information.
All times are UTC. It is up to the client to convert to local time.
"""
import ephem
from datetime import date, datetime, tzinfo, timezone, timedelta
import dateutil.parser
from flask import Flask, jsonify, abort, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/day/<lat>/<lon>/<day>', defaults={'output_type': 'js'})
@app.route('/api/day/<lat>/<lon>/<day>/<output_type>')
def sun_day(lat, lon, stday, output_type):
    day = parse_date(day)
    times = list_times(lat, lon, day, output_type)
    lat_long = "{0},{1}".format(lat,lon)
    output = {lat_long: {day.isoformat(): times}}
    return jsonify(output)

@app.route('/api/sun/')
def sun():
    # Populate variables from request
    lat = request.args.get('lat', None, type=str)
    lon = request.args.get('lon', None, type=str)
    start_day = request.args.get('start', None, type=str)
    end_day = request.args.get('end', None, type=str)
    output_type = request.args.get('output_type', 'iso', type=str)

    # Default to today if no start date specified
    if start_day is None:
        start = date.today()
    else:
        start = dateutil.parser.parse(start_day).date()

    if end_day is None:
        end = start
    else:
        end = dateutil.parser.parse(end_day).date()

    days_range = (end + timedelta(days=1) - start).days
    days = [start + timedelta(days=i) for i in range(days_range)]
    times = [{'date': day.isoformat(), 'events': list_times(lat, lon, day, output_type)} for day in days]
    output = {'latlon': {'lat': lat, 'lon': lon}, 'days': times}
    return jsonify(output)

@app.route('/api/sun/<lat>/<lon>/<start_day>/<end_day>',
            defaults={'output_type': 'js'})
@app.route('/api/sun/<lat>/<lon>/<start_day>/<end_day>/<output_type>')
def sun_period(lat, lon, start_day, end_day, output_type):
    start = parse_date(start_day)
    end = parse_date(end_day)
    days_range = (end + timedelta(days=1) - start).days
    days = [start + timedelta(days=i) for i in range(days_range)]
    times = {day.isoformat(): list_times(lat, lon, day, output_type) for day in days}
    lat_long = "{0},{1}".format(lat,lon)
    output = {lat_long: times}
    return jsonify(output)

def parse_date(day):
    """
    Parses a date in YYYYMMDD format and returns a Date object.
    """
    try:
        # Wrap input in int() in case of preceeding zeros
        output = date(int(day[:4]), int(day[4:6]), int(day[6:8]))
    except ValueError or TypeError:
        abort(500)
    return output

def list_times(latitude, longitude, day, output_type):
    """
    Uses calculate_sunrise() to work out the relevent events for a given day.

    Args:
      day (date): Date object
      latitude (str): Latitude
      longitude (str): Longitude
      output_type (str): 'js' = Javascript timestamp in ms,
        'dt' = Python datetime object, 'iso' = ISO 8601 format

    Returns:
      events (dict): dictionary containing events as Unix timestamps in ms

    Raises:
      TypeError: If day, latitude, longitude, or elevation are invalid.
    """
    location = ephem.Observer()
    location.lat = latitude
    location.lon = longitude
    location.pressure = 0
    # -6º is civil twilight; –0:34º with 0 pressure is the NOAA spec for
    # sunrise/set to take into account atmospheric refraction
    events = {'civil_dawn': ('-6', True),
              'sunrise': ('-0:34', True),
              'sunset': ('-0:34', False),
              'civil_dusk': ('-6', False)}
    output = {event: calculate_sunrise(location, day, events[event][0],
                events[event][1], output_type) for event in events}
    return output

def calculate_sunrise(location, day, horizon, dawn='True', output_type='iso'):
    """
    Calculate sunrise/set time and return it as a Julian Date.

    Args:
      location (object): an ephem.Observer object
      day (float): the Julian Day or Date
      horizon (str): the angle of the desired horizon
        e.g. astronomical dawn is -18
      dawn (bool): Dawn (True) or dusk (False)
      output_type (str): 'js' = Javascript timestamp in ms,
        'dt' = Python datetime object, 'iso' = ISO 8601 format

    Returns:
      suntime (int): naive (UTC) timestamp integer of the sunrise/sunset

    Raises:
      CircumpolarError: If sun does not rise or set during the Julian Day.
    """
    location.date = day
    location.horizon = horizon
    sun = ephem.Sun()
    sun.compute(location)
    if dawn is True:
        try:
            suntime = location.next_rising(sun).datetime()
        except ephem.CircumpolarError:
            suntime = None
    else:
        try:
            suntime = location.next_setting(sun).datetime()
        except ephem.CircumpolarError:
            suntime = None
    if suntime is not None:
        suntime = suntime.replace(tzinfo=timezone.utc)
        if output_type == 'js':
            # Parse datetime object as a Javascript datetime
            # (milliseconds since Unix epoch)
            output_time = round(suntime.timestamp() * 1000)
        elif output_type == 'dt':
            # Just a simple Python datetime object
            output_time = suntime
        elif output_type == 'iso':
            # A datetime in ISO 8601 format
            output_time = suntime.isoformat()
    else:
        output_time = suntime
    return output_time

if __name__ == "__main__":
    app.run()
