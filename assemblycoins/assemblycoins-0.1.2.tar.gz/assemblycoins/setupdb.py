import databases

def create_color_table():
  dbstring="create table colors (color_address varchar(140), source_address varchar(140), total_issued bigint, color_name varchar(200));"
  databases.dbexecute(dbstring, False)

def create_meta_table():
  dbstring="create table meta (lastblockdone integer);"
  databases.dbexecute(dbstring, False)

def create_outputs_table():
  dbstring="create table outputs (btc bigint, color_amount bigint, color_address varchar(200), spent bool, spent_at_txhash varchar(200), destination_address varchar(140), txhash varchar(200), txhash_index varchar(200), blockmade integer, previous_input varchar(3000), blockspent integer);"
  databases.dbexecute(dbstring, False)

def create_tx_queue_table():
  dbstring="create table tx_queue (from_public varchar(140), from_private varchar(140), destination varchar(140), fee_each bigint, source_address varchar(140), transfer_amount bigint, first_tried_at_block integer, success bool, txhash varchar(200), callback_url varchar(200), randomid varchar(200));"
  databases.dbexecute(dbstring, False)

def create_tables():
  create_color_table()
  create_meta_table()
  create_outputs_table()
  create_tx_queue_table()

if __name__ == '__main__':
  create_tables()
