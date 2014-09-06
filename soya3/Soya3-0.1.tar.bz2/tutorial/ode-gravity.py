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

import sys, os

import soya3 as soya



soya.init("first ODE test",width=1024,height=768)

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))


# create a world
scene = soya.World()
# load a model
head_model = soya.Model.get("caterpillar_head")
# instanciate two Body
heads = [ soya.Body(scene,head_model) for i in range(2)]
# adding two mass
for head in heads:
    head.mass = soya.SphericalMass()
# Setting the gravity of the scene
scene.gravity = soya.Vector(scene,0,-9.8,0)
#Set whether the body is influenced by the world's gravity
#or not. If body.gravity_mode is True it is, otherwise it isn't.
#(default to True)
heads[0].gravity_mode = False
heads[1].gravity_mode = True
#place the head
heads[0].x=-3
heads[0].x= 3

#light and camera stuff
light = soya.Light(scene)
light.set_xyz(30, 5, -30)

camera = soya.Camera(scene)
camera.z = 25

soya.set_root_widget(camera)
ml = soya.MainLoop(scene)
ml.main_loop()
