
import numpy as np
import os

import MSBWTGen

def doublingBuild(bwtDir, logger):
    
    MSBWTGen.clearAuxiliaryData(bwtDir)
    
    ###########################################
    #Section for init to X-mer, currently X = 1
    ###########################################
    #this value determines how we seed the merge k-mer wise
    currK = 10
    
    logger.info('Initializing '+str(currK)+'-mers...')
    
    seqs = np.load(bwtDir+'/seqs.npy')
    offsets = np.load(bwtDir+'/offsets.npy', 'r+')
    
    tc = {}
    binMod = 6**currK
    for x in xrange(0, offsets.shape[0]-1):
        sOff = offsets[x]
        eOff = offsets[x+1]
        
        #initialize the code
        currBin = 0
        for y in xrange(0, currK):
            currBin = 6*currBin+getCharOfSeq(seqs, offsets, x, y)
        
        #now for each value, we do this
        for y in xrange(0, eOff-sOff):
            #first save this
            tc[currBin] = tc.get(currBin, 0)+1
            
            #calculate next bin
            currBin = (6*currBin+getCharOfSeq(seqs, offsets, x, y+currK)) % binMod
    
    #TODO: is 4 billion enough? is 2^16 enough characters?
    
    #the string number, aka which read it is, we only need one of these
    seqIDType = '<u4'
    seqID = np.lib.format.open_memmap(bwtDir+'/seqID.npy', 'w+', seqIDType, (seqs.shape[0], ))
    
    #the offset of the symbol into the string, we only need one of these
    offseqType = '<u2'
    offseq = np.lib.format.open_memmap(bwtDir+'/offseq.npy', 'w+', offseqType, (seqs.shape[0], ))
    
    #relates the position of the symbol from the input to it's output, only one again
    revDictType = '<u8'
    revDict = np.lib.format.open_memmap(bwtDir+'/revDict.npy', 'w+', revDictType, (seqs.shape[0], ))
    
    #array indicating the end of k-mer groups, 1 indicates an end, still should only need one
    endsWrite = np.lib.format.open_memmap(bwtDir+'/ends'+str(currK)+'.npy', 'w+', '<u1', (seqs.shape[0], ))
    #endsWrite[np.cumsum(tc)-1] = 1
    
    fmTot = 0
    fm = {}
    for binType in sorted(tc.keys()):
        fm[binType] = fmTot
        fmTot += tc[binType]
        endsWrite[fmTot-1] = 1
        
    #create an additional array we will use for ping-ponging
    np.lib.format.open_memmap(bwtDir+'/ends'+str(2*currK)+'.npy', 'w+', '<u1', (seqs.shape[0], ))
    
    '''
    #init to string 0, offset 0
    sID = 0
    off = 0
    
    #iterate through each sequence and store it in the correct location
    for i in xrange(0, seqs.shape[0]):
        #pull the fmIndex value and increment it
        fmi = fm[seqs[i]]
        fm[seqs[i]] += 1
        
        #write the appropriate values in here
        seqID[fmi] = sID
        offseq[fmi] = off
        revDict[i] = fmi
        
        #check what needs to be incremented/reset
        if seqs[i] == 0:
            sID += 1
            off = 0
        else:
            off += 1
    '''
    i = 0
    for x in xrange(0, offsets.shape[0]-1):
        sOff = offsets[x]
        eOff = offsets[x+1]
        
        #initialize the code
        currBin = 0
        for y in xrange(0, currK):
            currBin = 6*currBin+getCharOfSeq(seqs, offsets, x, y)
        
        #now for each value, we do this
        for y in xrange(0, eOff-sOff):
            #pull the fm value and increment it
            fmi = fm[currBin]
            fm[currBin] += 1
            
            #write the appropriate values out
            seqID[fmi] = x
            offseq[fmi] = y
            revDict[i] = fmi
            i += 1
            
            #calculate next bin
            currBin = (6*currBin+getCharOfSeq(seqs, offsets, x, y+currK)) % binMod
    
    logger.info('Finished init.')
    ###########################################
    #End Init
    ###########################################
    
    #doubling loop
    changesMade = True
    while changesMade:
        changesMade = False
        endsRead = np.load(bwtDir+'/ends'+str(currK)+'.npy', 'r+')
        endsWrite = np.load(bwtDir+'/ends'+str(2*currK)+'.npy', 'r+')
        
        logger.info('Beginning iteration '+str(2*currK)+'...')
        
        rangeStart = 0
        for i in xrange(0, seqs.shape[0]):
            #we only act at the end of a range
            if endsRead[i] == 1:
                rangeEnd = i+1
                endsWrite[i] = 1
                
                if rangeEnd-rangeStart > 1:
                    #now handle the range
                    #inside pairs we will store the index of the kmer that is offset by currK from us AND
                    #the seqID and the offsetID
                    pairs = np.zeros((rangeEnd-rangeStart, ), ','.join([revDictType, seqIDType, offseqType]))
                    
                    for y in xrange(0, rangeEnd-rangeStart):
                        pInd = rangeStart+y
                        ind = getIndexOfSeq(offsets, seqID[pInd], offseq[pInd]+currK)
                        pairs[y] = (revDict[ind], seqID[pInd], offseq[pInd])
                    
                    npargsort = np.argsort(pairs)
                    prevRevDict = pairs[npargsort[0]][0]
                    
                    for x, ind in enumerate(npargsort):
                        if x == ind:
                            #no changes here
                            pass
                        else:
                            #make sure we loop again later
                            changesMade = True
                            
                            #update all of the things to be correct
                            seqID[rangeStart+x] = pairs[ind][1]
                            offseq[rangeStart+x] = pairs[ind][2]
                            revDict[getIndexOfSeq(offsets, pairs[ind][1], pairs[ind][2])] = rangeStart+x
                            
                        for z in xrange(prevRevDict, pairs[ind][0]):
                            if endsRead[z] == 1:
                                endsWrite[rangeStart+x-1] = 1
                                break
                        
                        prevRevDict = pairs[ind][0]
                        
                #now reset
                rangeStart = rangeEnd
                
            else:
                #do nothing
                pass 
        
        os.rename(bwtDir+'/ends'+str(currK)+'.npy', bwtDir+'/ends'+str(4*currK)+'.npy')
        currK *= 2
        
        
    msbwt = np.lib.format.open_memmap(bwtDir+'/msbwt.npy', 'w+', '<u1', (seqs.shape[0], ))
    for x in xrange(0, seqs.shape[0]):
        msbwt[x] = getCharOfSeq(seqs, offsets, seqID[x], offseq[x]-1)
    
def getCharOfSeq(seqs, offsets, seqID, index):
    return seqs[getIndexOfSeq(offsets, seqID, index)]
    
def getIndexOfSeq(offsets, seqID, index):
    l = offsets[seqID+1]-offsets[seqID]
    i = index % l
    return offsets[seqID]+i
    