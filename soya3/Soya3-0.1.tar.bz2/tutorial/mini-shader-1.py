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


# mini-shader-1: Soya's Mini Shaders : deforming a character with a "djinn"-like effect


# Shaders are pieces of code that can be used for altering or rewriting the OpenGL rendering pipeline.
# OpenGL proposes the GLSL language for writing shaders, and distinguishes 2 types of shaders:

#  * vertex shaders, in charge of tranforming vertex and performing per-vertex operation
#                    (e.g. lighting computation in the default rendering pipeline)

#  * pixel shaders (also called fragment shader), in charge of performing per-pixel operation
#                    (e.g. determining the color of a pixel using texture and vertex color)

# GLSL is complex to use because it does not allow to modify only a small part of the rendering
# pipeline: either you rewrite everything, or nothing... here come Soya's mini shaders!

# Soya splits vertex and pixel shaders in no less than 20 mini shaders. Each type of mini shader is in
# charge of a specific task in the rendering process, and can be modified independently from the other.
# Additionally, mini shaders can be set at any level in Soya: on a Body, World, Model, Material,...

# Then, Soya automagically assembles those mini shaders to generate the appropriate vertex and pixel
# shaders.


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

# A second, "djinn"-like, Balazar

balazar2 = soya.Body(scene, balazar_model)
balazar2.set_xyz(1.0, -1.5, 0.0)
balazar2.rotate_y(120.0)
balazar2.animate_blend_cycle("attente")


# Here, we define a "body-space deform" mini shader: a mini shader that deforms the model's geometry
# in the body space (= the X direction corresponds to Balazar's right, etc).
# This mini shader will deforms the model by squeezing its lower parts (= Balazar's legs), making
# him leg-less, like a djinn.

# The first argument ("djinn") is an arbitrary name for the mini shader.

# The second argument is the shader's code. Notice that Soya accepts a Python-like syntax for GLSL!

# In this code, gl_Vertex is the original vertex position, and current_vertex is the current vertex
# position in the rendering pipeline.

# This code tests if the Y coord of the vertex is less than 1.0 (=lower part of the model), and, if so,
# the current X and Z coords are squeezed by multiplying them by the Y coord squarred. Else, nothing is
# done (and thus the top of the character if not deformed).

djinn_mini_shader = soya.MiniShader("djinn", """
def void bodyspace_deform_mini_shader():
  if gl_Vertex.y < 1.0:
    current_vertex.x = current_vertex.x * gl_Vertex.y * gl_Vertex.y
    current_vertex.z = current_vertex.z * gl_Vertex.y * gl_Vertex.y
""")

# Soya accept also a "normal" GLSL syntax, like the following:

#djinn_mini_shader = soya.MiniShader("djinn", """
#void bodyspace_deform_mini_shader() {
#  if (gl_Vertex.y < 1.0) {
#    current_vertex.x = current_vertex.x * gl_Vertex.y * gl_Vertex.y;
#    current_vertex.z = current_vertex.z * gl_Vertex.y * gl_Vertex.y;
#    }
#  }""")

# Add the djinn mini shader to the second Balazar. Notice that we must 'instanciate' the mini shader,
# by adding parenthesis after its name.

# Soya will automagically create a complete vertex and pixel shaders that include our djinn mini shader,
# but also the usual vertex transformations, lighting, texturing, etc.

balazar2.add_mini_shader(djinn_mini_shader())


# Prints balazar2's mini shaders

print(balazar_model.mini_shaders)


# Here is the list of the 20 types of mini shaders, in their order in the rendering pipeline:

# Per-vertex mini shaders (will be combined to generate the vertex shader):

#  1) bodyspace_deform_mini_shader         : deforms the model in the body space (= modelview)

#  2) bodyspace_to_cameraspace_mini_shader : transforms vertices coordinates from body space to camera space

#  3) cameraspace_deform_mini_shader       : deforms the model in the camera space (= sceneview)

#  4) vertex_color_deform_mini_shader      : deforms the model's vertex colors

#  5) lighting_mini_shader                 : computes lighting effects

#  6) lighting_deform_mini_shader          : deforms lighting effects and color

#  7) texture_coords_mini_shader           : computes texture coords

#  8) texture_coords_deform_mini_shader    : deforms texture coords

#  9) fog_factor_mini_shader               : computes fog factor

# 10) fog_factor_deform_mini_shader        : deforms fog factor

# 11) cameraspace_to_viewport_mini_shader  : transforms vertices coordinates from camera space to 2D viewport

# 12) viewport_deform_mini_shader          : deforms the model in viewport space (= in the 2D viewport)


# Per-pixel mini shaders (will be combined to generate the pixel shader):

# 13) pixel_color_mini_shader        : deforms the pixel's color (before texturing, fog and anything else)

# 14) pixel_color_deform_mini_shader : deforms the pixel's color (before texturing, fog and anything else)

# 15) texturing_mini_shader          : applies the texture

# 16) texturing_deform_mini_shader   : deforms the pixel's color after texturing

# 17) cellshading_mini_shader        : apply cellshading color to the pixel

# 18) cellshading_deform_mini_shader : apply cellshading color to the pixel

# 19) fog_mini_shader                : apply the fog color to the pixel

# 20) pixel_deform_mini_shader       : deforms the final pixel's color



# Mini shaders without "Deform" in their name define the basic rendering pipeline. Soya provides
# default mini shaders for each task, but you can override Soya's default behavior with the appropriate
# mini shader.

# Mini shaders with "Deform" in their name are the most useful. They can be used as "hooks" for
# modifying the vertex positions, texture coords or colors, or the pixel colors, at various stages
# of the rendering pipeline.
# Default deforming mini shaders do nothing; but you can achieve nice special effects with them!


# Uncomment the following line to have the vertex and pixel shaders' source printed on console.
#soya.DEBUG_SHADER = 1


light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)

camera = soya.Camera(scene)
camera.z = 3.5

soya.set_root_widget(camera)

soya.MainLoop(scene).main_loop()


