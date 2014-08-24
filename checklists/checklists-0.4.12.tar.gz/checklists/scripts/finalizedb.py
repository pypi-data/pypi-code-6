"""Finalize the populating of the database.

When the load_taxonomy script was run the Species table was populated with
the complete list of species used by eBird. Then the scripts avibase_names and
load_species_names were used to load the common names for the subset of
species needed for a given application. For most locations that will only be
around 1000 species so the other 13000 or so won't be needed. Managing the
entries in the Species table is a regular admin task so it's better to delete
all the records that won't be used. Fortunately that's easy to do. When the
load_taxonomy script ran it set the include flag on each Species to False.
Then the load_species_names set it to True for each Species where a common
name was added. So finalizing the Species table is simply a matter of deleting
all the records where include remains False.
"""

from checklists.models import Species

def run():
    Species.objects.filter(include=False).delete()
