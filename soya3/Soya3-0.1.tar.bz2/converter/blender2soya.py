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


# export blender model to soya
# this file is understood to be executed automagically by Soya,
# NOT manually !

import sys, os, os.path, string, math
import bpy

# Default values :
PATH                  = os.path.join(os.path.dirname(bpy.data.filepath), "..")
FILENAME              = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
KEEP_POINTS_AND_LINES = 0

# Make current the animation of the given name, at the given time / key.
# Usefull for batch mode.
ANIMATION         = ""
ANIMATION_TIME    = 0.0

# Use this dictionary if you want to change some materials
MATERIALS_MAP = {
#  "old_material_name" : "new_material_name",
  }

MINI_SHADERS = []

CELLSHADING                     = 0
CELLSHADING_OUTLINE_COLOR       = (0.0, 0.0, 0.0, 1.0)
CELLSHADING_OUTLINE_WIDTH       = 0.0
CELLSHADING_OUTLINE_ATTENUATION = 0.3

# Scale the whole model
SCALE = 1.0

# The maximum angle between two smooth-lit faces.
MAX_FACE_ANGLE = 80.0


TMP_FILE = ""

PARAMS_NAMES = [attr for attr in globals().keys() if (attr[0] in string.ascii_uppercase) and (attr[1] in string.ascii_uppercase)]

