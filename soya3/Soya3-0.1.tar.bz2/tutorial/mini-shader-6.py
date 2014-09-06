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


# mini-shader-6: Soya's Mini Shaders : mini shaders everywhere!


import sys, os, os.path, soya3 as soya

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

scene = soya.World()

balazar_model = soya.AnimatedModel.get("balazar")
sword_model   = soya.Model.get("sword")

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


# Apply a "twist" BodySpaceDeformMiniShader to the second Balazar.

twist_mini_shader = soya.MiniShader("twist", """
uniform float self.time

def void bodyspace_deform_mini_shader():
  current_vertex.x = current_vertex.x * 0.5 * (1.0 + sin(5 * gl_Vertex.y + 0.3 * self.time))
  current_vertex.z = current_vertex.z * 0.5 * (1.0 + sin(5 * gl_Vertex.y + 0.3 * self.time))
""")

twist_mini_shader = soya.MiniShader("twist", """
uniform float self.time

def void bodyspace_deform_mini_shader():
  current_vertex.x = current_vertex.x * 0.5 * (1.0 + sin(5 * gl_Vertex.y + 0.3 * self.time))
  current_vertex.z = current_vertex.z * 0.5 * (1.0 + sin(5 * gl_Vertex.y + 0.3 * self.time))
""")

balazar2.add_mini_shader(twist_mini_shader())


# Apply the djinn mini shader to all Balazar.

djinn_mini_shader = soya.MiniShader("djinn", """
def void bodyspace_deform_mini_shader():
  if gl_Vertex.y < 1.0:
    current_vertex.x = current_vertex.x * gl_Vertex.y * gl_Vertex.y
    current_vertex.z = current_vertex.z * gl_Vertex.y * gl_Vertex.y
""")

balazar_model.add_mini_shader(djinn_mini_shader())

# Mini shaders can be added to materials too!
# You can comment the previous line and use the following one instead.

#soya.Material.get("balazar").add_mini_shader(djinn_mini_shader())

# XXX  CURRENT BUG / TODO: mini shaders added to models and materials do not have their time parameter
# updated yet. Moreover, adding / removing mini shaders to them do not recompile shader when performed
# after the first rendering.


# A sword.

sword1 = soya.Body(scene, sword_model)
sword1.set_xyz(1.0, -1.5, 0.0)
sword1.rotate_x(90.0)


# Apply the magic mini shader on the whole scene!

magic2_mini_shader = soya.MiniShader("magic2", """
uniform float self.time;
uniform vec4  self.color;
uniform float self.period;

void pixel_deform_mini_shader() {
  if (textures_enabled > 0) { // Little variant, which only affects textured pixels -- and thus not the outline!
    current_color += self.color * (0.5 + 0.5 * sin(0.1 * self.time + self.period * gl_FragCoord.y));
  }
}
""")

scene.add_mini_shader(magic2_mini_shader(color = [1.0, 1.0, 1.0, 1.0], period = 0.02))


light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


