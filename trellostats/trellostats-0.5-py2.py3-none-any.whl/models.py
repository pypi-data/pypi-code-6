from datetime import datetime
from peewee import Model, CharField, DateTimeField, FloatField, SqliteDatabase

db = SqliteDatabase('snapshots.db')


class Snapshot(Model):
    board_id = CharField()
    done_id = CharField()
    when = DateTimeField(default=datetime.now)
    cycle_time = FloatField()

