from datetime import datetime

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
import six
import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles

from .exc import ImproperlyConfigured
from .factory import ModelFactory


@compiles(sa.types.BigInteger, 'sqlite')
def compile_big_integer(element, compiler, **kw):
    return 'INTEGER'


class TransactionBase(object):
    id = sa.Column(sa.types.BigInteger, primary_key=True, autoincrement=True)
    issued_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    @property
    def entity_names(self):
        """
        Return a list of entity names that changed during this transaction.
        """
        return [changes.entity_name for changes in self.changes]

    @property
    def changed_entities(self):
        """
        Return all changed entities for this transaction log entry.

        Entities are returned as a dict where keys are entity classes and
        values lists of entitites that changed in this transaction.
        """
        manager = self.__versioning_manager__
        tuples = set(manager.version_class_map.items())
        entities = {}

        session = sa.orm.object_session(self)

        for class_, version_class in tuples:
            if class_.__name__ not in self.entity_names:
                continue

            tx_column = manager.option(class_, 'transaction_column_name')

            entities[version_class] = (
                session
                .query(version_class)
                .filter(getattr(version_class, tx_column) == self.id)
            ).all()
        return entities


class TransactionFactory(ModelFactory):
    model_name = 'Transaction'

    def __init__(self, remote_addr=True):
        self.remote_addr = remote_addr

    def create_class(self, manager):
        """
        Create Transaction class.
        """
        class Transaction(
            manager.declarative_base,
            TransactionBase
        ):
            __tablename__ = 'transaction'
            __versioning_manager__ = manager

            if self.remote_addr:
                remote_addr = sa.Column(sa.String(50))

            if manager.user_cls:
                user_cls = manager.user_cls
                registry = manager.declarative_base._decl_class_registry

                if isinstance(user_cls, six.string_types):
                    try:
                        user_cls = registry[user_cls]
                    except KeyError:
                        raise ImproperlyConfigured(
                            'Could not build relationship between Transaction'
                            ' and %s. %s was not found in declarative class '
                            'registry. Either configure VersioningManager to '
                            'use different user class or disable this '
                            'relationship ' % (user_cls, user_cls)
                        )
                user_id = sa.Column(
                    sa.Integer,
                    sa.ForeignKey(
                        '%s.id' % user_cls.__tablename__
                    ),
                    index=True
                )

                user = sa.orm.relationship(user_cls)

            def __repr__(self):
                fields = ['id', 'issued_at', 'user']
                field_values = OrderedDict()
                for field in fields:
                    if hasattr(self, field):
                        field_values[field] = getattr(self, field)
                return '<Transaction %s>' % ', '.join(
                    (
                        '%s=%r' % (field, value)
                        if not isinstance(value, six.integer_types)
                        # We want the following line to ensure that longs get
                        # shown without the ugly L suffix on python 2.x
                        # versions
                        else '%s=%d' % (field, value)
                        for field, value in field_values.items()
                    )
                )
        return Transaction
