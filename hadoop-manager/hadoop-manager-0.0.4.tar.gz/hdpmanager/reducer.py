__all__ = ['Reducer']

import sys
import traceback

from streamer import Streamer


class _Empty():
    pass


class Reducer(Streamer):

    def _set_serializers(self, serializers):
        self._read_protocol = serializers['inter']
        self._write_protocol = serializers['output']

    def reduce(self, key, values):
        """
        Override this methos for reducing the input
        Output can be either returned or yielded as a key, value pair

        :param key: key returned by the mapper
        :param values: generator over values retuned by the mapper for this key
        """
        return key, values

    def _try_reduce(self, key, values):
        try:
            self._out(self.reduce(key, values))
        except Exception, e:
            self.count('error records', 1)
            sys.stderr.write('error %s processing record; key:%s, values:\n' % (repr(e), repr(key)))
            traceback.print_exc(file=sys.stderr)

    def parse_line(self, line):
        line = line.rstrip()
        parts = line.split('\t')

        if not parts or len(parts) < 2:
            raise AttributeError('Empty line')

        key = self._read_protocol.decode(parts[0], cache_idx=0)
        values = [self._read_protocol.decode(x, cache_idx=1) for x in parts[1:]]

        return key, values

    def _reduce_next_key(self):
        last_key, last_values = self._last_line

        for value in last_values:
            yield value

        for line in self._input_stream:
            try:
                key, values = self.parse_line(line)
            except AttributeError:
                continue

            if last_key != key and last_key is not _Empty:
                self._last_line = (key, values)
                return

            for value in values:
                yield value

        self._last_line = _Empty, None

    def _reduce_first_line(self):
        for line in self._input_stream:
            try:
                self._last_line = self.parse_line(line)
            except AttributeError:
                pass
            except StopIteration:
                return
            else:
                return

    def parse_input(self):
        self._last_line = _Empty, None
        self._reduce_first_line()

        while self._last_line[0] is not _Empty:
            self._try_reduce(self._last_line[0], self._reduce_next_key())
