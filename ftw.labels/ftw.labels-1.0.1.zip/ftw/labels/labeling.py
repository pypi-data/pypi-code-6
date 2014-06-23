from ftw.labels.interfaces import ILabeling
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelSupport
from ftw.labels.utils import make_sortable
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


ANNOTATION_KEY = 'ftw.labels:labeling'


class Labeling(object):
    implements(ILabeling)
    adapts(ILabelSupport)

    def __init__(self, context):
        self.context = context
        self.jar = ILabelJar(self.context)

    def update(self, label_ids):
        available_labels = self.jar.storage.keys()

        for label_id in label_ids:
            if label_id not in available_labels:
                raise LookupError(
                    'Cannot activate label: '
                    'the label "{0}" is not in the label jar. '
                    'Following labels ids are available: {1}'.format(
                        label_id, ', '.join(available_labels)))

        # Do not replace self.storage, since it is a PersistentList!
        self.storage[:] = label_ids

    def active_labels(self):
        labels = []
        for label_id in self.storage:
            try:
                labels.append(self.jar.get(label_id))
            except KeyError:
                pass
        return sorted(labels, key=lambda cls: make_sortable(cls['title']))

    def available_labels(self):
        for label in self.jar.list():
            label['active'] = (label.get('label_id') in self.storage)
            yield label

    @property
    def storage(self):
        if getattr(self, '_storage', None) is None:
            annotation = IAnnotations(self.context)
            if ANNOTATION_KEY not in annotation:
                annotation[ANNOTATION_KEY] = PersistentList()
            self._storage = annotation[ANNOTATION_KEY]
        return self._storage
