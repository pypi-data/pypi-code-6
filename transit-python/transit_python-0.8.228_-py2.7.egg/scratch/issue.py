from transit.reader import Reader
from transit.writer import Writer
from StringIO import StringIO
import datetime


class DateHandler(object):
    @staticmethod
    def tag(d):
        return 'p'

    @staticmethod
    def rep(d):
        return str(d)

    @staticmethod
    def string_rep(d):
        return str(d)

    @staticmethod
    def from_rep(d):
        return datetime.datetime.strptime(d, '%Y-%m-%d').date()


my_data = {
    'start_date': datetime.date(2014, 9, 9),
    'end_date': datetime.date(2014, 10, 10)
}

io = StringIO()
writer = Writer(io, "json")
writer.register(datetime.date, DateHandler)
writer.write(my_data)
output = io.getvalue()
io.close()


reader = Reader()
reader.register('p', DateHandler)
parsed = reader.read(StringIO(output))

assert parsed['start_date'] == my_data['start_date']  # Should be fine
assert parsed['end_date'] == my_data['end_date']  # Error here - actual value of parsed['end_date'] is (u'start_date', u'2014-10-10')
print(parsed)
