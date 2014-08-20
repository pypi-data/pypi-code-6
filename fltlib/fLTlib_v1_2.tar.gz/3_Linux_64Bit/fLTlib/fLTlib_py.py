######################################################################
#
#   This is a python routing for "fLTlib". All funcitons in fLTlib
#    have the same name here.
#
#   In case the fLTlib file is missing or can't be load correctly,
#    this file will be loaded automatically by "fLTHelpFun.py"
#
#   This file only needs numpy support for fft and array calculation
#
#   If the fitting speed is too slow, please try to use the c/c++
#   library file: fLTlib.so (or in windows fLTlib.pyd)
#
######################################################################

import numpy             as np

MY_EXP_PAR_COUNT    = 5
MY_MAX_LAMDA        = 1e17
MY_MAX_TIMES_A      = 100
MY_MAX_TIMES_B      = 17
MY_MIN_PRE          = 1e-3

def myABS(_a):
    if (_a)>=(0):
        return (_a)
    else:
        return -(_a)

def myNdArray1D(A):
    if type(A).__module__ == np.__name__ :
        #print 'NumpyArray(%dD)'%(A.ndim)
        return A.reshape(-1)
    else:
        #print 'Not a numpy array'
        return np.array(A).reshape(-1) 

def myNd2Str(S, A): #"%.2f"
    return (np.vectorize(S.__mod__)(A))

def myMax(A):
    ii = np.unravel_index(A.argmax(), A.shape)
    return A[ii], ii

def sqrt(A):
    return pow(A, 0.5)

