#coding:utf-8

# Основано на https://github.com/andrewdyates/xmldsig

import copy
import hashlib
import re
import htmlentitydefs
from lxml import etree
from lxml.builder import ElementMaker
from rsa import pkcs1, transform

NS = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}
DS = ElementMaker(namespace=NS['ds'])

TRANSFORM_ENVELOPED_SIGNATURE = 'http://www.w3.org/2000/09/xmldsig#enveloped-signature'
TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS = 'http://www.w3.org/2001/10/xml-exc-c14n#WithComments'
TRANSFORM_C14N_EXCLUSIVE = 'http://www.w3.org/2001/10/xml-exc-c14n'
TRANSFORM_C14N_INCLUSIVE = 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'

ALGORITHM_DIGEST_SHA1 = "http://www.w3.org/2000/09/xmldsig#sha1"
ALGORITHM_SIGNATURE_RSA_SHA1 = "http://www.w3.org/2000/09/xmldsig#rsa-sha1"


class XMLSigException(Exception):
    pass


def _delete_elt(elt):
    assert elt.getparent() is not None, XMLSigException("Cannot delete root")
    if elt.tail is not None:
        p = elt.getprevious()
        if p is not None:
            if p.tail is None:
                p.tail = ''
            p.tail += elt.tail
        else:
            up = elt.getparent()
            assert up is not None, XMLSigException("Signature has no parent")
            if up.text is None:
                up.text = ''
            up.text += elt.tail
    elt.getparent().remove(elt)


def _enveloped_signature(t):
    sig = t.find(".//{%s}Signature" % NS['ds'])
    #sig = t.find(".//Signature")
    _delete_elt(sig)
    res = etree.tostring(t)
    u = _unescape(res.decode("utf8", 'replace')).encode("utf8").strip()
    return u


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

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
                if not text in ('&amp;', '&lt;', '&gt;'):
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def _c14n(t, exclusive, with_comments, inclusive_prefix_list=None):
    if inclusive_prefix_list:
        # работает только с lxml > 3.0
        cxml = etree.tostring(t, method="c14n", exclusive=exclusive, with_comments=with_comments,
                              inclusive_ns_prefixes=inclusive_prefix_list)
    else:
        cxml = etree.tostring(t, method="c14n", exclusive=exclusive, with_comments=with_comments)
    u = _unescape(cxml.decode("utf8", 'replace')).encode("utf8").strip()
    assert u[0] == '<', XMLSigException('C14N buffer doesn\'t start with \'<\'')
    assert u[-1] == '>', XMLSigException('C14N buffer doesn\'t end with \'>\'')
    return u


def _transform(uri, t, tr=None):
    if uri == TRANSFORM_ENVELOPED_SIGNATURE:
        return _enveloped_signature(t)

    if uri == TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS:
        nslist = None
        if tr is not None:
            elt = tr.find(".//{%s}InclusiveNamespaces" % 'http://www.w3.org/2001/10/xml-exc-c14n#')
            #elt = tr.find(".//InclusiveNamespaces")
            if elt is not None:
                nslist = elt.get('PrefixList', '').split()
        return _c14n(t, exclusive=True, with_comments=True, inclusive_prefix_list=nslist)

    if uri == TRANSFORM_C14N_EXCLUSIVE:
        nslist = None
        if tr is not None:
            elt = tr.find(".//{%s}InclusiveNamespaces" % 'http://www.w3.org/2001/10/xml-exc-c14n#')
            #elt = tr.find(".//InclusiveNamespaces")
            if elt is not None:
                nslist = elt.get('PrefixList', '').split()
        return _c14n(t, exclusive=True, with_comments=False, inclusive_prefix_list=nslist)

    if uri == TRANSFORM_C14N_INCLUSIVE:
        return _c14n(t, exclusive=False, with_comments=False)

    raise XMLSigException("unknown or unimplemented transform %s" % uri)


# TODO - support transforms with arguments
def _signed_info_transforms(transforms):
    ts = [DS.Transform(Algorithm=t) for t in transforms]
    return DS.Transforms(*ts)


# standard enveloped rsa-sha1 signature
def _enveloped_signature_template(c14n_method, digest_alg, transforms):
    return DS.Signature(
        DS.SignedInfo(
            DS.CanonicalizationMethod(Algorithm=c14n_method),
            DS.SignatureMethod(Algorithm=ALGORITHM_SIGNATURE_RSA_SHA1),
            DS.Reference(
                _signed_info_transforms(transforms),
                DS.DigestMethod(Algorithm=digest_alg),
                DS.DigestValue(),
                URI=""
            )
        ), xmlns="http://www.w3.org/2000/09/xmldsig#"
    )


def add_enveloped_signature(t, c14n_method=TRANSFORM_C14N_INCLUSIVE, digest_alg=ALGORITHM_DIGEST_SHA1, transforms=None):
    if transforms is None:
        transforms = (TRANSFORM_ENVELOPED_SIGNATURE, TRANSFORM_C14N_EXCLUSIVE_WITH_COMMENTS)
    signature_node = _enveloped_signature_template(c14n_method, digest_alg, transforms)
    t.getroot().insert(0, signature_node)


_id_attributes = ['ID', 'id']