class Blender2Soya:
  def __init__(self, args):
    self.parse_global_args()
    
    if "soya_params" in bpy.data.texts:
      self.parse_args(bpy.data.texts["soya_params"].as_string().split("\n"))
    self.parse_args(args)
    
  def parse_global_args(self):
    for param in PARAMS_NAMES:
      setattr(self, param.lower(), globals()[param])
      
  def parse_args(self, args):
    for arg in args:
      if "=" in arg:
        attr, val = arg.split("=", 1)
        attr = attr.lower()
        try: val = int(val)
        except:
          try: val = float(val)
          except: pass
        if   attr.startswith("material_"): # A material map
          self.materials_map[attr[9:]] = val
          
        elif attr == "mini_shader": # A mini shader
          #if not "(" in val: self.mini_shader.append((val, {}))
          #else:
          #  mini_shader, mini_shader_args = val.split("(", 1)
          #  mini_shader_args = mini_shader_args.split(")")[0]
          #  mini_shader_args_dict = {}
          #  for mini_shader_arg in mini_shader_args.split(","):
          #    if mini_shader_arg.strip():
          #      mini_shader_attr, mini_shader_val = mini_shader_arg.split("=")
          #      try: mini_shader_val = int(mini_shader_val)
          #      except:
          #        try: mini_shader_val = float(mini_shader_val)
          #        except: pass
          #      mini_shader_args_dict[mini_shader_attr] = mini_shader_val
          #  self.mini_shader.append((mini_shader, mini_shader_args_dict))
          self.mini_shaders.append("soya.mini_shader.short_name_2_mini_shader('''%s''')" % val)
          
        elif attr == "config_text": # Config text
          sys.stderr.write("(reading config text %s)\n" % val)
          self.parse_args(bpy.data.texts[val].as_string().split("\n"))
          
        elif attr == "config_file": # Config file
          sys.stderr.write("(reading config file %s)\n" % val)
          self.parse_args(open(val).read().split("\n"))
          
        else: setattr(self, attr, val)

    self.has_lod = hasattr(self, "lod_low") or hasattr(self, "lod_medium") or hasattr(self, "lod_high")
    
  def export(self):
    self.f = open(self.tmp_file, "w")
    self.f.write("""import soya3 as soya\n""")
    self.f.write("""import soya3.facecutter as facecutter\n""")
    self.f.write("\n")
    self.f.write("materials = set()\n")
    self.f.write("\n")

    if bpy.ops.object.mode_set.poll():
      bpy.ops.object.mode_set() # Close edit mode (required, else some Blender data are not available).
    
    if self.has_lod:
      if hasattr(self, "lod_medium"):
        self.medium_filename = self.filename + "_medium"
        self.set_lod(self.lod_medium)
        self.export_once(self.medium_filename)
        if self.lod_collision == self.lod_medium: self.collision_filename = self.medium_filename
      if hasattr(self, "lod_high"):
        self.high_filename = self.filename + "_high"
        self.set_lod(self.lod_high)
        self.export_once(self.high_filename)
        if self.lod_collision == self.lod_high: self.collision_filename = self.high_filename
      else:
        self.high_filename = self.medium_filename
      if hasattr(self, "lod_low"):
        self.low_filename = self.filename + "_low"
        self.set_lod(self.lod_low)
        self.export_once(self.low_filename)
        if self.lod_collision == self.lod_low: self.collision_filename = self.low_filename
      else:
        self.low_filename = self.medium_filename
        
      self.f.write("""model = soya.LODModel("%s", "%s", "%s", "%s")\n""" % (self.low_filename, self.medium_filename, self.high_filename, self.collision_filename))
      self.f.write("""model.filename = '%s'\n""" % self.filename)
      self.f.write("""model.save()\n""")

    else:
      self.export_once(self.filename)
      
    self.f.flush()
    self.f.close()
    
  def set_lod(self, level):
    for obj in bpy.data.objects:
      for mod in obj.modifiers:
        if mod.type == "SUBSURF": mod.levels = level
        
  def export_once(self, filename):
    if self.animation:
      for armature in bpy.data.objects:
        if armature.type == "ARMATURE":
          armature.animation_data.action = bpy.data.actions[self.animation]
      bpy.context.scene.frame_set(int(self.animation_time))
      
    nb_points_and_lines = 0
    
    self.f.write("""root_world = soya.World()\n""")
    self.f.write("""root_world.filename = '%s'\n""" % filename)
    self.f.write("\n")
    
    for obj in bpy.data.objects:
      if (obj.type == "MESH") and (len(obj.data.polygons) > 0):
        
        #mesh = obj.to_mesh(obj.users_scene[0], True, "PREVIEW")
        mesh = obj.to_mesh(bpy.context.scene, True, "PREVIEW")
        mesh.transform(obj.matrix_world)
        #mesh.update(True, True)
        
        # We use loop colors and not tessface vertex colors for determining if the mesh has vertex colors,
        # because tessface vertex colors seems bugged (additional blanck color at the end ???).
        mesh_has_vertex_color = (len(mesh.tessface_vertex_colors) > 0) and (len(mesh.vertex_colors) > 0) and (set(tuple(loop_color.color) for loop_color in mesh.vertex_colors[0].data) != { (1.0, 1.0, 1.0) })
        self.max_face_angle = mesh.auto_smooth_angle * 180.0 / math.pi
        
        for face in mesh.tessfaces:
          if (not self.keep_points_and_lines) and (len(face.vertices) <= 2):
            nb_points_and_lines += 1
            continue
          
          self.f.write("""f = soya.Face(root_world)\n""")
          
          if mesh.use_auto_smooth or face.use_smooth: self.f.write("""f.smooth_lit = 1\n""")
          if mesh.show_double_sided: self.f.write("""f.double_sided = 1\n""")
          
          if len(mesh.tessface_uv_textures) > 0: tessface_uv_texture = mesh.tessface_uv_textures[0].data[face.index]
          else:                                  tessface_uv_texture = None
          
          # vertices
          index = 1
          for vertex_id in face.vertices:
            # vertex coordinates
            vertex = mesh.vertices[vertex_id]
            co     = vertex.co
            self.f.write("""v = soya.Vertex(root_world, %s, %s, %s)\n""" % (co[0], co[1], co[2]))
            
            # vertex color
            if mesh_has_vertex_color:
              color = getattr(mesh.tessface_vertex_colors[0].data[face.index], "color%s" % index)
              self.f.write("""v.color = (%s, %s, %s, 1.0)\n""" % (color.r / 255.0, color.g / 255.0, color.b / 255.0))
              
            # vertex texture coordinates
            if tessface_uv_texture:
              uv = getattr(tessface_uv_texture, "uv%s" % index)
              self.f.write("""v.tex_x, v.tex_y = %s, %s\n""" % (uv[0], 1.0 - uv[1]))
              
            self.f.write("""f.append(v)\n""")
            index += 1
            
          # material
          if tessface_uv_texture.image:
            material_filename = tessface_uv_texture.image.name
            if "." in material_filename: material_filename = material_filename[:material_filename.rfind(".")]
            material_filename = self.materials_map.get(material_filename) or material_filename
            self.f.write("""f.material = soya.Material.get("%s")\n""" % material_filename)
            self.f.write("""materials.add(f.material)\n""")
            self.f.write("\n")
            
        bpy.data.meshes.remove(mesh)
        
    if nb_points_and_lines:
      self.f.write("blender2soya_batch.py: removing %s points and lines...\n" % nb_points_and_lines)
      
    # Soya has different axis conventions  
    self.f.write("""root_world.rotate_x(-90.0)\n""")
    
    # Ensure quad's vertices are coplanar, and split any bugous quads
    self.f.write("""facecutter.check_quads(root_world)\n""")
    
    if self.scale != 1.0:
      self.f.write("""root_world.scale(%s, %s, %s)\n""" % (self.scale, self.scale, self.scale))
      
    self.f.write("""root_world.model_builder = soya.VertexBufferModelBuilder(
        max_face_angle      = %s,
        outline_color       = %s,
        outline_width       = %s,
        outline_attenuation = %s,
)\n""" % (self.max_face_angle, self.cellshading_outline_color, self.cellshading_outline_width, self.cellshading_outline_attenuation))
   
    self.f.write("")
    for mini_shader in self.mini_shaders:
      self.f.write("""root_world.add_mini_shader(%s)\n""" % (mini_shader))
      
    self.f.write("\n")
    self.f.write("""root_world.save()\n""")
    self.f.write("""root_world.filename = ""\n""") # Invalidate the world -- needed to avoid weird bug
    self.f.write("\n")

args = sys.argv[sys.argv.index("-P") + 2:]
exporter = Blender2Soya(args)
exporter.export()

bpy.ops.wm.quit_blender()
