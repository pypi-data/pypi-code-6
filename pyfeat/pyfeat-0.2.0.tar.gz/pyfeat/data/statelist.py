r"""

==============================
Data container for state lists
==============================

.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>, Antonia Mey <antonia.mey@fu-berlin.de>

"""

import numpy as np
from ..exception.exception import NotConnectedSetError, MissingThermodynamicStatesError

class StateList( object ):
    r"""
    Container for the markov_state and therm_state arrays
    """
    def __init__( self, n_replicas, replica, replica_length, verbose=False, _skip_counting=False ):
        r"""
        Initialize the state lists
        
        Parameters
        ----------
        n_replicas : int
            number of replicas
        replica : list
            np.nparrays with imported data
        replica_length : np.ndarray( shape=(len(replica),), dtype=np.int32 )
            length of the imported replicas
        verbose : boolean (optional)
            be loud and noisy
        
        """
        # store length arguments
        self.n_replicas = n_replicas
        self.replica_length = replica_length
        self.replica_width = replica[0].shape[1]
        # get maximal trajectory length (from all replicas)
        self.max_replica_length = self.replica_length.max()
        if verbose:
            print "Found initial replica width %d" % self.replica_width
            print "Found maximal replica length %d" % self.max_replica_length
        if not _skip_counting:
            self.copy_states( replica )
            self.count_markov_states( verbose=verbose )
            self.count_thermodynamic_states( verbose=verbose )

    def copy_states( self, replica  ):
        r"""
        copies the data from the replica into the state list containers
        """
        # allocate space for markov and thermodynamic states
        self.markov_state = np.zeros( shape=(self.n_replicas,self.max_replica_length), dtype=np.int32 )
        self.therm_state = np.zeros( shape=self.markov_state.shape, dtype=np.int32 )
        # fill allocated space with state numbers
        for i in xrange( self.n_replicas ):
            self.markov_state[i,:self.replica_length[i]] = replica[i][:,0].astype( np.int32 )
            self.therm_state[i,:self.replica_length[i]] = replica[i][:,1].astype( np.int32 )
            if self.replica_width != replica[i].shape[1]:
                raise RuntimeError("Replica widths do not match")

    def count_markov_states( self, verbose=False ):
        r"""
        builds up the markov states samples containers 
        """
        # get maximal state numbers
        self.n_markov_states = 1 + self.markov_state.max()
        self.n_therm_states = 1 + self.therm_state.max()
        if verbose:
            print "Found %d markov states" % self.n_markov_states
            print "Found %d thermodynamic states" % self.n_therm_states
        # allocate and fill space for markov sample counts
        self.markov_sample = np.zeros( shape=(self.n_markov_states,), dtype=np.int32 )
        for i in xrange( self.n_replicas ):
            for t in xrange( self.replica_length[i] ):
                self.markov_sample[self.markov_state[i,t]] += 1
        # sanity check
        if not np.all( self.markov_sample != 0 ):
            raise NotConnectedSetError()
        # get maximal markov sample numbers
        self.max_markov_samples = self.markov_sample.max()
        if verbose:
            print "Markov state counts:"
            for i in xrange( self.n_markov_states ):
                print "[%6d]: %6d" % ( i, self.markov_sample[i] )
            print "Maximal sample number is %d" % self.max_markov_samples
        #print self.max_markov_samples

    def count_thermodynamic_states( self, verbose=False ):
        r"""
        allocates and fills markov state sequence with therm state sorting
        """
        self.therm_sample = np.zeros( shape=(self.n_therm_states,), dtype=np.int32 )
        for i in xrange( self.n_replicas ):
            for t in xrange( self.replica_length[i] ):
                self.therm_sample[self.therm_state[i,t]] += 1
        # sanity check
        if not np.all( self.therm_sample != 0 ):
            raise MissingThermodynamicStatesError()
        # get maximal thermodynamic sample numbers
        self.max_therm_samples = self.therm_sample.max()
        if verbose:
            print "Thermodynamic state counts:"
            for i in xrange( self.n_therm_states ):
                print "[%6d]: %6d" % ( i, self.therm_sample[i] )
            print "Maximal sample number is %d" % self.max_therm_samples
        # sort markov states
        self.markov_sequence = np.zeros( shape=(self.n_therm_states,self.max_therm_samples), dtype=np.int32 )
        C = np.zeros( shape=(self.n_therm_states,), dtype=np.int32 )
        for i in xrange( self.n_replicas ):
            for t in xrange( self.replica_length[i] ):
                j = self.therm_state[i,t]
                self.markov_sequence[j,C[j]] = self.markov_state[i,t]
                C[j] += 1
