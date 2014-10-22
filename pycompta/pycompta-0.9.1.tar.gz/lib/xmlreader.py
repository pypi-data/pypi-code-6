# -*- coding: utf-8 -*-

"""
PyCompta

Ce module lit les écritures aux format XML.
"""

__revision__ = "$Id: xmlreader.py,v 1.15 2005-01-03 16:10:37 jphc Exp $"

from xml.sax import make_parser #, SAXException
from xml.sax.handler import ContentHandler
from mx import DateTime

from pycompta.lib.entities import Ecriture, Immobilisation, ExceptionEcriture

def _montant(montant) :
    """
    remplace , par . et supprime espaces. transforme en un entier qui représente
    le montant en centimes
    """
    montant = montant.replace(',','.').replace(' ','')
    montant = int(round(100*float(montant)))
    return montant

class EcrituresContentHandler(ContentHandler):
    """
    SAX Content Handler qui produit une liste d'objets Ecriture.
    """

    def __init__(self):
        """
        elist : liste des écritures renvoyée après lecture du fichier
        """
        self.elist = []
        self.buffer = u''
        self.e = None
        self.ref = None
        self.coherent = False
        self.attrs = None

    def startElement(self, name, attrs):
        """
        See SAX ContentHandler interface
        """
        if name == 'ecritures' :
            pass
        elif name == 'ecriture' :
            try:
                date = DateTime.Date(*[int(x) for x in attrs['date'].split('-')])
                self.coherent = True
            except KeyError :
                date = DateTime.Date(1900,1,1) # fixme?
                self.coherent = False
            self.e = Ecriture( date )
            if attrs.has_key('type'):
                self.e.type = attrs['type']
        elif self.e == None :
            raise Exception("Element <%s> should be inside a <ecriture>"
                            % name.encode("ascii",  "backslashreplace"))
        elif name == 'credit' :
            self.e.add_credit( attrs['compte'], _montant(attrs['montant']) )
        elif name == 'debit' :
            self.e.add_debit( attrs['compte'], _montant(attrs['montant']) )
        elif name in ['libelle', 'reglement', 'reference'] :
            self.buffer = u''
        elif name in ['ref'] :
            self.buffer = u''
            try:
                self.ref = (attrs['type'], attrs['id'])
            except KeyError :
                self.ref = None
        elif name == 'analyse' :
            self.buffer = u''
            self.attrs = attrs
        else :
            raise Exception("Unexpected element: <%s>"
                            % name.encode("ascii", "backslashreplace"))

    def endElement(self, name):
        """
        See SAX ContentHandler interface
        """
        if name == 'ecritures' :
            pass
        elif name == 'ecriture' :
            if not self.coherent:
                raise ExceptionEcriture("'Ecriture' inconsistent: %s" % self.e)
            if not self.e.est_equilibre() :
                raise ExceptionEcriture("'Ecriture' unbalanced: %s" % self.e)
            self.elist.append(self.e)
            self.e = None
        elif name == 'libelle' :
            self.e.libelle = self.buffer
        elif name == 'reglement' :
            self.e.reglement = self.buffer
        elif name == 'reference' :
            self.e.reference = self.buffer
        elif name in ['credit', 'debit'] :
            pass
        elif name in ['ref'] :
            if self.ref :
                self.ref += (self.buffer,)
                self.e.refs.append( self.ref )
        elif name == 'analyse' :
            self.e.analyse[self.attrs['type']] = self.buffer
            self.attrs = None
        else :
            raise Exception("Unexpected element: </%s>"
                            % name.encode("ascii", "backslashreplace"))

    def characters(self, chars):
        """
        See SAX ContentHandler interface
        """
        self.buffer = self.buffer + chars

def get_ecritures(fichier) :
    """
    Lit un fichier XML d'écritures et renvoie une liste d'objets Ecriture.
    """
    handler = EcrituresContentHandler()
    parser = make_parser(["xml.sax.drivers2.drv_xmlproc"])
    parser.setContentHandler(handler)
    try:
        parser.parse(fichier)
    except Exception, e :
        import sys
        from traceback import format_exc
        sys.stderr.write("\n\n***** Error at line %s in file %s\n\n%s"
                         % (parser.getLineNumber(),
                            parser.getSystemId().encode('ascii', "backslashreplace"),
                            format_exc()))
        sys.exit(1)
    return handler.elist[:]

# Immobilisations ##############################################################

class ImmobilisationsContentHandler(ContentHandler):
    """
    SAX Content Handler qui produit une liste d'objets Immobilisation
    """

    def __init__(self):
        """
        immolist: liste des immobilisations renvoyée après lecture
        """
        self.immolist = []
        self.buffer = u''
        self.immo = None
        self.ref = None

    def startElement(self, name, attrs):
        """
        See SAX ContentHandler interface
        """
        if name == 'immobilisations' :
            pass
        elif name == 'immobilisation' :
            entree = DateTime.Date(*[int(x) for x in attrs['entree'].split('-')])
            if attrs.has_key('sortie'):
                sortie = DateTime.Date(*[int(x) for x in attrs['sortie'].split('-')])
            else:
                sortie = None
            self.immo = Immobilisation( u'', entree, sortie,
                                        int(attrs['duree']), attrs['compte'],
                                        _montant(attrs['montant']) )
        elif self.immo == None :
            raise Exception("Element <%s> should be inside a <immobilisation>"
                            % name.encode("ascii", "backslashreplace"))
        elif name in ['libelle', 'groupe'] :
            self.buffer = u''
        else :
            raise Exception("Unexpected element: <%s>"
                            % name.encode("ascii", "backslashreplace"))

    def endElement(self, name):
        """
        See SAX ContentHandler interface
        """
        if name == 'immobilisations' :
            pass
        elif name == 'immobilisation' :
            self.immolist.append(self.immo)
            self.immo = None
        elif name == 'libelle' :
            self.immo.libelle = self.buffer
        elif name == 'groupe' :
            self.immo.groupe = self.buffer
        else :
            raise Exception("Unexpected element: <%s>"
                            % name.encode("ascii", "backslashreplace"))

    def characters(self, chars):
        """
        See SAX ContentHandler interface
        """
        self.buffer = self.buffer + chars

def get_immobilisations(fichier) :
    """
    Lit un fichier XML d'immobilisations et renvoie une liste d'objets Immobilisation.
    """
    handler = ImmobilisationsContentHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(fichier)
    return handler.immolist[:]
