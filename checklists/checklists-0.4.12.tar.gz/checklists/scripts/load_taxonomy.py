"""Initialize the database with data for the SpeciesGroup and Species models.

The database must be empty otherwise an Integrity error will be raised. The
table is not cleared first in case the script is run inadvertently on an
existing database.
"""

from django.db import transaction

from checklists import get_data_path
from checklists.models import SpeciesGroup, Species, Rank

from utils import get_data, get_languages


@transaction.commit_on_success
def run():
    table = get_data(get_data_path('taxonomy.csv'))
    group_id = species_id = 1
    for index in range(1, len(table)):
        row = table[index]
        kwargs = {
            'id': group_id,
            'order': row[5],
            'family': row[6].split('(')[0].strip(),
            'genus': row[3].split(' ')[0],
        }
        if 'en' in get_languages() and '(' in row[6]:
            kwargs['name_en'] = row[6].split('(')[1][:-1].strip()
        group, created = SpeciesGroup.objects.get_or_create(**kwargs)
        if created:
            group_id += 1

        Species.objects.create(
            id=species_id,
            include=False,
            order=species_id,
            rank=Rank.objects.get(slug=row[1]),
            group=group,
            standard_name=row[4],
            scientific_name=row[3],
        )
        if created:
            species_id += 1