def _get_by_id(t, id_v):
    for id_a in _id_attributes:
        #logging.debug("Looking for #%s using id attribute '%s'" % (id_v,id_a))
        elts = t.xpath("//*[@%s='%s']" % (id_a, id_v))
        if elts is not None and len(elts) > 0:
            return elts[0]
    return None


def _alg(elt):
    uri = elt.get('Algorithm', None)
    if uri is None:
        return None
    else:
        return uri.rstrip('#')


b64d = lambda s: s.decode('base64')


def b64e(s):
    if type(s) in (int, long):
        s = transform.int2bytes(s)
    return s.encode('base64').replace('\n', '')


def _digest(s, hash_alg):
    h = getattr(hashlib, hash_alg)()
    h.update(s)
    digest = b64e(h.digest())
    return digest


def _remove_child_comments(t):
    root = t.getroot()
    for c in root.iter():
        if c.tag is etree.Comment or c.tag is etree.PI:
            _delete_elt(c)
    return t


def _process_references(t, sig=None):
    if sig is None:
        sig = t.find(".//{%s}Signature" % NS['ds'])
        #sig = t.find(".//Signature")
    #for ref in sig.findall(".//Reference"):
    for ref in sig.findall(".//{%s}Reference" % NS['ds']):
        uri = ref.get('URI', None)
        if uri is None or uri == '#' or uri == '':
            ct = _remove_child_comments(copy.deepcopy(t))
            obj = ct.getroot()
        elif uri.startswith('#'):
            ct = copy.deepcopy(t)
            obj = _get_by_id(ct, uri[1:])
        else:
            raise XMLSigException("Unknown reference %s" % uri)

        if obj is None:
            raise XMLSigException("Unable to dereference Reference URI='%s'" % uri)

        #for tr in ref.findall(".//Transform"):
        for tr in ref.findall(".//{%s}Transform" % NS['ds']):
            if isinstance(obj, str):
                obj = etree.fromstring(obj)
            obj = _transform(_alg(tr), obj, tr)

        dm = ref.find(".//{%s}DigestMethod" % NS['ds'])
        #dm = ref.find(".//DigestMethod")
        if dm is None:
            raise XMLSigException("Unable to find DigestMethod")
        hash_alg = (_alg(dm).split("#"))[1]
        digest = _digest(obj, hash_alg)
        dv = ref.find(".//{%s}DigestValue" % NS['ds'])
        #dv = ref.find(".//DigestValue")
        dv.text = digest


def sign(xml, private_key):
    signed_xml = sign_xml(xml, private_key)
    return etree.tostring(signed_xml)


def sign_xml(xml, private_key):
    if isinstance(xml, str):
        doc = etree.ElementTree(etree.fromstring(xml))
    elif isinstance(xml, etree._ElementTree):
        doc = xml
    else:
        raise XMLSigException("Unable to load xml from '%s'" % xml)

    sig = doc.getroot().find(".//{%s}Signature" % NS['ds'])
    #sig = doc.getroot().find(".//Signature")
    if sig is None:
        add_enveloped_signature(doc)
        sig = doc.getroot().find(".//{%s}Signature" % NS['ds'])
        #sig = doc.getroot().find(".//Signature")

    _process_references(doc, sig)
    si = sig.find(".//{%s}SignedInfo" % NS['ds'])
    #si = sig.find(".//SignedInfo")
    cm = si.find(".//{%s}CanonicalizationMethod" % NS['ds'])
    #cm = si.find(".//CanonicalizationMethod")
    cm_alg = _alg(cm)
    assert cm is not None and cm_alg is not None, XMLSigException("No CanonicalizationMethod")
    sic = _transform(cm_alg, si)
    # hack - remove xmlns=""
    sic = sic.replace(' xmlns=""', '')
    signed = pkcs1.sign(sic, private_key, 'SHA-1')
    sv = b64e(signed)
    si.addnext(DS.SignatureValue(sv))

    return doc


def verify(xml, public_key):
    """Return if <Signature> is valid for `xml`

    Args:
      xml: str of XML with xmldsig <Signature> element
      f_public: func from RSA key public function
      key_size: int of RSA key modulus size in bits
    Returns:
      bool: signature for `xml` is valid
    """
    if isinstance(xml, str):
        doc = etree.ElementTree(etree.fromstring(xml))
    elif isinstance(xml, etree._ElementTree):
        doc = xml
    else:
        raise XMLSigException("Unable to load xml from '%s'" % xml)

    sig = doc.getroot().find(".//{%s}Signature" % NS['ds'])
    if sig is None:
        raise XMLSigException("Is not signed xml!")
    else:
        _process_references(doc, sig)
        si = sig.find(".//{%s}SignedInfo" % NS['ds'])
        cm = si.find(".//{%s}CanonicalizationMethod" % NS['ds'])
        cm_alg = _alg(cm)
        assert cm is not None and cm_alg is not None, XMLSigException("No CanonicalizationMethod")
        sic = _transform(cm_alg, si)
        # hack - remove xmlns=""
        unsigned_xml = sic.replace(' xmlns=""', '')
        sve = sig.find(".//{%s}SignatureValue" % NS['ds'])
        signature = b64d(sve.text)
        return pkcs1.verify(unsigned_xml, signature, public_key)
