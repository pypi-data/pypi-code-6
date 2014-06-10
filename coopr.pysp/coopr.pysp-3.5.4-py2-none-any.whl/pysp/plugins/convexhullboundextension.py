import logging
import copy

from coopr.core.plugin import *
from coopr.pyomo import *
from coopr.opt import SolverFactory
from coopr.pysp import phextension
from coopr.pysp.phsolverserverutils import transmit_weights, transmit_fixed_variables
from coopr.pysp.phutils import *
import coopr.solvers.plugins.smanager.phpyro

from coopr.core import DeveloperError
from coopr.opt import UndefinedData

from six import iteritems, iterkeys

logger = logging.getLogger('coopr.pysp')

class convexhullboundextension(SingletonPlugin):

    coopr.core.plugin.implements(phextension.IPHExtension)

    def __init__(self, *args, **kwds):

        # the interval for which bound computations
        # are performed during the ph iteration k solves.
        # A bound update is always performed at iteration 0
        # with the (non-PH-augmented) objective and the update
        # interval starts with a bound update at ph iteration 1. 
        self._update_interval = 1

        # keys are ph iteration
        self._bound_history = {}

        self._is_minimizing = True

        # the bundle dual master model
        self._master_model = None

        # cached PH weight values, for purposes of subsequent restoration.
        # maps (scenario_name, variable_id) to the corresponding weight value.
        self._cached_ph_weights = {}

        # maps (iteration, scenario_name) to objective function value
        self._past_objective_values = {}

        # maps (iteration, scenario_name, variable_id) to value
        # maps iteration -> copy of each scenario solution
        self._past_var_values = {}

    def _iteration_k_bound_solves(self, ph, storage_key):

        if (ph._mipgap is not None) or (ph._mipgap > 0):
            logger.warn("A nonzero mipgap was detected when using "
                        "the phboundextension plugin. The bound "
                        "computation may as a result be conservative.")

        # Disable the solution caching mechanism so we can restore the
        # current solution. Failing to do this would cause the cache
        # to be overwritten in the call to ph.solve_subproblems()
        ph._enable_solution_caching = False

        # snapshot the solutions on the scenarios objects in the tree
        # for restoring after we're done
        ph_solutions = dict((scenario._name, scenario.package_current_solution()) \
                            for scenario in ph._scenario_tree._scenarios)

        # before we do anything, we need to cache the current PH
        # weights, so we can restore them below.
        self._cache_ph_weights(ph)

        # for these solves, we're going to be using the convex hull
        # master problem weights.
        self._push_weights_to_ph(ph)

        # Weights have not been pushed to instance parameters (or
        # transmitted to the phsolverservers) at this point
        ph._push_w_to_instances()

        # assign rhos from ck.
        self._assign_cks(ph)

        # Save the current fixed state and fix queue
        ph_fixed = dict((tree_node._name, copy.deepcopy(tree_node._fixed)) \
                             for tree_node in ph._scenario_tree._tree_nodes)

        ph_fix_queue = \
            dict((tree_node._name, copy.deepcopy(tree_node._fix_queue)) \
                 for tree_node in ph._scenario_tree._tree_nodes)

        # Free all currently fixed variables
        for tree_node in ph._scenario_tree._tree_nodes:
            tree_node.clear_fix_queue()
            for variable_id in ph_fixed[tree_node._name]:
                tree_node.free_variable(variable_id)

        # Push freed variable statuses to instances (or
        # transmit to the phsolverservers)
        ph._push_fixed_to_instances()

        # the following code assumes the weight terms are already active
        # but proximal terms need to be deactivated
        if ph._drop_proximal_terms is False:
            # deactivate all proximal terms and activate all weight terms
            ph.deactivate_ph_objective_proximal_terms(transmit=True)

        # Do the preprocessing
        ph._preprocess_scenario_instances()
        
        # Disable caching of results for this set of subproblem solves
        # so we can restore the original results. we modify the scenarios
        # and re-solve - which messes up the warm-start, which can 
        # seriously impact the performance of PH. plus, we don't want lower
        # bounding to impact the primal PH in any way - it should be free
        # of any side effects.
        ph.solve_subproblems(warmstart=not ph._disable_warmstarts)

        # compute the bound
        self._compute_bound(ph,storage_key)
        
        if ph._drop_proximal_terms is False:
            # reactivate proximal terms
            ph.activate_ph_objective_proximal_terms(transmit=True)

        # restore the original PH weights - we shouldn't need to
        # preprocess because we change the objective all the time in
        # the PH master.
        self._restore_ph_weights(ph)

        # restore the values of variables to their values prior to
        # invocation of this method. this will ensure that warm-starts
        # will be retained, and that the parent (primal) PH will not
        # be impacted.
        ph.restoreCachedScenarioSolutions()

        # Refix all previously fixed variables
        for tree_node in ph._scenario_tree._tree_nodes:
            for variable_id, fix_value in iteritems(ph_fixed[tree_node._name]):
                tree_node.fix_variable(variable_id, fix_value)

        # Push fixed variable statuses to instances (or
        # transmit to the phsolverservers)
        ph._push_fixed_to_instances()

        # Restore the fix_queue
        for tree_node in ph._scenario_tree._tree_nodes:
            tree_node._fix_queue.update(ph_fix_queue[tree_node._name])

        # Restore the solutions on the scenarios objects in the tree
        for scenario_name, scenario_solution in iteritems(ph_solutions):
            scenario = ph._scenario_tree.get_scenario(scenario_name)
            scenario.update_current_solution(scenario_solution)

        # Re-enable solution caching
        ph._enable_solution_caching = True


    #
    # Calculates the probability weighted sum of all suproblem (or
    # bundle) objective functions. Assumes all instances (or bundles)
    # have been solved and loaded with results so that when the
    # objective function expressions are evaluated the current optimal
    # solution is returned.
    #
    def _compute_bound(self,ph, storage_key):

        objective_bound = 0.0
        # doesn't matter if we are bundling, this gives the same
        # answer as using bundle objectives
        for scenario in ph._scenario_tree._scenarios:
            this_objective_value = scenario._objective
            this_gap = ph._gaps[scenario._name]
            if not isinstance(this_gap,UndefinedData):
                if self._is_minimizing:
                    this_objective_value -= this_gap
                else:
                    this_objective_value += this_gap
            objective_bound += (scenario._probability * this_objective_value)

        print("Computed objective lower bound=%12.4f" % objective_bound)

        self._bound_history[storage_key] = objective_bound

    #
    # 
    # 
    def _construct_bundle_dual_master_model(self, ph):

        self._master_model = ConcreteModel()
        for scenario in ph._scenario_tree._scenarios:
            for tree_node in scenario._node_list[:-1]:
                new_w_variable_name = "WVAR_"+tree_node._name+"_"+scenario._name
                new_w_k_parameter_name = "WDATA_"+tree_node._name+"_"+scenario._name+"_K"
                setattr(self._master_model,
                        new_w_variable_name,
                        Var(tree_node._standard_variable_ids,
                            within=Reals))
                setattr(self._master_model,
                        new_w_k_parameter_name,
                        Param(tree_node._standard_variable_ids,
                              within=Reals,
                              default=0.0,
                              mutable=True))
                setattr(self._master_model,
                        "V_"+scenario._name,
                        Var(within=Reals))
                # HERE - NEED TO MAKE CK VARAIBLE-DEPENDENT - PLUS WE NEED A SANE INITIAL VALUE (AND SUBSEQUENT VALUE)
        # DLW SAYS NO - THIS SHOULD BE VARIABLE-SPECIFIC
        setattr(self._master_model,
                "CK",
                Param(default=1.0, mutable=True))

        def obj_rule(m):
            expr = 0.0
            for scenario in ph._scenario_tree._scenarios:
                for tree_node in scenario._node_list[:-1]:
                    new_w_variable_name = "WVAR_"+tree_node._name+"_"+scenario._name
                    new_w_k_parameter_name = "WDATA_"+tree_node._name+"_"+scenario._name+"_K"            
                    w_variable = m.find_component(new_w_variable_name)
                    w_k_parameter = m.find_component(new_w_k_parameter_name)
                    expr += 1.0/(2.0*m.CK) * sum(w_variable[i]**2 - 2.0*w_variable[i]*w_k_parameter[i] for i in w_variable)
                expr -= getattr(m, "V_"+scenario._name)
            return expr

        self._master_model.TheObjective = Objective(sense=minimize, rule=obj_rule)

        self._master_model.W_Balance = ConstraintList()

        for stage in ph._scenario_tree._stages[:-1]:

            for tree_node in stage._tree_nodes:

                # GABE SHOULD HAVE A SERVICE FOR THIS???
                for idx in tree_node._standard_variable_ids:

                    expr = 0.0
                    for scenario in tree_node._scenarios:
                        scenario_probability = scenario._probability
                        new_w_variable_name = "WVAR_"+tree_node._name+"_"+scenario._name
                        w_variable = self._master_model.find_component(new_w_variable_name)
                        expr += scenario_probability * w_variable[idx]

                    self._master_model.W_Balance.add(expr == 0.0)

        # we can't populate until we see data from PH....
        self._master_model.V_Bound = ConstraintList()

