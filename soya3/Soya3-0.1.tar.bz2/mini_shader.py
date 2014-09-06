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

from __future__ import print_function

import soya3 as soya, os, os.path, weakref, re, cerealizer
from collections import defaultdict


#_MAIN_REGEXP     = re.compile(r"void\s+main\s*\(.*?{")
_COMMENT1_REGEXP  = re.compile("//.*?$", re.MULTILINE)
_COMMENT2_REGEXP  = re.compile("/\\*.*?\\*/", re.MULTILINE | re.DOTALL)
_MAIN_REGEXP      = re.compile("void\\s+(.*?)_mini_shader\\s*\\(\\s*\\)")
_UNIFORM_REGEXP   = re.compile(r"uniform\s+(?:float|int|vec3|vec4|)\s+([a-zA-Z0-9_]+?)\s*(?:=|;)")
_DEF_REGEXP       = re.compile("^def\\s+", re.MULTILINE)
_IF_REGEXP        = re.compile("if\\s(.*?):")
_DEF_MAIN_REGEXP  = re.compile("def\\s+void\\s+(.*?)\\s*\\(\\s*\\)")
_FOR_LIGHT_REGEXP = re.compile("for\\s+(.*?)\\s+in\\s+lights\\s*")

class GLSLShader(soya._soya._GLSLShader):
  def __init__(self, type, code):
    soya._soya._GLSLShader.__init__(self, type, code, frozenset(uniform.encode("ascii") for uniform in _UNIFORM_REGEXP.findall(code)))
  
class GLSLVertexShader(GLSLShader):
  def __init__(self, code): GLSLShader.__init__(self, soya.SHADER_TYPE_VERTEX, code)
    
class GLSLPixelShader(GLSLShader):
  def __init__(self, code): GLSLShader.__init__(self, soya.SHADER_TYPE_PIXEL, code)
    
GLSLProgram = soya._soya._GLSLProgram



def python_2_glsl(s):
  s = s.replace(" elif ", " else if ").replace("else:", "else {").replace("\\\n", " ")
  s = _IF_REGEXP .sub("if (\\1) {", s)
  s = _DEF_REGEXP.sub("", s)

  lines = s.split("\n")
  offsets = { 0 : 0 }
  nb_offset       = 0
  previous_offset = 0
  for i in range(len(lines)):
    if "#" in lines[i]: lines[i] = lines[i][:lines[i].find("#")]
    lines[i] = lines[i].rstrip()
    stripped = lines[i].lstrip()
    if not stripped: continue
    
    current_offset = len(lines[i]) - len(stripped)
    if   current_offset > previous_offset:
      nb_offset += 1
      offsets[current_offset] = nb_offset
    elif current_offset < previous_offset:
      old_nb_offset = nb_offset
      nb_offset = offsets[current_offset]
      for j in range(old_nb_offset - nb_offset):
        lines[i - 1] = "%s }" % lines[i - 1]
        
    if (lines[i][-1] != "{") and ("{" in lines[i]): lines[i] = "%s; }" % lines[i]
    if (lines[i][-1] != "{") and (lines[i][-1] != "}") and (lines[i][-1] != ";"): lines[i] = "%s;" % lines[i]
    previous_offset = current_offset
    
  s = "\n".join(lines) + " }" * nb_offset
  s = s.replace(":;", " {").replace(" pass;", " ;")
  return s

def _loop_for(loop, j):
  loop = loop.replace("current_light", str(j))
  loop = """    if (soya_light_id >= %s) {
    soya_light_id -= %s;
%s
}""" % (1 << j, 1 << j, loop)
  return loop
  
def _apply_light_loop(s):
  lines = s.split("\n")
  for_start  = 0
  nb_bracket = 0
  i = -1
  while i < len(lines) - 1:
    i += 1
    if   for_start:
      if   "{" in lines[i]: nb_bracket += 1
      elif "}" in lines[i]:
        nb_bracket -= 1
        if nb_bracket == 0:
          lines[i]  = lines[i].replace("}", "", 1)
          loop = lines[for_start + 1 : i]
          loop = "\n".join(loop)
          lines[for_start + 1 : i] = [_loop_for(loop, j) for j in reversed(range(_MAX_LIGHT))]
          for_start = 0
    elif _FOR_LIGHT_REGEXP.search(lines[i]):
      lines[i]   = "    soya_light_id = lights_enabled;"
      for_start  = i
      nb_bracket = 1
      
  s = "\n".join(lines)
  return s




