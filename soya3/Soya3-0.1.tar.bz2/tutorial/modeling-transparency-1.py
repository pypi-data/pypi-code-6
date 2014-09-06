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


# modeling-transparency-1: Transparency : semi-transparent cubes

# In this lesson, we'll build a semi-transparent cube.


# Imports and inits Soya.

import sys, os, os.path, soya3 as soya, soya3.cube

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

# Creates a material, and set its diffuse color to a semi-transparent white (alpha = 0.5).
# See lesson modeling-material-1.py about materials and material colors.
# Similarly, you can use per-vertex semi-transparent colors.

material = soya.Material()
material.diffuse = (1.0, 1.0, 1.0, 0.5)

# Creates a cube using our material.

cube_world = soya.cube.Cube(material = material)

# For optimization pupose, the cube module creates one-sided faces, i.e. only the exterior
# side of the faces are drawn, and not the interior side. Here, as the cube is
# semi-transparent, the interior side becomes visible and so we need to draw both sides.
# This is done by setting the face's double_sided attribute to 1.

for face in cube_world.children:
  face.double_sided = 1

# Compile the cube model.

cube_model = cube_world.to_model()

# Creates several semi-transparent cubes.

cube1 = soya.Body(scene, cube_model)
cube1.set_xyz(-0.3, 0.3, 0.0)
cube1.rotate_y(30.0)

cube2 = soya.Body(scene, cube_model)
cube2.set_xyz(0.0, 0.0, -1.5)
cube2.rotate_y(30.0)

cube3 = soya.Body(scene, cube_model)
cube3.set_xyz(0.6, -0.4, 0.5)
cube3.rotate_y(30.0)

# Creates a light.

light = soya.Light(scene)
light.set_xyz(1.0, 0.7, 1.0)

# Creates a camera.

camera = soya.Camera(scene)
camera.set_xyz(0.0, 0.0, 3.0)
soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()

