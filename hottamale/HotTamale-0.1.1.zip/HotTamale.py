# !/usr/bin/env python
# Author: Kyle Ondy <KyleOndy@gmail.com>
# URL: http://github.com/kyleondy/
#
# This file is part of HotTamale
#
# HotTamale is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HotTamale is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HotTamale.  If not, see <http://www.gnu.org/licenses/>.

import json
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3
from datetime import datetime, time
import sys, esky

if getattr(sys, "frozen", False):
    app = esky.Esky(sys.executable,"https://pypi.python.org/packages/source/H/HotTamale/")
    try:
        app.auto_update()
    except Exception as e:
        print("Error updating Hot Tamale:", e)

# configuration
DEBUG = True
QUERY = 'SELECT tickets_0.id, tickets_0.summary, tickets_0.description, (SELECT body  FROM main.comments  WHERE comments.ticket_id=main.tickets_0.id  AND (comments.body NOT Like "%Assigned%")  ORDER BY updated_at desc  LIMIT 1) AS ticketcomments, users_1.email AS created_by_email,users_1.first_name||" "||users_1.last_name AS created_by_name, tickets_0.created_at, tickets_0.priority, tickets_0.due_at, users_0.first_name AS assigned_to, tickets_0.updated_at  FROM main.tickets tickets_0, main.users users_1 LEFT OUTER JOIN main.users users_0  ON tickets_0.assigned_to = users_0.id WHERE users_1.id = tickets_0.created_by AND ( ( tickets_0.status = "open" )  AND ( tickets_0.priority < 3 ) ) ORDER BY tickets_0.id DESC'

app = Flask(__name__)
app.config.from_object(__name__)

def import_data():
    conn = sqlite3.connect("D:\Dropbox\SpiceRack\spiceworks_prod.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    return c.execute(QUERY)

@app.before_request
def before_request():
    g.data = import_data()

@app.route('/')
def display_data():
    #data = sorted(g.data, key=lambda person: person['klout']['score'], reverse=True)
    data = g.data
    return render_template('data.html', data=data)

@app.template_filter()
def friendly_time(dt, past_="ago",
    future_="from now",
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        period = int(period)
        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default

if __name__ == '__main__':
    app.run(debug=True)