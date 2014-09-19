#!/usr/bin/python

"""
A test that checks whether the image saving/loading facility keeps all required meta information.
"""
from medpy.io import load, save, header
import numpy
import random
import sys

tmp_folder = "/tmp/"
input_image = "/data_humbug1/maier/Temp/extractheaderinfo/test.dcm"
#input_image = "/data_humbug1/maier/Temp/extractheaderinfo/img.dcm"
#input_image = "/imagedata/HEOPKS/original/01/1.3.46.670589.11.17204.5.0.4192.2012081712402029360_0501_000001_13452067640003.v2"

types_int = ['nii', 'nii.gz', 'hdr', 'img', 'img.gz', 'dcm', 'dicom', 'mhd', 'mha','nrrd', 'nhdr']

dtypes = (numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64,
          numpy.int8, numpy.int16, numpy.int32, numpy.int64,
          numpy.float16, numpy.float32, numpy.float64, numpy.float128,
          numpy.complex64, numpy.complex128, numpy.complex256,
          numpy.bool)

delta = 0.0001 # maximum difference between meta data allowed (since rounding errors occure)

# load original input image
img, hdr = load(input_image)

# random index
idx = tuple([random.randint(0, img.shape[i] - 1) for i in range(len(img.shape))])

# extract information from original image
otype = input_image.split('.')[-1]
mdata = {'shape': img.shape,
         'dtype': img.dtype,
         'spacing': header.get_pixel_spacing(hdr),
         'offset': header.get_offset(hdr),
         'point': img[idx]}

print "ORIGINAL"
print "Type: {}".format(otype)
print "MData: {}".format(mdata)

def test01(img):
    # TEST 01: WHAT DATATYPES CAN THE FORMATS SAVE?
    for dt in dtypes:
        print '\n:::{}:::'.format(dt).upper()
        for t in types_int:
            print t.upper(), '\t->',
             
            try:
                img1 = img.astype(dt)
                name2 = tmp_folder + '.'.join(['tmp', t])
                save(img1, name2, hdr, True)
                print 'done.'
            except Exception as e:
                print 'failed: {}'.format(e)


def test02(img, idx):
    # TEST 02: CAN THEY BE LOADED AGAIN WITHOUT A CHANGE OF DATA TYPE OR DATA CONTENT?
    for dt in dtypes:
        print '\n:::{}:::'.format(dt).upper()
        for t in types_int:
            print t.upper(), '\t->',
             
            try:
                img1 = img.astype(dt)
                name2 = tmp_folder + '.'.join(['tmp', t])
                save(img1, name2, hdr, True)
                try:
                    img2, _ = load(name2)
                    if img2.dtype == img1.dtype and img2[idx] == img1[idx]:
                        print True
                    elif img2.dtype == img1.dtype:
                        print 'dtype: {} / value: {} != {}'.format(True, img2[idx], img1[idx])
                    elif img2[idx] == img1[idx]:
                        print 'dtype: {} != {} / value: {}'.format(img2.dtype, img1.dtype, True)
                    else:
                        print 'dtype: {} != {} / value: {} != {}'.format(img2.dtype, img1.dtype, img2[idx], img1[idx])
                except Exception as e:
                    print 'loading failed, reason: {}'.format(e)    
                
            except Exception as e:
                print 'saving unsupported'




def _compare(obj1, obj2, delta):
    if isinstance(obj1, (list, tuple, set, numpy.ndarray)):
        return _compare_seq(obj1, obj2, delta)
    elif isinstance(obj1, (int, float)):
        return _compare_number(obj1, obj2, delta)
    else:
        return _compare_others(obj1, obj2)
        

def _compare_others(obj1, obj2):
    return obj1 == obj2

def _compare_number(nb1, nb2, delta):
    diff = abs(nb1 - nb2)
    if diff > delta: return False
    return True

def _compare_seq(seq1, seq2, delta):
    if len(seq1) != len(seq2): return False
    for e1, e2 in zip(seq1, seq2):
        diff = abs(e1 - e2)
        if diff > delta: return False
    return True

def test03(img, hdr, idx, delta):
    # TEST 03: DOES ANY META-INFORMATION GET LOST DURING FORMAT CONVERSION? AND IF YES; WHICH?
    for tr in types_int: # reference type
        print ''
        oformat = tr
        
        # create, save and load reference image
        try:
            name_ref = tmp_folder + '.'.join(['tmp_ref', tr])
            save(img, name_ref, hdr, True)
            img_ref, hdr_ref = load(name_ref)
        except Exception as e:
            print '\tERROR: Could not generate reference image for type {}: {}'.format(otype, e)
            continue
        
        # extract meta-data from reference image
        mdata_ref = {'shape': img_ref.shape,
                     'dtype': img_ref.dtype,
                     'point': img_ref[idx],
                     'spacing': header.get_pixel_spacing(hdr_ref),
                     'offset': header.get_offset(hdr_ref),}        
        
        # print meta-data from reference image
        
        # iterate of test images
        for tt in types_int: # test type
            print '{} => {}'.format(oformat, tt),
            
            # create, save and load test images
            try:
                #print type(img_ref), type(hdr_ref)
                #print type(img_test), type(hdr_test)
                name_test = tmp_folder + '.'.join(['tmp_test', tt])
                save(img_ref, name_test, hdr_ref, True)
                img_test, hdr_test = load(name_test)
                
            except Exception as e:
                print '\tERROR: Could not generate test image. {}'.format(e)
                continue
            
            # extract meta-data from test image
            mdata_test = {'shape': img_test.shape,
                          'dtype': img_test.dtype,
                          'spacing': header.get_pixel_spacing(hdr_test),
                          'offset': header.get_offset(hdr_test),
                          'point': img_test[idx]}                    
            
            # compare reference against meta-image
            error = False
            for k in mdata_ref.keys():
                equal = _compare(mdata_ref[k], mdata_test[k], delta)
                #print '\n\t{} ({}) : {} = {}'.format(equal, k, mdata_ref[k], mdata_test[k]),
                if not equal:
                    error = True
                    print '\n\t{} ({}) : {} = {}'.format(equal, k, mdata_ref[k], mdata_test[k]),
            if not error:
                print '\t{}'.format(True)
            else:
                print '\n'
     
def test04(img, hdr, idx, delta):
    # TEST 04: COMBINE ALL OTHER TEST INTO ONE BIG
    
    for dt in dtypes:
        print '\n:::{}:::'.format(dt).upper()
        
        test03(img.astype(dt), hdr, idx, delta)
     
test04(img, hdr, idx, delta)
sys.exit(0)
    
    
