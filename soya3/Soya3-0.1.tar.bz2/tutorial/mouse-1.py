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


# mouse-1: 3D mouse cursor

# In this lesson, you'll learn how to display a 3D mouse cursor.

# See the raypicking-2 tuto for more mouse-oriented tutorials.


import sys, os, os.path, soya3 as soya, soya3.cube, soya3.sdlconst

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()


class Cursor(soya.Body):
  def __init__(self, parent, model = None):
    soya.Body.__init__(self, parent, model)
    
  def begin_round(self):
    soya.Body.begin_round(self)
    
    # Processes the events
    
    for event in soya.MAIN_LOOP.events:
      
      if event[0] == soya.sdlconst.MOUSEMOTION:
        self.mouse_pos = camera.coord2d_to_3d(event[1], event[2], -15.0)
        self.move(self.mouse_pos)
        
green = soya.Material(); green.diffuse = (0.0, 1.0, 0.0, 1.0)

Cursor(scene, soya.cube.Cube(None, green).to_model())

# Adds a light.

light = soya.Light(scene)
light.set_xyz(0.0, 0.2, 1.0)

# Creates a camera.

camera = soya.Camera(scene)
camera.set_xyz(0.0, 0.0, 4.0)
camera.fov = 100.0
soya.set_root_widget(camera)


# Main loop
try:
  soya.MainLoop(scene).main_loop()
except:
  soya.render(); soya.screenshot().resize((320, 240)).save(os.path.join(os.path.dirname(sys.argv[0]), "results", os.path.basename(sys.argv[0])[:-3] + ".jpeg"))

