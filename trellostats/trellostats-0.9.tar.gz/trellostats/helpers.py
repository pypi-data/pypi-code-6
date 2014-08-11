from peewee import SqliteDatabase


def cycle_time(ts, board, done):
    done_id = ts.get_list_id_from_name(done)
    cards = ts.get_list_data(done_id)
    return ts.cycle_time(cards)


def init_db(db_proxy):
    db_proxy.initialize(SqliteDatabase('snapshots.db'))
