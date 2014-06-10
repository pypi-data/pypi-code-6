#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2009 Sandia Corporation.
#  this software is distributed under the bsd license.
#  under the terms of contract de-ac04-94al85000 with sandia corporation,
#  the u.s. government retains certain rights in this software.
#  for more information, see the coopr readme.txt file.
#  _________________________________________________________________________

import math
import os
import types

from pyutilib.misc import flatten_tuple

from coopr.core.plugin import *
from coopr.pysp import phextension
from coopr.pysp.phutils import *
from coopr.pysp.phsolverserverutils import transmit_external_function_invocation_to_worker
from coopr.pysp.generators import scenario_tree_node_variables_generator, \
                                  scenario_tree_node_variables_generator_noinstances
from coopr.pyomo.base import *

from coopr.pyomo.base.set_types import *

from six import iteritems, iterkeys
from six.moves import xrange

has_yaml = False
try:
    import yaml
    has_yaml = True
except:
    pass

#
# Create a dictionary mapping scenario tree id to
# variable bounds
#
def collect_node_variable_bounds(tree_node):
    assert tree_node._variable_datas is not None
    var_bounds = {}
    for variable_id, vardatas in iteritems(tree_node._variable_datas):
        vardata = vardatas[0][0]
        if not vardata.is_expression():
            var_bounds[variable_id] = (vardata.lb, vardata.ub)
        else: # Expression
            var_bounds[variable_id] = (None,None)

    return var_bounds

# This function will be executed on a phsolverserver using
# the transmit_external_function_invocation_to_worker utility
def external_collect_variable_bounds(ph, scenario_tree, scenario_or_bundle, node_list):

    variable_bounds = {}
    for node_name in node_list:
        tree_node = scenario_tree._tree_node_map[node_name]
        variable_bounds[node_name] = collect_node_variable_bounds(tree_node)

    return variable_bounds

#=========================
class _slam_priority_descend_compare(object):
    
    def __init__(self,suffix):
        self._SlammingPriority = suffix

    def __call__(self,a, b):
        # used to sort the variable-suffix map for slamming priority
        value_a = self._SlammingPriority[a]
        value_b = self._SlammingPriority[b]
        return cmp(value_b, value_a)

#==================================================
class wwphextension(SingletonPlugin):

    coopr.core.plugin.implements(phextension.IPHExtension)
    
    # the below is a hack to get this extension into the
    # set of IPHExtension objects, so it can be queried
    # automagically by PH.
    coopr.core.plugin.alias("WWPHExtension")

    def __init__(self, *args, **kwds):

        # TBD - migrate all of the self attributes defined on-the-fly
        #       in the post-post-initialization routine here!
        self._suffixes = {}
        self._configuration_filename = None
        self._suffix_filename = None
        self._annotation_filename = None

        # we track various actions performed by this extension following a 
        # PH iteration - useful for reporting purposes, and for other plugins
        # to react to.
        self.variables_with_detected_cycles = []
        self.variable_fixed = False

    def _parse_yaml_file(self, ph, filename):

        if not has_yaml:
            raise RuntimeError("***WW PH Extension: The PyYAML module is required "
                               "to load file: "+filename)

        with open(filename) as f:
            config_data = yaml.load(f)

        for node_or_stage_name, variable_dicts in iteritems(config_data):

            # find the node or stage object in the scenario tree
            # and convert it to a list of nodes
            node_list = None
            for stage in ph._scenario_tree._stages[:-1]:
                if node_or_stage_name == stage._name:
                    node_list = stage._tree_nodes
                    break
                else:
                    for tree_node in stage._tree_nodes:
                        if tree_node._name == node_or_stage_name:
                            node_list = [tree_node]
                            break
                    if node_list is not None:
                        break

            if len(node_list) == 0:
                raise RuntimeError("***WW PH Extension: %s does not name an existing non-leaf Stage or Node in the scenario tree" % node_or_stage_name)
            
            for variable_string, variable_config_data in iteritems(variable_dicts):

                variable_name = None
                index_template = None
                if isVariableNameIndexed(variable_string):
                    variable_name, index_template = extractVariableNameAndIndex(variable_string)
                else:
                    variable_name = variable_string
                    index_template = None

                match_variable_ids = {}
                for node in node_list:
                    node_match_variable_ids = match_variable_ids[node._name] = []
                    for variable_id, (name,index) in iteritems(node._variable_ids):
                        if (variable_name == name):
                            if (index_template is None) and (index != None):
                                raise RuntimeError("***WW PH Extension: Illegal match template"
                                                   "="+variable_string+" specified in file="+filename)
                            if indexMatchesTemplate(index, index_template):
                                node_match_variable_ids.append(variable_id)
                # we shouldn't have any duplicates or empties
                for node in node_list:
                    assert len(set(match_variable_ids)) == len(match_variable_ids)
                    if len(match_variable_ids[node._name]) == 0:
                        raise RuntimeError("No variables matching string '%s' were found in "
                                           "scenario tree node %s" %
                                           (variable_string, node._name))

                for config_name, config_value in iteritems(variable_config_data):
                    
                    yield config_name, config_value, match_variable_ids