def split_code(s):
  s = _COMMENT1_REGEXP.sub("", s)
  s = _COMMENT2_REGEXP.sub("", s)
  s = s.replace("{", "{\n")
  s = s.replace("}", "}\n")

  s = _apply_light_loop(s)

  mains = defaultdict(list)
  lines = s.split("\n")
  cur   = "decl"
  nb_bracket = 0
  for i in range(len(lines)):
    main_match = _MAIN_REGEXP.search(lines[i])
    if main_match:
      cur = main_match.group(1)
      nb_bracket = 1
      continue
    elif "{" in lines[i]: nb_bracket += 1
      
    if   "}" in lines[i]:
      nb_bracket -= 1
      if (cur != "decl") and (nb_bracket == 0):
        cur        = "decl"
        main_match = None
        lines[i]   = lines[i].replace("}", "", 1)
    mains[cur].append(lines[i])
    
  return {func : "\n".join(lines) for (func, lines) in mains.items() }
 

class MiniShader(soya.SavedInAPath):
  DIRNAME = "mini_shaders"
  _alls   = weakref.WeakValueDictionary()
  default = None
  params  = {}
  
  def __init__(self, filename, code):
    if _DEF_MAIN_REGEXP.search(code): code = python_2_glsl(code)
    self._filename   = u""
    self.filename    = filename
    self.funcs       = split_code(code.replace("self.", "%s_p_" % self._filename))
    self.has_time    = "_p_time" in self.funcs["decl"]
    
  #def copy(self): return self
  
  def __call__(self, **params):
    # time parameter need to be present, in order to be updated
    if self.has_time and (not "time" in params): params["time"] = 0.0
    if not params: return self
    return MiniShaderWithParams(self, params)

  def added_into  (self, coord_syst): pass
  def removed_from(self, coord_syst): pass
  
  def parameters(self, **params):
    return ParamSetterMiniShader(self, params)
  
  def __repr__(self): return """%s.get("%s")""" % (self.__class__.__name__, self._filename)
  
  def get_class     (self): return self.__class__
  def get_funcs     (self): return self.funcs
  def advance_time  (self, proportion): pass # XXX optimize this in Cython
  
  def load(klass, filename):
    if isinstance(filename, bytes): filename = filename.decode("utf8")
    dirname  = klass._get_directory_for_loading_and_check_export(filename)
    filename = filename.replace("/", os.sep)

    code = open(os.path.join(dirname, klass.DIRNAME, filename + ".data"), "r").read()
    return klass(filename, code)
  load = classmethod(load)
  

class ParamSetterMiniShader(object):
  def __init__(self, mini_shader, params):
    self.__dict__["mini_shader"] = mini_shader
    self.__dict__["filename"]    = mini_shader._filename
    self.__dict__["params"]      = { ("%s_p_%s" % (self.filename, attr)).encode("ascii") : val for (attr, val) in params.items() }
    
  def added_into  (self, coord_syst): pass
  def removed_from(self, coord_syst): pass
  
  #def copy(self): return ParamSetterMiniShader(self.mini_shader, )
  def __getattr__(self, attr       ): return self.params["%s_p_%s" % (self.filename, attr)]
  def __setattr__(self, attr, value):
    if attr == "__dict__": object.__setattr__(self, attr, value)
    else:                  self.params["%s_p_%s" % (self.filename, attr)] = value
  def __repr__(self): return """%s.parameters(%s)""" % (repr(self.mini_shader), ", ".join("%s = %s" % (attr.decode("ascii").replace("%s_p_" % self.filename, ""), value) for attr, value in self.params.items()))
  
  def get_class     (self): return ParametersSetterMiniShader
  def get_funcs     (self): return {}
  def advance_time  (self, proportion): pass # XXX optimize this in Cython

