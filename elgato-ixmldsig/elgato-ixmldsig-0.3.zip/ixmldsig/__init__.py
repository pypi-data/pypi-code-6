# -*- coding: utf-8 -*-
__author__ = 'dsedad'

from lxml import etree as et
from uuid import uuid4
from decimal import Decimal
import datetime
from tzlocal import get_localzone

def convert_dn(dnstr):
    """
     Convert DN X509 string to dictionary
     example input: 'CN=4200040010007, O="\\"PING\\" d.o.o. Sarajevo", L=Sarajevo, ST=FBiH, C=BA'
    """
    def unquote(str):
        import re
        str = str.decode('string-escape')
        matched = re.match(r'^\"(.*)\"$', str)
        if matched:
            return matched.group(1)
        else:
            return str

    dn1 = dnstr.split(',')
    result = {}
    for elem in dn1:
        #elem = elem.strip()
        eq_pos = elem.index('=')
        result[elem[:eq_pos]]=unquote(elem[eq_pos+1:])
    return result

class IXmlDSig(object):
    """
    Sign invoice file or single invoice.
    """
    def __init__(self, sign_fn=None, verify_fn=None, get_dn=None, cert_file=None, tz = get_localzone()):
        """
        sign_fn: xmldsig signature function
        verify_fn: xmldsig signature function
        tz: timezone
        """
        self.sign_fn = sign_fn
        self.verify_fn = verify_fn
        self.get_dn = get_dn
        self.init_summary()
        self.tz = tz
        if cert_file:
            self.sign_dn = self.get_subjectDN(cert_file)

    def init_summary(self):
        self.__last_dn = None
        self.uuid_list = []
        self.inv_sum = Decimal(0)
        self.inv_cnt = 0
        self.last_uuid = None
        self.verify_exceptions = []
        self.timestamp = None
        self.summary = {}

    def verify_dn(self, ent_id, ent_name):
        assert ent_id != None, u"Ne postoji id tag"
        assert self.sign_dn['CN'] == ent_id.text, u"Pogresan id preduzeca: \"{}\"".format(ent_id.text)

        assert ent_name != None, u"Ne postoji name tag"
        assert self.sign_dn['O'] == ent_name.text, u"Pogresan naziv preduzeca: \"{}\"".format(ent_name.text)

    def get_subjectDN(self, cert_file):
        pem_cert_file = open(cert_file, 'r')
        cert = pem_cert_file.read()
        pem_cert_file.close()

        return convert_dn(self.get_dn(cert))

    def sign(self, invoice):
        """
         Sign invoice xml and return signed xml (as string)
        """
        if type(invoice) in (type(unicode()), type(str())):
            invoice = et.fromstring(invoice)

        uuid = et.SubElement(invoice, "uuid")
        uuid.text = str(uuid4())

        timestamp = et.SubElement(invoice, "timestamp")
        timestamp.text = str(datetime.datetime.now(self.tz).isoformat())

        self.last_uuid = uuid.text

        # Add uuid to list of uuids
        self.uuid_list.append(uuid.text)

        # Find amount, ent_id, ent_name
        amount = invoice.find('header').find('pay').find('amount')
        ent_id = invoice.find("header").find("payee").find("id")
        ent_name = invoice.find("header").find("payee").find("short_name")

        # Check DN
        self.verify_dn(ent_id, ent_name)

        # Calc sum & count
        self.inv_sum = self.inv_sum + Decimal(amount.text)
        self.inv_cnt = self.inv_cnt + 1

        # Sign and write
        invoice_str = et.tostring(invoice, encoding='utf8', method='xml', pretty_print = True)
        return self.sign_fn(invoice_str).encode("utf-8")

    def verify(self, invoice):
        """
         Verify invoice xml
        """
        if type(invoice) in (type(unicode()), type(str())):
            invoice = et.fromstring(invoice)
        amount = invoice.find('header').find('pay').find('amount')

        # Calc sum & count
        self.inv_sum = self.inv_sum + Decimal(amount.text)
        self.inv_cnt = self.inv_cnt + 1

        # Populate uuid in uuid_list
        uuid_tag = invoice.find('uuid')
        assert uuid_tag != None, u"Invoice ne posjeduje uuid tag"

        uuid_tag = uuid_tag.text
        self.uuid_list.append(uuid_tag)

        # Verify invoice signature
        invoice_str = unicode(et.tostring(invoice))
        try:
            dn_str = self.verify_fn(invoice_str, None)
            assert dn_str == self.__last_dn or self.__last_dn == None, u"Greska! Postoje razliciti DN-ovi u invoice datoteci"
            self.__last_dn = dn_str

            dn = convert_dn(dn_str)

            ent_id = invoice.find("header").find("payee").find("id")
            assert ent_id != None, u"Ne postoji id tag"
            assert dn['CN'] == ent_id.text, u"Pogresan id preduzeca: \"{}\"".format(ent_id.text)

            ent_name = invoice.find("header").find("payee").find("name")
            assert ent_name != None, u"Ne postoji name tag"
            assert dn['O'] == ent_name.text, u"Pogresan naziv preduzeca: \"{}\"".format(ent_name.text)

            return True
        except Exception as e:
            self.verify_exceptions.append({"uuid": uuid_tag, "exception": e})
            return False

    def sign_summary(self):
        summary = et.Element("summary")
        count = et.SubElement(summary, "count")
        count.text = str(self.inv_cnt)
        sum = et.SubElement(summary, "sum")
        sum.text = str(self.inv_sum)
        uuids = et.SubElement(summary, "uuids")
        uuids.text = ','.join(self.uuid_list)
        timestamp = et.SubElement(summary, "timestamp")
        timestamp.text = str(datetime.datetime.now(self.tz).isoformat())

        # Sign summary
        summary_src = et.tostring(summary, encoding='utf8', pretty_print = True)
        summary_signed = self.sign_fn(summary_src)
        self.summary = {"sum": sum.text, "cnt": count.text, "uuids": uuids.text, "timestamp": timestamp.text}
        return summary_signed.encode("utf-8")

    def verify_summary(self, summary):
        """
        Verify invoices summary
        """
        if type(summary) in (type(unicode()), type(str())):
            summary = et.fromstring(summary)

        sum = Decimal(summary.find('sum').text)
        count = int(summary.find('count').text)
        uuids = summary.find('uuids').text
        timestamp = summary.find('timestamp').text

        self.summary = {"sum": sum, "cnt": count, "uuids": uuids, "timestamp": timestamp}

        assert sum == self.inv_sum, u"PROBLEM: Potpisana suma {} <> sume racuna {}".format(sum, self.inv_sum)
        assert count == self.inv_cnt, u"PROBLEM: Potpisani broj racuna {} <> broja racuna {}".format(count, self.inv_cnt)
        assert uuids == ",".join(self.uuid_list), u"PROBLEM: UUID racuna ne odgovaraju onim u kontrolnom bloku"

        summary_str = unicode(et.tostring(summary))
        try:
            dn_str = self.verify_fn(summary_str, None)
            assert dn_str == self.__last_dn or self.__last_dn == None, \
                u"Greska! Postoje razliciti DN-ovi u invoice datoteci"
            self.__last_dn = dn_str

        except Exception as e:
            raise e

        return True

