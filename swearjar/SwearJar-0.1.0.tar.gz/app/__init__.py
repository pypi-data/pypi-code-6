from flask import Flask, render_template, g
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(                           
    DATABASE='test_sinners.db', # TODO <--- DB name?
    DEBUG=True,
    SECRET_KEY='development key', # Do we care?   
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('APP_SETTINGS', silent=True) # TODO <-- we care?

from app.module_one.controller import module_one

app.register_blueprint(module_one)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