#==================================================

    def process_suffix_file(self, ph):

        self.slam_list = []

        if self._suffix_filename is None:
            return

        if os.path.exists(self._suffix_filename) is False:
            raise RuntimeError("***WW PH Extension: The suffix file "+self._suffix_filename+" either does not exist or cannot be read")

        print("WW PH Extension: Loading variable suffixes from file="+self._suffix_filename)

        for suffix_name, suffix_value, variable_ids in self._parse_yaml_file(ph, self._suffix_filename):

            if suffix_name in self._suffixes:
                self_suffix_dict = self._suffixes[suffix_name]
            else:
                self_suffix_dict = self._suffixes[suffix_name] = {}

            # decide what type of suffix value we're dealing with.
            is_int = False
            is_bool = False
            converted_value = None
            try:
                converted_value = bool(suffix_value)
                is_bool = True
            except ValueError:
                pass
            try:
                converted_value = int(suffix_value)
                is_int = True
            except ValueError:
                pass

            if (not is_int) and (not is_bool):
                raise RuntimeError("WW PH Extension unable to deduce type of data "
                                   "referenced in ww ph extension suffix file"
                                   "="+self._suffix_filename+"; value="+suffix_value)

            for node_name, node_variable_ids in iteritems(variable_ids):
                for variable_id in node_variable_ids:
                    self_suffix_dict[variable_id] = converted_value

        if "SlammingPriority" in self._suffixes:
            self.slam_list = list(self._suffixes["SlammingPriority"].keys())

        if self.slam_list != []:
            self.slam_list.sort(_slam_priority_descend_compare(self._suffixes["SlammingPriority"]))

#==================================================
    def process_annotation_file(self, ph):
        # note: these suffixes can have a string value
        # very similar to suffixes, except for the following:
        # annotation names are from a restricted list, and
        # annotations can have various types that might depend on the name of the annotation
        # not all type checking will be done here, but some might be

        self._obj_family_normalized_rho = {}

        if self._annotation_filename is None:
            return

        AnnotationTypes = {}
        AnnotationTypes['going_price'] = None # Real
        AnnotationTypes['obj_effect_family_name'] = None # String
        AnnotationTypes['obj_effect_family_factor'] = None # Real
        AnnotationTypes['decision_hierarchy_level'] = None # non-negative int
        AnnotationTypes['feasibility_direction'] = ['down', 'up', 'either', 'None']
        AnnotationTypes['relax_int'] = None # int
        AnnotationTypes['reasonable_int'] = None # int
        AnnotationTypes['low_int'] = None # int

        if os.path.exists(self._annotation_filename) is False:
            raise RuntimeError("***WW PH Extension: The annotation file "+self._annotation_filename+" either does not exist or cannot be read")

        print("WW PH Extension: Loading variable annotations from file="+self._annotation_filename)

        for annotation_name, annotation_value, variable_ids in self._parse_yaml_file(ph, self._annotation_filename):
                    
            if annotation_name in self._suffixes:
                self_suffix_dict = self._suffixes[annotation_name]
            else:
                self_suffix_dict = self._suffixes[annotation_name] = {}

            # check for some input errors
            if annotation_name not in AnnotationTypes:
                print("Error encountered.")
                print("Here are the annotations that can be given (they are case sensitive):")
                for i in AnnotationTypes:
                    print(i)
                raise RuntimeError("WW ph extension annotation file="+self._annotation_filename+"; "
                                   "contains unknown annotation: "+annotation_name)

            # check for some more input errors
            if AnnotationTypes[annotation_name] is not None:
                if annotation_value not in AnnotationTypes[annotation_name]:
                    raise RuntimeError("WW ph extension annotation file="+self._annotation_filename+"; "
                                       "contains unknown annotation value="+annotation_value+" "
                                       "for: "+annotation_name)

            # if this is a new obj effect family, then we need new maps
            if annotation_name == 'obj_effect_family_name':
                if annotation_value not in self._obj_family_normalized_rho:
                    self._obj_family_normalized_rho[annotation_value] = 0.0

            for node_name, node_variable_ids in iteritems(variable_ids):
                for variable_id in node_variable_ids:
                    self_suffix_dict[variable_id] = converted_value

    #
    # Store the variable bounds on the tree node by variable id
    # If this is parallel ph, then we need to do this by transmitting
    # an external function invocation that collects the variable
    # bounds from a given list of node names. We do this in such
    # a way as to minimize the amount of data we need to transfer
    # (e.g., in the case of a two stage problem, we request information
    # about the root node from only one of the PH solver servers)
    #

    def _collect_variable_bounds(self,ph):

        if not isinstance(ph._solver_manager,
                          coopr.solvers.plugins.smanager.phpyro.SolverManager_PHPyro):

            for stage in ph._scenario_tree._stages[:-1]:

                for tree_node in stage._tree_nodes:

                    tree_node._variable_bounds = collect_node_variable_bounds(tree_node)

        else:

            nodes_needed = {}
            if ph._scenario_tree.contains_bundles():
                for tree_node in ph._scenario_tree._tree_nodes:
                    if not tree_node.is_leaf_node():
                        representative_scenario = tree_node._scenarios[0]._name
                        representative_bundle = None
                        for bundle in ph._scenario_tree._scenario_bundles:
                            if representative_scenario in bundle._scenario_names:
                                representative_bundle = bundle._name
                                break
                        assert representative_bundle != None
                        if representative_bundle not in nodes_needed:
                            nodes_needed[representative_bundle] = [tree_node._name]
                        else:
                            nodes_needed[representative_bundle].append(tree_node._name)
            else:
                for tree_node in ph._scenario_tree._tree_nodes:
                    if not tree_node.is_leaf_node():
                        representative_scenario = tree_node._scenarios[0]._name
                        if representative_scenario not in nodes_needed:
                            nodes_needed[representative_scenario] = [tree_node._name]
                        else:
                            nodes_needed[representative_scenario].append(tree_node._name)

            action_handle_map = {}
            for object_name, node_list in iteritems(nodes_needed):
                function_args = (node_list,)
                new_action_handle = \
                    transmit_external_function_invocation_to_worker(ph,
                                                                    object_name,
                                                                    "coopr.pysp.plugins.wwphextension",
                                                                    "external_collect_variable_bounds",
                                                                    return_action_handle=True,
                                                                    function_args=function_args)
                action_handle_map[new_action_handle] = object_name

            num_results_so_far = 0
            num_results = len(action_handle_map)
            while (num_results_so_far < num_results):
                ah = ph._solver_manager.wait_any()
                results = ph._solver_manager.get_results(ah)
                object_name = action_handle_map[ah]
                for node_name, node_bounds in iteritems(results):
                    tree_node = ph._scenario_tree._tree_node_map[node_name]
                    tree_node._variable_bounds = node_bounds
                num_results_so_far += 1

