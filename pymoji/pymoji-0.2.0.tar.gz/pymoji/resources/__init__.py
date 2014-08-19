# -*- encoding: utf-8 -*-


def load_soft_bank_resources():
    from pymoji.resources.soft_bank import SOFT_BANK_CONFIG
    return SOFT_BANK_CONFIG


def load_moji_resources():
    from pymoji.resources.nature import NATURE_MOJI_RESOURCES
    from pymoji.resources.objects import OBJECTS_MOJI_RESOURCES
    from pymoji.resources.people import PEOPLE_MOJI_RESOURCES
    from pymoji.resources.places import PLACES_MOJI_RESOURCES
    from pymoji.resources.symbols import SYMBOLS_MOJI_RESOURCES
    return dict(
            NATURE_MOJI_RESOURCES.items() +
            OBJECTS_MOJI_RESOURCES.items() +
            PEOPLE_MOJI_RESOURCES.items() +
            PLACES_MOJI_RESOURCES.items() +
            SYMBOLS_MOJI_RESOURCES.items()
    )
