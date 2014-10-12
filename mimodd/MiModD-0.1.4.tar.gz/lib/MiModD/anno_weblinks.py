# VERSION
from . import mimodd_base
version = mimodd_base.Version((0, 0, 2))

# new in 0,0,2:
# support for yeast genome

species_synonyms = {
                    # Worm
                    '6239' : 6239,
                    'Caenorhabditis elegans' : 6239,
                    'C. elegans' : 6239,
                    'C.elegans' : 6239,

                    # Yeast
                    '1196866' : 1196866,
                    'Saccharomyces cerevisiae' : 1196866,
                    'S. cerevisiae' : 1196866,
                    'S.cerevisiae' : 1196866,

                    # Synechocystis
                    '1148' : 1148,
                    'Synechocystis sp. PCC 6803' : 1148,
                    'Synechocystis PCC 6803' : 1148,
                    'Synechocystis' : 1148,
                    'PCC 6803' : 1148
                    }
links = {
        6239 :
            {
            'gene' : 'http://www.wormbase.org/species/c_elegans/gene/{gene}',
            'pos'  : 'http://www.wormbase.org/tools/genome/gbrowse/c_elegans_PRJNA13758?name={chromosome}:{start}..{stop}'
            },
        1196866 :
            {
            'gene' : 'http://www.yeastgenome.org/cgi-bin/locus.fpl?locus={gene}',
            'pos'  : 'http://browse.yeastgenome.org/fgb2/gbrowse/scgenome/?name={chromosome}:{start}..{stop}'
            },
        1148 :
            {
            'gene' : 'http://genome.microbedb.jp/cyanobase/Synechocystis/genes/search?q={gene}&keyword=search&m=gene_symbol%2Cgi_gname%2Cdefinition%2Cgi_pname',
            'pos'  : 'http://genome.microbedb.jp/cgi-bin/gbrowse/Synechocystis/?name={chromosome}:{start}..{stop}'
            }
        }
