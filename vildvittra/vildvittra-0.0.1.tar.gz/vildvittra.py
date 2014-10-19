import numpy; 
import itertools; 
import png
import array



def convertBinayBases(listIn, bitsIn, bitsOut):
    '''
    bitIN and bitOut are the nuber of bits per int the data. 
    bitIN and bitOut must be in the range 1-8
    This function might add or destroy zeros in the end of a list.
    But do not tell this to anyone, because it is a secret.
    '''

    bitList=array.array('B')
    
    for numIn in listIn:
        for bitIn in range(bitsIn):
            bit=numIn % (2**(bitIn+1))
            numIn -= bit
            bitList.append( bit/(2**bitIn) )
    
    if bitsOut == 1: return bitList
    
    bitIter=iter(bitList)
    listOut=array.array('B')
    while True:
        numOut=0
        for bitOut in range(bitsOut):
            try: numOut += bitIter.next()*(2**bitOut)
            except StopIteration:
                if not numOut==0:
                    listOut.append(numOut)
                return listOut
        listOut.append(numOut)


def fileToData(name):
    '''
    This function is very secret, but here is a hint:
    len = lenght of data
    '''
    f = open(name, 'r')
    data = array.array('B', (ord(char) for char in f.read() ) )
    f.close
    name = array.array('B', (ord(char) for char in name+'\n' ) )
    length = numpy.array([len(data)], dtype=numpy.uint32)
    length.dtype = numpy.uint8
    return  {'len': len(length) + len(name) + len(data),
             'data': itertools.chain(length, name, data) }


def zeros():
    while True: yield 0


def dataToFile(data):
    '''
    This function is very secret, but here is a hint:
    data should be itterable
    '''
    data = itertools.chain( data, zeros() )
    lenght = 0
    for byte in range(4):
        lenght += data.next()*(256**byte)

    name = ''
    nextChar = chr(data.next()) 
    while nextChar != '\n':        
        name += nextChar
        nextChar = chr(data.next()) 

    fileData = ''.join(chr(data.next()) for byte in range(lenght))

    f = open(name,'w')
    f.write(fileData)
    f.close

    return name
    



def hidePNG(original, bad_coppy, secret):
    '''
    This function is so secret, I will not say what it does.
    However, secret should be a dict
    '''

    fileOrg = open(original, 'rb')
    fileCop = open(bad_coppy, 'wb')

    read = png.Reader(fileOrg).read()
    data = numpy.hstack(itertools.imap(numpy.uint8, read[2]))
    
    if read[3]['greyscale']:colors=1
    else: colors=3
    
    bitBasis = (8*secret['len'])/len(data) + 1
    if bitBasis > 6:
        raise MemoryError('Det aer pin-tjockt med skitstoevlar')

    secret = convertBinayBases(secret['data'], 8, bitBasis) 
    lenght = len(secret)+1
    
    data[0] = data[0] - data[0]%8 + bitBasis
    data[1:lenght ] = (data[1:lenght ] 
                      -data[1:lenght ]%(2*bitBasis)
                      +secret )
    
    w=png.Writer(read[0],read[1],**read[3])
    w.write(fileCop, data.reshape(read[1], colors*read[0]) )
    fileOrg.close()
    fileCop.close()




def findPNG(image):
    '''
    This function is so secret, I will not say what it does.
    Nope, I am not tellig you anything.
    '''
    imageFile = open(image, 'rb')
    read = png.Reader(imageFile).read()
    data = numpy.hstack(itertools.imap(numpy.uint8, read[2]))
    bitBasis = data[0]%8
    return convertBinayBases( data[1:]%(2*bitBasis), bitBasis, 8) 



def vild(original, bad_coppy, secret):
    '''
    Snealla seota meaniska!
    '''
    hidePNG(original, bad_coppy, fileToData(secret) )


def vittra(bad_coppy):
    '''
    Nu ska blodet flyta!
    '''
    dataToFile( findPNG(bad_coppy) )
    

