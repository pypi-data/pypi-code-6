import numpy as np
from unittest import TestCase, main
from pyfeat.data.statelist import StateList
from pyfeat.exception.exception import NotConnectedSetError, MissingThermodynamicStatesError

class StateListSingleReplicaTestCase( TestCase ):
    def testZeros( self ):
        r"""
        Unit test with a single replica trajectory all containing zeros
        """
        replica = [ np.zeros(shape=(100,2),dtype=np.float64)]
        replica_length = np.ones(1,dtype=np.int32)*100
        states = StateList( 1, replica, replica_length, _skip_counting=True )
        self.assertEqual( 1, states.n_replicas )
        self.assertEqual( states.replica_width, replica[0].shape[1] )
        self.assertTrue( np.all( np.equal( states.replica_length, replica_length ) ) )
        self.assertEqual( replica_length.max(), states.max_replica_length )
        states.copy_states( replica )
        self.assertTrue( np.all( np.equal( replica[0][:,0], states.markov_state ) ) )
        self.assertTrue( np.all( np.equal( replica[0][:,1], states.therm_state ) ) )
        states.count_markov_states()
        self.assertEqual( 1, states.n_markov_states )
        self.assertEqual( 1, states.n_therm_states )
        self.assertTrue( np.all( np.equal( np.ones(1,dtype=np.int32)*100, states.markov_sample ) ) )
        self.assertEqual( 100, states.max_markov_samples )
        states.count_thermodynamic_states()
        self.assertEqual( 100, states.max_therm_samples )
        self.assertEqual( 1, states.therm_sample.shape[0] )
        self.assertEqual( 100, states.therm_sample[0] )
        self.assertEqual( 1, states.markov_sequence.shape[0] )
        self.assertEqual( 100, states.markov_sequence.shape[1] )
    def testRandom( self ):
        r"""
        Unit test with a single replica containing zeros with random length
        """
        replica_length = np.ones(1,dtype=np.int32)*np.random.randint(200,high=250,size=1)
        replica = [ np.zeros(shape=(replica_length,2),dtype=np.float64)]
        states = StateList( 1, replica, replica_length, _skip_counting=True )
        self.assertEqual( 1, states.n_replicas )
        self.assertEqual( states.replica_width, replica[0].shape[1] )
        self.assertTrue( np.all( np.equal( states.replica_length, replica_length ) ) )
        self.assertEqual( replica_length.max(), states.max_replica_length )
        states.copy_states( replica )
        self.assertTrue( np.all( np.equal( replica[0][:,0], states.markov_state ) ) )
        self.assertTrue( np.all( np.equal( replica[0][:,1], states.therm_state ) ) )
        states.count_markov_states()
        self.assertEqual( 1, states.n_markov_states )
        self.assertEqual( 1, states.n_therm_states )
        self.assertTrue( np.all( np.equal( np.ones(1,dtype=np.int32)*replica_length, states.markov_sample ) ) )
        self.assertEqual( replica_length, states.max_markov_samples )
        states.count_thermodynamic_states()
        self.assertEqual( replica_length[0], states.max_therm_samples )
        self.assertEqual( 1, states.therm_sample.shape[0] )
        self.assertEqual( replica_length[0], states.therm_sample[0] )
        self.assertEqual( 1, states.markov_sequence.shape[0] )
        self.assertEqual( replica_length[0], states.markov_sequence.shape[1] )
    def testMarkovException( self ):
        r"""
        Unit test for testing that an exception is thrown, when Markov states are not in a connected set
        """
        replica = [ np.zeros(shape=(100,2),dtype=np.float64)]
        replica[0][:,0] = np.ones(shape=(100,),dtype=np.float64)
        replica_length = np.ones(1,dtype=np.int32)*100
        states = StateList( 1, replica, replica_length, _skip_counting=True )
        states.copy_states( replica )
        self.assertRaises( NotConnectedSetError, states.count_markov_states )
    def testThermodynamicException( self ):
        r"""
        Unit test for testing that an exception is thrown, when Thermodynamic states are missing
        """
        replica = [ np.zeros(shape=(100,2),dtype=np.float64)]
        replica[0][:,1] = np.ones(shape=(100,),dtype=np.float64)
        replica_length = np.ones(1,dtype=np.int32)*100
        states = StateList( 1, replica, replica_length, _skip_counting=True )
        states.copy_states( replica )
        states.count_markov_states()
        self.assertRaises( MissingThermodynamicStatesError, states.count_thermodynamic_states )

