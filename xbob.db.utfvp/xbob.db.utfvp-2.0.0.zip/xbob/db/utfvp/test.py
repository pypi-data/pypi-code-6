#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the UTFVP database.
"""

import os, sys
import unittest
import xbob.db.utfvp

class UTFVPDatabaseTest(unittest.TestCase):
  """Performs various tests on the UTFVP database."""

  def test01_clients(self):
    # test whether the correct number of clients is returned
    db = xbob.db.utfvp.Database()
    
    self.assertEqual(len(db.groups()), 3)
    self.assertEqual(len(db.protocols()), 8)
    self.assertEqual(len(db.protocol_names()), 8)
    self.assertEqual(len(db.purposes()), 3)

    self.assertEqual(len(db.clients()), 360)
    self.assertEqual(len(db.clients(protocol='1vsall')), 360)
    self.assertEqual(len(db.clients(protocol='nom')), 360)
    self.assertEqual(len(db.clients(protocol='nomLeftRing')), 60)
    self.assertEqual(len(db.clients(protocol='nomLeftMiddle')), 60)
    self.assertEqual(len(db.clients(protocol='nomLeftIndex')), 60)
    self.assertEqual(len(db.clients(protocol='nomRightIndex')), 60)
    self.assertEqual(len(db.clients(protocol='nomRightMiddle')), 60)
    self.assertEqual(len(db.clients(protocol='nomRightRing')), 60)
    
    self.assertEqual(len(db.client_ids()), 360)
    self.assertEqual(len(db.client_ids(protocol='1vsall')), 360)
    self.assertEqual(len(db.client_ids(protocol='nom')), 360)
    self.assertEqual(len(db.client_ids(protocol='nomLeftRing')), 60)
    self.assertEqual(len(db.client_ids(protocol='nomLeftMiddle')), 60)
    self.assertEqual(len(db.client_ids(protocol='nomLeftIndex')), 60)
    self.assertEqual(len(db.client_ids(protocol='nomRightIndex')), 60)
    self.assertEqual(len(db.client_ids(protocol='nomRightMiddle')), 60)
    self.assertEqual(len(db.client_ids(protocol='nomRightRing')), 60)

    self.assertEqual(len(db.models()), 1900) #1300 + 300 + 50 * 6
    self.assertEqual(len(db.models(protocol='1vsall')), 1300)
    self.assertEqual(len(db.models(protocol='nom')), 300)
    self.assertEqual(len(db.models(protocol='nomLeftRing')), 50)
    self.assertEqual(len(db.models(protocol='nomLeftMiddle')), 50)
    self.assertEqual(len(db.models(protocol='nomLeftIndex')), 50)
    self.assertEqual(len(db.models(protocol='nomRightIndex')), 50)
    self.assertEqual(len(db.models(protocol='nomRightMiddle')), 50)
    self.assertEqual(len(db.models(protocol='nomRightRing')), 50)

    self.assertEqual(len(db.model_ids()), 1900) #1300 + 300 + 50 * 6
    self.assertEqual(len(db.model_ids(protocol='1vsall')), 1300)
    self.assertEqual(len(db.model_ids(protocol='nom')), 300)
    self.assertEqual(len(db.model_ids(protocol='nom', groups='dev')), 108) #18 subjects *6 fingers
    self.assertEqual(len(db.model_ids(protocol='nom', groups='eval')), 192) #32 subjects *6 fingers

    self.assertEqual(len(db.model_ids(protocol='nomLeftRing')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomLeftRing', groups='dev')), 18) 
    self.assertEqual(len(db.model_ids(protocol='nomLeftRing', groups='eval')), 32)

    self.assertEqual(len(db.model_ids(protocol='nomLeftMiddle')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomLeftMiddle', groups='dev')), 18)
    self.assertEqual(len(db.model_ids(protocol='nomLeftMiddle', groups='eval')), 32)

    self.assertEqual(len(db.model_ids(protocol='nomLeftIndex')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomLeftIndex', groups='dev')), 18)
    self.assertEqual(len(db.model_ids(protocol='nomLeftIndex', groups='eval')), 32)

    self.assertEqual(len(db.model_ids(protocol='nomRightIndex')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomRightIndex', groups='dev')), 18)
    self.assertEqual(len(db.model_ids(protocol='nomRightIndex', groups='eval')), 32)

    self.assertEqual(len(db.model_ids(protocol='nomRightMiddle')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomRightMiddle', groups='dev')), 18)
    self.assertEqual(len(db.model_ids(protocol='nomRightMiddle', groups='eval')), 32)

    self.assertEqual(len(db.model_ids(protocol='nomRightRing')), 50)
    self.assertEqual(len(db.model_ids(protocol='nomRightRing', groups='dev')), 18)
    self.assertEqual(len(db.model_ids(protocol='nomRightRing', groups='eval')), 32)


  def test02_objects(self):
    # tests if the right number of File objects is returned
    db = xbob.db.utfvp.Database()
    
    # Protocol '1vsall'
    self.assertEqual(len(db.objects(protocol='1vsall')), 1440) #1440 - 60 users * 6 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='1vsall', groups='world')), 140) #35 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='1vsall', groups='world', purposes='train')), 140) #35 fingers * 4 acq

    # Dev group
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev')), 1300) #(1440-140)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',))), 1300)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', purposes='enrol')), 1300)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='enrol')), 1)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe')), 1299)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', purposes='probe', classes='impostor')), 1300)
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='client')), 3) # 4 acq - 1
    self.assertEqual(len(db.objects(protocol='1vsall', groups='dev', model_ids=('1_2_3',), purposes='probe', classes='impostor')), 1296) #1300 - 4 acq   
    

    #####################################################
    # Protocol 'nom'
    self.assertEqual(len(db.objects(protocol='nom')), 1440) #1440 - 60 subjects * 6 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nom', groups='world')), 240) #10 users * 6 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nom', groups='world', purposes='train')), 240) #10 users * 6 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nom', groups='dev')), 432) #18 users * 6 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',))), 218) #18 users * 6 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', purposes='enrol')), 216) #18 users * 6 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe')), 216) #18 users * 6 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nom', groups='dev', model_ids=('11_2',), purposes='probe', classes='impostor')), 214) #384 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nom', groups='eval')), 768) #32 users * 6 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',))), 386) #32 users * 6 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', purposes='enrol')), 384) #18 users * 6 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='enrol')), 2) 
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe')), 384) #18 users * 6 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nom', groups='eval', model_ids=('30_2',), purposes='probe', classes='impostor')), 382) #384 - 2 
    

    #####################################################
    # Protocol 'nomLeftRing'
    self.assertEqual(len(db.objects(protocol='nomLeftRing')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='dev', model_ids=('11_1',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftRing', groups='eval', model_ids=('30_1',), purposes='probe', classes='impostor')), 62) #64 - 2 
    

    #####################################################
    # Protocol 'nomLeftMiddle'
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='dev', model_ids=('11_2',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftMiddle', groups='eval', model_ids=('30_2',), purposes='probe', classes='impostor')), 62) #64 - 2 


    #####################################################
    # Protocol 'nomLeftIndex'
    self.assertEqual(len(db.objects(protocol='nomLeftIndex')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='dev', model_ids=('11_3',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomLeftIndex', groups='eval', model_ids=('30_3',), purposes='probe', classes='impostor')), 62) #64 - 2 


    #####################################################
    # Protocol 'nomRightIndex'
    self.assertEqual(len(db.objects(protocol='nomRightIndex')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='dev', model_ids=('11_4',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightIndex', groups='eval', model_ids=('30_4',), purposes='probe', classes='impostor')), 62) #64 - 2 


    #####################################################
    # Protocol 'nomRightMiddle'
    self.assertEqual(len(db.objects(protocol='nomRightMiddle')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='dev', model_ids=('11_5',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightMiddle', groups='eval', model_ids=('30_5',), purposes='probe', classes='impostor')), 62) #64 - 2 


    #####################################################
    # Protocol 'nomRightRing'
    self.assertEqual(len(db.objects(protocol='nomRightRing')), 240) #1440 - 60 subjects * 1 fingers * 4 acq

    # World group
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='world')), 40) #10 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='world', purposes='train')), 40) #10 users * 1 fingers * 4 acq
    
    # Dev group
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev')), 72) #18 users * 1 fingers * 4 acq
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',))), 38) #18 users * 1 fingers * 2 acq + 2
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', purposes='enrol')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe')), 36) #18 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='dev', model_ids=('11_6',), purposes='probe', classes='impostor')), 34) #36 - 2 
        
    # Eval group
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval')), 128) #32 users * 1 fingers * 4 acq  
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',))), 66) #32 users * 1 fingers * 2 acq + 2  
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', purposes='enrol')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='enrol')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe')), 64) #32 users * 1 fingers * 2 acq 
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe', classes='client')), 2)
    self.assertEqual(len(db.objects(protocol='nomRightRing', groups='eval', model_ids=('30_6',), purposes='probe', classes='impostor')), 62) #64 - 2 



  def test03_driver_api(self):

    from bob.db.script.dbmanage import main
    self.assertEqual(main('utfvp dumplist --self-test'.split()), 0)
    self.assertEqual(main('utfvp dumplist --protocol=1vsall --class=client --group=dev --purpose=enrol --model=1_2_3 --self-test'.split()), 0)
    self.assertEqual(main('utfvp checkfiles --self-test'.split()), 0)
    self.assertEqual(main('utfvp reverse 0001/0001_1_1_120509-135315 --self-test'.split()), 0)
    self.assertEqual(main('utfvp path 37 --self-test'.split()), 0)

