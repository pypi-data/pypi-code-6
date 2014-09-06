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


# mini-shader-per-pixel-lighting-1: Soya's Mini Shaders : per-pixel lighting


import sys, os, os.path, soya3 as soya, soya3.sphere as sphere

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

scene = soya.World()

sphere_model = sphere.Sphere(slices = 10, stacks = 10).to_model()


# A first sphere with normal cellshading (per-vertex)

b1 = soya.Body(scene, sphere_model)
b1.set_xyz(-1.2, -0.5, 0.0)

cellshading_mini_shader = soya.MiniShader.get("cellshading")

b1.add_mini_shader(cellshading_mini_shader())


# A second sphere with per-pixel cellshading (better quality)

b2 = soya.Body(scene, sphere_model)
b2.set_xyz(1.2, -0.5, 0.0)


per_pixel_cellshading_mini_shader = soya.MiniShader.get("per_pixel_cellshading")

b2.add_mini_shader(per_pixel_cellshading_mini_shader())


light = soya.Light(scene)
light.set_xyz(0.0, 1.0, 1.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