#==================================================
    def pre_ph_initialization(self,ph):
        # we don't need to intefere with PH initialization.
        pass
#==================================================

#==================================================
    def post_instance_creation(self, ph):
        # we don't muck with the instances.
        pass

#==================================================
    def post_ph_initialization(self, ph):
        
        # Be verbose (even if ph is not)
        self.Verbose = False

        # set up "global" record keeping.
        self.cumulative_discrete_fixed_count = 0
        self.cumulative_continuous_fixed_count = 0

        # we always track convergence of continuous variables, but we may not want to fix/slam them.
        self.fix_continuous_variables = False

        # there are occasions where we might want to fix any values at the end of the
        # run if the scenarios agree - even if the normal fixing criterion (e.g.,
        # converged for N iterations) don't apply. one example is when the term-diff
        # is 0, at which point you really do have a solution. currently only applies
        # to discrete variables.
        self.fix_converged_discrete_variables_at_exit = False

        # set up the mipgap parameters (zero means ignore)
        # note: because we lag one iteration, the final will be less than requested
        # initial and final refer to PH iteration 1 and PH iteration X, where
        # X is the iteration at which the convergence metric hits 0.
        self.Iteration0MipGap = 0.0
        self.InitialMipGap = 0.10
        self.FinalMipGap = 0.001
        self.MipGapExponent = 1.0 # linear by default

        # use the convergence metric value from iteration 0 as the basis for 
        # scaling the mipgap in subsequent iterations. if set to False, we 
        # instaed start scaling from the convergence metric value following
        # iteration 1. the latter arguably makes more sense, as it accounts
        # for weights and such, i.e., some sub-prolem interactions. 
        self.StartMipGapFromIter0Metric = True 

        # when cyling is detected for a var, the rho will be multiplied by this factor
        # note: 1 is a no-op
        self.rho_reduction_factor=1

        # "Read" the defaults for parameters that control fixing
        # (these defaults can be overridden at the variable level)
        # for all six of these, zero means don't do it.
        self.Iter0FixIfConvergedAtLB = 0 # 1 or 0
        self.Iter0FixIfConvergedAtUB = 0  # 1 or 0
        self.Iter0FixIfConvergedAtNB = 0  # 1 or 0 (converged to a non-bound)
        # TBD: check for range errors for all six of these
        self.FixWhenItersConvergedAtLB = 10
        self.FixWhenItersConvergedAtUB = 10
        self.FixWhenItersConvergedAtNB = 12  # converged to a non-bound
        self.FixWhenItersConvergedContinuous = 0

        # "default" slamming parms:
        # TBD: These should get ovverides from suffixes
        # notice that for a particular var, all could be False
        self.CanSlamToLB = False
        self.CanSlamToMin = False
        self.CanSlamToAnywhere = True
        self.CanSlamToMax = False
        self.CanSlamToUB = False
        self.PH_Iters_Between_Cycle_Slams = 1  # zero means "slam at will"
        self.SlamAfterIter = len(ph._scenario_tree._stages[-1]._tree_nodes)

        # default params associated with fixing due to weight vector oscillation.
        self.CheckWeightOscillationAfterIter = 0
        self.FixIfWeightOscillationCycleLessThan = 10        

        # flags enabling various rho computation schemes.
        self.ComputeRhosWithSEP = False
        self.RhosSEPMult = 0.0

        self.CycleLengthSlamThreshold = len(ph._scenario_tree._stages[-1]._tree_nodes)
        self.W_hash_history_len = max(100, self.CycleLengthSlamThreshold+1)

        # do I report potential cycles, i.e., those too short to base slamming on?
        self.ReportPotentialCycles = False

        # end of parms

        self._last_slam_iter = -1    # dynamic

        # constants for W vector hashing (low cost rand() is all we need)
        # note: July 09, dlw is planning to eschew pre-computed random vector (dlw April 2014: "huh?")
        # another note: the top level reset is OK, but really it should
        #   done way down at the index level with a serial number (stored)
        #   to avoid correlated hash errors
        # the hash seed was deleted in 1.1 and we seed with the
        self.W_hash_seed = 17  # we will reset for dynamic rand vector generation
        self.W_hash_rand_val = self.W_hash_seed # current rand
        self.W_hash_a = 1317       # a,b, and c are for a simple generator
        self.W_hash_b = 27699
        self.W_hash_c = 131072  # that period should be usually long enough for us!
                                # (assuming fewer than c scenarios)

        if "my_stage" in self._suffixes:
            suffix_component = self._suffixes["my_stage"]
        else:
            suffix_component = self._suffixes["my_stage"] = {}

        # set up tree storage for statistics that we care about tracking.
        for stage in ph._scenario_tree._stages[:-1]:

            for tree_node in stage._tree_nodes:

                # we're adding a lot of statistics / tracking data to each tree node.
                # these are all maps from variable name to a parameter that tracks the corresponding information.
                tree_node._num_iters_converged = dict.fromkeys(tree_node._variable_ids,0)
                tree_node._last_converged_val = dict.fromkeys(tree_node._variable_ids,0.5)
                tree_node._w_hash = dict(((variable_id,ph_iter),0) for variable_id in tree_node._variable_ids for ph_iter in ph._iteration_index_set)
                tree_node._w_sign_vector = dict.fromkeys(tree_node._variable_ids,[]) # sign vector for weights at the last PH iteration
                tree_node._w_last_sign_flip_iter = dict.fromkeys(tree_node._variable_ids,0) # the number of iterations since the last flip in the sign (TBD - of any scenario in the vector)?                

                suffix_component.update((variable_id,stage) for variable_id in tree_node._variable_ids)

        if self._configuration_filename is not None:
            if os.path.exists(self._configuration_filename) is True:
                print("WW PH Extension: Loading user-specified configuration from file=" + self._configuration_filename)
                try:
                    # TODO: execfile is gone in py3k, but the following did not work in ph.py for load cfg files. It may or
                    #       may not work here
                    #exec(compile(open(self._configuration_filename).read(),self._configuration_filename,'exec'),globals(), locals())
                    execfile(self._configuration_filename)
                except:
                    raise RuntimeError("Failed to load WW PH configuration file="+self._configuration_filename)
            else:
                raise RuntimeError("***WW PH Extension: The configuration file "+self._configuration_filename+" either does not exist or cannot be read")
        else:
            print("WW PH Extension: No user-specified configuration file supplied - using defaults")

        # process any suffix and/or annotation data, if they exists.
        self.process_suffix_file(ph)
        self.process_annotation_file(ph)

        # set up the mip gap for iteration 0.
        if self.Iteration0MipGap > 0.0:
            print("WW PH Extension: Setting mipgap to %.7f, as specified in the configuration file" % self.Iteration0MipGap)
            ph._mipgap = self.Iteration0MipGap

