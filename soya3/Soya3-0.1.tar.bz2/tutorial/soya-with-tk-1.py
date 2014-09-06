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


# soya-with-tk-1: Using Soya inside Tk mainloop

# In this lesson, we'll embed Soya's MainLoop inside a Tk mainloop.
# Interfacing Soya with other GUI system should be very similar.
# Notice that, if you have the choice, using the MainLoop in the "normal way"
# may give a smoother animation.


# Import the Soya and Tkinter module.

import sys, os, os.path, soya3 as soya, soya3.gui, tkinter

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates a scene.

scene = soya.World()

# Create a body displaying a caterpillar head.

head = soya.Body(scene, soya.Model.get("caterpillar_head"))

# Creates a light.

light = soya.Light(scene)
light.set_xyz(2.0, 5.0, 0.0)

# Creates a camera.

camera = soya.Camera(scene)
camera.set_xyz(0.0, 15.0, 15.0)
camera.look_at(head)

# Creates a widget group, containing the camera and a label showing the FPS.

soya.set_root_widget(soya.gui.RootLayer(None))
soya.gui.CameraViewport(soya.root_widget, camera)
soya.gui.FPSLabel(soya.root_widget)

# Create the MainLoop, but DON'T start it (= don't call MainLoop.main_loop()).

soya.MainLoop(scene)


# Create a Tk window, with a button.
# When the button is clicked, the head moves up.

class Window(tkinter.Tk):
  def __init__(self):
    tkinter.Tk.__init__(self)
    
    self.button = tkinter.Button(self, text = "Move upward", command = self.button_click)
    self.button.pack()
    
    # Call self.update_soya() in 30 milliseconds (see after's doc for more info).
    
    self.after(30, self.update_soya)
    
  def button_click(self):
    head.y += 1
    
  def update_soya(self):
    
    # Call again self.update_soya(), in 30 milliseconds.
    # This should be done BEFORE calling soya.MAIN_LOOP.update(), since update may consume time!
    
    self.after(30, self.update_soya)
    
    # Update Soya, and render.
    
    soya.MAIN_LOOP.update()
    
window = Window()

tkinter.mainloop()