class MY_LL_FIT(object):
    def __init__(self, Tm = 100):
        self.gl_np=0; self.mySetTm(Tm)
        self.gl_t1vm = 0.0; self.gl_a1vt1  =0.0; self.gl_a1vm=0.0; self.gl_exp_mvt1=0.0; self.gl_n0_A1=0.0
        self.gl_n1_A1= 0.0; self.gl_dyda_1 = np.zeros(5)
        self.gl_t2vm = 0.0; self.gl_a2vt2  =0.0; self.gl_a2vm=0.0; self.gl_exp_mvt2=0.0; self.gl_n0_A2=0.0
        self.gl_n1_A2= 0.0; self.gl_dyda_2 = np.zeros(5)
    
    def mySetTm(self, Tm = 100):
        self.gl_m = Tm
        
    def myLegendre_0(self, x, para, dyda):
        # para 0 ~ 4 : A1 T1 A2 T2 Offset
        if (x > 1):
            dtmpA   = 2.0 *(x - 1.0); dtmpC = 1.0/(dtmpA - 1.0)
            dtmpB = (dtmpA + 3.0); dtmpD = 2 * self.gl_t1vm
            dyda[0] = dtmpB * (dtmpD * self.gl_dyda_2[0] + dtmpC * self.gl_dyda_1[0])
            dyda[1] =  dtmpB * ( dtmpD * self.gl_dyda_2[1] + self.gl_n1_A1 * 2.0 / self.gl_m + dtmpC * self.gl_dyda_1[1])
            dtmpA = 2 * self.gl_t2vm
            dyda[2] =  dtmpB * (dtmpA * self.gl_dyda_2[2] + dtmpC * self.gl_dyda_1[2])
            dyda[3] =  dtmpB * (dtmpA * self.gl_dyda_2[3] + self.gl_n1_A2 * 2.0 / self.gl_m + dtmpC * self.gl_dyda_1[3])
            dyda[4] = 0; self.gl_n1_A1 = para[0] * dyda[0]; self.gl_n1_A2 = para[2] * dyda[2]
            y = self.gl_n1_A1 + self.gl_n1_A2
            for i in xrange(4, -1, -1):
                self.gl_dyda_1[i] = self.gl_dyda_2[i]; self.gl_dyda_2[i] = dyda[i]
        elif (x==1):
            y = self.myLegendre_c1(para, dyda)
        else:
            y = self.myLegendre_c0(para, dyda)
        return y
    
    def myLegendre_c0(self, para, dyda):
        # para 0 ~ 4 : A1 T1 A2 T2 Offset
        dtmpA = para[1]; self.gl_t1vm = dtmpA / self.gl_m
        self.gl_exp_mvt1 = np.exp(- self.gl_m/dtmpA); dtmpB = (1.0 - self.gl_exp_mvt1)
        dyda[0] = self.gl_t1vm * dtmpB
        dtmpC = para[0]; self.gl_a1vm = dtmpC / self.gl_m; self.gl_a1vt1 = dtmpC / dtmpA
        dyda[1] = dtmpB * self.gl_a1vm - self.gl_a1vt1 * self.gl_exp_mvt1
        dtmpA = para[3]; self.gl_t2vm = dtmpA / self.gl_m
        self.gl_exp_mvt2 = np.exp(- self.gl_m/dtmpA); dtmpB = (1.0 - self.gl_exp_mvt2)
        dyda[2] = self.gl_t2vm * dtmpB; dtmpC = para[2]
        self.gl_a2vm = dtmpC / self.gl_m; self.gl_a2vt2 = dtmpC / dtmpA
        dyda[3] = dtmpB * self.gl_a2vm - self.gl_a2vt2 * self.gl_exp_mvt2
        dyda[4] = 1.0; self.gl_n0_A1 = para[0] * dyda[0]; self.gl_n0_A2 =para[2] * dyda[2]
        y = self.gl_n0_A1 + self.gl_n0_A2 + para[4]
        self.gl_dyda_1[:] = dyda
        #if(self.gl_np<3):
        #    for i in xrange(5):
        #        print "%lf "%(self.gl_dyda_1[i]);
        #    print "a0=%lf+%lf+%lf=%lf\n"%(self.gl_n0_A1, self.gl_n0_A2, para[4], y)
        #self.gl_np = self.gl_np + 1
        return y
    
    def myLegendre_c1(self, para, dyda):
        # para 0 ~ 4 : A1 T1 A2 T2 Offset        
        dtmpA = 6.0 * self.gl_t1vm * self.gl_t1vm
        dyda[0] = dtmpA - 3.0 * self.gl_t1vm - self.gl_exp_mvt1 * (dtmpA + 3.0 * self.gl_t1vm)
        self.gl_n1_A1 = para[0] * dyda[0]
        dyda[1] = self.gl_n1_A1 / para[1] + 6.0 * self.gl_n0_A1 / self.gl_m - 3.0 * para[0] * self.gl_exp_mvt1 * (1.0 / para[1] + 2.0 / self.gl_m)
        
        dtmpA = 6.0 * self.gl_t2vm * self.gl_t2vm
        dyda[2] = dtmpA - 3.0 * self.gl_t2vm - self.gl_exp_mvt2 * (dtmpA + 3.0 * self.gl_t2vm)
        self.gl_n1_A2 = para[2] * dyda[2]
        dyda[3] = self.gl_n1_A2 / para[3] + 6.0 * self.gl_n0_A2 / self.gl_m - 3.0 * para[2] * self.gl_exp_mvt2 * (1.0 / para[3] + 2.0 / self.gl_m)
        dyda[4] = 0; y = self.gl_n1_A1 + self.gl_n1_A2
        self.gl_dyda_2[:] = dyda
        #if(self.gl_np<3):
        #    for i in xrange(5):
        #        print "%lf "%(self.gl_dyda_2[i]);
        #    print "a1=%lf+%lf=%lf\n"%(self.gl_n1_A1, self.gl_n1_A2, y)
        #self.gl_np = self.gl_np + 1   
        return y
        #//---------------------------------------------------------------------------
        #//      User Define Function
        #//      A0 = at/m (1-exp(-m/t)); A1= 3 at/m/m [2t - m -exp(-m/t)(2t + m)]
        #//      A(n+1) = (2n+3)(2t/m A(n) + 1/(2n-1) A(n-1) ); n=1,2,3 -> A(2),A(3),A(4)
        #//      dA/da  = (2n+3)(2t/m A'(a)(n) + 1/(2n-1) A'(a)(n-1))
        #//      dA/dt  = (2n+3)(2t/m A'(t)(n) + A(n) 2/m + 1/(2n-1) A'(t)(n-1));
        #//---------------------------------------------------------------------------

    def myEXP2LengendreC(self, dA, dT, dM, nN, pdOut):
        i = nN; j=2
        if(nN<1 or myABS(dA)<1e-17):
            return 0;
        dAT = dA * dT /dM; dETM = np.exp(- dM / dT); dAN1 = dAT*(1-dETM)
        pdOut[0] = dAN1; i = i - 1
        if (i<=0):
            return 1
        dabsMin = myABS(dAN1/dA); dTMP = dT + dT
        dAN = 3*dAT/dM *( dTMP - dM - dETM * ( dTMP + dM) );
        pdOut[1] = dAN
        dMT = (dT + dT)/dM;  dabsMin = myABS(dAN/dA)
        ii = i - 1; jj=2
        for i in xrange(ii, 0, -1):
            dJ = j;
            dTMP = (dJ + 3) * (dMT * dAN + dAN1/(dJ - 1) );
            dabsTemp = myABS(dTMP/dA);
            if(dabsTemp < MY_MIN_PRE and dabsMin < dabsTemp):
                pdOut[jj]=0; jj=jj+1
                break
            dabsMin = dabsTemp;
            pdOut[jj]=dTMP; jj=jj+1
            dAN1 = dAN; dAN = dTMP; j = j + 2
        
        ii = i - 1;
        for i in xrange(ii, 0, -1):
            pdOut[jj]=0; jj=jj+1
        
        return(j/2+1)
    
    def myDoubleEXPCheck_ex(self, dA1, dT1, dA2, dT2, i):
        # we suppose dT1 >= dT2
        # This is for noise cut, the cut values are from 5000 random fit
        if   (dT2 > 0.13):
            k = 5 #cut 6,7 ...
        elif (dT1 > 0.25):
            if (dT2 > 0.058):
                k = 4
            else:
                k = 3
        elif (dT1 > 0.21):
            if (dT2 > 0.062):
                k = 4
            else:
                k = 3
        elif (dT1 > 0.17):
            if (dT2 > 0.070):
                k = 4
            else:
                k = 3
        elif (dT1 > 0.13):
            if (dT2 > 0.078):
                k = 4
            else:
                k = 3
        elif (dT1 > 0.11):
            if (dT2 > 0.084):
                k = 4
            else:
                k = 3
        else:
            k = 3
            
        if(k>=i):
            k=-1
        #if(dA1>dA2): #{ }
        return k
    
    def myDoubleEXPCheck(self, pFit, i, dTm):
        if (pFit[1]>pFit[3]):
            return self.myDoubleEXPCheck_ex(pFit[0], pFit[1]/dTm, pFit[2], pFit[3]/dTm, i)
        return self.myDoubleEXPCheck_ex(pFit[2], pFit[3]/dTm, pFit[0], pFit[1]/dTm, i)
    
    def mySingleEXPCheck(self, dTemp, i):
        if(dTemp>0.17):
            if(i>3):
                k=3
            else:
                k = -1
        else:
            if (i>4):
                k=4
            else:
                k = -2
        return k

    def myCheckAndCorrect(self, aa, nExpCount, pFit, dTm):
        if nExpCount==1:# only the first exp
            dT = pFit[1]
            dTemp = dT/dTm; dA = pFit[0]; nCount = 1
        elif nExpCount==2:# only the second exp
            dT = pFit[3]
            dTemp = dT/dTm; dA = pFit[2]; nCount = 1
        elif nExpCount==3:# Two exp
            nCount = 2
        else: #no exp, only offset, we do nothing
            return False
   
        i = aa.size; pTemp = 0.0 * aa; pTemp1 = 1 * pTemp
        if (nCount == 1):
            k = self.mySingleEXPCheck(dTemp, i)
            if ( k <= 0 ):
                return False
            j = self.myEXP2LengendreC(dA, dT, dTm, i, pTemp)
            if (j < 0 ):
                return False
            pTemp2 = aa
            pTemp2[k:i] = pTemp[k:i] # for(j=k;j<i;j++){ pTemp2[j] = pTemp[j];} // do copy
        else:
            # correct for two exp
            if(myABS(pFit[0]) > myABS(pFit[2])):
                dTemp = myABS(pFit[2]/pFit[0]);
                if(dTemp < 30): # treat as single,  pFit[0], pFit[1]
                    dTemp = pFit[1]/dTm; k = self.mySingleEXPCheck(dTemp, i)
                    if (k<=0):
                        return False
                else: # treat as ddd,
                    k = self.myDoubleEXPCheck(pFit, i, dTm)
                    if (k<=0):
                        return False
            else:
                if(pFit[2] == 0): # both A are zero
                    return False
                else:
                    dTemp = myABS(pFit[0]/pFit[2])
                    if (dTemp < 30): # treat as single,  pFit[2], pFit[3]
                        dTemp = pFit[3]/dTm; k = self.mySingleEXPCheck(dTemp, i)
                        if (k<=0):
                            return False
                    else: # treat as ddd,
                        k = self.myDoubleEXPCheck(pFit, i, dTm)
                        if (k<=0):
                            return False
            # set k for copy starting
            j = self.myEXP2LengendreC(pFit[0], pFit[1], dTm, i, pTemp)
            if (j<0):
                return False
            j = self.myEXP2LengendreC(pFit[2], pFit[3], dTm, i, pTemp1)
            if (j<0):
                return False
            pTemp2 = aa
            pTemp2[k:i] = pTemp[k:i] + pTemp1[k:i] # for(j=k;j<i;j++){ pTemp2[j] = pTemp[j] + pTemp1[j];} // do copy
        return True

    ##################################################    
    # End of Classs MY_LL_FIT
    ##################################################