#==================================================
    def post_iteration_0_solves(self, ph):

        self._collect_variable_bounds(ph)

        # Collect possible existing Suffix components that we will check inside the next loop
        Iter0FixIfConvergedAtLB = None
        if 'Iter0FixIfConvergedAtLB' in self._suffixes:
            Iter0FixIfConvergedAtLB = self._suffixes['Iter0FixIfConvergedAtLB']
        Iter0FixIfConvergedAtUB = None
        if 'Iter0FixIfConvergedAtUB' in self._suffixes:
            Iter0FixIfConvergedAtUB = self._suffixes['Iter0FixIfConvergedAtUB']
        Iter0FixIfConvergedAtNB = None
        if 'Iter0FixIfConvergedAtNB' in self._suffixes:
            Iter0FixIfConvergedAtNB = self._suffixes['Iter0FixIfConvergedAtNB']
        CostForRho = None
        if 'CostForRho' in self._suffixes:
            CostForRho = self._suffixes['CostForRho']

        for stage, tree_node, variable_id, variable_values, is_fixed, is_stale in \
            scenario_tree_node_variables_generator_noinstances(ph._scenario_tree,
                                                               includeDerivedVariables=False,
                                                               includeLastStage=False):

            if (is_stale is False):

                if (self.ComputeRhosWithSEP) and (not CostForRho is None):

                    node_average = tree_node._averages[variable_id]
                    deviation_from_average = 0.0
                    sumprob = 0.0
                    for scenario in tree_node._scenario:
                        scenario_probability = scenario._probability
                        varvalue = scenario._x[tree_node._name][variable_id]
                        deviation_from_average += (scenario_probability * math.fabs(var_value.value - node_average))
                        sumprob += scenario_probability
                    deviation_from_average /= sumprob  # expected deviation

                    node_min = self.Int_If_Close_Enough(ph, tree_node._minimums[variable_id])
                    node_max = self.Int_If_Close_Enough(ph, tree_node._maximums[variable_id])

                    if tree_node.is_variable_discrete(variable_id):
                        denominator = max(node_max - node_min + 1, 1)
                    else:
                        denominator = max(deviation_from_average, 1)

                    # CostForRho are the costs to be used as the numerator in the rho computation below.
                    if variable_id in CostForRho[variable_id]:
                        ph.setRhoAllScenarios(tree_node, variable_id, CostForRho[variable_id] * self.RhosSEPMult / denominator)
                
                if is_fixed is False:

                    if tree_node.is_variable_discrete(variable_id):
                        node_min = self.Int_If_Close_Enough(ph, tree_node._minimums[variable_id])
                        node_max = self.Int_If_Close_Enough(ph, tree_node._maximums[variable_id])

                        # update convergence prior to checking for fixing.
                        self._int_convergence_tracking(ph, tree_node, variable_id, node_min, node_max)
                                    
                        lb = self.Iter0FixIfConvergedAtLB
                        if (not Iter0FixIfConvergedAtLB is None) and (variable_id in Iter0FixIfConvergedAtLB):
                            lb = Iter0FixIfConvergedAtLB[variable_id]

                        ub = self.Iter0FixIfConvergedAtUB
                        if (not Iter0FixIfConvergedAtUB is None) and (variable_id in Iter0FixIfConvergedAtUB):
                            ub = Iter0FixIfConvergedAtUB[variable_id]

                        nb = self.Iter0FixIfConvergedAtNB
                        if (not Iter0FixIfConvergedAtNB is None) and (variable_id in Iter0FixIfConvergedAtNB):
                            nb = Iter0FixIfConvergedAtNB[variable_id]

                        if self._should_fix_discrete_due_to_conv(tree_node, variable_id, lb, ub, nb):
                            self._fix_var(ph, tree_node, variable_id, node_min)
                        elif self.W_hash_history_len > 0:   # if not fixed, then hash - no slamming at iteration 0
                            self._w_history_accounting(ph, tree_node, variable_id) # obviously not checking for cycles at iteration 0!

                    else:

                        node_min = tree_node._minimums[variable_id]
                        node_max = tree_node._maximums[variable_id]

                        self._continuous_convergence_tracking(ph, tree_node, variable_id, node_min, node_max)

