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


# mini-shader-cellshading-1: Soya's Mini Shaders : cellshading

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


# A second Balazar with cellshading

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(1.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")

# Soya has a pre-defined mini shader for cellshading, so we don't have to write them manually
# (you can find it in the soya3/data/mini_shaders directory if you want to hack!).

cellshading_mini_shader = soya.MiniShader.get("cellshading")

# Add the two mini shaders to the second Balazar.

# The cellshading mini shader has the following parameters:

#  * bright_color_cut_at : size of the bright region (use lower values for bigger bright regions)
#  * bright_color        : the color added to the bright regions (the alpha color component
#                          indicates how much of this color is added)

#  * dark_color_cut_at   : size of the bright region (use higher values for bigger bright regions)
#  * dark_color          : the color added to the dark regions (the alpha color component
#                          indicates how much of this color is added)

#  * anti_alias          : antialias (=make smoother) the limit between regions (set to 0.0 to disable)

balazar2.add_mini_shader(cellshading_mini_shader(
  bright_color_cut_at = 0.9,
  bright_color        = [1.0, 1.0, 1.0, 0.3],
  dark_color_cut_at   = 0.2,
  dark_color          = [0.0, 0.0, 0.0, 0.7],
  anti_alias          = 0.1,
))


light = soya.Light(scene)
light.set_xyz(-1.5, 0.0, 0.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


