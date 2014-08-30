from whoosh.fields import TEXT, ID, Schema

bw2_schema = Schema(
    name=TEXT(stored=True),
    comment=TEXT(stored=True),
    product=TEXT(stored=True),
    categories=TEXT(stored=True),
    location=TEXT(stored=True),
    database=ID(stored=True),
    key=ID(stored=True)
)
