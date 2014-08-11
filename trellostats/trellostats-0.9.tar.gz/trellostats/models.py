from datetime import datetime
from peewee import Model, CharField, DateTimeField, FloatField, SqliteDatabase, Proxy

db_proxy = Proxy()


class Snapshot(Model):
    board_id = CharField()
    done_id = CharField()
    when = DateTimeField(default=datetime.now)
    cycle_time = FloatField()

    class Meta:
        database = db_proxy

    def __repr__(self):
        return "<Snapshot:{}:{}>".format(self.board_id, self.cycle_time)