# jpw: not sure if we care about cycle detection in continuous variables?
#                           if self.W_hash_history_len > 0:
#                              self._w_history_accounting(ph, tree_node, variable_id)


#==================================================
    def post_iteration_0(self, ph):

        pass

#==================================================

    def pre_iteration_k_solves(self, ph):

        # NOTE: iteration 0 mipgaps are handled during extension initialization, following PH initialization.

        if (self.InitialMipGap > 0 and self.FinalMipGap >= 0) and self.InitialMipGap > self.FinalMipGap:

            if ph._current_iteration == 1:
                print("WW PH Extension: Setting mipgap to %.7f, as specified in the configuration file" % self.InitialMipGap)
                ph._mipgap = self.InitialMipGap

            else:
                m0 = ph._converger._metric_history[0]
                m1 = ph._converger._metric_history[1]
                m = ph._converger.lastMetric()
                mlast = ph._converger._convergence_threshold

                basis_value = m0
                if self.StartMipGapFromIter0Metric == False:
                    basis_value = m1

                x = 1.0 - (m-mlast)/(basis_value-mlast)
                y = 1.0 - x**self.MipGapExponent

                g0 = self.InitialMipGap
                glast = self.FinalMipGap

                new_gap = y * (g0-glast) + glast

                if new_gap > g0:
                    print("WW PH Extension: ***CAUTION - setting mipgap to thresholded maximal initial value=%.7f; unthresholded value=%.7f" % (g0, new_gap))
                    new_gap = g0
                else:
                    print("WW PH Extension: Setting mipgap to %.7f, based on current value of the convergence metric" % new_gap)
                ph._mipgap = new_gap