def myEXP_LL_Fit(x, para, dyda, mySelf=None):
    if mySelf <> None:
        y = mySelf.pUser.myLegendre_0(x, para, dyda)
    else:
        y = 0
    return y

def myEXP_LL_Range(para, mySelf=None):
    #// A1 T1 A2 T2 Offset
    if(para[1]<=0):
        para[1]=1e-17
    if(para[3]<=0):
        para[3]=1e-17
    if mySelf==None:
        return

class MY_LM_FIT_Conv(object):
    def __init__(self, rData = None):
        self.gl_nCount_save = -1; self.nCountA = MY_EXP_PAR_COUNT + 2
        #Self.pWork, *pWork2;
        self.gl_z = 0.0; #*gl_r,    *gl_fr,    *gl_fr_img;     // nx * 2
        self.rDataSave = None
        #*rDataSave;
        #*gl_dfda, *gl_fdfda;  // na * nx * 2
        #*gl_y,    *gl_fy;     // na * nx * 2
        self.gl_nCount = 0; self.gl_nCount2 = 0; self.ex_nIndex_i = 0
        self.pLMFIT = None
        if rData <> None:
            self.mySetRes(rData)
    
    def mySetRes(self, rData, nLen = None):
        if nLen == None:
            nLen = rData.size
        self.gl_nCount = nLen
        self.rDataSave = rData
        self.myInit()
        
    def myResetMem(self, i):
        # i=0, direct release, i=1 check and release
        if (i==1):
            if(self.gl_nCount == self.gl_nCount_save):
                return
        self.pWork=None; self.pWork2=None

    #//---------------------------------------------------------------------------
    #//   User Define Function
    #//   Y = A1 *exp(- t / T1)+ A2 *exp(- t / T2) + A3* exp(- t / T3) + A4;
    #//   dy/dA1 = exp(- t / T1);  dy/dA2 = exp(- t / T2);  dy/dA3 = exp(- t / T3);
    #//   dy/dA4 = 1;
    #//   dy/dT1 = A1 * (t / T1 / T1) * exp(- t / T1);
    #//   dy/dT2 = A2 * (t / T2 / T2) * exp(- t / T2);
    #//   dy/dT3 = A3 * (t / T3 / T3) * exp(- t / T3);
    #//---------------------------------------------------------------------------
    #// gl_nIndex_i == 0 first time
    #// cal:    y = f * r = ifft(fft(f) . fft(r));
    #//      dyda = ifft( fft(dfda) . fft(r) );
    #//      return y(1), dyda(1)
    #// gl_nIndex_i >0
    #//      return y(.), dyda(.)
    
    def myInit(self):
        if (self.gl_nCount <= 0 or (not hasattr(self, 'rDataSave'))):
            return
        ii = self.gl_nCount; self.gl_nCount2 = ii * 2;
        #myResetMem(1)
        self.pWork  = np.zeros([3, ii])
        self.pWork2 = 1.0j * np.zeros([2, ii])

        self.gl_nCount_save = self.gl_nCount;
        self.rr_gl_nCount   = np.arange(self.gl_nCount)

        self.gl_z    = self.pWork[0]
        self.gl_y    = self.pWork[1];    self.gl_fy    = self.pWork2[0]
        self.gl_r    = self.pWork[2];    self.gl_fr    = self.pWork2[1]
        
        self.gl_dfda = np.zeros([5, ii]);   self.gl_fdfda = 1.0j * np.zeros([5, ii]);
        
        self.gl_fr_img = self.gl_fr.imag

        # Calculate for fft(R)
        self.gl_fr[:] = np.fft.fft(self.rDataSave)
        
    def myEXP2(self, x, para, dyda):
        #para 0  1  2  3  4
        #     A1 T1 A2 T2 Off
        dtmpB = x / para[1];       dyda[0] = np.exp(-dtmpB)
        dtmpA = para[0] * dyda[0]; y       = dtmpA
        dyda[1] = dtmpA * dtmpB / para[1]
        
        dtmpB = x / para[3];       dyda[2] = np.exp(-dtmpB) 
        dtmpA = para[2] * dyda[2]; y       = y + dtmpA
        dyda[3] = dtmpA * dtmpB / para[3]
        y = y + para[4]
        dyda[4] = 1
        return y
                
    def myConv2fr(self, A, fA):
        fA[:] = np.fft.fft(A)
        Z = np.abs(np.fft.ifft(fA * self.gl_fr))
        return Z
    
    def  myEXP2_conv(self, x, para, dyda):
        self.ex_nIndex_i = self.pLMFIT.nCurIndex
        if(self.ex_nIndex_i == 0):
            #first time, loop gl_nCount
            ex_pX1 = self.pLMFIT.pdIn_X
            for i in self.rr_gl_nCount:
                self.gl_y[i] = self.myEXP2(ex_pX1[i], para, dyda)
                self.gl_dfda[:,i] = dyda
            #cal:    y = f * r = ifft(fft(f) . fft(r));
            self.gl_y[:] = self.myConv2fr(self.gl_y, self.gl_fy);
            for j in xrange(5):
                self.gl_dfda[j] = self.myConv2fr(self.gl_dfda[j], self.gl_fdfda[j])
        i = self.ex_nIndex_i
        y = self.gl_y[i]
        dyda[:] = self.gl_dfda[:,i]
        return y
        
    ##################################################    
    # End of Classs MY_LM_FIT_Conv
    ##################################################
    