class StateListMultipleReplicaTestCase( TestCase ):
    def testZeros( self ):
        r"""
        Unit test with several equally long trajectories with entries zero
        """
        num_replica = 3
        length = 100
        replica = [ np.zeros(shape=(length,2),dtype=np.float64), np.zeros(shape=(length,2),dtype=np.float64), np.zeros(shape=(length,2),dtype=np.float64) ]
        replica_length = np.ones(3,dtype=np.int32)*length
        states = StateList( num_replica, replica, replica_length, _skip_counting=True )
        self.assertEqual( num_replica, states.n_replicas )
        for i in xrange( num_replica ):
            self.assertEqual( states.replica_width, replica[i].shape[1] )
        self.assertTrue( np.all( np.equal( states.replica_length, replica_length ) ) )
        self.assertEqual( replica_length.max(), states.max_replica_length )
        states.copy_states( replica )
        states.count_markov_states()
        self.assertEqual( 1, states.n_markov_states )
        self.assertEqual( 1, states.n_therm_states )
        self.assertTrue( np.all( np.equal( np.ones(1,dtype=np.int32)*num_replica*length, states.markov_sample ) ) )
        self.assertEqual( num_replica*length, states.max_markov_samples )
        states.count_thermodynamic_states()
        self.assertEqual( num_replica*length, states.max_therm_samples )
        self.assertEqual( 1, states.therm_sample.shape[0] )
        self.assertEqual( num_replica*length, states.therm_sample[0] )
        self.assertEqual( 1, states.markov_sequence.shape[0] )
        self.assertEqual( num_replica*length, states.markov_sequence.shape[1] )
    def testRandom( self ):
        r"""
        Unit test with several trajectories with entries zero and random lengths
        """
        num_replica = np.random.randint( 3, high=10, size=1 )
        replica_length = np.random.randint( 200, high=300, size=num_replica )
        replica = []
        for i in xrange( num_replica ):
            replica.append( np.zeros( shape=(replica_length[i],2), dtype=np.float64 ) )
        states = StateList( num_replica, replica, replica_length, _skip_counting=True )
        self.assertEqual( num_replica, states.n_replicas )
        for i in xrange( num_replica ):
            self.assertEqual( states.replica_width, replica[i].shape[1] )
        self.assertTrue( np.all( np.equal( states.replica_length, replica_length ) ) )
        self.assertEqual( replica_length.max(), states.max_replica_length )
        states.copy_states( replica )
        states.count_markov_states()
        self.assertEqual( 1, states.n_markov_states )
        self.assertEqual( 1, states.n_therm_states )
        self.assertEqual( replica_length.sum(), states.markov_sample[0] )
        self.assertEqual( replica_length.sum(), states.max_markov_samples )
        states.count_thermodynamic_states()
        self.assertEqual( replica_length.sum(), states.max_therm_samples )
        self.assertEqual( 1, states.therm_sample.shape[0] )
        self.assertEqual( replica_length.sum(), states.therm_sample[0] )
        self.assertEqual( 1, states.markov_sequence.shape[0] )
        self.assertEqual( replica_length.sum(), states.markov_sequence.shape[1] )
    def testSequences( self ):
        r"""
        Unit test with several equally long trajectories with uniform state entries in each trajectory
        """
        num_replica = 5
        length = 10
        replica_length = np.ones( shape=(num_replica,), dtype=np.int32 ) * length
        replica = []
        for i in xrange( num_replica ):
            replica.append( np.ones( shape=(replica_length[i],2), dtype=np.float64 )*i )
        states = StateList( num_replica, replica, replica_length, _skip_counting=True )
        self.assertEqual( num_replica, states.n_replicas )
        for i in xrange( num_replica ):
            self.assertEqual( states.replica_width, replica[i].shape[1] )
        self.assertTrue( np.all( np.equal( states.replica_length, replica_length ) ) )
        self.assertEqual( replica_length.max(), states.max_replica_length )
        states.copy_states( replica )
        for i in xrange( num_replica ):
            for t in xrange( replica_length[i] ):
                self.assertEqual( replica[i][t,0], states.markov_state[i,t] )
                self.assertEqual( replica[i][t,1], states.therm_state[i,t] )
        states.count_markov_states()
        self.assertEqual( num_replica, states.n_markov_states )
        self.assertEqual( num_replica, states.n_therm_states )
        self.assertTrue( np.all( np.equal( replica_length, states.markov_sample ) ) )
        self.assertEqual( length, states.max_markov_samples )
        states.count_thermodynamic_states()
        self.assertEqual( length, states.max_therm_samples )
        self.assertEqual( num_replica, states.therm_sample.shape[0] )
        self.assertTrue( np.all( np.equal( replica_length, states.therm_sample ) ) )
        self.assertEqual( num_replica, states.markov_sequence.shape[0] )
        self.assertEqual( length, states.markov_sequence.shape[1] )
        for i in xrange( num_replica ):
            self.assertTrue( np.all( np.equal( states.markov_sequence[i,:], replica[i][:,0] ) ) )



