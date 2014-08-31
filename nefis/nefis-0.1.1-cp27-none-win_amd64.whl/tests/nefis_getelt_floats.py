import nefis
import numpy as np
import struct

def test_nefis_getelt_floats():
    #-------------------------------------------------------------------------------
    error, version = nefis.getnfv()
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
    #-------------------------------------------------------------------------------
    usr_index = np.arange(15).reshape(5,3)
    usr_index[0,0] = 1
    usr_index[0,1] = 1
    usr_index[0,2] = 1
    usr_index[1,0] = 0
    usr_index[1,1] = 0
    usr_index[1,2] = 0
    usr_index[2,0] = 0
    usr_index[2,1] = 0
    usr_index[2,2] = 0
    usr_index[3,0] = 0
    usr_index[3,1] = 0
    usr_index[3,2] = 0
    usr_index[4,0] = 0
    usr_index[4,1] = 0
    usr_index[4,2] = 0
    np.ascontiguousarray(usr_index, dtype=np.int32)

    usr_order = np.arange(5).reshape(5)
    usr_order[0] = 1
    usr_order[1] = 2
    usr_order[2] = 3
    usr_order[3] = 4
    usr_order[4] = 5
    np.ascontiguousarray(usr_order, dtype=np.int32)

    grp_name = 'map-const'
    elm_name = 'THICK'
    length = 20

    error, buffer_res = nefis.getelt(fp, grp_name, elm_name, usr_index, usr_order, length)

    print('NEFIS error code (getels): %d' % error)
    if not error == 0:
        print("=========")
        error, err_string = nefis.neferr()
        print('    NEFIS error string       : %s' % err_string)
        print("=========")

    fmt = "%df" % (length/4)
    numbers = struct.unpack(fmt, buffer_res)

    print('')
    print(numbers)
    print('')
    #-------------------------------------------------------------------------------
    print("---------")
    error = nefis.clsnef(fp)
    print('NEFIS error code (clsnef): %d' % error)
    print("---------")


if __name__ == "__main__":
    test_nefis_getelt_floats()

