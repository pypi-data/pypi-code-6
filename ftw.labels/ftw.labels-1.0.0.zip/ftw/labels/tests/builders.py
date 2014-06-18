from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.interfaces import ILabelSupport
from ftw.labels.interfaces import ILabeling
import transaction


class LabelRootBuilder(ArchetypesBuilder):

    portal_type = 'Folder'

    def __init__(self, *args, **kwargs):
        super(LabelRootBuilder, self).__init__(*args, **kwargs)
        self.providing(ILabelRoot)
        self.labels = []

    def with_labels(self, *labels):
        self.labels.extend(labels)
        return self

    def after_create(self, obj):
        super(LabelRootBuilder, self).after_create(obj)
        jar = ILabelJar(obj)
        for title, color in self.labels:
            jar.add(title, color)

        if self.session.auto_commit:
            transaction.commit()


builder_registry.register('label root', LabelRootBuilder)


class LabelledPageBuilder(ArchetypesBuilder):

    portal_type = 'Document'

    def __init__(self, *args, **kwargs):
        super(LabelledPageBuilder, self).__init__(*args, **kwargs)
        self.providing(ILabelSupport)
        self.activated_label_ids = []

    def with_labels(self, *label_ids):
        self.activated_label_ids = label_ids
        return self

    def after_create(self, obj):
        super(LabelledPageBuilder, self).after_create(obj)

        ILabeling(obj).update(self.activated_label_ids)
        if self.session.auto_commit:
            transaction.commit()


builder_registry.register('labelled page', LabelledPageBuilder)
