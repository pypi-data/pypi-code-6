from flask import Flask

__version__ = (1, 2)

api_app = Flask("bw2restapi")

from .activity import ActivityAPI
from .database import DatabaseAPI, list_activities_for_database, list_databases