class MiniShaderWithParams(object):
  def __init__(self, mini_shader, params):
    if "remove_at_time" in params: self._remove_at_time = params.pop("remove_at_time")
    else:                          self._remove_at_time = 0
    self.__dict__["mini_shader"] = mini_shader
    self.__dict__["filename"]    = mini_shader._filename
    self.__dict__["params"]      = { ("%s_p_%s" % (self.filename, attr)).encode("ascii") : val for (attr, val) in params.items() }
    
  def __getattr__(self, attr       ): return self.params["%s_p_%s" % (self.filename, attr)]
  def __setattr__(self, attr, value):
    if attr.startswith("_"): object.__setattr__(self, attr, value)
    else:                    self.params[("%s_p_%s" % (self.filename, attr)).encode("ascii")] = value
  def __repr__(self): return """%s(%s)""" % (repr(self.mini_shader), ", ".join("%s = %s" % (attr.decode("ascii").replace("%s_p_" % self.filename, ""), value) for attr, value in self.params.items()))
  
  def get_class     (self): return self.mini_shader.__class__
  def get_funcs     (self): return self.mini_shader.funcs
  
  def advance_time  (self, proportion): # XXX optimize this in Cython
    time = ("%s_p_time" % self.filename).encode("ascii")
    if time in self.params:
      self.params[time] += proportion
      if self._remove_at_time and (self.params[time] >= self._remove_at_time):
        if self._coord_syst:
          self._coord_syst.remove_mini_shader(self)
        
  def added_into  (self, coord_syst):
    if self._remove_at_time: self._coord_syst = coord_syst
    
  def removed_from(self, coord_syst):
    if self._remove_at_time: self._coord_syst = None



cerealizer.register(MiniShader, soya.SavedInAPathHandler(MiniShader))
cerealizer.register(MiniShaderWithParams)
cerealizer.register(ParamSetterMiniShader)

_VERTEX_MINI_SHADERS = [
  "bodyspace_deform",
  "bodyspace_to_cameraspace",
  "cameraspace_deform",
  "vertex_color_deform",
  "lighting",
  "lighting_deform",
  "texture_coords",
  "texture_coords_deform",
  "fog_factor",
  "fog_factor_deform",
  "cameraspace_to_viewport",
  "viewport_deform",
  ]
_PIXEL_MINI_SHADERS = [
  "pixel_color",
  "pixel_color_deform",
  "texturing",
  "texturing_deform",
  "specular",
  "specular_deform",
  "fog",
  "pixel_deform",
  ]


_MAX_LIGHT = 4
def set_max_light(max_light = 4):
  global _MAX_LIGHT
  _MAX_LIGHT = max_light
  
_DEFAULT_MINI_SHADER          = MiniShader.get("default")
_DEFAULT_LIGHTING_MINI_SHADER = MiniShader.get("per_vertex_lighting")





class OrderedMiniShaders(defaultdict):
  def __init__(self, mini_shaders):
    defaultdict.__init__(self, list)
    for mini_shader in [_DEFAULT_MINI_SHADER, _DEFAULT_LIGHTING_MINI_SHADER] + mini_shaders:
      for func in mini_shader.get_funcs():
        if func == "decl": continue
        self[func].append(mini_shader)
        
  def mini_shader_for_func(self, func):
    if func in self:
      if func.endswith("deform"): return  self[func]
      else:                       return [self[func][-1]]
    return []
    

def _add_default_vars(s):
  if "lights_enabled"   in s: s = "uniform int lights_enabled;\n%s" % s
  if "textures_enabled" in s: s = "uniform int textures_enabled;\n%s" % s
  if "lighting_mode"    in s: s = "uniform int lighting_mode;\n%s" % s
  if "fog_type"         in s: s = "uniform int fog_type;\n%s" % s
  return s

_SHADERS_CACHE = {}
def _mini_shaders_2_vertex_shader(mini_shaders):
  func_mini_shaders = [(func, mini_shaders.mini_shader_for_func(func)) for func in _VERTEX_MINI_SHADERS]
  mini_shaders = tuple(sum((mini_shaders for (func, mini_shaders) in func_mini_shaders), []))
  shader_name = ">".join("%s:%s" % (func, mini_shader.filename) for (func, mini_shaders) in func_mini_shaders for mini_shader in mini_shaders)
  shader      = _SHADERS_CACHE.get(shader_name)
  if shader is None:
    code = """#version 130
uniform int lights_enabled;
uniform int lighting_mode;
uniform int fog_type;
uniform int textures_enabled;

int  soya_light_id;

varying float current_fog_factor;
%s
void main() {
  vec4 current_vertex       = gl_Vertex;
  vec3 current_normal       = gl_Normal;
  vec4 current_front_color  = gl_Color;
  vec4 current_back_color   = gl_Color;
  current_fog_factor  = 1.0;
  %s
  gl_Position   = current_vertex;
  gl_FrontColor = current_front_color;
  gl_BackColor  = current_back_color;
}
""" % (
  "".join(mini_shader.get_funcs()["decl"] for mini_shader          in set(mini_shaders)),
  "".join(mini_shader.get_funcs()[func]   for (func, mini_shaders) in func_mini_shaders for mini_shader in mini_shaders),)
    
    #print(code)
    print("* Soya * Generating VERTEX SHADER: %s" % shader_name)
    if soya.DEBUG_SHADER:
      print(code)
      print()
    shader = _SHADERS_CACHE[shader_name] = GLSLVertexShader(code)
  return shader


