# -*- coding: utf-8 -*-
"""
Работа с файлами лицензий
"""


class LicenseException(Exception):
    pass


def get_project_lic_data():
    from django.conf import settings

    try:
        lic_filename = settings.LIC_KEY_FILE
    except AttributeError:
        raise LicenseException('`LIC_KEY_FILE` not defined in django '
            'settings file')

    try:
        public_key = settings.PUBLIC_KEY
    except AttributeError:
        raise LicenseException('`PUBLIC_KEY` not defined in django '
            'settings file')

    return get_lic_data(lic_filename, public_key)


def get_lic_data(xml_file, public_key):
    '''
    Функция читает файл лицензии, и если он корректен,
    возвращает словарь, содержащий данные о лицензии.
    Если файл лицензии некорректен - возвращается None
    @xml_file - имя файла лицензии
    @public_key - публичный ключ
    '''

    import os
    import rsa
    import re
    import copy
    import hashlib
    import htmlentitydefs
    import datetime
    import binascii
    from lxml import etree
    from rsa import pkcs1, transform
    from rsa.pkcs1 import VerificationError

    public_key = rsa.key.PublicKey.load_pkcs1_openssl_pem(public_key)

    NS = {
        'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }
    TRANSFORM_ENVELOPED_SIGNATURE = (
        'http://www.w3.org/2000/09/xmldsig#enveloped-signature'
    )
    TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS = (
        'http://www.w3.org/2001/10/xml-exc-c14n#WithComments'
    )
    TRANSFORM_C14N_EXCLUSIVE = 'http://www.w3.org/2001/10/xml-exc-c14n'
    TRANSFORM_C14N_INCLUSIVE = 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'

    _id_attributes = ['ID', 'id']

    def _get_by_id(t, id_v):
        for id_a in _id_attributes:
            elts = t.xpath("//*[@%s='%s']" % (id_a, id_v))
            if elts is not None and len(elts) > 0:
                return elts[0]
        return None

    def b64d(s):
        return s.decode('base64')

    def b64e(s):
        if type(s) in (int, long):
            s = transform.int2bytes(s)
        return s.encode('base64').replace('\n', '')

    def _alg(elt):
        uri = elt.get('Algorithm', None)
        if uri is None:
            return None
        else:
            return uri.rstrip('#')

    def _digest(str, hash_alg):
        h = getattr(hashlib, hash_alg)()
        h.update(str)
        digest = b64e(h.digest())
        return digest

    def _delete_elt(elt):
        if elt.getparent() is None:
            raise ValueError("Cannot delete root")
        if elt.tail is not None:
            p = elt.getprevious()
            if p is not None:
                if p.tail is None:
                    p.tail = ''
                p.tail += elt.tail
            else:
                up = elt.getparent()
                if up is None:
                    raise ValueError("Signature has no parent")
                if up.text is None:
                    up.text = ''
                up.text += elt.tail
        elt.getparent().remove(elt)

    def _remove_child_comments(t):
        root = t.getroot()
        for c in root.iter():
            if c.tag is etree.Comment or c.tag is etree.PI:
                _delete_elt(c)
        return t

    def _unescape(text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    if text not in ('&amp;', '&lt;', '&gt;'):
                        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text  # leave as is
        return re.sub("&#?\w+;", fixup, text)

    def _c14n(t, exclusive, with_comments, inclusive_prefix_list=None):
        cxml = etree.tostring(
            t, method="c14n",
            exclusive=exclusive,
            with_comments=with_comments
        )
        u = _unescape(cxml.decode("utf8", 'replace')).encode("utf8").strip()
        if u[0] != '<':
            raise ValueError("C14N buffer doesn't start with '<'")
        if u[-1] != '>':
            raise ValueError("C14N buffer doesn't end with '>'")
        return u

    def _enveloped_signature(t):
        sig = t.find(".//{%s}Signature" % NS['ds'])
        _delete_elt(sig)
        res = etree.tostring(t)
        u = _unescape(res.decode("utf8", 'replace')).encode("utf8").strip()
        return u

    def _transform(uri, t, tr=None):
        if uri == TRANSFORM_ENVELOPED_SIGNATURE:
            return _enveloped_signature(t)

        if uri in (
            TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS,
            TRANSFORM_C14N_EXCLUSIVE
        ):
            nslist = None
            if tr is not None:
                elt = tr.find(
                    ".//{%s}InclusiveNamespaces"
                    % 'http://www.w3.org/2001/10/xml-exc-c14n#')
                if elt is not None:
                    nslist = elt.get('PrefixList', '').split()
            return _c14n(
                t, exclusive=True,
                with_comments=(uri == TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS),
                inclusive_prefix_list=nslist
            )

        if uri == TRANSFORM_C14N_INCLUSIVE:
            return _c14n(t, exclusive=False, with_comments=False)

        raise ValueError("unknown or unimplemented transform %s" % uri)

    def _process_references(t, sig=None):
        if sig is None:
            sig = t.find(".//{%s}Signature" % NS['ds'])

        for ref in sig.findall(".//{%s}Reference" % NS['ds']):
            obj = None
            uri = ref.get('URI', None)
            if uri is None or uri == '#' or uri == '':
                ct = _remove_child_comments(copy.deepcopy(t))
                obj = ct.getroot()
            elif uri.startswith('#'):
                ct = copy.deepcopy(t)
                obj = _get_by_id(ct, uri[1:])
            else:
                raise ValueError("Unknown reference %s" % uri)

            if obj is None:
                raise ValueError(
                    "Unable to dereference Reference URI='%s'" % uri)

            for tr in ref.findall(".//{%s}Transform" % NS['ds']):
                obj = _transform(_alg(tr), obj, tr)

            dm = ref.find(".//{%s}DigestMethod" % NS['ds'])
            if dm is None:
                raise ValueError("Unable to find DigestMethod")
            hash_alg = _alg(dm).split("#")[1]
            digest = _digest(obj, hash_alg)
            dv = ref.find(".//{%s}DigestValue" % NS['ds'])
            dv.text = digest

    def check_lic_file(xml_file):
        try:
            doc = etree.parse(xml_file)
            sig = doc.getroot().find(".//{%s}Signature" % NS['ds'])
            if sig is None:
                raise ValueError("Is not signed xml!")
            else:
                _process_references(doc, sig)
                si = sig.find(".//{%s}SignedInfo" % NS['ds'])
                cm = si.find(".//{%s}CanonicalizationMethod" % NS['ds'])
                cm_alg = _alg(cm)
                if cm is None or cm_alg is None:
                    raise ValueError("No CanonicalizationMethod")
                sic = _transform(cm_alg, si)
                unsigned_xml = sic.replace(' xmlns=""', '')
                sve = sig.find(".//{%s}SignatureValue" % NS['ds'])
                signature = b64d(sve.text)
                return pkcs1.verify(unsigned_xml, signature, public_key)
        except (ValueError, binascii.Error):
            return False

    # ------------------------------------------------
    try:
        check_lic_file(xml_file)
    except VerificationError as err:
        raise LicenseException("License verification error: %s" % err)

    data = {}
    if not os.access(xml_file, os.R_OK):
        raise LicenseException("Read permission denied: %s" % xml_file)
    doc = etree.parse(xml_file)
    if doc is None or doc.getroot() is None:
        if doc is not None:
            doc.freeDoc()
        return data
    element = doc.find('//LicenceData')
    for e in element:
        tag = e.tag

        if tag in ('startdate', 'enddate'):
            data[tag] = datetime.datetime.strptime(e.text, '%d.%m.%Y')
        else:
            data[tag] = e.text
    return data