def myEXP_LM_Fit_Conv(x, para, dyda, mySelf=None):
    if mySelf <> None:
        y = mySelf.pUser.myEXP2_conv(x, para, dyda)
    else:
        y = 0
    return y    

def myEXP_LM_Range_Conv(para, mySelf=None):
    # A1 T1 A2 T2 A3 T3 Offset
    if(para[1]<=0):
        para[1]=1e-17
    if(para[3]<=0):
        para[3]=1e-17
    if mySelf==None:
        return

class MyLMFIT(object):
    def __init__(self, nCountPar, pFitFun=None, pRangeCheckFun=None):
        self.mySetParaCount(nCountPar); self.mySetFitFun(pFitFun, pRangeCheckFun)
        self.test = 0
    
    def mySetFitFun(self, _F, _R):
        self.UserFun_Fit = _F; self.UserFun_Range= _R
        
    def mySetParaCount(self, ii):        
        self.nCountPar = ii; self.pdAlpha = np.zeros([ii,ii]); self.pdCovar = np.zeros([ii,ii])
        self.pAtry     = np.zeros(ii); self.pBeta   = np.zeros(ii)
        self.pValdA    = np.zeros(ii); self.pDyda   = np.zeros(ii)
        self.DI        = np.diag_indices(ii)
  
        
    def mySetData(self, xData, yData, nCount=None):        
        self.pdIn_X = myNdArray1D(xData); self.pdIn_Y = myNdArray1D(yData)
        if not nCount:
            nCount = self.pdIn_X.size
        self.nCountDat = np.min([self.pdIn_X.size, self.pdIn_Y.size, nCount])
        #print 'data length=%d'%(self.nCountDat)
        
    def mySetParaAll(self, dFitStart, nFitSwitch):
        self.pPara = 1 * myNdArray1D(dFitStart); np1 = 1 * myNdArray1D(nFitSwitch)
        np1[np1<>0]= 1; self.nPara = np1
        #print 'start: %s'%myNd2Str("%.2f", self.pPara)
        #print 'FitSwitch: %s'%myNd2Str("%d", self.nPara)
        
    def myCheckWeight(self):
        if self.pdWeight.size < self.nCountDat:
            self.pdWeight = np.concatenate((self.pdWeight, np.zeros(self.nCountDat-self.pdWeight.size)), axis=1) # extend
        self.nCountWeightSave=self.nCountDat
        
    def mySetWeightToOne(self):
        self.pdWeight = np.ones(self.nCountDat); self.myCheckWeight()
    
    def mySetWeight(self, dWeight):
        self.pdWeight = myNumpyArray(dWeight); self.myCheckWeight()
        
    def myCovReshape(self, ppCov, nCount, nFitSwitch, nFitCount):
        # this function only enters for the last time, to shape the output
        for i in xrange(nFitCount, nCount):
            for j in xrange(i):
                ppCov[i,j]=0; ppCov[j,i]=0
        k=nFitCount - 1;
        for j in xrange(nCount-1, -1, -1):
            if (nFitSwitch[j]):
                for i in xrange(nCount):
                    fTemp=ppCov[i][k]; ppCov[i][k]= ppCov[i][j]; ppCov[i][j]=fTemp
                for i in xrange(nCount):
                    fTemp=ppCov[k][i]; ppCov[k][i]= ppCov[j][i]; ppCov[j][i]=fTemp
                k = k - 1
    
    def myGetFitResult(self, pFitA, pFitErr = None):
        j = 1.0 * (self.nCountDat - self.nCountFit)
        pFitA[:] = self.pPara
        if pFitErr <> None:
            for i in xrange(self.nCountPar):
                if(self.nPara[i]<>0 and j>0):
                    pFitErr[i] = sqrt(myABS(self.dChiFun * self.pdCovar[i,i]/j))
                else:
                    pFitErr[i] = 0
    
    def myGaussJ_ex(self, a, n, b, m):
        ppValpL = a; ppValpR = b;
        pnIndex = np.arange(n); pnIndexT = 1*pnIndex
        pnIndeR = 1*pnIndex;    pnIndeC  = 1*pnIndex
        
        for i in xrange(n):
            #dBig, ii = myMax(np.abs(ppValpL))
            #nRow = ii[0]; nCol = pnIndex[ii[1]];
            dBig = ppValpL[pnIndexT[i], pnIndex[i]]
            nRow=i; nCol=i; pnIndeR[i] = pnIndexT[i]; pnIndeC[i] = pnIndex[i]
            for j in xrange(i, n):
                for k in xrange(i, n):
                    dTemp = myABS(ppValpL[pnIndexT[j], pnIndex[k]])
                    if (dTemp > dBig):
                        nRow = j; nCol = k;
                        dBig = dTemp; pnIndeR[i] = pnIndexT[j]; pnIndeC[i] = pnIndex[k]
            if (nRow <> i):
                nTemp = pnIndexT[nRow]; pnIndexT[nRow] = pnIndexT[i]; pnIndexT[i]= nTemp
                
            if (nCol <> i):
                nTemp = pnIndex[nCol]; pnIndex[nCol] = pnIndex[i]; pnIndex[i]= nTemp
            dTemp = ppValpL[pnIndexT[i], pnIndex[i]]
            if (dTemp == 0.0):
                return
            dTemp=1.0/dTemp;  nTempT = pnIndexT[i]; nTemp = pnIndex[i]; ppValpL[nTempT, nTemp] = 1
            for j in xrange(n):
                ppValpL[nTempT, pnIndex[j]] = ppValpL[nTempT, pnIndex[j]] * dTemp
            for j in xrange(m):
                ppValpR[nTempT, j] = ppValpR[nTempT, j] * dTemp
            for j in xrange(n):
                if (j==nTempT):
                    continue
                dTemp = ppValpL[j, nTemp]; ppValpL[j, nTemp]=0.0
                for k in xrange(n):
                    l=pnIndex[k]; ppValpL[j, l] = ppValpL[j, l] - ppValpL[nTempT, l] * dTemp
                for k in xrange(m):
                    ppValpR[j,k] = ppValpR[j,k] - ppValpR[nTempT,k] * dTemp
                    
        pnIndex = np.arange(n); pnIndexT = 1 * pnIndex
        for i in xrange(n):
            k = pnIndex[pnIndeR[i]]; l = pnIndeC[i]
            if(k<> l):
                nTemp = pnIndexT[l];  pnIndexT[l]=pnIndexT[k];  pnIndexT[k]=nTemp
                pnIndex[pnIndexT[l]]=l; pnIndex[pnIndexT[k]]=k
                dTemp = 1 * a[k]; a[k] = a[l]; a[l]=dTemp
                dTemp = 1 * b[k]; b[k]=b[l]; b[l]= dTemp
            pnIndeC[i]=l; pnIndeR[i]=k
        for i in xrange(n-1,-1,-1):
            k = pnIndeR[i]; l = pnIndeC[i]
            if( k <> l ):
                dTemp = 1 * a[:, k]; a[:, k]=a[:, l]; a[:, l]= dTemp


    def myLM_Min_exx(self, pPara_ex, ppAlpha_ex, pBeta_ex):
        dChiX = 0
        for j in xrange(self.nCountFit):
            ppAlpha_ex[j, 0:j+1] = 0
        pBeta_ex[:]=0;
        for i in xrange(self.nCountDat):
            self.nCurIndex = i
            dModOut = self.UserFun_Fit(self.pdIn_X[i], pPara_ex , self.pDyda, self)
            dSig   = self.pdWeight[i]
            dDelta = self.pdIn_Y[i] - dModOut; j=0
            for l in xrange(self.nCountPar):
                if (self.nPara[l]) :
                    dWT = self.pDyda[l] * dSig; k=0
                    for m in xrange(l+1):
                        if (self.nPara[m]):
                            ppAlpha_ex[j, k] = ppAlpha_ex[j, k] + dWT * self.pDyda[m];k=k+1
                    pBeta_ex[j] = pBeta_ex[j] + dDelta * dWT; j=j+1
            dChiX = dChiX + dDelta*dDelta*dSig
        for j in xrange(1, self.nCountFit):
            ppAlpha_ex[:j,j]=ppAlpha_ex[j,:j]  # lower to uper              
        #print 'dChiX = %f'%(dChiX)
        if hasattr(self, 'disp'):
            print ('.'),#print('.', end="")
        return dChiX
        
    def myLM_Min_ex(self):
        if (self.dlamdaFun < 0.0): # We use a 0 value to Initialize the starting point
            self.nCountFit = 0;
            for j in xrange(self.nCountPar):
                if(self.nPara[j]):
                    self.nCountFit = self.nCountFit + 1
            self.dlamdaFun = 1; self.dlamda_ex = 1
            self.dChi_ex   = self.myLM_Min_exx(self.pPara, self.pdAlpha, self.pBeta)
            self.dChiFun   = self.dChi_ex
            self.pAtry[:]  = self.pPara
            self.ppOnedA   = self.pValdA.reshape(-1,1)
            if hasattr(self, 'disp'):
                print('Wait'),
            
        for j in xrange(self.nCountFit):
            self.pdCovar[j, :self.nCountFit]=self.pdAlpha[j, :self.nCountFit]            
        self.pdCovar[self.DI] = self.pdAlpha[self.DI] * (1.0+(self.dlamdaFun))
        self.pValdA[:]=self.pBeta                

        self.myGaussJ_ex(self.pdCovar, self.nCountFit, self.ppOnedA, 1)
        if (self.dlamdaFun == 0.0):
            self.myCovReshape(self.pdCovar, self.nCountPar, self.nPara, self.nCountFit)
            if hasattr(self, 'disp'):
                print;print('Finished !')
            return # Once converged, evaluate covariance matrix.
        
        #Did the trial succeed?
        j=0;
        for l in xrange(self.nCountPar):
            if (self.nPara[l]):
                self.pAtry[l] = self.pPara[l] + self.pValdA[j]; j=j+1
        #///////////////////////////////////////////////////////////////////////////////
        self.UserFun_Range(self.pAtry, self);
        #///////////////////////////////////////////////////////////////////////////////
        self.dChiFun= self.myLM_Min_exx(self.pAtry, self.pdCovar, self.pValdA)
        
        if (self.dChiFun < self.dChi_ex):
            self.dlamda_ex = self.dlamdaFun
            self.dlamdaFun = self.dlamdaFun * 0.2; self.dChi_ex = self.dChiFun
            self.pBeta[:]=self.pValdA 
            for j in xrange(self.nCountFit):
                for k in xrange(self.nCountFit):
                    self.pdAlpha[j, k]=self.pdCovar[j, k]
            self.pPara[:]=self.pAtry
        else:
            if  (self.dlamdaFun > self.dlamda_ex):#{ // last time is here      AAA
                self.dlamda_ex = self.dlamdaFun; self.dlamdaFun = self.dlamdaFun * 10.0
            elif(self.dlamdaFun < self.dlamda_ex):#{ // last time is in //Success, or in CCC,    BBB
                if( self.dlamdaFun * 4 > self.dlamda_ex):#{  //last time is in CCC,
                    self.dlamda_ex = self.dlamdaFun; self.dlamdaFun = self.dlamdaFun * 5.0
                else:#{   // last time is in //Success,
                    self.dlamda_ex = self.dlamdaFun; self.dlamdaFun = self.dlamdaFun * 5.0

            else:#{ // first time or last time, it is wrong, maybe dlamdaFun is too big,  CCC
                self.dlamda_ex = self.dlamdaFun; self.dlamdaFun = self.dlamdaFun / 2.0
            self.dChiFun = self.dChi_ex
        
    def myLM_Min_ex2(self):
        if (self.dlamdaFun < 0.0): # We use a 0 value to Initialize the starting point
            self.nCountFit = 0;
            for j in xrange(self.nCountPar):
                if(self.nPara[j]):
                    self.nCountFit = self.nCountFit + 1
            self.dlamdaFun = 1; self.dlamda_ex = 1
            self.dChi_ex   = self.myLM_Min_exx(self.pPara, self.pdAlpha, self.pBeta)
            self.dChiFun   = self.dChi_ex
            self.pAtry[:]  = self.pPara
            self.ppOnedA   = self.pValdA.reshape(-1,1)
            if hasattr(self, 'disp'):
                print ('Wait'),
            
        for j in xrange(self.nCountFit):
            self.pdCovar[j, :self.nCountFit]=self.pdAlpha[j, :self.nCountFit]            
        self.pdCovar[self.DI] = self.pdAlpha[self.DI] * (1.0+(self.dlamdaFun))
        self.pValdA[:]=self.pBeta                

        self.myGaussJ_ex(self.pdCovar, self.nCountFit, self.ppOnedA, 1)
        if (self.dlamdaFun == 0.0):
            self.myCovReshape(self.pdCovar, self.nCountPar, self.nPara, self.nCountFit)
            if hasattr(self, 'disp'):
                print;print('Finished !')
            return # Once converged, evaluate covariance matrix.
        
        #Did the trial succeed?
        j=0;
        for l in xrange(self.nCountPar):
            if (self.nPara[l]):
                self.pAtry[l] = self.pPara[l] + self.pValdA[j]; j=j+1
        #///////////////////////////////////////////////////////////////////////////////
        self.UserFun_Range(self.pAtry, self);
        #///////////////////////////////////////////////////////////////////////////////
        self.dChiFun= self.myLM_Min_exx(self.pAtry, self.pdCovar, self.pValdA)
        if (self.dChiFun < self.dChi_ex):
            self.dlamda_ex = self.dlamdaFun
            self.dlamdaFun = self.dlamdaFun * 0.1; self.dChi_ex = self.dChiFun
            self.pBeta[:]=self.pValdA 
            for j in xrange(self.nCountFit):
                for k in xrange(self.nCountFit):
                    self.pdAlpha[j, k]=self.pdCovar[j, k]
            self.pPara[:]=self.pAtry
        else:
            self.dlamdaFun = self.dlamdaFun * 10; self.dChiFun = self.dChi_ex
            
    def myLM_Min(self):
        i = 0            
        if  (not hasattr(self, 'pdIn_Y')) or (not hasattr(self, 'pdIn_X')) or (self.nCountDat <=0) or (self.nCountPar <=0):
            i = -1; return (i, 0)
        if not hasattr(self, 'pdWeight'):
            self.mySetWeightToOne()
        if (self.nCountDat > self.nCountWeightSave):
            i = -1; return (i, 0)
            
        self.dlamdaFun = -1; self.myLM_Min_ex();
        dChi = self.dChiFun; dLamda = self.dlamdaFun; i=0; j=0;
        while(self.dlamdaFun < MY_MAX_LAMDA and i < MY_MAX_TIMES_A and j < MY_MAX_TIMES_B):
            self.myLM_Min_ex()
            if(dLamda < self.dlamdaFun): # On success, dlamda_ex will reduce 1/10 and we also monitor this
                j=j+1
            else:
                j=0
            dLamda = self.dlamdaFun; i=i+1
        dChi = self.dChiFun; dLamda = self.dlamdaFun;
        self.dlamdaFun = 0; self.myLM_Min_ex()
        return(i, dChi)
    
    def myLM_Min2(self):
        i = 0
        if  (not hasattr(self, 'pdIn_Y')) or (not hasattr(self, 'pdIn_X')) or (self.nCountDat <=0) or (self.nCountPar <=0):
            i = -1; return (i, 0)
        if not hasattr(self, 'pdWeight'):
            self.mySetWeightToOne()
        if (self.nCountDat > self.nCountWeightSave):
            i = -1; return (i, 0)
            
        self.dlamdaFun = -1; self.myLM_Min_ex2();
        dChi = self.dChiFun; dLamda = self.dlamdaFun; i=0; j=0;
        while(self.dlamdaFun < MY_MAX_LAMDA and i < MY_MAX_TIMES_A and j < MY_MAX_TIMES_B):
            self.myLM_Min_ex2()
            if(dLamda < self.dlamdaFun): # On success, dlamda_ex will reduce 1/10 and we also monitor this
                j=j+1
            else:
                j=0
            dLamda = self.dlamdaFun; i=i+1
        dChi = self.dChiFun; dLamda = self.dlamdaFun;
        self.dlamdaFun = 0; self.myLM_Min_ex2()
        return(i, dChi)
    
    ##################################################    
    # End of Classs MyLMFIT
    ##################################################

