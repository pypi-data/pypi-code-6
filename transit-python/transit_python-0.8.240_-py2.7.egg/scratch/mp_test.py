import transit.writer as twriter
import transit.reader as treader
from io import BytesIO
from StringIO import StringIO
from datetime import datetime
import dateutil.tz
from uuid import UUID

b = BytesIO()
#b = StringIO()
r = treader.Reader(protocol="msgpack")
w = twriter.Writer(b, protocol="msgpack")

UUIDS = (UUID('5a2cbea3-e8c6-428b-b525-21239370dd55'),
         UUID('d1dc64fa-da79-444b-9fa4-d4412f427289'),
         UUID('501a978e-3a3e-4060-b3be-1cf2bd4b1a38'),
         UUID('b3ba141a-a776-48e4-9fae-a28ea8571f58'))

w.write(UUIDS)
print(b.getvalue())
b.seek(0)
print r.read(b)
