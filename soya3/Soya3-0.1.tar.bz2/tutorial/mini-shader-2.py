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


# mini-shader-2: Soya's Mini Shaders : passing parameters to mini shaders

# Mini shaders can have parameters.


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


# A second Balazar

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(0.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")


# The djinn mini shader has been modified to add a parameter called "cut_at", which indicates
# at which Y value the djin effect begins.

# Parameters must be declared as "uniform" in GLSL.

# In Soya, parameters are prefixed with "self." to avoid name clash (if another mini shader
# uses the same paramater name). 


djinn_mini_shader = soya.MiniShader("djinn", """
uniform float self.cut_at

def void bodyspace_deform_mini_shader():
  float factor
  if gl_Vertex.y < self.cut_at:
    factor = gl_Vertex.y / self.cut_at
    current_vertex.x = current_vertex.x * factor * factor
    current_vertex.z = current_vertex.z * factor * factor
""")

# Add the djinn mini shader to the second Balazar, with a cut_at value of 1.0.

balazar2.add_mini_shader(djinn_mini_shader(cut_at = 1.0))


# Create a third Balazar

balazar3 = soya.Body(scene, balazar_model)
balazar3.set_xyz(1.0, -1.5, 0.0)
balazar3.rotate_y(120.0)
balazar3.animate_blend_cycle("attente")

# Add the djinn mini shader to the third Balazar, with a cut_at value of 1.7.

balazar3.add_mini_shader(djinn_mini_shader(cut_at = 1.7))


# The following special variables are available in mini shader's code :

# Usefull GLSL variables:

#   gl_Vertex      : the original vertex position, in body space (not modified during the rendering)
#   gl_Normal      : the original vertex normal, in body space (not modified during the rendering)
#   gl_Color       : the original vertex color (not modified during the rendering)
#   gl_FragCoord   : the original pixel position (not modified during the rendering)
#   gl_TexCoord[0] : the current texture coords

# Soya's special variables:

#   current_vertex     : the current vertex position, modified through the rendering pipeline
#   current_normal     : the current vertex normal, modified through the rendering pipeline
#   current_color      : the current vertex or pixel color, modified through the rendering pipeline
#   current_fog_factor : the current fog factor (1.0: no fog, 0.0: 100% fog), modified through the rendering pipeline

#   textures_enabled : 1 if texturing is enabled
#   texture0         : the texture

#   lights_enabled : lights status (bitset, bit 1 is enabled status for light0, bit 2 for light1, etc)
#   lighting_mode  : lighting mode (0: lighting disabled, 1: lighting enabled)
#   fog_type       : fog type (-1: fog disabled, 0: linear, 1: exponential, 2: exponential squared)


light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


