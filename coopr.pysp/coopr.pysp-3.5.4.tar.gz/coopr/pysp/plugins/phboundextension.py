import logging
import copy

from coopr.core.plugin import *
from coopr.pysp import phextension
from coopr.pysp.phutils import *
import coopr.solvers.plugins.smanager.phpyro

from coopr.core import DeveloperError
from coopr.opt import UndefinedData

from six import iteritems

logger = logging.getLogger('coopr.pysp')

class phboundextension(SingletonPlugin):

    coopr.core.plugin.implements(phextension.IPHExtension)

    coopr.core.plugin.alias("phboundextension")

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
        self._cntr = 0

    def _iteration_k_bound_solves(self,ph,storage_key):

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

        # Weights have not been pushed to instance parameters (or
        # transmitted to the phsolverservers) at this point
        ph._push_w_to_instances()

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

        # Push freed variable statuses on instances (or
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

    def report_best_bound(self):
        print("")
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
        print("%15s %15s" % ("Iteration", "Bound"))
        output_filename = "phbound.txt"
        output_file = open(output_filename,"w")
        keys = list(self._bound_history.keys())
        if None in keys:
            keys.remove(None)
            print("%15s %15s" % ("Trivial", self._bound_history[None]))
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
        Called after PH initialization
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
            print("PH lower bound extension using update interval="
                  +str(self._update_interval)+", extracted from "
                  "environment variable="+update_interval_variable_name)
        else:
            print("PH lower bound extension using default update "
                  "interval="+str(self._update_interval))

    def post_iteration_0_solves(self, ph):
        """
        Called after the iteration 0 solves
        """

        # Always compute a lower/upper bound here because it requires no work.
        # The instances (or bundles) have already been solved with the original
        # (non-PH-augmented) objective and are loaded with results.

        if ph._verbose:
            print("Invoking post iteration 0 solve callback in PH bounds extension")
        
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

    def post_iteration_0(self, ph):
        """
        Called after the iteration 0 solves, averages computation, and weight computation
        """
        pass

    def pre_iteration_k_solves(self, ph):
        """
        Called immediately before the iteration k solves
        """
        if ph._verbose:
            print("Invoking post iteration k solve callback in PH bounds extension")

        if ((ph._current_iteration-1) % self._update_interval) != 0:
            return

        self._iteration_k_bound_solves(ph,ph._current_iteration-1)

        if ph._verbose:
            print("Lower bound=%12.4f" % self._bound_history[ph._current_iteration])

    def post_iteration_k_solves(self, ph):
        """
        Called after the iteration k solves!
        """
        pass

    def post_iteration_k(self, ph):
        """
        Called after the iteration k is finished, after weights have been updated!
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

