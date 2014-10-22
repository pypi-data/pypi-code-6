# -*- coding: utf-8 -*-

"""
Tree models for data being displayed in the main window.
"""

import gtk
import gtk.glade
import gobject

class EcritureTreeModel(gtk.GenericTreeModel):

    column_types = ( gobject.TYPE_STRING, # date
                     gobject.TYPE_STRING, # libelle
                     gobject.TYPE_INT,    # total
                     gobject.TYPE_STRING, # bgcolor
                     )

    def __init__(self, tree=None):
        gtk.GenericTreeModel.__init__(self)
        self.tree = tree

    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY|gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_types)

    def on_get_column_type(self, index):
        return self.column_types[index]

    def on_get_iter(self, path):
        if self.tree:
            return self.tree.findall('.//ecritures')[path[0]]

    def on_get_path(self, rowref):
        if self.tree:
            return self.tree.findall('.//ecritures').index(rowref)

    def on_get_value(self, rowref, column):
        if self.tree:
            return self.tree.findall('.//ecritures').index(rowref)

    def on_iter_next(self, rowref):
        pass

    def on_iter_children(self, parent):
        pass

    def on_iter_has_child(self, rowref):
        pass

    def on_iter_n_children(self, rowref):
        pass

    def on_iter_nth_child(self, parent, n):
        pass

    def on_iter_parent(self, child):
        pass

class PlanComptableTreeModel(gtk.GenericTreeModel):

    column_types = ( gobject.TYPE_INT,    # numero
                     gobject.TYPE_STRING, # libelle
                     )

    def __init__(self, tree):
        gtk.GenericTreeModel.__init__(self)
        self.tree = tree
        self.parents = {}
        for parent in self.tree.getiterator():
            for child in parent:
                self.parents[child] = parent

    def on_get_flags(self):
        return gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_types)

    def on_get_column_type(self, index):
        return self.column_types[index]

    def on_get_iter(self, path):
        #print 'on_get_iter', path,
        rowref = self.tree.getroot()
        while path:
            rowref = rowref[path[0]]
            path = path[1:]
        # print rowref
        return rowref

    def on_get_path(self, rowref):
        #print 'on_get_path', rowref,
        path = []
        while rowref != self.tree.getroot():
            parent = self.parents[rowref]
            path.append(list(parent).index(rowref))
            rowref = parent
        path.reverse()
        #print path
        return path

    def on_get_value(self, rowref, column):
        #print 'on_get_value', rowref, column
        if column == 0:
            return int(rowref.get('numero'))
        elif column == 1:
            return rowref.get('nom')
        raise AssertionError

    def on_iter_next(self, rowref):
        #print 'on_iter_next', rowref
        try:
            i = list(self.parents[rowref]).index(rowref)
            return self.parents[rowref][i+1]
        except IndexError:
            return None

    def on_iter_children(self, parent):
        #print 'on_iter_children', parent
        return parent[0]

    def on_iter_has_child(self, rowref):
        #print 'on_iter_has_child', rowref, rowref.get('numero'), len(rowref)
        return len(rowref) > 0

    def on_iter_n_children(self, rowref):
        #print 'on_iter_n_children', rowref
        return len(rowref)

    def on_iter_nth_child(self, parent, n):
        #print 'on_iter_nth_child', parent, n
        if parent is None:
            return self.tree.getroot()[n]

    def on_iter_parent(self, child):
        #print 'on_iter_parent', child
        parent = self.parents[child]
        if parent == self.tree.getroot():
            return None
        else:
            return parent
