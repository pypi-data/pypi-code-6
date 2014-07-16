from taxonome.taxa import sqlitets

from .test_taxa import LiquoriceTest

class SqliteLiquoriceTest(LiquoriceTest):
    taxon_collection_class = sqlitets.SqliteTaxonDB
    taxon_collection_args = (':memory:',)