def myFitParaCheck(F): #return 0 / 1 int value for fit
    F = np.array(F, dtype=np.int16).reshape(-1);
    F[np.where(F<>0)] = 1;
    return F

def myGetExpCount(nFit_fit):
    nFitCount = 0
    if(nFit_fit[0]<>0 or nFit_fit[1]<>0):
        nFitCount = 1
    if(nFit_fit[2]<>0 or nFit_fit[3]<>0):
        nFitCount |= 2
    return nFitCount

def myGenExpStart_LL(pIn, Tm, nFit_fit, nExpCount=-1):
    # guess A0, T0, A1, T1, Offset for LL fit
    pdOut = np.zeros(MY_EXP_PAR_COUNT)
    if(nExpCount<0 or nExpCount>2):
        nExp = myGetExpCount(nFit_fit)
    else:
        nExp = nExpCount
    if nExp==1:
        pdOut[2] = 0;   pdOut[3] = 1;   pdOut[0] = myABS(pIn[1]); pdOut[1] = Tm;              pdOut[4] = pIn[0] + pIn[1]
    elif nExp==2:
        pdOut[0] = 0;   pdOut[1] = 1;   pdOut[2] = myABS(pIn[1]); pdOut[3] = Tm;              pdOut[4] = pIn[0] + pIn[1]
    elif nExp==3:
        pdOut[0] = myABS(pIn[1])/2;       pdOut[1] = Tm;        pdOut[2] = myABS(pIn[1])/2;   pdOut[3] = Tm * 1.7;  pdOut[4] = pIn[0] + pIn[1]
    else:
        pdOut[0] = 0;   pdOut[1] = 1;   pdOut[2] = 0;           pdOut[3] = 1;               pdOut[4] = pIn[0]
    return pdOut
  
