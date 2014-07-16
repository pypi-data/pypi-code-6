import sqlite3
import json

from taxonome.config import config
SP_FUZZY_THRESHOLD = float(config['main']['name-fuzzy-threshold'])
from taxonome.utils import qgram
from taxonome.tracker import noop_tracker

from .author import Authority
from .base import Name, Taxon
from .collection import TaxaResource

SCHEMA = """
PRAGMA foreign_keys = ON;

create table if not exists taxa (info text, distribution text,
                                 taxonid INTEGER PRIMARY KEY);

create table if not exists names (genus text, sp_epithet text, subnames text,
                                  authority text,
                                  is_accepted integer, taxonid integer,
                                  FOREIGN KEY(taxonid) REFERENCES taxa(taxonid)
                                 );

create index if not exists spnames_ix ON names (genus, sp_epithet);
create index if not exists taxnames_ix ON names (taxonid, is_accepted);

create table if not exists individuals (info text, taxonid integer,
                                        FOREIGN KEY(taxonid) REFERENCES taxa(taxonid)
                                       );

create index if not exists taxon_individuals_ix ON individuals (taxonid);
"""

def flatten_name(name):
    """Turn a name into a tuple ready to go into the database."""
    subnames = json.dumps(name.subnames)
    authority = json.dumps(name.authority.to_dict())
    return (name.g, name.sp, subnames, authority)

def rebuild_name(namerow):
    """Build a name from a database row."""
    g, sp, subnames, authority, *extra = namerow
    subnames = json.loads(subnames)
    n = Name([g, sp] +  subnames, authority=None)
    n.authority = Authority.from_dict(json.loads(authority))
    return n

def build_unqualified_name_str(namerow):
    """Build a plain string name from a database row."""
    g, sp, subnames, authority, *extra = namerow
    subnames = json.loads(subnames)
    return " ".join([g, sp] + [r+" "+sn for (r,sn) in subnames])

class SqliteTaxonDB(TaxaResource):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        # check_same_thread is not very well documented, but seems to allow us
        # to use the connection across threads.
        self.conn = sqlite3.connect(dbfile, check_same_thread=False)
        self.conn.executescript(SCHEMA)
        self.conn.commit()
    
    def add(self, taxon, commit=True):
        cur = self.conn.cursor()
        cur.execute('insert into taxa values (?, ?, NULL)',
                    (json.dumps(taxon.info), json.dumps(list(taxon.distribution))))
        
        # Sqlite docs guarantee that an INTEGER PRIMARY KEY is an alias for rowid,
        # so we can do this and save a lookup:
        taxonid = cur.lastrowid
        
        # Names
        cur.execute('insert into names values (?, ?, ?, ?, ?, ?)',
                        flatten_name(taxon.name) + (1, taxonid))
        for name in taxon.othernames:
            cur.execute('insert into names values (?, ?, ?, ?, ?, ?)',
                            flatten_name(name) + (0, taxonid))
        
        # Individuals
        for individual in taxon.individuals:
            cur.execute('insert into individuals values (?, ?)',
                        (json.dumps(individual), taxonid))

        if commit:
            self.conn.commit()
    
    def build(self, taxasource):
        for t in taxasource:
            self.add(t, commit=False)
        self.conn.commit()
    
    def resolve_name(self, name):
        if isinstance(name, Name):
            check_match = name.match_qualified
        else:
            # Unqualified name
            name = Name(name, authority=None)
            check_match = name.match_unqualified

        results = []
        for row in self.conn.execute('select * from names where genus=? and sp_epithet=?',
                                        (name.g, name.sp)):
            candidate = rebuild_name(row)
            if not check_match(candidate):
                continue
            
            taxonid = row[-1]
            if row[-2]:  # is_accepted
                candidate_acc = candidate
            else:
                accrow = self.conn.execute('select * from names where taxonid=? and is_accepted=1',
                                        (row[-1],)).fetchone()
                candidate_acc = rebuild_name(accrow)
            
            results.append((candidate, candidate_acc, taxonid))
        
        return results
    
    def __contains__(self, name):
        if isinstance(name, Taxon):
            return name.name in self
        return bool(self.resolve_name(name))

    def __len__(self):
        cur = self.conn.execute('select count(*) from taxa')
        return cur.fetchone()[0]
    
    def fuzzy_resolve_name(self, name, tracker=noop_tracker):
        if isinstance(name, Name):
            check_auth = True
            rawname = name.plain
        else:
            # Unqualified name
            rawname = name
            name = Name(name, authority=None)
            check_auth = False
        
        # Fuzzy matching - check rows where either the genus or the species matches
        target_qgrams = qgram.qgrams(rawname)
        candidates = [] # (score, row)
        for row in self.conn.execute('select * from names where genus=? or sp_epithet=?',
                                        (name.g, name.sp)):
            candidate_qgrams = qgram.qgrams(build_unqualified_name_str(row))
            score = qgram.overlap(candidate_qgrams, target_qgrams)
            if score > SP_FUZZY_THRESHOLD:
                candidates.append((score, row))
        
        if not candidates:
            return []
        
        # Only check the names with the best fuzzy match
        candidates.sort(key=lambda x: x[0], reverse=True)
        bestscore = candidates[0][0]
        
        # Check authorities, find accepted names, and build results
        results = []
        for score, row in candidates:
            if score < bestscore:
                break
            candidate = rebuild_name(row)
            if check_auth and not candidate.authority==name.authority:
                continue
            
            taxonid = row[-1]
            if row[-2]:  # is_accepted
                candidate_acc = candidate
            else:
                accrow = self.conn.execute('select * from names where taxonid=? and is_accepted=1',
                                        (row[-1],)).fetchone()
                candidate_acc = rebuild_name(accrow)
            
            results.append((candidate, candidate_acc, taxonid))
        
        return results

    def __iter__(self):
        # This is not very efficient, but it's used to get a sample of rows
        # to display in the GUI. It would also be used if someone built one
        # SqliteTaxonDB from another, but that doesn't seem too important.
        cur = self.conn.execute('select taxonid from taxa')
        for tid, in cur:
            yield self.get_by_id(tid)
    
    def get_by_id(self, taxonid):
        infoj, distribj = self.conn.execute('select info, distribution from taxa where taxonid=?', (taxonid,)).fetchone()
        namerows = self.conn.execute('select * from names where taxonid=?', (taxonid,))
        othernames = set()
        for row in namerows:
            name = rebuild_name(row)
            if row[-2]: # accepted name
                accname = name
            else:
                othernames.add(name)
        
        t = Taxon(accname)
        t.othernames = othernames
        t.info = json.loads(infoj)
        t.distribution = set(json.loads(distribj))
        
        individuals = self.conn.execute('select * from individuals where taxonid=?', (taxonid,))
        t.individuals = [json.loads(r[0]) for r in individuals]
        
        return t
