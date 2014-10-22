import numpy
import itertools
import png
import old




def fileToData(name):
    '''
    This function is very secret, but here is a hint:
    lenght is the nuber of bytes in the output
    '''
    f = open(name, 'r')
    data = numpy.fromstring( name + '\n' + f.read(), 
                             dtype=numpy.uint8 )
    f.close

    lenght = 4+len(data)
    if not lenght < 2**32:
        raise MemoryError('Den hoevdingen blir stoerre ju mera eol han dricker. Taenk om en vacker dag han blaaser upp sig saa han spricker.')
    lenght = numpy.array([lenght], dtype=numpy.uint32)
    lenght.dtype = numpy.uint8
    return  numpy.hstack((lenght, data))


def filesToData(*names):
    data=numpy.hstack( (fileToData(name) for name in names) ) 
    return numpy.hstack( (data, 
                          numpy.zeros(4, dtype=numpy.uint8) ) )


def dataToFile(data):
    '''
    This function is very secret, but here is a hint:
    data should be a numpy.array with dtype=numpy.uint8
    '''
    data = data.tostring()

    place = 0
    while data[place] != '\n': 
        place += 1

    name=data[:place]

    f = open(name,'w')
    f.write(data[place+1:])
    f.close

    return name


def dataToFiles(data):
    '''
    This function is very secret, but here is a hint:
    data should be a numpy.array with dtype=numpy.uint8
    '''
    lenght = data[0:4]
    lenght.dtype = numpy.uint32
        
    names=[]
    prevLenght = 0
    while lenght[0] != 0:
        names.append( dataToFile( 
                        data[prevLenght + 4: prevLenght + lenght[0]] ) )
        prevLenght += lenght[0]
        lenght = data[prevLenght : prevLenght + 4]
        lenght.dtype = numpy.uint32

    return tuple(names)


def hidePNG(original, bad_coppy, secret):
    '''
    This function is so secret, I will not say what it does.
    However, secret should be a numpy.array with dtype=numpy.uint8
    '''
    fileOrg = open(original, 'rb')
    read = png.Reader(fileOrg).read()
    data = numpy.hstack(itertools.imap(numpy.uint8, read[2]))
    fileOrg.close()
    
    bitBasis = 8*len(secret)/len(data) + 1
    if bitBasis > 6:
        raise MemoryError('Haer var det pin-tjockt med skitstoevlar')

    data=numpy.unpackbits(data).reshape(-1,8)
    secret = numpy.hstack( ( numpy.unpackbits(secret),
                             numpy.zeros(bitBasis - 8*len(secret) %bitBasis, 
                                         dtype=numpy.uint8 ) )
                          ).reshape(-1,bitBasis)

    data[0,5:8] = numpy.unpackbits( numpy.array([bitBasis] ,dtype=numpy.uint8) )[5:8]
    data[1:len(secret)+1,8-bitBasis:8] = secret
 
    w=png.Writer(read[0],read[1],**read[3])
    fileCop = open(bad_coppy, 'wb')
    w.write(fileCop, numpy.packbits(data).reshape(read[1], -1 ) )
    fileCop.close()




def findPNG(image):
    '''
    This function is so secret, I will not say what it does.
    Nope, I am not tellig you anything.
    '''
    imageFile = open(image, 'rb')
    read = png.Reader(imageFile).read()
    data = numpy.unpackbits( numpy.hstack(itertools.imap(numpy.uint8, read[2]))
                             ).reshape(-1,8)

    bitBasis = numpy.packbits( numpy.hstack( (numpy.zeros(5,dtype=numpy.uint8), 
                                              data[0,5:8]) ) )[0]

    return numpy.packbits( data[1:,8-bitBasis:8] )



def vild(original, bad_coppy, *secrets):
    '''
    Snealla seota meaniska!
    '''
    hidePNG(original, bad_coppy, filesToData(*secrets) )


def vittra(bad_coppy, **kw):
    '''
    Nu ska blodet flyta!
    use: kw = {'old' : True}, for files done by vildvittra < 0.0.3 
    '''
    if kw[old]: return old.vittra(bad_coppy)
    return dataToFiles( findPNG(bad_coppy), **kw )
    

