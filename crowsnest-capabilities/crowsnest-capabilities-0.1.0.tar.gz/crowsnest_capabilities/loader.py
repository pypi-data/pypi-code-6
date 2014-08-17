from collections import defaultdict
import os

import yaml

from .models import Action, Event, DataField
from .structure import capabilities

_already_loaded = False


def _find_documents():
    documents = []

    for dirpath, child_dirs, filenames in os.walk(os.path.dirname(os.path.abspath(__file__)) + '/definitions/'):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), 'r') as f:
                documents.append(yaml.load(f.read()))

    return documents


def _combine_documents(documents):
    """ Get and parse all of the documents

    Perform basic validation, like making sure there are no collisions
    """

    all_keys = [key for document in documents for key in document.keys()]
    key_counts = defaultdict(int)
    def update_count(key):
        key_counts[key] += 1

    # count the keys
    map(update_count, all_keys)

    # get the non-unique keys
    non_unique_keys = [key for key, count in key_counts.iteritems() if count > 1]

    if non_unique_keys:
        raise Exception("Duplicate entries for: {}".format(non_unique_keys))

    # merge all dicts into one
    master_document = {}
    map(lambda document: master_document.update(document), documents)

    return master_document


def _malformed(name, msg):
    return 'Malformed name `{}`: {}'.format(name, msg)


def _assert_lists_equivalent(list1, list2, name, msg):
    assert sorted(list1) == sorted(list2), _malformed(name, msg)


def _build_field(name, field):
    # a string value is a shortcut for the type
    if isinstance(field, basestring):
        return DataField(name, type=field)
    # a list value is a shortcut for valid_values
    if isinstance(field, list) or isinstance(field, tuple):
        return DataField(name, valid_values=field)

    # everything else is just mapping to DataField kwargs
    assert isinstance(field, dict), 'definition must be a dict, list, or string'
    # if a default is provided, assume required is false
    if 'default' in field:
        field['required'] = False
    return DataField(name, **field)


def _build_capabilities(document):
    """ Validate and build some real structures for all of the capabilities and events """

    for name, mapping in document.iteritems():
        # make sure it's a 4-item, dot-separated qualifier mapping to a dict
        assert len(name.split('.')) == 4, _malformed(name, 'must be a 4-item, dot-separated qualifier')
        assert isinstance(mapping, dict), _malformed(name, 'must map to a dict')

        # specific cases for action and event
        if name.startswith('action.'):
            # make sure we have these keys in the root
            expected_keys = ['inputs', 'outputs', 'async_generated_event']
            _assert_lists_equivalent(mapping.keys(), expected_keys, name, 'must have exactly entries {}'.format(expected_keys))

            # make sure inputs and outputs are dicts
            assert isinstance(mapping['inputs'], dict), _malformed(name, '`inputs` must be a dict')
            assert isinstance(mapping['outputs'], dict), _malformed(name, '`outputs` must be a dict')

            # make sure async_generated_event is a string and a key to something else in the document
            assert isinstance(mapping['async_generated_event'], basestring), _malformed(name, '`async_generated_event` must be a string')
            assert mapping['async_generated_event'].startswith('event.'), _malformed(name, '`async_generated_event` must be an event')
            assert mapping['async_generated_event'] in document, _malformed(name, '`async_generated_event` must be an existing event')

            # makes sure fields are reset (can cause strange data integrity problems if accidentally omitted)
            input_fields = {}
            output_fields = {}

            # build inputs and outputs within a try block so we can provide better error messages
            try:
                for field_name, field_value in mapping['inputs'].iteritems():
                    input_fields[field_name] = _build_field(field_name, field_value)
                for field_name, field_value in mapping['outputs'].iteritems():
                    output_fields[field_name] = _build_field(field_name, field_value)
            except AssertionError as e:
                # wrap the assert error with the action name malformed text
                raise AssertionError(_malformed(name, str(e)))

            capabilities[name] = Action(name, input_fields, output_fields, mapping['async_generated_event'])
        elif name.startswith('event.'):
            # make sure we have these keys in an event
            expected_keys = ['outputs']
            _assert_lists_equivalent(mapping.keys(), expected_keys, name, 'must have exactly entries {}'.format(expected_keys))

            # make sure outputs is a dict
            assert isinstance(mapping['outputs'], dict), _malformed(name, '`outputs` must be a dict')

            # make sure fiels are reset (can cause strange data integrity problems if accidentally omitted)
            output_fields = {}

            # build outputs within a try block so we can provide better error messages
            try:
                for field_name, field_value in mapping['outputs'].iteritems():
                    output_fields[field_name] = _build_field(field_name, field_value)
            except AssertionError as e:
                # wrap the assert error with the action name malformed text
                raise AssertionError(_malformed(name, str(e)))

            capabilities[name] = Event(name, output_fields)

        else:
            raise AssertionError(_malformed(name, 'must be a `action` or `event`'))


def load():
    """ Master load function """

    # only run this once
    global _already_loaded
    if _already_loaded:
        return

    print 'Loading capabilities.'

    documents = _find_documents()
    master_document = _combine_documents(documents)
    _build_capabilities(master_document)

    # mark as loaded
    _already_loaded = True
