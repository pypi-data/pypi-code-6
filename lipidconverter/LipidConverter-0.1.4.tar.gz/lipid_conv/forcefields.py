#Lipid-converter.py
#Copyright (C) 2014 Per Larsson Peter Kasson 

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.

#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the
#Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
#Boston, MA  02110-1301, USA.

# This needs to be updated when a new forcefield is introduced
ff_transformations = ['charmm36',
                      'berger',
                      'gromos43a1-S3',
                      'gromos53a6',
                      'gromos54a7',
                      'opls',
                      'lipid11']

ff_conversions = ['charmm36',
                  'gromos43a1-S3',
                  'berger']

ff_sortings = ['charmm36',
               'berger',
               'gromos43a1-S3',
               'gromos54a7',
               'gromos53a6',
               'opls',
               'lipid11']

# These are all lipids that are defined in the current 
# release of amber/lipid11, and how they are made
# up of different headgroups and tails, as well
# as the corresponding "normal" name in charmm36
lipid11_residues = {'DPPC':['PA','PC','PA'],
                    'DPPE': ['PA','PE','PA'],
                    'DPPS': ['PA','PS','PA'],
                    'DPPG': ['PA','PGR','PA'],
                    'DPPA': ['PA','PH-','PA'],
                    'DOPC': ['OL','PC','OL'],
                    'DOPE': ['OL','PE','OL'],
                    'DOPS': ['OL','PS','OL'],
                    'DOPG': ['OL','PGR','OL'],
                    'DOPA': ['OL','PH-','OL'],
                    'POPC': ['PA','PC','OL'],
                    'POPE': ['PA','PE','OL'],
                    'POPS': ['PA','PS','OL'],
                    'POPG': ['PA','PGR','OL'],
                    'POPA': ['PA','PH-','OL']}


is_lipid = ['POPC','POPE','POPG','POPS','DMPC','DOPC','DPPC']
