import pdb
import types
import os

import guidata.dataset.dataitems as di

from .base import ConfigItem


class Value(ConfigItem):

    def __init__(self, default=None, **options_gui_item):
        super(Value, self).__init__(name="")
        self.value = default
        self.target = None
        self.options_gui_item = options_gui_item

    def setup_value(self, value):
        return value

    def setup_gui_item(self):
        def callback(data_set, gui_item, value):
            value_item = gui_item.get_prop("extension", "value_item")
            value_item.value = value
            target = value_item.target
            if target is not None:
                to, method = target
                to.value = method(value)  # sets value to value_item
                setattr(data_set, to._name, method(value))  # sets value to gui_item
        # we are changing options below, so we work with a copy
        options = self.options_gui_item.copy()
        if "label" not in options:
            options["label"] = self._name
        options["default"] = self.value
        gui_item = self.create_gui_item(options)
        gui_item.set_prop("display", callback=callback)
        return wrap(gui_item, self)

    def __get__(self, from_, type_):
        return self.value



def wrap(gui_item, value_item):
    """set property for retreiving value_item from gui_item
       and pathc gui_items check method:
    """

    # we monkey patch the check_value method but still want to have access to the originial
    # method from guidata as it implements many features which we want to use too, eg checking for
    # a min or max value, etc...
    # binding the original method to a parameter does the trick which was not obvious, so test
    # carefully if you have a reason to change this:

    def check_value(self, value, orig_check_value=gui_item.check_value):
        value_item = self.get_prop("extension", "value_item")
        ok_value_item = hasattr(value_item, "check") and value_item.check(value)
        ok_gui_item = orig_check_value(value)
        return ok_value_item and ok_gui_item

    gui_item.set_prop("extension", value_item=value_item)
    gui_item.check_value = types.MethodType(check_value, gui_item)
    return gui_item


class IntValue(Value):

    def check(self, value):
        return isinstance(value, int)

    def create_gui_item(self, options):
        return di.IntItem(**options)


class FloatValue(Value):

    def check(self, value):
        return isinstance(value, (int, long, float))

    def create_gui_item(self, options):
        return di.FloatItem(**options)


class StringValue(Value):

    def check(self, value):
        return isinstance(value, basestring)

    def create_gui_item(self, options):
        return di.StringItem(**options)


class BoolValue(Value):

    def check(self, value):
        return isinstance(value, bool)

    def create_gui_item(self, options):
        return di.BoolItem(**options)


class _FiniteDomainValue(Value):

    def __init__(self, choices, *a, **kw):
        super(_FiniteDomainValue, self).__init__(*a, **kw)
        self.choices = choices

    def check(self, value):
        return value in self.choices


class SingleValued(_FiniteDomainValue):

    def create_gui_item(self, options):
        if not all(isinstance(c, basestring) for c in self.choices):
            raise Exception("MultipleValued only works with strings as choices")
        options = options.copy()
        options["choices"] = self.choices
        if self.value is not None:
            options["default"] = self.choices.index(self.value)
        return di.ChoiceItem(**options)

    def _setup_value(self, value):
        if isinstance(value, int):
            # if value is int and all choices are not int: choose by index:
            if any(isinstance(c, int) for c in self.choices):
                return value
            try:
                new_value = self.choices[value]
            except IndexError:
                raise IndexError("index %d is out of range for %r" % (value, self))
            return new_value
        return super(SingleValued, self).setup_value(value)


class MultipleValued(_FiniteDomainValue):

    def create_gui_item(self, options):
        if not all(isinstance(c, basestring) for c in self.choices):
            raise Exception("MultipleValued only works with strings as choices")
        options = options.copy()
        options["choices"] = self.choices
        cols = options.get("cols")
        rows = options.get("rows")
        if cols:
            del options["cols"]
        if rows:
            del options["rows"]
        if self.value is not None:
            options["default"] = [i for (i, v) in enumerate(self.choices) if v in self.value]
        gui_item = di.MultipleChoiceItem(**options)
        if cols:
            gui_item = gui_item.vertical(cols)
        if rows:
            gui_item = gui_item.horizontal(rows)
        return gui_item

    def _setup_value(self, value):
        if all(isinstance(v, int) for v in value):
            # if value is int and all choices are not int: choose by index:
            if any(isinstance(c, int) for c in self.choices):
                return value
            new_values = []
            try:
                for v in value:
                    new_value = self.choices[v]
                    new_values.append(new_value)
            except IndexError:
                raise IndexError("index %d is out of range for %r" % (value, self))
            return new_values
        return super(MultipleValued, self).setup_value(value)

    def check(self, value):
        return all(vi in self.choices for vi in value)


class ExistingFileValue(StringValue):

    def check(self, value):
        ok = isinstance(value, basestring)
        return ok and os.path.exists(value)

    def create_gui_item(self, options):
        return di.FileOpenItem(**options)


class ExistingFilesValue(StringValue):

    def check(self, value):
        ok = isinstance(value, (tuple, list))
        ok = ok and all(isinstance(vi, basestring) for vi in value)
        ok = ok and all(os.path.exists(vi) for vi in value)
        return ok

    def create_gui_item(self, options):
        options = options.copy()
        options["default"] = options.get("default") or [""]
        return di.FilesOpenItem(**options)


class FileForSaveValue(StringValue):

    def check(self, value):
        if not isinstance(value, basestring):
            return False
        dirname = os.path.dirname(value)
        return os.path.exists(dirname) and os.path.isdir(dirname)

    def create_gui_item(self, options):
        options = options.copy()
        options["default"] = options.get("default") or ""
        return di.FileSaveItem(**options)


class DirectoryValue(StringValue):

    def create_gui_item(self, options):
        options = options.copy()
        options["default"] = options.get("default") or ""
        return di.DirectoryItem(**options)
