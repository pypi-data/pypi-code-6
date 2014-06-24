#!python
# Copyright (c) 2014, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of iggy.
#
# iggy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iggy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iggy.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from pyasp.asp import *
import argparse
from __iggy__ import query, utils, bioquali

if __name__ == '__main__':
       
    parser = argparse.ArgumentParser()
    parser.add_argument("networkfile",
                        help="influence graph in SIF format")
    parser.add_argument("observationfile",
                        help="observations in bioquali format")
                        
    parser.add_argument('--no_zero_constraints',
			help="turn constraints on zero variations OFF, default is ON",
			action="store_true")
			
    parser.add_argument('--propagate_unambigious_influences',
			help="turn constraints ON that if all predecessor of a node have the same influence this must have an effect, default is ON",
			action="store_true")
			
    parser.add_argument('--no_founded_constraint',
			help="turn constraints OFF that every variation must be explained by an input, default is ON",
			action="store_true")
			
    parser.add_argument('--autoinputs',
			help="compute possible inputs of the network (nodes with indegree 0)",
			action="store_true")

    parser.add_argument('--scenfit',
			help="compute scenfit of the data, default is mcos",
			action="store_true")
    
    parser.add_argument('--show_colorings',type=int, default=-1,
			help="number of colorings to print, default is OFF, 0=all")

    parser.add_argument('--show_predictions',
			help="show predictions",
			action="store_true")

			
			

    args = parser.parse_args()
    
    net_string = args.networkfile
    obs_string = args.observationfile

    LC =args.propagate_unambigious_influences
    CZ= not (args.no_zero_constraints)
    FC= not (args.no_founded_constraint)

    print ' all observed changes must be explained by an predecessor'
    if LC : print ' unambigious influences propagate'
    if CZ : print ' no-change observations must be explained'
    if FC : print ' all observed changes must be explained by an input'
    
    print '\nReading network',net_string, '...',
    net = bioquali.readSIFGraph(net_string)
    print 'done.'
    edge_counter=0
    activation_counter=0
    inhibition_counter=0
    node_counter=0
    for a in net:
      if a.pred() == 'edge' : edge_counter+=1
      if a.pred() == 'obs_elabel' :
	if a.arg(2) == '1' : activation_counter+=1
        if a.arg(2) == '-1' : inhibition_counter+=1
      if a.pred() == 'vertex' : node_counter+=1
    print "   Nodes:",node_counter," Edges:",edge_counter," Activations:",activation_counter," Inhibitions:",inhibition_counter," Unspecified:",(edge_counter-(activation_counter+inhibition_counter))

    print '\nReading observations',obs_string, '...',
    mu = bioquali.readProfile(obs_string)
    print 'done.'
    count_plus=0
    count_zero=0
    count_minus=0
    count_notminus=0
    count_notplus=0
    count_inputs=0
    for a in mu:
      if a.pred() == 'obs_vlabel' :
        if a.arg(2) == '1' : count_plus+=1
	if a.arg(2) == '0' : count_zero+=1 
	if a.arg(2) == '-1' : count_minus+=1 
	if a.arg(2) == 'notMinus' : count_notminus+=1
	if a.arg(2) == 'notPlus' : count_notplus+=1
      if a.pred() == 'input' :count_inputs+=1
    print "   observed +:",count_plus, "observed -:",count_minus," observed 0:",count_zero," observed notPlus:",count_notplus," observed notMinus:",count_notminus," unobserved:",(node_counter-(count_plus+count_minus+count_plus+count_notminus+count_notplus)),' inputs:',count_inputs

    if args.autoinputs :
      print '\nComputing input nodes ...',
      inputs = query.guess_inputs(net)
      net = net.union(inputs)
      print 'done.'
      print "   number of inputs:", len(inputs)
	
    net_with_data = net.union(mu)

    if args.scenfit :
      print '\nComputing scenfit of network and data ...',
      scenfit = query.get_scenfit(net_with_data, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
      print 'done.'
      if scenfit == 0 : print "   The network and data are consistent: scenfit = 0."
      else: print "   The network and data are inconsistent: scenfit = "+str(scenfit)+'.'


      if args.show_colorings >= 0 :
	print '\nCompute scenfit colorings...',
	colorings = query.get_scenfit_colorings(net_with_data, args.show_colorings, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
	print 'done.'
	count=0
	for c in colorings :
	  count+=1
	  print 'Coloring',str(count)+':'
	  utils.print_coloring(c)

      if args.show_predictions :
	print '\nCompute predictions under scenfit ...',
	predictions = query.get_predictions_under_scenfit(net_with_data, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
	print 'done.'
	utils.print_predictions(predictions)



    if not args.scenfit :
      print '\nComputing mcos of network and data ...',
      mcos = query.get_mcos(net_with_data, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
      print 'done.'
      if mcos == 0 : print "   The network and data are consistent: mcos = 0."
      else: print "   The network and data are inconsistent: mcos = "+str(mcos)+'.'


      if args.show_colorings >= 0 :
	print '\nCompute mcos colorings...',
	colorings = query.get_mcos_colorings(net_with_data, args.show_colorings, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
	print 'done.'
	count=0
	for c in colorings :
	  count+=1
	  print 'Coloring',str(count)+':'
	  utils.print_coloring(c)

      if args.show_predictions :
	print '\nCompute predictions under mcos ...',
	predictions = query.get_predictions_under_mcos(net_with_data, LucaConstraint=LC, ConstrainedZero=CZ, FoundedConstraint=FC)
	print 'done.'
	utils.print_predictions(predictions)








      #if args.mics:
        #print '\nComputing minimal inconsistent cores (mic\'s) ...',
        #mics = query.get_minimal_inconsistent_cores(net_with_data)
        #print 'done.'
        #count = 1
        #oldmic = 0
        #for mic in mics:
          #if oldmic != mic:
            #print 'mic '+str(count)+':'
            #utils.print_mic(mic.to_list(),net.to_list(),mu.to_list())
            #count+=1
            #oldmic= mic

 

    utils.clean_up()