def myGenExpStart(pIn):
    #Guess a simple initial value for EXP fitting
    pdOut = np.zeros(MY_EXP_PAR_COUNT);dLen=pIn.size;
    if dLen >=3:
        pdOut[4] = pIn[-1];
        if  dLen > 50:
            T0 = 10; pdOut[0] = (pIn[0] + pIn[9] + pIn[18]) / 4; dVal = pIn[T0]-pIn[T0+10]
            if dVal<>0:
                pdOut[1] = sqrt(myABS(10.0 * (pIn[T0+5]-pdOut[4]) * (T0 + 5.0) / dVal));pdOut[3] = pdOut[1] * 2;
            else:
                dVal = pIn[T0]-pIn[T0+30]
                if dVal<>0:
                    pdOut[1] = sqrt(myABS(10.0 * (pIn[T0+5]-pdOut[4]) * (T0 + 5.0) / dVal));pdOut[3] = pdOut[1] * 2;
                else:
                    pdOut[1] = dLen / 10.0; pdOut[3] = pdOut[1] * 5;
        else:
            pdOut[0] = (pIn[0] + pIn[1] + pIn[2]) / 4;
            pdOut[1] = dLen / 10.0;
            pdOut[3] = pdOut[1] * 2;
    return pdOut

def myGenExpStart_Conv(pIn, pInR):
    pdOut = np.zeros(MY_EXP_PAR_COUNT)
    llLen = pIn.size
    if(llLen<3):
        return pdOut   
    pdOut[4] = pIn[-3].sum()
    dLen     = pInR[-3].sum()
    if dLen<>0:
        pdOut[4] = pdOut[4]/dLen
    pdOut[2] = 0
    if(llLen > 50):
        ni = int(llLen/50)
    else:
        ni = 1
    rr = np.arange(0,llLen,ni); pIn2=pIn[rr]
    dMax, nMax = myMax(pIn2); nMax = rr[nMax]
    dSum = pIn2.mean()
    rr2 = np.where(pIn2>dSum)
    pdOut[0] = (dMax - pIn2.min()) * 1.1
    if dLen<>0:
        pdOut[0] = pdOut[0]/dLen
    pdOut[1] = np.array(rr2).size; pdOut[3] = pdOut[1] * ni * 5
    return pdOut

