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


# mini-shader-remove-at-time-1: Soya's Mini Shaders : temporary mini-shader


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


# Here, we define a PixelDeformMiniShader (see the mini-shader-4 tuto).

magic_mini_shader = soya.MiniShader("magic", """
uniform float self.time
uniform vec4  self.color
uniform float self.period

def void pixel_deform_mini_shader():
  current_color += self.color * (0.5 + 0.5 * sin(0.1 * self.time + self.period * gl_FragCoord.y))
""")


# A second angry Balazar!

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(0.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")

# The special attribute 'remove_at_time' indicate the duration of the mini-shader.
# It will be automatically removed after that duration.

balazar2.add_mini_shader(magic_mini_shader(remove_at_time = 50.0, color = [ 1.0, -1.0, -1.0, 1.0], period = 0.01))


light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


