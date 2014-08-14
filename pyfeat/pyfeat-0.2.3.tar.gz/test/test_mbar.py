import numpy as np
from unittest import TestCase, main
from pyfeat.estimator import MBAR
from pyfeat.estimator.mbar.ext import mbar_eq



class MbarTestCase( TestCase ):
    def test_ext_zeros_small( self ):
        nt = 10
        ns = 100
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        emf1 = np.ones( shape=(nt,), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        mbar_eq( emf1, eu_ijt, emf2 )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], 1.0, delta=1.0e-13 )
    def test_ext_zeros_large( self ):
        nt = 30
        ns = 10000
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        emf1 = np.ones( shape=(nt,), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        mbar_eq( emf1, eu_ijt, emf2 )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], 1.0, delta=1.0e-11 )
    def test_ext_zeros_small_random( self ):
        nt = 10
        ns = 100
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        emf1 = np.ones( shape=(nt,), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        n = np.random.randint( int( ns*0.8 ), high=int( ns-1 ), size=nt )
        mbar_eq( emf1, eu_ijt, emf2, n.astype( np.int32 ) )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], 1.0, delta=1.0e-13 )
    def test_ext_zeros_large_random( self ):
        nt = 30
        ns = 10000
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        emf1 = np.ones( shape=(nt,), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        n = np.random.randint( int( ns*0.8 ), high=int( ns-1 ), size=nt )
        mbar_eq( emf1, eu_ijt, emf2, n.astype( np.int32 ) )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], 1.0, delta=1.0e-11 )
    def test_ext_geom_small( self ):
        nt = 10
        ns = 100
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        f1 = np.array( range( nt ), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        mbar_eq( np.exp(f1), eu_ijt, emf2 )
        val = nt * ( 1.0 - np.exp(-1.0) ) / ( 1.0 - np.exp(-nt) )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], val, delta=1.0e-13 )
    def test_ext_geom_large( self ):
        nt = 30
        ns = 10000
        eu_ijt = np.ones( shape=(nt,nt,ns), dtype=np.float64 )
        f1 = np.array( range( nt ), dtype=np.float64 )
        emf2 = np.zeros( shape=(nt,), dtype=np.float64 )
        mbar_eq( np.exp(f1), eu_ijt, emf2 )
        val = nt * ( 1.0 - np.exp(-1.0) ) / ( 1.0 - np.exp(-nt) )
        for i in xrange( nt ):
            self.assertAlmostEqual( emf2[i], val, delta=1.0e-10 )

if '__main__' == __name__:

    main()
