from sqlalchemy import create_engine

def connect(db_url):
  engine = create_engine(db_url)
  return engine



if __name__ == '__main__':
  db = connect('postgres://brian:brian@localhost:5432/nl')
  print db