#==================================================
    def post_iteration_k_solves(self, ph):

        # Collect possible existing Suffix components that we will check inside the next loop
        FixWhenItersConvergedAtLB = None
        if 'FixWhenItersConvergedAtLB' in self._suffixes:
            FixWhenItersConvergedAtLB = self._suffixes['FixWhenItersConvergedAtLB']
        FixWhenItersConvergedAtUB = None
        if 'FixWhenItersConvergedAtUB' in self._suffixes:
            FixWhenItersConvergedAtUB = self._suffixes['FixWhenItersConvergedAtUB']
        FixWhenItersConvergedAtNB = None
        if 'FixWhenItersConvergedAtNB' in self._suffixes:
            FixWhenItersConvergedAtNB = self._suffixes['FixWhenItersConvergedAtNB']

        # track all variables for which cycles have been detected - other plugins may want to react to / report on this information.
        self.variables_with_detected_cycles = []
        self.variable_fixed = False

        for stage, tree_node, variable_id, variable_values, is_fixed, is_stale in \
            scenario_tree_node_variables_generator_noinstances(ph._scenario_tree,
                                                               includeDerivedVariables=False,
                                                               includeLastStage=False):

            # if the variable is stale, don't waste time fixing and cycle checking. for one,
            # the code will crash :-) due to None values observed during the cycle checking computation.
            if (is_stale is False) and (is_fixed is False):

                variable_name, index = tree_node._variable_ids[variable_id]
                full_variable_name = variable_name+indexToString(index)
                if tree_node.is_variable_discrete(variable_id):
                    node_min = self.Int_If_Close_Enough(ph, tree_node._minimums[variable_id])
                    node_max = self.Int_If_Close_Enough(ph, tree_node._maximums[variable_id])

                    # update convergence prior to checking for fixing.
                    self._int_convergence_tracking(ph, tree_node, variable_id, node_min, node_max)

                    lb = self.FixWhenItersConvergedAtLB
                    if (not FixWhenItersConvergedAtLB is None) and (variable_id in FixWhenItersConvergedAtLB):
                        lb = FixWhenItersConvergedAtLB[variable_id]

                    ub = self.FixWhenItersConvergedAtUB
                    if (not FixWhenItersConvergedAtUB is None) and (variable_id in FixWhenItersConvergedAtUB):
                        ub = FixWhenItersConvergedAtUB[variable_id]

                    nb = self.FixWhenItersConvergedAtNB
                    if (not FixWhenItersConvergedAtNB is None) and (variable_id in FixWhenItersConvergedAtNB):
                        nb = FixWhenItersConvergedAtNB[variable_id]

                    if self._should_fix_discrete_due_to_conv(tree_node, variable_id, lb, ub, nb):
                            
                        self._fix_var(ph, tree_node, variable_id, node_min)
                        
                    else: # if not fixed, then hash and slam as necessary.

                        if self.W_hash_history_len > 0:
                            self._w_history_accounting(ph, tree_node, variable_id)

                            computed_cycle_length, msg = self.compute_cycle_length(ph, tree_node, variable_id, False)

                            if computed_cycle_length > 0:
                                self.variables_with_detected_cycles.append((variable_id, computed_cycle_length, tree_node))

                            if (computed_cycle_length >= self.CycleLengthSlamThreshold) and ((ph._current_iteration - self._last_slam_iter) > self.PH_Iters_Between_Cycle_Slams):
                                # TBD: we may not want to slam immediately - it may disappear on it's own after a few iterations, depending on what other variables do.
                                # note: we are *not* slamming the offending variable, but a selected variable
                                if self.Verbose or ph._verbose:
                                    print("Cycle issue detected with variable="+full_variable_name)
                                    print(msg)
                                    print("Cycle length exceeds iteration slamming threshold="+str(self.CycleLengthSlamThreshold)+"; choosing a variable to slam")

                                self._pick_one_and_slam_it(ph)
                                self._reset_w_reduce_rho(ph, tree_node, variable_id, full_variable_name)
                            elif (computed_cycle_length > 1) and (computed_cycle_length < self.CycleLengthSlamThreshold):
                                # there was a (potential) cycle, but the slam threshold wasn't reached.
                                if (self.ReportPotentialCycles) and (self.Verbose or ph._verbose):
                                    print("Cycle issue detected with variable="+full_variable_name)
                                    print(msg)
                                    print("Taking no action to break cycle - length="+str(computed_cycle_length)+" does not exceed slam threshold="+str(self.CycleLengthSlamThreshold))
                            elif (computed_cycle_length >= self.CycleLengthSlamThreshold) and ((ph._current_iteration - self._last_slam_iter) > self.PH_Iters_Between_Cycle_Slams):
                                # we could have slammed, but we recently did and are taking a break to see if things settle down on their own.
                                if self.Verbose or ph._verbose:
                                    print("Cycle issue detected with variable="+full_variable_name)
                                    print(msg)
                                    print("Taking no action to break cycle - length="+str(computed_cycle_length)+" does exceed slam threshold="+str(self.CycleLengthSlamThreshold)+ \
                                              ", but another variable was slammed within the past "+str(self.PH_Iters_Between_Cycle_Slams)+" iterations")
                else:

                    # obviously don't round in the continuous case.
                    node_min = tree_node._minimums[variable_id]
                    node_max = tree_node._maximums[variable_id]

                    # update w statistics for whatever nefarious purposes are enabled.
                    if self.W_hash_history_len > 0:   
                        self._w_history_accounting(ph, tree_node, variable_id)

                        # update convergence prior to checking for fixing.
                        self._continuous_convergence_tracking(ph, tree_node, variable_id, node_min, node_max)

                    if self._should_fix_continuous_due_to_conv(tree_node, variable_id):
                        # fixing to max value for safety (could only be an issue due to tolerances).
                        self._fix_var(ph, tree_node, variable_id, node_max)
                        # note: we currently don't slam continuous variables!

        # TBD: the 1 might need to be parameterized - TBD - the 1 should be the PH ITERATIONS BETWEEN CYCLE SLAMS
        if (ph._current_iteration > self.SlamAfterIter) and \
           ((ph._current_iteration - self._last_slam_iter) > self.PH_Iters_Between_Cycle_Slams) and \
           (ph._converger.isImproving(self.PH_Iters_Between_Cycle_Slams)):
            print("Slamming criteria are satisifed - accelerating convergence")
            self._pick_one_and_slam_it(ph)
            self._just_slammed_ = True
        else:
            self._just_slammed_ = False

        ### THIS IS EXPERIMENTAL - CODE MAY BELONG SOMEWHERE ELSE ###
        for stage, tree_node, variable_id, variable_values, is_fixed, is_stale in \
            scenario_tree_node_variables_generator_noinstances(ph._scenario_tree,
                                                               includeDerivedVariables=False,
                                                               includeLastStage=False):

            last_flip_iter = tree_node._w_last_sign_flip_iter[variable_id]
            flip_duration = ph._current_iteration - last_flip_iter

            if (self.CheckWeightOscillationAfterIter > 0) and (ph._current_iteration >= self.CheckWeightOscillationAfterIter):
                if (last_flip_iter is 0) or (flip_duration >= self.FixIfWeightOscillationCycleLessThan): 
                    pass
                else:
                    if self._slam(ph, tree_node, variable_id) is True:
                        tree_node._w_last_sign_flip_iter[variable_id] = 0 
                        return            

#==================================================
    def post_iteration_k(self, ph):

        pass

#==================================================
    def post_ph_execution(self, ph):

        if self.fix_converged_discrete_variables_at_exit is True:
            print("WW PH extension: Fixing all discrete variables that are converged at termination")
            self._fix_all_converged_discrete_variables(ph)

#=========================
    def Int_If_Close_Enough(self, ph, x):
        # if x is close enough to the nearest integer, return the integer
        # else return x
        if abs(round(x)-x) <= ph._integer_tolerance:
            return int(round(x))
        else:
            return x

#=========================
    def _int_convergence_tracking(self, ph, tree_node, variable_id, node_min, node_max):
        
        # keep track of cumulative iters of convergence to the same int
        if (node_min == node_max) and (type(node_min) is types.IntType):
            if node_min == tree_node._last_converged_val[variable_id]:
                tree_node._num_iters_converged[variable_id] += 1
            else:
                tree_node._num_iters_converged[variable_id] = 1
                tree_node._last_converged_val[variable_id] = node_min
        else:
            tree_node._num_iters_converged[variable_id] = 0
            tree_node._last_converged_val[variable_id] = 0.5

