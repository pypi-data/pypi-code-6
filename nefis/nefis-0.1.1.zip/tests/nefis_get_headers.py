import nefis
import numpy as np

def test_nefis_get_headers():
    #-------------------------------------------------------------------------------
    error, version = nefis.getnfv()
    print('')
    print('Library version: %s' % version[4:])
    print('')
    #-------------------------------------------------------------------------------
    dat_file = 'trim-f34.dat'
    def_file = 'trim-f34.def'
    coding = ' '
    ac_type = 'r'
    fp = -1
    print("---------")
    print(dat_file)
    print(def_file)
    print(coding)
    print(ac_type)
    print("---------")

    #-------------------------------------------------------------------------------
    error, fp = nefis.crenef(dat_file, def_file, coding, ac_type)
    print('File set (should be zero): %d' % fp)
    print('NEFIS error code (crenef): %d' % error)
    print("---------")
    if not error == 0:
        error, err_string = nefis.neferr()
        print('    NEFIS error string       : %s' % err_string)
        print("=========")
    #-------------------------------------------------------------------------------
    error, def_header = nefis.gethdf(fp)
    if not error == 0:
        error, err_string = nefis.neferr()
        print('    NEFIS error string       : %s' % err_string)
        print("=========")
    #-------------------------------------------------------------------------------
    error, dat_header = nefis.gethdt(fp)
    if not error == 0:
        error, err_string = nefis.neferr()
        print('    NEFIS error string       : %s' % err_string)
        print("=========")
    #-------------------------------------------------------------------------------
    print(def_header)
    print(dat_header)
    #-------------------------------------------------------------------------------
    print("---------")
    error = nefis.clsnef(fp)
    print('NEFIS error code (clsnef): %d' % error)
    print("---------")


if __name__ == "__main__":
    test_nefis_get_headers()
