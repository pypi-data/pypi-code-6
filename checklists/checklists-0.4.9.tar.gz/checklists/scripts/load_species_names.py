"""Load the Species common names for a given language."""

from django.db import transaction

from checklists.models import Species

from utils import get_data


@transaction.commit_on_success
def run(*args):
    for filename in args:
        table = get_data(filename)
        for index in range(1, len(table)):
            row = table[index]
            species = Species.objects.get(scientific_name=row[0])
            species.include = True
            setattr(species, table[0][1], row[1])
            species.save()