# Loop version... a little slower ???
#def _apply_light_loop(s):
#  lines = s.split("\n")
#  i = -1
#  while i < len(lines) - 1:
#    i += 1
#    if _FOR_LIGHT_REGEXP.search(lines[i]):
#      varname    = _FOR_LIGHT_REGEXP.findall(lines[i])[0]
#      lines[i]   = "    for(int %s = 0; %s < %s; %s++) {\n" % (varname, varname, _MAX_LIGHT, varname)
#      lines[i]  += "      if((lights_enabled & (1 << %s)) == 0) continue;" % varname
#  s = "\n".join(lines)
#  return s


_SHADERS_CACHE = {}
def _mini_shaders_2_pixel_shader(mini_shaders):
  func_mini_shaders = [(func, mini_shaders.mini_shader_for_func(func)) for func in _PIXEL_MINI_SHADERS]
  mini_shaders = tuple(sum((mini_shaders for (func, mini_shaders) in func_mini_shaders), []))
  shader_name = ">".join("%s:%s" % (func, mini_shader.filename) for (func, mini_shaders) in func_mini_shaders for mini_shader in mini_shaders)
  shader      = _SHADERS_CACHE.get(shader_name)
  if shader is None:
    code = """#version 130
uniform int lights_enabled;
uniform int lighting_mode;
uniform int fog_type;
uniform int textures_enabled;
uniform sampler2D texture0;

int  soya_light_id;

varying float current_fog_factor;
%s
void main() {
  vec4 current_color = gl_Color;
  %s
  gl_FragColor = current_color;
}
""" % (
  "".join(mini_shader.get_funcs()["decl"] for mini_shader          in set(mini_shaders)),
  "".join(mini_shader.get_funcs()[func]   for (func, mini_shaders) in func_mini_shaders for mini_shader in mini_shaders),)
    
    print("* Soya * Generating PIXEL  SHADER: %s" % shader_name)
    if soya.DEBUG_SHADER:
      print(code)
      print()
    shader = _SHADERS_CACHE[shader_name] = GLSLPixelShader(code)
  return shader


_PROGRAMS_CACHE = {}
def _mini_shaders_2_program(mini_shaders):
  for mini_shader in mini_shaders:
    if mini_shader and not isinstance(mini_shader, ParamSetterMiniShader): break
  else: # No real mini shaders => render without shader
    return soya.get_default_program()
    
  mini_shaders = OrderedMiniShaders(mini_shaders)
  
  vertex_shader = _mini_shaders_2_vertex_shader(mini_shaders)
  pixel_shader  = _mini_shaders_2_pixel_shader (mini_shaders)
  program = _PROGRAMS_CACHE.get((vertex_shader, pixel_shader))
  if program is None:
    program = _PROGRAMS_CACHE[(vertex_shader, pixel_shader)] = GLSLProgram(vertex_shader, pixel_shader)
  return program

soya._soya._set_mini_shaders_2_program(_mini_shaders_2_program)


def short_name_2_mini_shader(val):
  if not "(" in val: return MiniShader.get(val)
  else:
    mini_shader, mini_shader_args = val.split("(", 1)
    mini_shader_args = mini_shader_args.split(")")[0]
    mini_shader_args_dict = {}
    for mini_shader_arg in mini_shader_args.split(","):
      if mini_shader_arg.strip():
        mini_shader_attr, mini_shader_val = mini_shader_arg.split("=")
        try: mini_shader_val = int(mini_shader_val)
        except:
          try: mini_shader_val = float(mini_shader_val)
          except: pass
        mini_shader_args_dict[mini_shader_attr] = mini_shader_val
    return MiniShader.get(mini_shader)(**mini_shader_args_dict)
