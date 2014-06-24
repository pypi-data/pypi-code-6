from ftw.labels.interfaces import ILabelSupport
from ftw.labels.interfaces import ILabeling
from operator import itemgetter
from plone.indexer.decorator import indexer


@indexer(ILabelSupport)
def labels(obj):
    labeling = ILabeling(obj)
    return map(itemgetter('label_id'), labeling.active_labels())