#=========================
    def _continuous_convergence_tracking(self, ph, tree_node, variable_id, node_min, node_max):
        # keep track of cumulative iters of convergence to the same value within tolerance.
        if abs(node_max - node_min) <= ph._integer_tolerance:
            if abs(node_min - tree_node._last_converged_val[variable_id]) <= ph._integer_tolerance:
                tree_node._num_iters_converged[variable_id] = tree_node._num_iters_converged[variable_id] + 1
            else:
                tree_node._num_iters_converged[variable_id] = 1
                tree_node._last_converged_val[variable_id] = node_min
        else:
            tree_node._num_iters_converged[variable_id] = 0
            tree_node._last_converged_val[variable_id] = 0.2342343243223423 # TBD - avoid the magic constant!

#=========================
    def _w_history_accounting(self, ph, tree_node, variable_id):
        # do the w hash accounting work
        # we hash on the variable ph weights, and not the values; the latter may not shift for some time, while the former should.
        self.W_hash_rand_val = self.W_hash_seed

        new_sign_vector = []
        old_sign_vector = tree_node._w_sign_vector[variable_id]

        for scenario in tree_node._scenarios:
           weight_value = scenario._w[tree_node._name][variable_id]
           weight_sign = True
           if weight_value < 0.0:
               weight_sign = False
           tree_node._w_hash[variable_id,ph._current_iteration] += weight_value * self.W_hash_rand_val

           new_sign_vector.append(weight_sign)
           self.W_hash_rand_val = (self.W_hash_b + self.W_hash_a * self.W_hash_rand_val) % self.W_hash_c

        hash_val = tree_node._w_hash[variable_id,ph._current_iteration]

        num_flips = 0
        for i in xrange(0,len(old_sign_vector)):
           if new_sign_vector[i] != old_sign_vector[i]:
              num_flips += 1

        tree_node._w_sign_vector[variable_id] = new_sign_vector

        if num_flips >= 1:
           tree_node._w_last_sign_flip_iter[variable_id] = ph._current_iteration        

#=========================
    def compute_cycle_length(self, ph, tree_node, variable_id, report_possible_cycles):
        # return cycles back to closest hash hit for hashval or 0 if no hash hit

        # if the values are converged, then don't report a cycle - often, the weights at convergence are 0s, and even
        # if they aren't, they won't move if the values are uniform.
        if (tree_node._num_iters_converged[variable_id] == 0) and (variable_id not in tree_node._fixed):
            current_hash_value = None
            current_hash_value = tree_node._w_hash[variable_id,ph._current_iteration]
            # scan starting from the farthest point back in history to the closest - this is required to
            # identify the longest possible cycles, which is what we want.
            for i in xrange(max(ph._current_iteration - self.W_hash_history_len - 1, 1), ph._current_iteration - 1, 1):
                this_hash_value = None
                this_hash_value = tree_node._w_hash[variable_id,i]
                if abs(this_hash_value - current_hash_value) <= ph._integer_tolerance:
                    if report_possible_cycles is True:
                        variable_name, index = tree_node._variable_ids[variable_id]
                        print("Possible cycle detected via PH weight hashing - variable="+variable_name+indexToString(index)+" node="+ tree_node._name)
                    msg = "Current hash value="+str(current_hash_value)+" matched (within tolerance) hash value="+str(this_hash_value)+" found at PH iteration="+str(i)+"; cycle length="+str(ph._current_iteration - i)
                    return ph._current_iteration - i, msg
        return 0, ""

#=========================

    def _fix_var(self, ph, tree_node, variable_id, fix_value):

        # fix the variable, account for it and maybe output some trace information
        # note: whether you fix at current values or not can severly impact feasibility later
        # in the game. my original thought was below - but that didn't work out. if you
        # make integers, well, integers, all appears to be well.
        # IMPT: we are leaving the values for individual variables alone, at potentially
        #       smallish and heterogeneous values. if we fix/round, we run the risk of
        #       infeasibilities due to numerical issues. the computed value below is
        #       strictly for output purposes. dlw note: as of aug 1 '09,
        #       node_min and node_max should be
        #       int if they should be (so to speak)

        variable_name, index = tree_node._variable_ids[variable_id]
        if self.Verbose or ph._verbose:
            print("Fixing variable="+variable_name+indexToString(index)+" at tree node="+tree_node._name+" to value="+str(fix_value)+"; converged for "+str(tree_node._num_iters_converged[variable_id])+" iterations")

        tree_node.fix_variable(variable_id, fix_value)

        if tree_node.is_variable_discrete(variable_id):
            self.cumulative_discrete_fixed_count += 1
        else:
            self.cumulative_continuous_fixed_count += 1

        # set the global state flag indicator
        self.variable_fixed = True

#=========================
    # the last 3 input arguments are the number of iterations the variable is required to
    # be at the respective bound (or lack thereof) before fixing can be initiated.
    def _should_fix_discrete_due_to_conv(self, tree_node, variable_id, lb_iters, ub_iters, nb_iters):
        # return True if this should be fixed due to convergence

        # jpw: i don't think this logic is correct - shouldn't "non-bound" be moved after the lb/ub checks - this doesn't check a bound!
        # dlw reply: i meant it to mean "without regard to bound" so i have updated the document
        if nb_iters > 0 and tree_node._num_iters_converged[variable_id] >= nb_iters:
            return True
        else:
            # there is a possibility that the variable doesn't have a bound specified, in which
            # case we should obviously ignore the corresponding lb_iters/ub_iters/nb_iters - which
            # should be none as well!
            (lb, ub) = tree_node._variable_bounds[variable_id]
            conval = tree_node._last_converged_val[variable_id]
            # note: if they are converged node_max == node_min
            if (lb is not None) and (lb_iters > 0) and (tree_node._num_iters_converged[variable_id] >= lb_iters) and (conval == lb):
                return True
            elif (ub is not None) and (ub_iters > 0) and (tree_node._num_iters_converged[variable_id] >= ub_iters) and (conval == ub):
                return True
        # if we are still here, nothing triggered fixing
        return False

