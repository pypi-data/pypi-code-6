# -*- coding: utf-8 -*-

# Soya 3D
# Copyright (C) 2001-2014 Jean-Baptiste LAMY
# Copyright (C) 2004-2012 Marmoute - Pierre-Yves David - marmoute@nekeme.net
# http://www.lesfleursdunormal.fr/static/informatique/soya3d/index_en.html

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# The two body will now have different wheight.
# the most heavy will be leess deviante than the other one

import sys, os

import soya3 as soya


soya.init("collision-3-mass_influence",width=1024,height=768)
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# create world
scene = soya.World()
# getting the head model
head_model = soya.Model.get("caterpillar_head")
# creating two head
heads = (
  soya.Body(scene,head_model),
  soya.Body(scene,head_model))
## Adding a mass ##
heads[0].mass = soya.SphericalMass()
heads[1].mass = soya.SphericalMass(8)

### Creating a Geometry object __for each__ Body###
soya.GeomSphere(heads[0],1.2)
soya.GeomSphere(heads[1],1.2)
######
#placing the body face to face
heads[0].x = -25
heads[1].x =  25
heads[0].look_at(heads[1])
heads[1].look_at(heads[0])
heads[0].set_xyz(-25,-0.5,-0.7)
heads[1].set_xyz(25,0.4,0.8)
#pushing them forward
heads[0].add_force(soya.Vector(heads[0],0,0,-1000))
heads[1].add_force(soya.Vector(heads[1],0,0,-8000)) # the bigger body need a bigger push

#placing light over the duel
light = soya.Light(scene)
light.set_xyz(0, 15,0)
# adding camera
camera = soya.Camera(scene)
camera.set_xyz(0,0,50)
#running soya
soya.set_root_widget(camera)
ml = soya.MainLoop(scene)
ml.main_loop()
