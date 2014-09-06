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


# mini-shader-3: Soya's Mini Shaders : time parameter


import sys, os, os.path, soya3 as soya

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

scene = soya.World()

balazar_model = soya.AnimatedModel.get("balazar")

# A first normal Balazar

balazar1 = soya.Body(scene, balazar_model)
balazar1.set_xyz(-1.0, -1.5, 0.0)
balazar1.rotate_y(120.0)
balazar1.animate_blend_cycle("attente")

# A second Balazar, after eating too many mushrooms!

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(1.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")


# Here, we define a CameraSpaceDeformMiniShader: a mini shader that deforms the model's geometry
# in the camera space (= the X direction corresponds to the right of the screen).
# This mini shader will deforms the model with a wavy effect.

# The special parameter "time" (self.time) is automagically updated by Soya.

wavy_mini_shader = soya.MiniShader("wavy", """
uniform float self.time

def void cameraspace_deform_mini_shader():
  current_vertex.x = current_vertex.x + 0.2 * sin(0.2 * self.time + 3 * current_vertex.y)

  # You may try this variant
  #current_vertex.x = current_vertex.x + 0.1 * gl_Vertex.y * sin(0.2 * self.time + 3 * current_vertex.y)
""")

# Add the wavy mini shader to the second Balazar.

balazar2.add_mini_shader(wavy_mini_shader())




light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


