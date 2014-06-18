from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.utils import make_sortable
from OFS.interfaces import IApplication
from persistent.mapping import PersistentMapping
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import implements
from zope.interface import Interface


ANNOTATION_KEY = 'ftw.labels:jar'


class LabelJar(object):
    implements(ILabelJar)
    adapts(ILabelRoot)

    def __init__(self, context):
        self.context = context

    def add(self, title, color):
        label_id = self._make_id(title)
        self.storage[label_id] = PersistentMapping(
            dict(
                label_id=label_id,
                title=title,
                color=color
            )
        )
        return label_id

    def remove(self, label_id):
        if label_id not in self.storage:
            return False

        del self.storage[label_id]
        return True

    def update(self, label_id, title, color):
        self.storage[label_id].update(
            dict(
                title=title,
                color=color
            )
        )

    def get(self, label_id):
        return dict(self.storage[label_id])

    def list(self):
        labels = map(dict, self.storage.values())
        return sorted(labels, key=lambda cls: make_sortable(cls['title']))

    @property
    def storage(self):
        if getattr(self, '_storage', None) is None:
            annotation = IAnnotations(self.context)
            if ANNOTATION_KEY not in annotation:
                annotation[ANNOTATION_KEY] = PersistentMapping()
            self._storage = annotation[ANNOTATION_KEY]
        return self._storage

    def _make_id(self, title):
        normalizer = getUtility(IIDNormalizer)
        label_id = base_id = normalizer.normalize(title)

        counter = 0
        while label_id in self.storage:
            counter += 1
            label_id = '{0}-{1}'.format(base_id, counter)

        return label_id


@implementer(ILabelJar)
@adapter(Interface)
def jar_discovery(context):
    """An ILabelJar adapter for non-ILabelRoot objects, walking
    up the acquisition chain for finding the ILabelJar.
    This allows to adapt any object, which is within an ILabelRoot,
    to ILabelJar without the need to find the root.
    """
    return ILabelJar(aq_parent(aq_inner(context)))


@implementer(ILabelJar)
@adapter(IApplication)
def jar_discovery_app_reached(context):
    """Exits the ILabelJar discovery loop when the Zope app is reached.
    See the jar_discovery docstring for more details.
    """
    raise LookupError('Could not find ILabelJar on any parents.'
                      ' No parent seems to provide ILabelRoot.')
