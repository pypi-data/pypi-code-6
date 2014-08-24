import email.message
import logging
import os
import smtplib


_DEFAULT_HOST = "localhost"
_DEFAULT_PORT = 25
_DEFAULT_USE_STARTTLS = False
_DEFAULT_USE_SSL = False
_DEFAULT_USE_LMTP = False
_DEFAULT_USER = None
_DEFAULT_PASSWORD = None


logger = logging.getLogger(__name__)


class Mailer:
    """
    A Mailer represents a connection to an SMTP server.

    It can be used with a context manager, like this::

        mailer = Mailer(...)
        with mailer:
            mailer.send(msg)

    However, using the ``open`` and ``close`` methods is also available.
    """

    def __init__(self, host=_DEFAULT_HOST, port=_DEFAULT_PORT,
                 use_starttls=_DEFAULT_USE_STARTTLS, use_ssl=_DEFAULT_USE_SSL,
                 use_lmtp=_DEFAULT_USE_LMTP, user=_DEFAULT_USER,
                 password=_DEFAULT_PASSWORD):
        """Construct a new Mailer object based on the arguments passed."""
        self.host = host
        self.port = port
        self.use_starttls = use_starttls
        self.use_ssl = use_ssl
        self.use_lmtp = use_lmtp
        self.user = user
        self.password = password
        self._smtp = None

    @staticmethod
    def from_environ(prefix="MAIL_", environ=None):
        """
        Create a Mailer instance from environment variables.

        The expected variable names are ``HOST``, ``PORT``, ``USE_STARTTLS``,
        ``USE_SSL``, ``USE_LMTP``, ``USER`` and ``PASSWORD``.

        Note that boolean variables (``USE_*``) are true for any non-empty
        value and false for anything else — this is how ``bool`` works in
        Python.
        """
        if environ is None:
            environ = os.environ

        variables = [
            ("host", _DEFAULT_HOST, str),
            ("port", _DEFAULT_PORT, int),
            ("use_starttls", _DEFAULT_USE_STARTTLS, bool),
            ("use_ssl", _DEFAULT_USE_SSL, bool),
            ("use_lmtp", _DEFAULT_USE_LMTP, bool),
            ("user", _DEFAULT_USER, str),
            ("password", _DEFAULT_PASSWORD, str),
        ]

        kwargs = {}
        for key, default, type_func in variables:
            env_var = "{prefix}{key}".format(prefix=prefix, key=key.upper())
            kwargs[key] = type_func(environ.get(env_var, default))

        return Mailer(**kwargs)

    @staticmethod
    def _create_smtp(host, port, use_starttls, use_ssl, use_lmtp):
        """Create an approriate SMTP object based on the arguments passed."""
        logger.debug("Creating SMTP connection to %s:%d.", host, port)

        if (use_starttls and use_ssl) or (use_ssl and use_lmtp) \
            or (use_starttls and use_lmtp):
            raise ValueError("You can only pick a single server type.")

        if use_starttls:
            smtp = smtplib.SMTP(host, port)
            smtp.starttls()
            smtp.ehlo()
            return smtp
        elif use_ssl:
            return smtplib.SMTP_SSL(host, port)
        elif use_lmtp:
            return smtplib.LMTP(host, port)
        else:
            return smtplib.SMTP(host, port)

    def open(self):
        """Open the connection to the SMTP server."""
        if self._smtp is not None:
            raise RuntimeError("Already connected to an SMTP server.")

        logger.info("Opening connection to %s:%d.", self.host, self.port)

        self._smtp = self._create_smtp(self.host, self.port, self.use_starttls,
                                       self.use_ssl, self.use_lmtp)
        if self.user is not None or self.password is not None:
            logger.info("Logging in to %s:%d server.", self.host, self.port)
            self._smtp.login(self.user, self.password)

    def close(self):
        """Close the connection to the SMTP server."""
        if self._smtp is None:
            raise RuntimeError("Not connected to an SMTP server.")

        logger.info("Closing connection to %s:%d.", self.host, self.port)

        self._smtp.quit()
        self._smtp = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def send(self, msg):
        """Send an email Message."""
        self._smtp.send_message(msg)
