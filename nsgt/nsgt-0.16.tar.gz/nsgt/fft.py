'''
Created on 27.02.2014

@author: thomas
'''

import numpy as N
from warnings import warn

realized = False

if False and not realized:
    try:
        import pyfft.cl as pyfft_cl
    except ImportError:
        pyfft_cl = None
    
    if pyfft_cl is not None:
        # opencl fft # power-2 only, therefore not ready yet
        from pyfft_cl import Plan
        import pyopencl as cl
        import pyopencl.array as cl_array
        
        class fftpool:
            ctx = cl.create_some_context(interactive=False)
            queue = cl.CommandQueue(ctx)
    
            def __init__(self,measure,dtype=float):
                self.pool = {}
    
        class fftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def __call__(self,x,outn,ref):
                plan = Plan(x.shape, queue=fftpool.queue)
                gpu_data = cl_array.to_device(fftpool.ctx,fftpool.queue,x)
                plan.execute(gpu_data.data)
                result = gpu_data.get()
                return result
                
        class rfftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                pass
    
        class ifftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                pass
    
        class irfftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype   )
            def init(self,n,measure,outn):
                pass
            
        realized = True
        
        
if not realized:
    # try to use FFT3 if available, else use numpy.fftpack
    try:
        import fftw3
    except ImportError:
        fftw3 = None
    
    try:
        import fftw3f
    except ImportError:
        fftw3f = None

    if fftw3 is not None:
        # fftw3 methods
        class fftpool:
            def __init__(self,measure,dtype=float):
                self.measure = measure
                self.dtype = N.dtype(dtype)
                dtsz = self.dtype.itemsize
                if dtsz == 4:
                    self.tpfloat = N.float32
                    self.tpcplx = N.complex64
                    self.fftw = fftw3f
                elif dtsz == 8:
                    self.tpfloat = N.float64
                    self.tpcplx = N.complex128
                    self.fftw = fftw3
                else:
                    raise TypeError("nsgt.fftpool: dtype '%s' not supported"%repr(self.dtype))
                self.pool = {}
                
            def __call__(self,x,outn=None,ref=False):
                lx = len(x)
                try:
                    transform = self.pool[lx]
                except KeyError:
                    transform = self.init(lx,measure=self.measure,outn=outn)
                    self.pool[lx] = transform
                plan,pre,post = transform
                if pre is not None:
                    x = pre(x)
                plan.inarray[:] = x
                plan()
                if not ref:
                    tx = plan.outarray.copy()
                else:
                    tx = plan.outarray
                if post is not None:
                    tx = post(tx)
                return tx
    
        class fftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                inp = self.fftw.create_aligned_array(n,dtype=self.tpcplx)
                outp = self.fftw.create_aligned_array(n,dtype=self.tpcplx)
                plan = self.fftw.Plan(inp,outp, direction='forward', flags=('measure' if measure else 'estimate',))
                return (plan,None,None)
    
        class rfftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                inp = self.fftw.create_aligned_array(n,dtype=self.tpfloat)
                outp = self.fftw.create_aligned_array(n//2+1,dtype=self.tpcplx)
                plan = self.fftw.Plan(inp,outp, direction='forward', realtypes='halfcomplex r2c',flags=('measure' if measure else 'estimate',))
                return (plan,None,None)
    
        class ifftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                inp = self.fftw.create_aligned_array(n,dtype=self.tpcplx)
                outp = self.fftw.create_aligned_array(n,dtype=self.tpcplx)
                plan = self.fftw.Plan(inp,outp, direction='backward', flags=('measure' if measure else 'estimate',))
                return (plan,None,lambda x: x/len(x))
    
        class irfftp(fftpool):
            def __init__(self,measure=False,dtype=float):
                fftpool.__init__(self,measure,dtype=dtype)
            def init(self,n,measure,outn):
                inp = self.fftw.create_aligned_array(n,dtype=self.tpcplx)
                outp = self.fftw.create_aligned_array(outn if outn is not None else (n-1)//2,dtype=self.tpfloat)
                plan = self.fftw.Plan(inp,outp, direction='backward', realtypes='halfcomplex c2r', flags=('measure' if measure else 'estimate',))
                return (plan,lambda x: x[:n],lambda x: x/len(x))
            
        realized = True
        

if not realized:
    # fall back to numpy methods
    warn("nsgt.fft falling back to numpy.fft")
    
    class fftp:
        def __init__(self,measure=False,dtype=float):
            pass
        def __call__(self,x,outn=None,ref=False):
            return N.fft.fft(x)
    class ifftp:
        def __init__(self,measure=False,dtype=float):
            pass
        def __call__(self,x,outn=None,n=None,ref=False):
            return N.fft.ifft(x,n=n)
    class rfftp:
        def __init__(self,measure=False,dtype=float):
            pass
        def __call__(self,x,outn=None,ref=False):
            return N.fft.rfft(x)
    class irfftp:
        def __init__(self,measure=False,dtype=float):
            pass
        def __call__(self,x,outn=None,ref=False):
            return N.fft.irfft(x,n=outn)


import unittest

class TestFFT(unittest.TestCase):
    @staticmethod
    def rms(x):
        return N.sqrt(N.mean(N.square(N.abs(x))))

    def setUp(self):
        pass

    def test_rfft(self,n=1000):
        seq = N.random.random(n)
        ft = rfftp()
        a = ft(seq)
        b = N.fft.rfft(seq)
        self.assertAlmostEqual(self.rms(a-b),0)
    def test_irfft(self,n=1000):
        seq = N.random.random(n)+N.random.random(n)*1.j
        ft = irfftp()
        a = ft(seq)
        b = N.fft.irfft(seq)
        self.assertAlmostEqual(self.rms(a-b),0)
    def test_fft(self,n=1000):
        seq = N.random.random(n)
        ft = fftp()
        a = ft(seq)
        b = N.fft.fft(seq)
        self.assertAlmostEqual(self.rms(a-b),0)
    def test_ifft(self,n=1000):
        seq = N.random.random(n)+N.random.random(n)*1.j
        ft = ifftp()
        a = ft(seq)
        b = N.fft.ifft(seq)
        self.assertAlmostEqual(self.rms(a-b),0)

if __name__ == '__main__':
    unittest.main()
