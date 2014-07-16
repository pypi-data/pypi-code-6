# -*- coding: utf-8 -*-
"""This module fetches information from the World Register of Marine Species
webservice.

http://www.marinespecies.org/

Technical note: tested using the Python 3 patches for suds available at
https://bitbucket.org/bernh/suds-python-3-patches/wiki/Home
"""
from suds.client import Client

from taxonome import Name, Taxon
from taxonome.taxa.collection import TaxaResource, TaxonSet

WSDL_URL = "http://www.marinespecies.org/aphia.php?p=soap&wsdl=1"

def _make_taxon(record):
    tax = Taxon(record.valid_name, record.valid_authority)
    
    if record.status == "accepted":
        tax.lsid = record.lsid
        tax.url = str(record.url)
    else:
        syn = Name(record.scientificname, record.authority)
        tax.othernames.add(syn)

    return tax

class WoRMSTaxaResource(TaxaResource):
    def __init__(self):
        super().__init__()
        self.service = Client(WSDL_URL)
        self.cache_by_id = {}
    
    def get_by_id(self, aphia_id):
        tax = self.cache_by_id[aphia_id]

        if tax.url is None:
            # Cached record is from a synonym - get the main record
            tax = self.cache_by_id[aphia_id] = \
                _make_taxon(self.service.service.getAphiaRecordByID(aphia_id))

        for synrecord in self.service.service.getAphiaSynonymsByID(aphia_id):
            syn = Name(synrecord.scientificname, synrecord.authority)
            tax.othernames.add(syn)
        
        return tax
    
    def resolve_name(self, key):
        if isinstance(key, Name):
            return [(n, an, tid) for n, an, tid in self.resolve_name(key.plain) \
                                            if n.authority==key.authority]
        
        names = []
        for record in self.service.service.getAphiaRecords(key):
            n = Name(record.scientificname, record.authority)
            an = Name(record.valid_name, record.valid_authority)
            self.cache_by_id[record.valid_AphiaID] = _make_taxon(record)
            names.append((n, an, record.valid_AphiaID))
        return names

_instance = None
def _get_instance():
    global _instance
    if not _instance:
        _instance = WoRMSTaxaResource()
    return _instance

def select(*args, **kwargs):
    return _get_instance().select(*args, **kwargs)

def resolve_name(*args, **kwargs):
    return _get_instance().resolve_name(*args, **kwargs)
