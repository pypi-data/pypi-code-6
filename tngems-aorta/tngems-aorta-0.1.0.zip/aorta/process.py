import select
import os
import logging
import sys
import time

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from libtng.process import BaseProcess
from libtng import db
from libtng import brokers
from libtng.process import BaseProcess
from libtng.config import Settings
import psycopg2
import sqlalchemy.exc

ConnectionError = (
    sqlalchemy.exc.OperationalError,
    psycopg2.OperationalError
)


class Aorta(BaseProcess):
    """The main Aorta process.

    Polls the specified database for notifications and dispatches
    them to the desired event handlers.

    Catches operational errors.
    """
    logger_main = 'aorta.main'
    logger_notifies = 'aorta.notifies'
    on_fail_cooldown = 10.0

    def __init__(self, config_file, using, channels,
        poll_interval=5.0, *args, **kwargs):
        """Initialize a new :class:`Aorta` process instance.

        Args:
            config_file (str): specifies the TNGEMS configuration
                file.
            using (str): identifies the database connection to use.
            channels (list): specifies the channels to listen on.
            poll_interval (float): interval between polls at database.
        """
        self.poll_interval = poll_interval
        self.channels = channels
        self.using = using
        self.config_file = config_file
        self.logger = logging.getLogger(self.logger_main)
        self.connection = None
        self.cursor = None
        BaseProcess.__init__(self, *args, **kwargs)

    def setup(self):
        """Set up the Aorta environment.

        Args:
            config_file (str): specifies the configuration
                file holding the Aorta settings.

        Returns:
            libtng.config.Settings
        """
        self.logger.info("Initializing Aorta main event loop")
        settings = Settings.fromfile(self.config_file)
        settings.setup_databases(db.connections)
        settings.setup_brokers(brokers)
        self.setup_connection()



    def setup_connection(self):
        assert self.connection is None
        assert self.cursor is None
        self.logger.info("Setting up database connection")
        try:
            self.connection = db.connections.get_session(self.using)\
                .bind.raw_connection()
        except ConnectionError as e:
            self.logger.critical("Cannot connect to database")
            return False
        self.logger.info("Succesfully established database connection")
        self.connection.detach()
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
        map(self.subscribe_channel, self.channels)
        self.logger.info("Listening...")
        return True

    def teardown_connection(self):
        self.logger.info("Tearing down database connection")
        if bool(self.connection or self.cursor): # Recovering from lost connection
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None:
                self.connection.close()
                self.logger.info("Disconnected from database")
        self.connection = None
        self.cursor = None

    def subscribe_channel(self, channel):
        """Subscribes to the specified channel."""
        query = "LISTEN \"{0}\";".format(channel)
        self.cursor.execute(query)
        self.logger.info(
            'Subscribed to channel "{0}" ({1})'.format(channel, query))

    def get_notifies(self, connection):
        return connection.notifies

    def process_notification(self, notification):
        """Processes a notification received from the PostgreSQL
        server.

        Args:
            notification (Notify): the notification.

        Returns:
            None
        """
        pass

    def main_event(self):

        # Setup database connection if it doesn't exist,
        # but return immediately if no connection could
        # be made.
        if not bool(self.connection or self.cursor):
            if not self.setup_connection():
                return

        args = [self.connection], [], [], self.poll_interval
        if select.select(*args) == ([],[],[]):
            return

        # Poll the connection and handle any errors.
        try:
            self.connection.poll()
        except ConnectionError as e:
            msg = "Unable to poll database server for notifications: {0}"\
                .format(str(e))
            self.logger.critical(msg)
            self.teardown_connection()
            time.sleep(self.poll_interval)
            return

        # Polled succesfully, process notifies.
        notifies = self.get_notifies(self.connection)
        self.logger.info(
            "Received {0} notifications.".format(len(notifies)))
        while notifies:
            n = notifies.pop()
            self.process_notification(n)

    def do_cleanup(self, graceful):
        self.teardown_connection()