#~ class StateListRandomTestCase( TestCase ):
    #~ def setUp( self ):
        #~ self.num_replica = 1
        #~ self.num_t_states = 2
        #~ self.num_m_states = 2
        #~ self.replica = []
        #~ self.replica_length = np.random.randint( 9, high=12, size=self.num_replica )
        #~ for i in xrange( self.num_replica ):
            #~ r = np.zeros( shape=(self.replica_length[i],3), dtype=np.float64 )
            #~ r[:,0] = np.random.randint( 0, high=self.num_m_states, size=self.replica_length[i] )
            #~ r[:,1] = np.random.randint( 0, high=self.num_t_states, size=self.replica_length[i] )
            #~ r[:,2] = np.random.rand( self.replica_length[i] )
            #~ self.replica.append( r )
            #~ print r
        #~ self.states = StateList( self.num_replica, self.replica, self.replica_length )
    #~ def tearDown( self ):
        #~ pass
    #~ def test_state_counts( self ):
        #~ self.assertEqual( self.states.n_markov_states, self.num_m_states, "Counted wrong number of markov states" )
        #~ self.assertEqual( self.states.n_therm_states, self.num_t_states, "Counted wrong number of thermodynamic states" )


# class StateListSequentialTestCase( TestCase ):
#     def setUp( self ):
#         pass


# class StateListErrorTest( TestCase ):
#     def setUp ( self ):
#         self.length = 10
#         ones = np.ones( shape=(self.length,), dtype=np.float64 )
#         self.replica1 = np.zeros( shape=(self.length,2), dtype=np.float64 )
#         self.replica2 = np.zeros( shape=(self.length,2), dtype=np.float64 )
#         self.replica1[:,0] = ones[:]
#         self.replica2[:,1] = ones[:]
#     def test_error( self ):
#         self.assertRaises( NotConnectedSetError, StateList, 1, [self.replica1], np.ones(1,dtype=np.int32)*self.length )
#         self.assertRaises( MissingThermodynamicStatesError, StateList, 1, [self.replica2], np.ones(1,dtype=np.int32)*self.length )


if '__main__' == __name__:

    main()