def myLegendre_P(nPoint=1000, nFact=10):
    # this function is similar to makeLP_rec, and no need scipy support 
    P = np.zeros((nFact, nPoint)); X =  np.zeros(nPoint)
    j=nPoint-1; dTemp1 = 2.0/j; dTemp2 =-1
    for i in xrange(nPoint):
        X[i] =dTemp2; dTemp2 = dTemp2 + dTemp1
    X[j] = 1
    if nFact>0:
        P[0,:] = np.ones(nPoint)
    if nFact>1:
        P[1,:] = X
    if nFact>2:
        pdTemp1 = P[0,:]
        for j in xrange(2, nFact):
            pdTemp2 = P[j-1,:]; pdTemp = P[j,:]; n = j-1
            pdTemp[:]  = ( (2*n+1) * X[:]  * pdTemp2[:]  - n * pdTemp1[:] )/(n+1)
            pdTemp1 = pdTemp2
    return P, X

def lmFit(x, para, dyda, mySelf=None):
    #//---------------------------------------------------------------------------
    #//  *User Define Function
    #//      Y = A1 * exp(- t / T1)+ A2 * exp(- t / T2) + A3;
    #//      dy/dA1 = exp(- t / T1);   dy/dA2 = exp(- t / T2); dy/dA3 = 1;
    #//      dy/dT1 = A1 * (t / T1 / T1) * exp(- t / T1);
    #//      dy/dT2 = A2 * (t / T2 / T2) * exp(- t / T2);
    #//  *para 0 ~ 4 : A1 T1 A2 T2 A3
    #//---------------------------------------------------------------------------
    dtmpB = x / para[1]; dyda[0] = np.exp(-dtmpB); dtmpA = para[0] * dyda[0]; y = dtmpA
    dyda[1] = dtmpA * dtmpB / para[1]
    dtmpB = x / para[3]; dyda[2] = np.exp(-dtmpB); dtmpA = para[2] * dyda[2]; y = y + dtmpA
    y = y + para[4]
    dyda[3] = dtmpA * dtmpB / para[3]
    dyda[4] = 1
    return y

def lmFitRange(para, mySelf=None):
    if(para[1]<=0):
        para[1]=1e-17
    if(para[3]<=0):
        para[3]=1e-17
    if not mySelf:
        return
    
def myFitEXP_LM(Y, F=[1,1,0,0,0], S=None):
    # Normal LM fit for Single and Double EXP curves
    # F should be only 1 and 0
    F = myFitParaCheck(F)
    # Generate Fiting initial, if not given
    if not S:
        S = myGenExpStart(Y)

    #Prepare LM fitting functions
    lm = MyLMFIT(MY_EXP_PAR_COUNT, lmFit, lmFitRange)
    lm.disp = 1
    #Set data and initial/Switch for fitting
    xData = 1.0 * np.arange(1, Y.size + 1)
    lm.mySetData(xData, Y)
    lm.mySetParaAll(S, F)
    #Fitting
    (j, dChi) = lm.myLM_Min()
    #Calculate the fitting error
    dFitResult = np.zeros(MY_EXP_PAR_COUNT); dFitError  = np.zeros(MY_EXP_PAR_COUNT)
    lm.myGetFitResult(dFitResult, dFitError)
    return (dChi, j, dFitResult, dFitError)

