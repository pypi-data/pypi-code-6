# -*- coding: utf-8 -*-
import os

from ZConfig.components.logger.handlers import HandlerFactory


class EnvFileHandlerFactory(HandlerFactory):
    def create_loghandler(self):
        from ZConfig.components.logger import loghandler
        path = self.section.path % os.environ
        max_bytes = self.section.max_size
        old_files = self.section.old_files
        when = self.section.when
        interval = self.section.interval
        if when or max_bytes or old_files or interval:
            if not old_files:
                raise ValueError("old-files must be set for log rotation")
            if when:
                if max_bytes:
                    raise ValueError("can't set *both* max_bytes and when")
                if not interval:
                    interval = 1
                handler = loghandler.TimedRotatingFileHandler(
                    path, when=when, interval=interval,
                    backupCount=old_files)
            elif max_bytes:
                handler = loghandler.RotatingFileHandler(
                    path, maxBytes=max_bytes, backupCount=old_files)
            else:
                raise ValueError(
                    "max-bytes or when must be set for log rotation")
        else:
            handler = loghandler.FileHandler(path)
        return handler
