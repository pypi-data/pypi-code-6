'''
EWKB structure based on https://github.com/postgis/postgis/blob/svn-trunk/liblwgeom/lwin_wkb.c
BYTES   TYPE      value
0-1     char      big/little endian
1-5     u_int_32  wkb type including has_srid flag
5-9     u_int_32  srid (or start of body if no srid is set)
'''
import struct
import codecs

#Flags in wkb type
_ZDIM_FLAG = 0x80000000
_MDIM_FLAG = 0x40000000
_SRID_FLAG = 0x20000000
_BBOX_FLAG = 0x10000000

#Sections of header
_ENDIAN_OFFSET = 0
_TYPE_OFFSET = 1
_SRID_OFFSET = 5
_SRID_END_OFFSET = 9

#Endian symbols used by struct
_LITTLE_ENDIAN = '<'
_BIG_ENDIAN = '>'

def has_little_endian(wkb):
    return _endian_symbol(wkb) == _LITTLE_ENDIAN

def drop_srid(ewkb):
    '''
    Drop srid specification if present from ewkb
    '''
    endian_symbol, wkbtype, srid = _get_full_header(ewkb)
    if srid is not None:
        return _header_to_bytes(endian_symbol, _drop_type_srid(wkbtype), None) + _get_ewkb_body(ewkb)
    return ewkb

def set_srid(wkb, to_srid):
    '''
    Returns a ewkb object with the provided srid specified
    '''
    if to_srid is None:
        return drop_srid(wkb)
    endian_symbol, wkbtype, srid = _get_full_header(wkb)

    if srid is not None:
        return _header_to_bytes(endian_symbol, wkbtype, to_srid) + _get_ewkb_body(wkb)
    else:
       return _header_to_bytes(endian_symbol, _add_type_srid(wkbtype), to_srid) + _get_wkb_body(wkb)


def get_srid(wkb):
    '''
    Get the srid from ewkb object, returns none if not specified
    '''
    endian_symbol, wkbtype, srid = _get_full_header(wkb)
    return srid

def get_type_int(wkb):
    '''
    Get the type-integer from wkb object
    '''
    endian_symbol, wkbtype, srid = _get_full_header(wkb)
    return wkbtype

def _endian_symbol(wkb):
    try:
        endian_byte =  struct.unpack_from('<B', wkb, _ENDIAN_OFFSET)[0]
    except TypeError:
        pass
    else:
        if endian_byte == 1:
            return _LITTLE_ENDIAN
        elif endian_byte == 0:
            return _BIG_ENDIAN
    _raise_typeerror(wkb)

def _raise_typeerror(wkb):
    #Postgis likes to use hex-encoded wkbs, so this method provides useful error message
    try:
        codecs.decode(wkb, 'hex_codec')
    except:
        raise TypeError('Input %s does not seem to be a wkb' % (type(wkb), ))
    else:
        raise TypeError('Error parsing wkb, is it hex-encoded?')

def _srid(wkb, es):
    return struct.unpack_from(es+'I', wkb, _SRID_OFFSET)[0]

def _has_srid(wkbtype):
    return wkbtype & _SRID_FLAG != 0

def _get_type(wkb, es):
    return struct.unpack_from(es+'I', wkb, _TYPE_OFFSET)[0]

def _get_full_header(wkb):
    es = _endian_symbol(wkb)
    wkbtype = _get_type(wkb, es)
    srid = None
    if _has_srid(wkbtype):
        srid = _srid(wkb, es)
    return es, wkbtype, srid

def _header_to_bytes(es, wkbtype, srid):
    endianval = int(es == _LITTLE_ENDIAN)
    if srid is not None:
        return struct.pack(es+'BII', endianval, wkbtype, srid)
    return struct.pack(es+'BI', endianval, wkbtype)

def _drop_type_srid(wkbtype):
    return wkbtype & (~_SRID_FLAG)

def _add_type_srid(wkbtype):
    return wkbtype | _SRID_FLAG

def _get_ewkb_body(ewkb):
    return ewkb[_SRID_END_OFFSET:]

def _get_wkb_body(wkb):
    return wkb[_SRID_OFFSET:]

