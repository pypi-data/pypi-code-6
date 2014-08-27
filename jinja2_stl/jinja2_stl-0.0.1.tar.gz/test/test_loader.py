# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six
import pytest

if six.PY3:
    from unittest.mock import patch, call, MagicMock
else:
    from mock import patch, call, MagicMock

from jinja2 import BaseLoader, TemplateNotFound

from jinja2_stl.loader import FilestorageTemplateLoader


class TestFilestorageTemplateLoader(object):
    def test_template_loader_is_subclass_of_base_loader(self):
        assert issubclass(FilestorageTemplateLoader, BaseLoader)

    def test_storage_saved_on_init(self):
        storage = MagicMock()
        loader = FilestorageTemplateLoader(storage=storage)

        assert loader._storage == storage

    def test_get_source_return_tuple(self, environment, storage):
        loader = FilestorageTemplateLoader(storage=storage)

        result = loader.get_source(environment, 'index.html')

        assert type(result) == tuple

    def test_raise_template_not_found_when_template_not_exists(self, environment, storage):
        storage.exists.return_value = False
        loader = FilestorageTemplateLoader(storage=storage)

        with pytest.raises(TemplateNotFound):
            loader.get_source(environment, 'index.html')

    def test_open_template(self, environment, storage):
        loader = FilestorageTemplateLoader(storage=storage)
        loader.get_source(environment, 'index.html')

        assert storage.open.called

    def test_read_opened_file(self, environment, storage):
        f = MagicMock()
        f.__enter__.return_value = f
        storage.open.return_value = f
        loader = FilestorageTemplateLoader(storage=storage)
        loader.get_source(environment, 'index.html')

        assert f.read.called

    def test_first_item_in_returned_tuple_is_file_content(self, environment, storage):
        f = MagicMock()
        f.__enter__.return_value = f
        storage.open.return_value = f
        loader = FilestorageTemplateLoader(storage=storage)
        result = loader.get_source(environment, 'index.html')

        assert result[0] == f.read.return_value

    def test_last_item_in_returned_tuple_is_function(self, environment, storage):
        loader = FilestorageTemplateLoader(storage=storage)
        result = loader.get_source(environment, 'index.html')

        assert callable(result[2])

    def test_uptodate_function_return_true_when_template_has_same_size(self, environment, storage):
        storage.size.return_value = 123456789
        loader = FilestorageTemplateLoader(storage=storage)
        result = loader.get_source(environment, 'index.html')
        uptodate = result[2]

        assert uptodate()

    def test_uptodate_function_return_false_when_template_size_is_changed(self, environment, storage):
        storage.size.side_effect = [1234567, 90123456]
        loader = FilestorageTemplateLoader(storage=storage)
        result = loader.get_source(environment, 'index.html')
        uptodate = result[2]

        assert not uptodate()

    def test_second_size_call_is_executed_in_uptodate_function(self, environment, storage):
        loader = FilestorageTemplateLoader(storage=storage)
        result = loader.get_source(environment, 'index.html')
        uptodate = result[2]

        assert storage.size.call_count == 1

        uptodate()
        assert storage.size.call_count == 2