#        self._master_model.pprint()

    #
    # populate the master bundle model from the PH parameters
    #
    def _populate_bundle_dual_master_model(self, ph):

        current_iteration = ph._current_iteration

        # first step is to update the historical information from PH

        for scenario in ph._scenario_tree._scenarios:
            primal_objective_value = scenario._objective
            self._past_objective_values[(current_iteration, scenario._name)] = primal_objective_value

#        print "PAST OBJECTIVE FUNCTION VALUES=",self._past_objective_values

        assert current_iteration not in self._past_var_values
        iter_var_values = self._past_var_values[current_iteration] = {}
        for scenario in ph._scenario_tree._scenarios:
            iter_var_values[scenario._name] = copy.deepcopy(scenario._x)

#        print "PAST VAR VALUES=",self._past_var_values

        # propagate PH parameters to concrete model and re-preprocess.
        for scenario in ph._scenario_tree._scenarios:
            for tree_node in scenario._node_list[:-1]:
                new_w_k_parameter_name = \
                    "WDATA_"+tree_node._name+"_"+scenario._name+"_K"
                w_k_parameter = \
                    self._master_model.find_component(new_w_k_parameter_name)
                ph_weights = scenario._w[tree_node._name]

                for idx in w_k_parameter:
                    w_k_parameter[idx] = ph_weights[idx]

        # V bounds are per-variable, per-iteration
        for scenario in ph._scenario_tree._scenarios:
            scenario_name = scenario._name
            v_var = getattr(self._master_model, "V_"+scenario_name)
            expr = self._past_objective_values[(current_iteration, scenario_name)]
            for tree_node in scenario._node_list[:-1]:
                new_w_variable_name = "WVAR_"+tree_node._name+"_"+scenario_name
                w_variable = self._master_model.find_component(new_w_variable_name)
                expr += sum(iter_var_values[scenario_name][tree_node._name][var_id] * w_variable[var_id] for var_id in w_variable)

            self._master_model.V_Bound.add(v_var <= expr)

