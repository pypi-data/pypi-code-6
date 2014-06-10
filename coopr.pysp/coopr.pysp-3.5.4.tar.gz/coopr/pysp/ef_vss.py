#  _________________________________________________________________________
#
#  Coopr: A COmmon Optimization Python Repository
#  Copyright (c) 2013 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  For more information, see the Coopr README.txt file.
#  _________________________________________________________________________

from coopr.core.plugin import *
from coopr.pysp import phextension
from coopr.pyomo import Param, value
from coopr.opt import SolverFactory
from copy import deepcopy
from coopr.pysp import create_ef_instance, write_ef, SolverManagerFactory

def create_expected_value_instance(average_instance, scenario_tree, scenario_instances, verbose=False):

    rootnode = scenario_tree._stages[0]._tree_nodes[0]
    ScenCnt = len(rootnode._scenarios)

    for p in average_instance.active_components(Param):

        average_parameter_object = getattr(average_instance, p)

        for index in average_parameter_object:
            average_value = 0.0
            for scenario in rootnode._scenarios:
                scenario_parameter_object = getattr(scenario_instances[scenario._name], p)
                average_value += value(scenario_parameter_object[index])
            average_value = average_value / float(len(scenario_instances))
            average_parameter_object[index] = average_value

    average_instance.preprocess()

def fix_ef_first_stage_variables(scenario_tree, expected_value_instance):

    if ph._verbose:
        print "Fixing first stage variables at mean instance solution values."

    stage = ph._scenario_tree._stages[0]
    root_node = stage._tree_nodes[0] # there should be only one root node!
    for variable_name, index_template in stage._variables.iteritems():

        variable_indices = root_node._variable_indices[variable_name]
        for index in variable_indices:
            for scen in root_node._scenarios:
                inst = ph._instances[scen._name]
                print "HEYYYY fix varstatus !!!!!xxxxxx"
                #if getattr(inst, variable_name)[index].status != VarStatus.unused:
                if 1 == 1:
                    print "variable_name=",variable_name
                    fix_value = getattr(average_instance, variable_name)[index].value
                    getattr(inst, variable_name)[index].fixed = True
                    getattr(inst, variable_name)[index].value = fix_value



