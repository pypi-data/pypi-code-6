

# experimental to mimic R code

class Boolean(object):


    def __init__(self, cnograph, midas):

        self.cnograph = cnograph
        self.midas = midas

    def simulateT0(self):
        # inhibitors are set to 1
        # stimuli are set to 0
        """
         # !! hack. SimulatorT1 expect the inhibitors values to be 0 or 1.
         # Then, it flips them. So, the 0-values are flipped to 1. finally,
         # the values that are equal to 1 are set to NA...
         # Here, since this is T0, all inhibitors are set to 0. simulatorT1 will
         # therefore flip them to 1 and finally NA. So, we set all inhibitors to 1.

         # Need to be very careful if simulatorT1 changes

         # Finally run the simulator with the particular set of experiments at t0
         newInput = simulatorT1(CNOlistT0, model, simList, indexList, mode=0)
         return(newInput)
        """
        pass
        #     simRes = cSimulator(CNOlist, model, simList, indexList, mode=0)


    def simulateT1(self):

        # SOME VALUES ARE NA from the data. Kepp that information somewhere (temp_store)
        # EDGES that are inhibitors should also be ketp somewhere
            

        # INIT STEP 1
        # inhibitors --------------
        # if mode == 0, inhibitors are all set to 1 why ?
        # if mode > 0 inhibitors = content of the experiment itself
        # !!! FLIP AND REDEFINE INHIBITORS
        # value = 1 - inhibitor value so in mode 0, there are now all 0
        # if value == 1, set to it NA why ?
        # stimuli -----------------
        # if mode == 0, stimuli are all set to 0
        # if mode > 0, stimuli are all set to the content of the experiment

        # INIT STEP 2
        # set initial values to NA for all conditions/species
        # set initial values of the stimuli for all conditions based on INIT STEP 1
        # set initial values of the inhibitors for all conditions based on INIT STEP 1
        pass
        # INIT STEP 3
        # prev = init

        # STARTING LOOP
        #
        # output = prev
        # set NAs if required from ignoreCube
        # flip values with neg inputs: 0 becomes 1 and 1 becomes 0
        #
        # compute first the AND GATES
        # and gates are computed min over inputs
        # if there is an NA, 
        # OR GATES
        #
        # rest inhbitors and stimuli
        # 1 -  if initial value of iinhibitors is 0, set it back to 0
        # 2 -  stimuli. ???? not sure how
        # 3 -  set NA to 0 for each conds/species in new_input and output_prev


        # STOP CRITERIA:
        # 1 - for each cond/species diff = abs(new_input - output_pre); if all diff < test_val stop
        # 2 - count < nSpecies * 1.2

        # FINALLY once loop is over, 
        # set unresolved bits to NA: if newinput != output_prev: set to NA
        # useful for self loops I guess



    def fit(self, sim):
        pass



    def test_example():

        # simple stimuli 
        # S1 1 A1 1 A2 1 A3 1 A4
        # S2 1 B1 -1 B2
        # S3 -1 C1 -1 C2
        # S4 1 D1 -1 D2
        # S5 1 E1 1 E1
        # S6 1 F1 -1 F1
        # S7 1 G1 -1 G1
        # S8 1 H1
        # S9 1 H2
        # H1^H2 = H3

        # conditions: 
        # 1 - all Si on 
        # 2 - all Si on 
        # 3 - some stimuli off


        #S10 1 I1 
        #S11 -1 I2
        #I1^I2 = I3
        #S10 1 I1 
        #S11 1 I2
        # = I3





        





