#        print "V_BOUNDS CONSTRAINT:"
#        self._master_model.V_Bound.pprint()

        self._master_model.preprocess()

        solver = SolverFactory("cplex")
        results=solver.solve(self._master_model,tee=False)
        self._master_model.load(results)
#        print "MASTER MODEL WVAR FOLLOWING SOLVE:"
#        self._master_model.pprint()

#        self._master_model.pprint()

    # 
    # we often want to cache the current PH weights, in case the
    # convex hull weights don't work out - or if we're just using the
    # convex hull extension to compute lower bounds.
    #
    def _cache_ph_weights(self, ph):

        self._cached_ph_weights.clear()

        for scenario in ph._scenario_tree._scenarios:
            self._cached_ph_weights[scenario._name] = \
                copy.deepcopy(scenario._w)


    #
    # set the PH weights to the values found in the cache.
    #
    def _restore_ph_weights(self, ph):

        for scenario in ph._scenario_tree._scenarios:
            cached_weights = self._cached_ph_weights[scenario._name]
            scenario._w = copy.deepcopy(cached_weights)

    #
    # take the weights from the current convex hull master problem
    # solution, and push them into the PH scenario instances - so we
    # can do the solves and compute a lower bound.
    #

    def _push_weights_to_ph(self, ph):

        for scenario in ph._scenario_tree._scenarios:
            for tree_node in scenario._node_list[:-1]:

                new_w_variable_name = "WVAR_"+tree_node._name+"_"+scenario._name
                w_variable = self._master_model.find_component(new_w_variable_name)

                ph_weights = scenario._w[tree_node._name]

                for idx in w_variable:
                    ph_weights[idx] = w_variable[idx].value

    #
    # move the variable rhos from PH into the analogous CK parameter
    # in the convex hull master.
    #
    def _assign_cks(self, ph):
        
        # TBD: for now, we're just grabbing the default rho from PH - we need to
        #      extract them per-variable in the very near future.
        self._master_model.CK = ph._rho

    def report_best_bound(self):
        print("")
        print("PHBOUNDEXTENSION - REPORTING BEST OBJECTIVE BOUND ")
        best_bound = None
        if len(self._bound_history) > 0:
            if self._is_minimizing:
                best_bound = max(self._bound_history.values())
            else:
                best_bound = min(self._bound_history.values())
        print("Best Objective Bound: "+str(best_bound))
        print("")
        output_filename = "phbestbound.txt"
        output_file = open(output_filename,"w")
        output_file.write("%.17g\n" % best_bound)
        output_file.close()
        print("Best Lower Bound written to file="+output_filename)

    def report_bound_history(self):
        print("")
        print("PHBOUNDEXTENSION - REPORTING OBJECTIVE BOUND HISTORY")
        print("%15s %15s" % ("Iteration", "Bound"))
        output_filename = "phbound.txt"
        output_file = open(output_filename,"w")
        keys = list(self._bound_history.keys())
        if None in keys:
            keys.remove(None)
            print("%15s %15s" % ("Trival", self._bound_history[None]))
            output_file.write("Trivial: %.17g\n" % self._bound_history[None])
        for key in sorted(keys):
            print("%15s %15s" % (key, self._bound_history[key]))
            output_file.write("%d: %.17g\n" % (key,self._bound_history[key]))
        print("")
        output_file.close()
        print("Lower bound history written to file="+output_filename)

    ############ Begin Callback Functions ##############

    def pre_ph_initialization(self,ph):
        """
        Called before PH initialization.
        """
        pass

    def post_instance_creation(self, ph):
        """
        Called after PH initialization has created the scenario
        instances, but before any PH-related
        weights/variables/parameters/etc are defined!
        """
        pass

    def post_ph_initialization(self, ph):
        """
        Called after PH initialization!
        """
        self._is_minimizing = True if (ph._objective_sense == minimize) else False
        # TODO: Check for ph options that may not be compatible with
        #       this plugin and warn / raise exception
        
        # Enable ph's solution caching (which may be a little more
        # expensive)
        ph._enable_solution_caching = True

        # grab the update interval from the environment variable, if
        # it exists.
        update_interval_variable_name = "PHBOUNDINTERVAL"
        if update_interval_variable_name in os.environ:
            self._update_interval = int(os.environ[update_interval_variable_name])
            print("PH lower bound etension using update interval="
                  +str(self._update_interval)+", extracted from "
                  "environment variable="+update_interval_variable_name)
        else:
            print("PH lower bound etension using default update "
                  "interval="+str(self._update_interval))

        print("***INSIDE CONVEX HULL POST-PH INITIALIZATION CALLBACK***")

        self._construct_bundle_dual_master_model(ph)

    def post_iteration_0_solves(self, ph):
        """Called after the iteration 0 solves!"""
        if ph._verbose:
            print("Invoking post iteration 0 solve callback in PH bounds extension")

        # Always compute a lower/upper bound here because it requires
        # no work.  The instances (or bundles) have already been
        # solved with the original (non-PH-augmented) objective and
        # are loaded with results.
        
        # Warn if the iteration 0 solves were performed with a mipgap.
        # Hopefully no plugins change this option on the ph class
        # after the solves but before now.
        # I think wwphextension does this in post_iteration_0, so we
        # should be safe in that regard.
        if (ph._mipgap is not None) or (ph._mipgap > 0):
            logger.warn("A nonzero mipgap was detected when using the "
                        "phboundextension plugin. The bound computation "
                        "may as a result be conservative.")

        self._compute_bound(ph,None)

        if ph._verbose:
            print("Lower bound=%12.4f" % self._bound_history[None])

        # YIKES - WHY IS THIS HERE????!!
        self._populate_bundle_dual_master_model(ph)

    def post_iteration_0(self, ph):
        """
        Called after the iteration 0 solves, averages computation, and
        weight computation!
        """
        pass

    def pre_iteration_k_solves(self, ph):
        """
        Called immediately before the iteration k solves!
        """
        if ph._verbose:
            print("Invoking pre iteration k solve callback in PH bounds extension")

        if ((ph._current_iteration-1) % self._update_interval) != 0:
            return

        self._iteration_k_bound_solves(ph,ph._current_iteration-1)

        if ph._verbose:
            print("Lower bound=%12.4f" % self._bound_history[ph._current_iteration])

        # YIKES - WHY IS THIS HERE????!!
        self._populate_bundle_dual_master_model(ph)

        if ph._current_iteration > 5:
            print("WE ARE PAST ITERATION 5 - STARTING TO TRUST CONVEX "
                  "HULL BOUND EXTENSION FOR WEIGHT UPDATES")
            ph._ph_weight_updated_enabled = False
            self._push_weights_to_ph(ph)

    def post_iteration_k_solves(self, ph):
        """
        Called after the iteration k solves!
        """
        pass

    def post_iteration_k(self, ph):
        """
        Called after the iteration k is finished, after weights have
        been updated!
        """
        pass

    def post_ph_execution(self, ph):
        """
        Called after PH has terminated!
        """

        if ph._verbose:
            print("Invoking post execution callback in PH bounds extension")

        if (ph._current_iteration % self._update_interval) == 0:
            self._iteration_k_bound_solves(ph,ph._current_iteration)

        self.report_bound_history()
        self.report_best_bound()
