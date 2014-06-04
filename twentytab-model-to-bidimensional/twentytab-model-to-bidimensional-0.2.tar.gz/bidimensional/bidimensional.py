
class Bidimensional(object):

    def __init__(self, model, queryset=[], depth=-1):
        self.model = model
        self.depth = depth
        self.queryset = queryset

    def _recursive_keys(self, model, key="", depth=0):
        headers = []
        related = []
        for field in model._meta.fields:
            if not hasattr(field, 'related'):
                headers.append(u'{}{}'.format(key, field.name))
            else:
                related.append(field)

        for field in related:
            if (self.depth > 0 and depth < self.depth) or self.depth < 0:
                headers.extend(self._recursive_keys(
                    field.related.parent_model,
                    u'{}{}__'.format(key, field.name),
                    depth + 1
                ))
            else:
                headers.append(u'{}{}'.format(key, field.name))

        return headers

    def _recursive_items(self, item, key="", depth=0):

        element = {}
        related = []

        model = item.__class__

        for field in model._meta.fields:
            if not hasattr(field, 'related'):
                element[u'{}{}'.format(key, field.name)] = ''
                if item:
                    element[u'{}{}'.format(key, field.name)] = getattr(item, field.name, '')
            else:
                related.append(field)

        for field in related:
            rel_item = getattr(item, field.name, '')
            if rel_item and ((self.depth > 0 and depth < self.depth) or self.depth < 0):

                recursive_elem = self._recursive_items(
                    rel_item,
                    u'{}{}__'.format(key, field.name),
                    depth + 1
                )
                element.update(recursive_elem)

            else:
                element[u'{}{}'.format(key, field.name)] = rel_item
        return element

    def headers(self):
        return self._recursive_keys(self.model)

    def items(self):
        res = []
        for el in self.queryset:
            res.append(self._recursive_items(el, depth=self.depth))
        return res