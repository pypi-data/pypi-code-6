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


# mini-shader-inherited-parameters-1: Soya's Mini Shaders : inheriting mini shader's parameters

# In this lesson, we'll create several cellshaded characters, but the cellshading parameters
# (bright and dark colors, etc) will be defined in the scene, and then inherited by the characters.


import sys, os, os.path, soya3 as soya

# Initializes Soya (creates and displays the 3D window).

soya.init()

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

scene = soya.World()


balazar_model = soya.AnimatedModel.get("balazar")


balazar1 = soya.Body(scene, balazar_model)
balazar1.set_xyz(-1.5, -1.5, 0.0)
balazar1.rotate_y(120.0)
balazar1.animate_blend_cycle("attente")

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(0.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")

balazar3 = soya.Body(scene, balazar_model)
balazar3.set_xyz(1.5, -1.5, 0.0)
balazar3.rotate_y(120.0)
balazar3.animate_blend_cycle("attente")


# Add cellshading mini shader to the second and third Balazars (see lesson mini-shader-cellshading-1)
# but without specifying any parameter.

cellshading_mini_shader = soya.MiniShader.get("cellshading")

balazar2.add_mini_shader(cellshading_mini_shader())
balazar3.add_mini_shader(cellshading_mini_shader())


# Create a "parameter-setter" mini shader, for setting the cellshading's parameters in the scene.

# Those parameters will be inherited by each child of the scene, including the Balazars.

# This is interesting, because the cellshading paramaters are usually scene-dependent
# (e.g. a dark dungeon VS a lighful beach) rather than character-dependent.

scene.add_mini_shader(cellshading_mini_shader.parameters(
  bright_color_cut_at = 0.9,
  bright_color        = [1.5, 1.0, 0.0, 0.15],
  dark_color_cut_at   = 0.2,
  dark_color          = [0.2, -0.3, -0.3, 0.5],
  anti_alias          = 0.1,
))


light = soya.Light(scene)
light.set_xyz(-1.5, 0.0, 1.0)
light.linear = 0.5
light.constant = 0.0

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


