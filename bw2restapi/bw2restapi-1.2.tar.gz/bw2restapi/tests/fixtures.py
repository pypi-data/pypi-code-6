biosphere_data = {
    ("biosphere", "1"): {
        'categories': ['things'],
        'exchanges': [],
        'name': 'an emission',
        'unit': 'kg'
        },
    ("biosphere", "2"): {
        'categories': ['things'],
        'exchanges': [],
        'name': 'another emission',
        'unit': 'kg'
        },
}

food_data = {
    ("food", "1"): {
        'categories': ['stuff', 'meals'],
        'exchanges': [{
            'amount': 0.5,
            'input': ('food', "2"),
            'type': 'technosphere',
            'uncertainty type': 0},
            {'amount': 0.05,
            'input': ('biosphere', "1"),
            'type': 'biosphere',
            'uncertainty type': 0}],
        'location': 'CA',
        'name': 'lunch',
        'unit': 'kg'
        },
    ("food", "2"): {
        'categories': ['stuff', 'meals'],
        'exchanges': [{
            'amount': 0.25,
            'input': ('food', "1"),
            'type': 'technosphere',
            'uncertainty type': 0},
            {'amount': 0.15,
            'input': ('biosphere', "2"),
            'type': 'biosphere',
            'uncertainty type': 0}],
        'location': 'CH',
        'name': 'dinner',
        'unit': 'kg'
        },
    }