#=========================
    def _should_fix_continuous_due_to_conv(self, tree_node, variable_id):

        if self.fix_continuous_variables:
            if self.FixWhenItersConvergedContinuous > 0 and tree_node._num_iters_converged[variable_id] >= self.FixWhenItersConvergedContinuous:
                return True

        # if we are still here, nothing triggered fixing
        return False

#=========================
    def _slam(self, ph, tree_node, variable_id):
        # this function returns a boolean indicating if it slammed
        # TBD in the distant future: also: slam it to somewhere it sort of wants to go
        # e.g., the anywhere case could be to the mode
        #   or if more than one dest is True, pick the one closest to the average
        #   as of sept 09, it is written with the implicit assumption that only one
        #   destination is True or that if not, then min/max trumps lb/ub and anywhere trumps all

        fix_value = None  # assume the worst
        variable_name, index = tree_node._variable_ids[variable_id]
        lb, ub = tree_node._variable_bounds[variable_id]

        if tree_node.is_variable_discrete(variable_id):
            node_min = self.Int_If_Close_Enough(ph, tree_node._minimums[variable_id])
            node_max = self.Int_If_Close_Enough(ph, tree_node._maximums[variable_id])
            anywhere = round(tree_node._averages[variable_id])
        else:
            node_min = tree_node._minimums[variable_id]
            node_max = tree_node._maximums[variable_id]
            anywhere = tree_node._averages[variable_id]

        slam_basis_string = ""
        if self.CanSlamToLB:
            fix_value = lb
            slam_basis_string = "lower bound"
        if self.CanSlamToMin:
            fix_value = node_min
            slam_basis_string = "node minimum"
        if self.CanSlamToUB:
            fix_value = ub
            slam_basis_string = "upper bound"
        if self.CanSlamToMax:
            fix_value = node_max
            slam_basis_string = "node maximum"
        if self.CanSlamToAnywhere:
            fix_value = anywhere
            slam_basis_string = "node average (anywhere)"
        if fix_value is None:
            print("Warning: Not allowed to slam variable="+variable_name+indexToString(index)+" at tree node="+tree_node._name)
            return False
        else:
            print("Slamming variable="+variable_name+indexToString(index)+" at tree node="+tree_node._name+" to value="+str(fix_value)+"; value="+slam_basis_string)
            self._fix_var(ph, tree_node, variable_id, fix_value)
            return True

#=========================
    def _pick_one_and_slam_it(self, ph):

        my_stage_suffix = None
        if "my_stage" in self._suffixes:
            my_stage_suffix = self._suffixes["my_stage"]

        for variable_id in self.slam_list:

            didone = False;   # did we find at least one node to slam in?
            # it is possible (even likely) that the slam list contains variable values that
            # reside in the final stage - which, because of the initialization loops in
            # the post_ph_initialization() method, will not have a _stage attribute defined.
            # check for the presence of this attribute and skip if not present, as it
            # doesn't make sense to slam variable values in the final stage anyway.
            variable_stage = None
            if (my_stage_suffix is not None) and (variable_id in my_stage_suffix):
                variable_stage = my_stage_suffix[variable_id]
            if variable_stage is not None: # None => the variable isn't used.
                for tree_node in variable_stage._tree_nodes:
                    # determine if the variable is already fixed (the trusting version...).
                    if variable_id not in tree_node._fixed:
                        didone = self._slam(ph, tree_node, variable_id)
                if didone:
                    self._last_slam_iter = ph._current_iteration
                    return

        if self.Verbose or ph._verbose:
            print("Warning: Nothing free with a non-zero slam priority - no variable will be slammed")

        # DLW says: Hey, look at this: if we were to start deleting from the slam list this would be wrong."
        if len(self.slam_list) == 0:
            if self.Verbose or ph._verbose:
                print("   (No Slamming Priorities were specified in a suffix file.)")

#=========================
    def _reset_w_reduce_rho(self, ph, tree_node, variable_id, variable_name):
        # reset w to zero and reduce rho
        if self.Verbose or ph._verbose:
            print("Resetting W for variable="+variable_name+" and multiplying rho by the rho_reduction_factor="+str(self.rho_reduction_factor))
        for scenario in tree_node._scenarios:
            scenario._w[tree_node._name][variable_id] = 0
            scenario._rho[tree_node._name][variable_id] *= self.rho_reduction_factor
    

#==========================
# a simple utility to fix any discrete variables to their common value, assuming they
# are at a common value
#==========================

    def _fix_all_converged_discrete_variables(self, ph):

        num_variables_fixed = 0

        for stage, tree_node, variable_id, variable_values, is_fixed, is_stale in \
            scenario_tree_node_variables_generator_noinstances(ph._scenario_tree,
                                                               includeDerivedVariables=False,
                                                               includeLastStage=False):

            # if the variable is stale, don't waste time fixing and cycle checking. for one,
            # the code will crash :-) due to None values observed during the cycle checking computation.
            if (is_stale is False) and (is_fixed is False):

                if tree_node.is_variable_discrete(variable_id):
                    node_min = self.Int_If_Close_Enough(ph, tree_node._minimums[variable_id])
                    node_max = self.Int_If_Close_Enough(ph, tree_node._maximums[variable_id])

                    if node_min == node_max:
                        self._fix_var(ph, tree_node, variable_id, node_min)
                        num_variables_fixed += 1

        print("Total number of variables fixed at PH termination due to convergence="+str(num_variables_fixed))
