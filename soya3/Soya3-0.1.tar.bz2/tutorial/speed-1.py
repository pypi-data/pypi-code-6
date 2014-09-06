# -*- coding: utf-8 -*-

# Soya 3D
# Copyright (C) 2001-2014 Jean-Baptiste LAMY
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


# state-1: CoordSystState object

# In this lesson, you'll learn how to use CoordSystState to interpolate between
# two State (position, orientation and scaling) of a 3D object.


import sys, os, os.path, soya3 as soya, soya3.cube

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()


# Create a body class that interpolates between two States.

class InterpolatingBody(soya.Body):
  def __init__(self, parent = None, model = None):
    soya.Body.__init__(self, parent, model)
    
    self.speed  = soya.CoordSystSpeed(None)
    
    self.state1 = soya.CoordSystState(self)
    self.state2 = soya.CoordSystState(self)
    
    self.factor = 0.0
    
  def begin_round(self):
    self.factor = 0.0
    self.state1 = self.state2
    self.state2 = soya.CoordSystState(self)
    self.state2.add_speed(self.speed)
    
  def advance_time(self, proportion):
    self.factor += proportion
    self.interpolate(self.state1, self.state2, self.factor)


body = InterpolatingBody(scene, soya.cube.Cube(None).to_model())

# Moves, rotates and scales the States.
# Notice that States have the Soya's usual positioning method (actually State even inherit
# from CoordSyst).

body.speed.x = 0.2
body.speed.rotate_y(2.0)


# Adds a light.

light = soya.Light(scene)
light.set_xyz(0.0, 0.2, 1.0)

# Creates a camera.

camera = soya.Camera(scene)
camera.set_xyz(0.0, 0.0, 4.0)
camera.fov = 100.0
soya.set_root_widget(camera)


# Main loop

soya.MainLoop(scene).main_loop()


# TODO / exercice : turn this demo into a puzzle game !