def myFitEXP_LM_Conv(Y, R, F=[1,1,0,0,1], S=None):
    # LM fit for EXP curves converluting with a system response function
    # F should be only 1 and 0
    F = myFitParaCheck(F)
    # Generate Fiting initial, if not given
    if not S:
        S = myGenExpStart_Conv(Y, R)
    #print np.array(S)
    
    #Prepare Converlution for R
    lmfit_conv = MY_LM_FIT_Conv(R)
    #Prepare LM fitting functions
    lm = MyLMFIT(MY_EXP_PAR_COUNT, myEXP_LM_Fit_Conv, myEXP_LM_Range_Conv)
    #Save objects for internal calling
    lm.pUser = lmfit_conv; lmfit_conv.pLMFIT = lm
    lm.disp = 1
    #Set data and initial/Switch for fitting
    xData = 1.0 * np.arange(1, Y.size + 1)
    lm.mySetData(xData, Y)
    lm.mySetParaAll(S, F)
    #Fitting
    (j, dChi) = lm.myLM_Min2()
    #Calculate the fitting error
    dFitResult = np.zeros(MY_EXP_PAR_COUNT); dFitError  = np.zeros(MY_EXP_PAR_COUNT)
    lm.myGetFitResult(dFitResult, dFitError)
    return (dChi, j, dFitResult, dFitError)
    
def myMean_ex(Y):
    Y1 = Y.reshape(-1)
    return (Y1[:-1] + Y1[1:])/2.0

def myLegendre_A2(Y, nCount, P=None, NoFilterOut=None):
    # this function is similar to LT, and add the filter out if NoFilterOut is not set
    nPoint = Y.size
    if P == None:
        bNewP = 1
    else:
        if P.shape[0]<nCount:
            bNewP = 1
        else:
            bNewP = 0
    if bNewP == 1:
        P, X = myLegendre_P(nPoint, nCount) 
    A = np.zeros(nCount)
    for l in xrange(nCount):
        A[l]  = (2.0*l + 1.0)*(Y*P[l,:]).sum()/nPoint
    if NoFilterOut <> None:
        return A
    else:
        Y2 = A.dot(P[:nCount])
        return A, Y2
    
def myLegendre_A(Y, nCount, P=None, NoFilterOut=None):
    # this function uses middle value to calulate LT, it will give less error than myLegendre_A2
    # Test code:
    # A1, Y1 = myLegendre_A(Y, 5)
    # A2, Y2 = myLegendre_A2(Y, 5)
    # print np.array((Y-Y1).sum()), np.array((Y-Y2).sum())
    #
    nPoint = Y.size
    if P == None:
        bNewP = 1
    else:
        if P.shape[0]<nCount:
            bNewP = 1
        else:
            bNewP = 0
    if bNewP == 1:
        P, X = myLegendre_P(nPoint, nCount) 
    A = np.zeros(nCount); Y1 = myMean_ex(Y);
    nPoint2=nPoint-1; n1 = 2.0 / nPoint2; n2 = 1.0/nPoint2
    for l in xrange(nCount):
        A[l]  = (n1*l + n2)*(Y1*myMean_ex(P[l,:])).sum()
    if NoFilterOut <> None:
        return A
    else:
        Y2 = A.dot(P[:nCount])
        return A, Y2

def myFitEXP_LL(Y, Tm, F=[1,1,0,0,0], S=None):
    # F should be only 1 and 0
    F = myFitParaCheck(F)
    # Single or Double EXP, or even more for future multi-EXP curves
    nExpCount = myGetExpCount(F)
    # Generate Fiting initial, if not given
    if not S:
        S = myGenExpStart_LL(Y, Tm, F, nExpCount) #aa, Tm, nFit_fit, nExpCount
    #print S
    
    #Prepare Legendre Functions in terms of Tm
    llfit = MY_LL_FIT(Tm)
    #Prepare LM fitting functions
    lm    = MyLMFIT(MY_EXP_PAR_COUNT, myEXP_LL_Fit, myEXP_LL_Range)
    lm.pUser = llfit
    
    #Set the X and Y data for fitting
    xData = 1.0 * np.arange(Y.size); yData = 1.0 * Y
    lm.mySetData(xData, yData)
    lm.mySetParaAll(S, F)
    
    #Fitting and calcualte the result for real decay time
    (j, dChi) = lm.myLM_Min2()
    dFitResult = np.zeros(MY_EXP_PAR_COUNT)
    lm.myGetFitResult(dFitResult)
    if(llfit.myCheckAndCorrect(yData, nExpCount, dFitResult, Tm)):
        lm.mySetData(xData, yData); j=100
    
    #In case we change the time scale, fit again for calculating the real error
    if(j>=100):
        lm.mySetParaAll(dFitResult, F)
        (j, dChi) = lm.myLM_Min()
        
    #Calculate the fitting error
    dFitError  = np.zeros(MY_EXP_PAR_COUNT)
    lm.myGetFitResult(dFitResult, dFitError)
    return (dChi, j, dFitResult, dFitError)
        
def myUnmixing(Y, P, INV = None):
    # Y should be 1-dim, P should be 2-dim with the last (or the 2nd) dim same as Y
    nm   = P.shape

    # we prepare the starting arrays for unmixing
    ppdY = np.zeros([nm[0],1]);         ppdY[:, 0]=(Y*P).sum(1)
    ppdA = np.zeros([nm[0], nm[0]]);    ppdA[np.diag_indices(nm[0])] = (P*P).sum(1)
    rr = np.arange(nm[0])
    for i in rr:
        for j in rr[i+1:]:
            ppdA[j,i] = (P[i]*P[j]).sum()
            ppdA[i,j] = ppdA[j, i]
    
    # We unmix by calculating the maxtrix inverse using Gauss-Jodan method
    lm = MyLMFIT(nm[0])
    lm.myGaussJ_ex(ppdA, nm[0], ppdY, 1);
    
    # We calculate the left part
    pCurveL = np.zeros(nm[1]); pCurveL[:] = Y - ppdY.reshape(-1).dot(P)
    
    # We calculate the error of each component
    dSum = (pCurveL*pCurveL).sum()
    if (nm[0]<>nm[1]):
        dSum = dSum / (nm[1]-nm[0])
    pYD = np.zeros(nm[0]); pYD[:] = ((ppdA*ppdA).sum(0) * dSum)**0.5
    
    if INV==None:
        return dSum, ppdY.reshape(-1), pYD, pCurveL
    else:
        return dSum, ppdY.reshape(-1), pYD, pCurveL, ppdA
    

    
    
    

    