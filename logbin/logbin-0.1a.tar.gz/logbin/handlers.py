import logging
import sys


class PackStreamHandler(logging.Handler):

    def __init__(self, stream=None):
        super(PackStreamHandler, self).__init__()
        if stream is None:
            stream = sys.stderr
        self.stream = stream
        self.setLevel(logging.DEBUG)  # Log everything by default

    def flush(self):
        """
        Flushes the stream.
        """
        self.acquire()
        try:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
        finally:
            self.release()

    def serialize(self, record):
        import msgpack
        import traceback

        record_dict = {
            'args': record.args,
            'created': record.created,
            'exc_info': None,  # We cannot serialize this :(
            'exc_text': record.exc_text,
            'filename': record.filename,
            'funcName': record.funcName,
            'levelname': record.levelname,
            'levelno': record.levelno,
            'lineno': record.lineno,
            'module': record.module,
            'msecs': record.msecs,
            'msg': record.msg,
            'name': record.name,
            'pathname': record.pathname,
            'process': record.process,
            'processName': record.processName,
            'relativeCreated': record.relativeCreated,
            'thread': record.thread,
            'threadName': record.threadName}

        if record.exc_info is not None:
            # We cannot serialize exception information.
            # The best workaround here is to simply add the
            # relevant information to the message, as the
            # formatter would..
            exc_class = u'{0}.{1}'.format(
                record.exc_info[0].__module__,
                record.exc_info[0].__name__)
            exc_message = str(record.exc_info[1])
            exc_repr = repr(record.exc_info[1])
            exc_traceback = '\n'.join(
                traceback.format_exception(*record.exc_info))

            record_dict['_orig_msg'] = record_dict['msg']
            record_dict['msg'] += "\n\n"
            record_dict['msg'] += exc_traceback
            record_dict['_exc_class'] = exc_class
            record_dict['_exc_msg'] = exc_message
            record_dict['_exc_repr'] = exc_repr
            record_dict['_exc_traceback'] = exc_traceback

        return msgpack.packb(record_dict)

    def emit(self, record):
        self.acquire()
        try:
            packed = self.serialize(record)
            self.stream.write(packed)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
        finally:
            self.release()
