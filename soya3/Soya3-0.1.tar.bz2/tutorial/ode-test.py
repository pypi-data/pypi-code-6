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


#create world

ode_world = soya.World()
#scene = ode_world
scene = soya.World(ode_world)
#activate ODE support



sword_model = soya.Model.get("sword")

sword = soya.Body(scene,sword_model)
sword.ode = True
sword.x = 1.0

blade = soya.BoxedMass(0.00005,50,5,1)
pommeau = soya.SphericalMass(50,0.5)
pommeau.translate((25,0,0))
sword.mass = blade+pommeau

def v (x,y,z):
  return soya.Vector(sword,x,y,z)
sword.add_force(v(10,200,0),v(25,0.001,0.002))
sword.add_force(v(0,60,0),v(0,25,0.5))
sword.add_force(v(0,0,-2303*5),v(-25,0.0001,0.0001))

head_model = soya.Model.get("caterpillar_head")
head = soya.Body(scene,head_model)
head.ode = True
head.mass = soya.SphericalMass(1,1,"total_mass")

head.add_force(soya.Vector(head,15,34,56),soya.Vector(head,0.4,0.3,0.2))
head.add_force(soya.Vector(scene,-150,1,-500))
head.z  = 0
head.x  = 20
head.y  = -5
scene.turn_x = 34
scene.turn_y = 23
scene.turn_z = 12

light = soya.Light(scene)
light.set_xyz(30, 5, -30)

camera = soya.Camera(scene)
camera.z = 5.0
camera.x = 1
camera.y = 1


scene.z = -5
scene.x = 0.5
scene.y = 0.5
ode_world.gravity = soya.Vector(ode_world,0.0005,-0.03,2)
soya.set_root_widget(camera)
ml = soya.MainLoop(ode_world)
ml.main_loop()
