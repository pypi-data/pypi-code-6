from datetime import datetime, timedelta
import functools

from django.conf import settings
from django.db import transaction, IntegrityError

from .models import DBMutex


class DBMutexError(Exception):
    """
    Thrown when a lock cannot be acquired.
    """
    pass


class DBMutexTimeoutError(Exception):
    """
    Thrown when a lock times out before it is released.
    """
    pass


class db_mutex(object):
    """
    An object that acts as a context manager and a function decorator for acquiring a
    DB mutex lock.

    Args:
        lock_id: The ID of the lock one is trying to acquire

    Raises:
        DBMutexError when the lock cannot be obtained
        DBMutexTimeoutError when the lock was deleted during execution

    Examples:
        This context manager/function decorator can be used in the following way

        from db_mutex import db_mutex

        # Lock a critical section of code
        try:
            with db_mutex('lock_id'):
                # Run critical code here
                pass
        except DBMutexError:
            print 'Could not obtain lock'
        except DBMutexTimeoutError:
            print 'Task completed but the lock timed out'

        # Lock a function
        @db_mutex('lock_id'):
        def critical_function():
            # Critical code goes here
            pass

        try:
            critical_function()
        except DBMutexError:
            print 'Could not obtain lock'
        except DBMutexTimeoutError:
            print 'Task completed but the lock timed out'
    """
    mutex_ttl_seconds_settings_key = 'DB_MUTEX_TTL_SECONDS'

    def __init__(self, lock_id):
        self.lock_id = lock_id
        self.lock = None

    def get_mutex_ttl_seconds(self):
        """
        Returns a TTL for mutex locks. It defaults to 30 minutes. If the user specifies None
        as the TTL, locks never expire.
        """
        return getattr(settings, self.mutex_ttl_seconds_settings_key, timedelta(minutes=30).total_seconds())

    def delete_expired_locks(self):
        """
        Deletes all expired mutex locks if a ttl is provided.
        """
        ttl_seconds = self.get_mutex_ttl_seconds()
        if ttl_seconds is not None:
            DBMutex.objects.filter(creation_time__lte=datetime.utcnow() - timedelta(seconds=ttl_seconds)).delete()

    def __call__(self, func):
        return self.decorate_callable(func)

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()

    def start(self):
        """
        Acquires the db mutex lock. Takes the necessary steps to delete any stale locks.
        Throws a DBMutexError if it can't acquire the lock.
        """
        # Delete any expired locks first
        self.delete_expired_locks()
        try:
            with transaction.atomic():
                self.lock = DBMutex.objects.create(lock_id=self.lock_id)
        except IntegrityError:
            raise DBMutexError('Could not acquire lock: {0}'.format(self.lock_id))

    def stop(self):
        """
        Releases the db mutex lock. Throws an error if the lock was released before the function finished.
        """
        if not DBMutex.objects.filter(id=self.lock.id).exists():
            raise DBMutexTimeoutError('Lock {0} expired before function completed'.format(self.lock_id))
        else:
            self.lock.delete()

    def decorate_callable(self, func):
        """
        Decorates a function with the db_mutex decorator by using this class as a context manager around
        it.
        """
        def wrapper(*args, **kwargs):
            with self:
                result = func(*args, **kwargs)
            return result
        functools.update_wrapper(wrapper, func)
        return wrapper
