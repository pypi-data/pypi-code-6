import pytest
from .. import locale


def test_localized():

    localized = locale.Localized({
        'id': 'cake',
        'name': {
            'en': 'Delicious cake',
            'de': 'Leckerer Kuchen'
        },
        'description': {
            'en': 'You know.. cake!'
        }
    }, languages=['en', 'de'], language='de')

    assert localized.default_language == 'en'
    assert localized.language == 'de'

    assert localized.id == 'cake'
    assert localized.name == 'Leckerer Kuchen'

    assert localized.description == 'You know.. cake!'

    with pytest.raises(AttributeError):
        localized.unknown_attribute
