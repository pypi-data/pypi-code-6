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
import sys, os, os.path, weakref, cerealizer

if os.path.exists(os.path.join(__path__[0], "build")):
  # We are using a source directory.
  # We need to get the binary library in "./build/lib.xxx-yyy"
  import distutils.util
  __path__.append(os.path.join(__path__[0], "build", "lib.%s-%s" % (distutils.util.get_platform(), sys.version[0:3]), "soya3"))
  
from soya3._soya import *
from soya3._soya import _CObj

_soya = sys.modules["soya3._soya"]


class SavedInAPathHandler(cerealizer.ObjHandler):
  def collect(self, obj, dumper):
    global _SAVING
    if (not _SAVING is obj) and obj._filename: # self is saved in another file, save filename only
      return cerealizer.Handler.collect(self, obj, dumper)
    else: return cerealizer.ObjHandler.collect(self, obj, dumper)
    
  def dump_obj(self, obj, dumper, s):
    global _SAVING
    cerealizer.ObjHandler.dump_obj(self, obj, dumper, s)
    if (not _SAVING is obj) and obj._filename: # self is saved in another file, save filename only
      dumper.dump_ref(obj._filename, s)
    else: dumper.dump_ref("", s)
    
  def dump_data(self, obj, dumper, s):
    global _SAVING
    if (not _SAVING is obj) and obj._filename: # self is saved in another file, save filename only
      return cerealizer.Handler.dump_data(self, obj, dumper, s)
    else: cerealizer.ObjHandler.dump_data(self, obj, dumper, s)
    
  def undump_obj(self, dumper, s):
    filename = dumper.undump_ref(s)
    if filename: return self.Class._reffed(filename)
    return cerealizer.ObjHandler.undump_obj(self, dumper, s)
  
  def undump_data(self, obj, dumper, s):
    if not getattr(obj, "_filename", 0): # else, has been get'ed
      cerealizer.ObjHandler.undump_data(self, obj, dumper, s)


AUTO_EXPORTERS_ENABLED = 1

def set_root_widget(widget):
  """set_root_widget(WIDGET)

Sets the root widget to WIDGET. The root widget is the widget that is rendered first.
It defaults to the first Camera you create."""
  global root_widget
  root_widget = widget
  _soya.set_root_widget(widget)
  



DATADIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATADIR):
  DATADIR = "/usr/share/soya3"
  if not os.path.exists(DATADIR):
    DATADIR = "/usr/local/share/soya3"
    if not os.path.exists(DATADIR):
      DATADIR = "/usr/share/python-soya3"
      if not os.path.exists(DATADIR):
        DATADIR = os.path.join(os.getcwd(), "data")
        if not os.path.exists(DATADIR):
          import warnings
          warnings.warn("Soya3's data directory cannot be found !")
  
  
path = [DATADIR]

_SAVING = None # The object currently being saved. XXX not thread-safe, hackish

def _getter(klass, filename): return klass._reffed(filename)
_loader = _getter

class SavedInAPath(object):
  """SavedInAPath

Base class for all objects that can be saved in a path, such as Material,
World,..."""
  DIRNAME = ""
  SRC_DIRNAMES_EXTS = []
  
  def _get_directory_for_loading(klass, filename, ext = ".data"):
    if os.pardir in filename: raise ValueError("Cannot have .. in filename (security reason)!", filename)
    
    if klass.DIRNAME in ("models", "animated_models"):
      for p in path:
        if os.path.exists(os.path.join(p, klass.DIRNAME)): break
        
    src_filename = filename.split("@")[0]
    for p in path:
      d = os.path.join(p, klass.DIRNAME, filename + ext)
      if os.path.exists(d): return p
      for src_dirname, src_ext in klass.SRC_DIRNAMES_EXTS:
        d = os.path.join(p, src_dirname, src_filename + src_ext)
        if os.path.exists(d): return p
        
    raise ValueError("Cannot find a %s named %s!" % (klass, filename))
      
  _get_directory_for_loading = classmethod(_get_directory_for_loading)
  
  def _get_directory_for_saving(klass, filename, ext = ".data"):
    if os.pardir in filename: raise ValueError("Cannot have .. in filename (security reason)!", filename)
    
    if klass.DIRNAME in ("models", "animated_models"):
      for p in path:
        if p is DATADIR: continue
        if os.path.exists(os.path.join(p, klass.DIRNAME)): break
        
    src_filename = filename.split("@")[0]
    for p in path:
      if p is DATADIR: continue
      d = os.path.join(p, klass.DIRNAME)
      if os.path.exists(d): return p
    raise RuntimeError("Unable to find a %s directory to save %s"%(klass.DIRNAME,filename))
      
  _get_directory_for_saving = classmethod(_get_directory_for_saving)
  
  def _get_directory_for_loading_and_check_export(klass, filename, ext = ".data"):
    dirname = klass._get_directory_for_loading(filename, ext)
    if AUTO_EXPORTERS_ENABLED:
      src_filename  = filename.split("@")[0]
      full_filename = os.path.join(dirname, klass.DIRNAME, filename + ext)
      if os.path.exists(full_filename): exported_date = os.path.getmtime(full_filename)
      else:                             exported_date = 0
      for src_dirname, src_ext in klass.SRC_DIRNAMES_EXTS:
        d = os.path.join(dirname, src_dirname, src_filename + src_ext)
        if os.path.exists(d) and exported_date < os.path.getmtime(d):
          print("* Soya * Converting %s to %s..." % (d, klass.__name__))
          klass._export(d, filename)
          break
    return dirname
  
  _get_directory_for_loading_and_check_export = classmethod(_get_directory_for_loading_and_check_export)
  
  def _export(klass, src, filename): raise NotImplementedError
  _export = classmethod(_export)
  
  def get(klass, filename):
    """SavedInAPath.get(filename)

Gets the object of this class with the given FILENAME attribute.
The object is loaded from the path if it is not already loaded.
If it is already loaded, the SAME object is returned.
Raise ValueError if the file is not found in soya.path."""
    if isinstance(filename, bytes): filename = filename.decode("utf8")
    return klass._alls.get(filename) or klass._alls.setdefault(filename, klass.load(filename))
  get = classmethod(get)
  
  def load(klass, filename):
    """SavedInAPath.load(filename)

Loads the object of this class with the given FILENAME attribute.
Contrary to get, load ALWAYS returns a new object.
Raise ValueError if the file is not found in soya.path."""
    if isinstance(filename, bytes): filename = filename.decode("utf8")
    dirname  = klass._get_directory_for_loading_and_check_export(filename)
    filename = filename.replace("/", os.sep)
    
    obj = cerealizer.loads(open(os.path.join(dirname, klass.DIRNAME, filename + ".data"), "rb").read())
    obj.loaded()
    return obj
  load = classmethod(load)
  _reffed = get
  
  def loaded(self):
    if self.filename: self._alls[self.filename] = self
    
  def save(self, filename = None):
    """SavedInAPath.save(filename = None)

Saves this object. If no FILENAME is given, the object is saved in the path,
using its filename attribute. If FILENAME is given, it is saved at this
location."""
    if os.pardir in self.filename: raise ValueError("Cannot have .. in filename (security reason)!", filename)
    if not filename: filename = os.path.join(self._get_directory_for_saving(self.filename, ".data"), self.DIRNAME, self.filename + ".data")
    
    global _SAVING
    try:
      _SAVING = self # Hack !!
      data = cerealizer.dumps(self, 1) # Avoid destroying the file if the serialization causes an error.
      open(filename or os.path.join(p, self.filename.replace("/", os.sep)) + ".data", "wb").write(data)
    finally:
      _SAVING = None
      
  def __reduce_ex__(self, arg):
    if (not _SAVING is self) and self._filename: # self is saved in another file, save filename only
      return (_getter, (self.__class__, self.filename)) # can be shared
    return _CObj.__reduce_ex__(self, arg)
  
  def __reduce__(self):
    if (not _SAVING is self) and self._filename: # self is saved in another file, save filename only
      return (_getter, (self.__class__, self.filename)) # can be shared
    return _CObj.__reduce__(self)
  
  def get_filename(self): return self._filename
  def set_filename(self, filename):
    if isinstance(filename, bytes): filename = filename.decode("utf8")
    if self._filename:
      try: del self._alls[self.filename]
      except KeyError: pass
    if filename: self._alls[filename] = self
    self._filename = filename
  filename = property(get_filename, set_filename)
  
  def availables(klass):
    """SavedInAPath.availables() -> list

Returns the list of the filename all the objects available in the current path."""
    filenames = dict(klass._alls)
    for p in path:
      p = os.path.join(p, klass.DIRNAME)
      if os.path.exists(p):
        for filename in os.listdir(p):
          if filename.endswith(".data"): filenames[filename[:-5]] = 1
    filenames = list(filenames.keys())
    filenames.sort()
    return filenames
  availables = classmethod(availables)
  
  def __setstate__(self, state):
    super(SavedInAPath, self).__setstate__(state)

# We MUST extends all Pyrex classes in Python,
# at least for weakref-ing their instance.

class Image(SavedInAPath, _soya._Image):
  """A Soya image, suitable for e.g. texturing.

Attributes are:

 - pixels : the raw image data (e.g. in a form suitable for PIL).

 - width.

 - height.

 - nb_color: the number of color channels (1 => monochrome, 3 => RGB, 4 => RGBA).
"""
  DIRNAME = "images"
  _alls   = weakref.WeakValueDictionary()
  palette = None
  
  def load(klass, filename):
    if filename[0] == "/": # Old-style, non-relative filename
      filename = filename.split(os.sep)[-1]
    if ".." in filename: raise ValueError("Cannot have .. in filename (security reason)!", filename)
    filename = filename.replace("/", os.sep)
    for p in path:
      file = os.path.join(p, klass.DIRNAME, filename)
      if os.path.exists(file):
        image = open_image(file)
        image._filename = filename
        return image
    raise ValueError("No %s named %s" % (klass.__name__, filename))
  load = classmethod(load)
  
  def save(klass, filename = None): raise NotImplementedError("Soya cannot save image.")
  
  def availables(klass):
    """SavedInAPath.availables() -> list

Returns the list of the filename all the objects available in the current path."""
    filenames = dict(klass._alls)
    for p in path:
      for filename in os.listdir(os.path.join(p, klass.DIRNAME)):
        filenames[filename] = 1
    filenames = list(filenames.keys())
    filenames.sort()
    return filenames
  availables = classmethod(availables)

  
class Material(_soya._Material, SavedInAPath):
  """Material

A material regroups all the surface attributes, like colors, shininess and
texture. You should NEVER use None as a material, use soya._DEFAULT_MATERIAL instead.

Attributes are:

- diffuse: the diffuse color.

- specular: the specular color; used for shiny part of the surface.

- emissive: the emissive color; this color is applied even in the dark.

- separate_specular: set it to true to enable separate specular; this usually
  results in a more shiny specular effect.

- shininess: the shininess ranges from 0.0 to 128.0; 0.0 is the most metallic / shiny
  and 128.0 is the most plastic.

- texture: the texture (a soya.Image object, or None if no texture).

- clamp: set it to true if you don't want to repeat the texture when the texture
  coordinates are out of the range 0 - 1.0.

- additive_blending: set it to true for additive blending. For semi-transparent surfaces
  (=alpha blended) only. Usefull for special effect (Ray, Sprite,...).

- mip_map: set it to true to enable mipmaps for this materials texture. (default: True)
"""

  DIRNAME = "materials"
  SRC_DIRNAMES_EXTS = [("images", ".png"), ("images", ".jpeg")]
  _alls = weakref.WeakValueDictionary()
  
  def __deepcopy__(self, memo): # For facecutter
    return self
    
  def _export(klass, src, filename):
    image = Image.get(os.path.basename(src))
    p = os.path.join(os.path.dirname(src), os.pardir, klass.DIRNAME, filename + ".data")
    if os.path.exists(p): material = cerealizer.loads(open(p, "rb").read())
    else:
      material = Material()
      material.filename = filename
    material.texture = image
    material.save()
  _export = classmethod(_export)

class PythonMaterial(_soya._PythonMaterial, Material):
  pass

class PythonMainLoopingMaterial(_soya._PythonMainLoopingMaterial, Material):
  pass

class Model(SavedInAPath, _soya._Model):
  """Model

A Model is an optimized model. Models cannot be modified, but they are rendered very
quickly, and they can be used several time, e.g. if you want to 2 same cubes in a scene.
Models are used in conjunction with Body."""
  DIRNAME = "models"
  SRC_DIRNAMES_EXTS = [("blender", ".blend"), ("obj", ".obj"), ("obj", ".mtl"), ("3ds", ".3ds"), ("worlds", ".data")]
  _alls = weakref.WeakValueDictionary()
  
  def _export(klass, src, filename):
    try:
      world = World.get(filename)
    except IOError: pass # For LOD model, 3 worlds are created with different filenames, and the model file is automatically generated
    else:
      model = world.to_model()
      model.filename = filename
      model.save()
  _export = classmethod(_export)
  
  def availables(klass): return World.availables()
  availables = classmethod(availables)
  
  
class VertexBufferedModel(Model, _soya._VertexBufferedModel):
  """VertexBufferedModel

The basic class of Model, rendered with vertex buffer object."""
  
class LODModel(Model, _soya._LODModel):
  """LODModel

A class of Model that supports LOD (Level-Of-Details), i.e. the model is rendered with
a level of detail that depends on the rendering quality (see soya.quality)."""
  
class Point(_soya._Point):
  """A Point is just a 3D position. It is used for math computation, but it DOESN'T display
anything."""

class Vector(_soya._Vector):
  """A Vector is a 3D vector (and not a kind of list or sequence ;-). Vectors are
useful for 3D math computation. 

Most of the math operators, such as +, -, *, /, abs,... work on Vectors and do
what they are intended to do ;-)"""

class Plane(_soya._Plane):
  """A Plane in 3D space. Just used for math computation, doesn't display anything."""

class Vertex(_soya._Vertex):
  """Vertex

A Vertex is a subclass of Point, which is used for building Faces.
A Vertex doesn't display anything ; you MUST put it inside a Face.

Attributes are (see also Point for inherited attributes):

 - diffuse: the vertex diffuse color (also aliased to 'color' for compatibility)
 - emissive: the vertex emissive color (lighting-independant color)
 - tex_x, tex_y: the text
ure coordinates (sometime called U and V).
"""

class Body(_soya._Body):
  """Body

A Body is a Soya 3D object that display a Model. The Body contains data about the
position, the orientation and the scaling, and the Model contains the geometric data.

This separation allows to use several time the same Model at different position, without
dupplicating the geometric data.

Attributes are (see also CoordSyst for inherited attributes):

 - model : the Model (a Model object, defaults to None).
"""

def do_cmd(cmd):
  print("* Soya * Running '%s'..." % cmd)
  os.system(cmd)
  
def do_cmd_popen(cmd):
  print("* Soya * Running '%s'..." % cmd)
  p = os.popen(cmd)
  import time; time.sleep(1.0)
  return p.read()
  
class World(SavedInAPath, _soya._World, Body):
  """World

A World is a Soya 3D object that can contain other Soya 3D objects, including other Worlds.
Worlds are used to group 3D objects ; when a World is moved, all the objects it contains
are moved too, since they are part of the World.
Mostly for historical reasons, World is a subclass of Body, and thus can display a Model.

Worlds can be saved in the "worlds" directory ; see SavedInAPath.

Attributes are (see also Body, CoordSyst and SavedInAPath for inherited attributes):

 - children : the list of 3D object contained in the World (default to an empty list).
   use World.add(coordsyst) and World.remove(coordsyst) for additions and removals.

 - atmosphere : the atmosphere specifies atmospheric properties of the World (see
   Atmosphere). Default is None.

 - model_builder : the model_builder specifies how the World is compiled into Model.
   Default is None, which result in the use of the default ModelBuilder.
"""

  DIRNAME = "worlds"
  SRC_DIRNAMES_EXTS = [("blender", ".blend")] #, ("obj", ".obj"), ("obj", ".mtl"), ("3ds", ".3ds")]
  _alls = weakref.WeakValueDictionary()
  
  def loaded(self):
    SavedInAPath.loaded(self)
    _soya._World.loaded(self)
    for i in self:
      if hasattr(i, "loaded"): i.loaded()
      
  def _export(klass, src, filename):
    if   src.endswith(".blend"):
      import tempfile
      tmp_file = tempfile.mkstemp()[1]
      do_cmd("blender %s -P %s FILENAME=%s TMP_FILE=%s %s" % (
        src,
        os.path.join(os.path.dirname(__file__), "converter", "blender2soya.py"),
        filename,
        tmp_file,
        (" CONFIG_TEXT=%s" % filename.split("@")[-1]) * bool("@" in filename),
        ))
      code = open(tmp_file).read()
      #try: os.unlink(tmp_file)
      #except: pass
      exec(code)
      
    #elif src.endswith(".obj") or src.endswith(".mtl"):
    #  import soya3.objmtl2soya
    #  world = soya3.objmtl2soya.loadObj(os.path.splitext(src)[0] + ".obj")
    #  world.filename = filename
    #  world.save()
      
    #elif src.endswith(".3ds"):
    #  import soya3._3DS2soya
    #  world = soya3._3DS2soya.load_3ds(os.path.splitext(src)[0] + ".3ds")
    #  world.filename = filename
    #  world.save()
  _export = classmethod(_export)
  
World._reffed = World.load

class VertexBufferModelBuilder(object):
  """VertexBufferModelBuilder

ModelBuilder for simple / normal / regular Model. The VertexBufferModelBuilder attributes allows to
customize the World -> Model computation.

Attributes are :

 - max_face_angle (default 80.0) : if the angle (in degree) between 2 faces is less than
   this value, vertices of the two faces can be merged if they are enough close. Set it
   to 180.0 or more to disable this feature.

 - outline_color (default black) : the color of the outline

 - outline_width (default 4.0) : the maximum line width when the cell-shaded model
   is very near the camera (use 0.0 to disable outlines)

 - outline_attenuation (default : 0.3) : specify how much the distance affect the
   outline_width
"""
  def __init__(self, max_face_angle = 80.0, outline_color = BLACK, outline_width = 0.0, outline_attenuation = 0.3):
    self.max_face_angle      = max_face_angle
    self.outline_color       = outline_color
    self.outline_width       = outline_width
    self.outline_attenuation = outline_attenuation
    
  def to_model(self, world):
    model = VertexBufferedModel(world, self.max_face_angle, 0, world.search_all(lambda item: isinstance(item, Light) and item.static), self.outline_color, self.outline_width, self.outline_attenuation)
    for mini_shader in world.mini_shaders: model.add_mini_shader(mini_shader)
    return model

  
#class _LODWorld:
#  def __init__(self, low_quality_world_filename, medium_quality_world_filename, high_quality_world_filename, collision_world_filename):
#    self.low_quality_world_filename    = low_quality_world_filename
#    self.medium_quality_world_filename = medium_quality_world_filename
#    self.high_quality_world_filename   = high_quality_world_filename
#    self.collision_world_filename      = collision_world_filename
    
  
    

class Light(_soya._Light):
  """Light

A Light is a 3D object that enlights the other objects.

Attributes are (see also CoordSyst for inherited attributes):

 - directional : True for a directional light (e.g. like the sun), instead of a
   positional light. The position of a directional light doesn't matter, and only
   the constant component of the attenuation is used. Default is false.
 - constant, linear and quadratic : the 3 components of the light attenuation. Constant
   reduces the light independently of the distance, linear increase with the distance,
   and quadratic increase the squared distance. Default is 1.0, 0.0 and 0.0.
 - cast_shadow : True if the light cast shadows on Models that have shadows enabled.
   Default is true.
 - shadow_color : the color of the shadow . Default is a semi-transparent black
   (0.0, 0.0, 0.0, 0.5).
 - top_level : XXX ???
 - static : True if the light can be used for static lighting when compiling a World into
   a Model. Default is true.
 - ambient : the light's ambient color, which is not affected by the light's orientation
   or attenuation. Default is black (no ambient).
 - diffuse : the light's color. Default is white.
 - specular : the light's specular color. Default is white.
 - angle : if angle < 180.0, the light is a spotlight.
 - exponent : modify how the spotlight's light is spread.
"""

class Camera(_soya._Camera):
  """Camera

The Camera specifies from where the scene is viewed.

Attributes are (see also CoordSyst and Widget for inherited attributes):

 - front, back : objects whose distance from the camera is not between front and back
   are clipped. Front defaults to 0.1 and back to 100.0.
   If the back / front ratio is too big, you loose precision in the depth buffer.

 - fov : the field of vision (or FOV), in degrees. Default is 60.0.

 - to_render : the world that is rendered by the camera. Default is None, which means
   the root scene (as returned by get_root()).

 - left, top, width, height : the viewport rectangle, in pixel. Use it if you want to
   render only on a part of the screen. It defaults to the whole screen.

 - ortho : True for orthogonal rendering, instead of perspective. Default is false.

 - partial : XXX ???. probably DEPRECATED by NoBackgroundAtmosphere.
"""

class Face(_soya._Face):
  """Face

A Face displays a polygon composed of several Vertices (see the Vertex class).
Notice that Face are SLOW ; Faces are normally used for building model but not for
rendering them. To get a fast rendering, you should put several Faces in a World, and
then compile the World into a Model (see the modeling-X.py tutorial series).

According to the number of Vertices, the result differs:
 - 1 Vertex => Plot
 - 2        => Line
 - 3        => Triangle
 - 4        => Quad

All the vertices are expected to be coplannar.

Interesting properties are:

 - vertices: the list of Vertices

 - material: the material used to draw the face's surface

 - double_sided: true if you want to see both sides of the Face. Default is false.

 - solid: true to enable the use of this Face for raypicking. Default is true.

 - lit: true to enable lighting on the Face. Default is true.

The following options are used when compiling the Face into a Model,
but does not affect the rendering of the Face itself:

 - static_lit: true to enable static lighting (faster). If true, when compiling the Face
   into a Model, all Lights available will be applied as static lighting. Default is true.

 - smooth_lit: true to compute per-vertex normal vectors, instead of per-face normal vector.
   This makes the Model looking smooth (see tutorial modeling-smoothlit-1.py).
   Notice that Soya automatically disable smooth_lit between 2 faces that makes a sharp
   angle (see ModelBuilder.max_face_angle attribute).
   Default is false.
"""

class Atmosphere(_soya._Atmosphere):
  """Atmosphere

An Atmosphere is an object that defines all the atmospheric attributes of a World, such
as fog, background or ambient lighting.

To apply an Atmosphere to a World, as well as everything inside the World, do :

    world.atmosphere = my_atmosphere

You can safely put several Worlds one inside the other, with different Atmospheres.

Attributes are :

 - fog: true to activate fog, false to disable fog (default value).

 - fog_color: the fog color (an (R, G, B, A) tuple of four floats). Defaults to black.

 - fog_type: the type of fog. fog_type can take 3 different values :
   - 0, linear fog: the fog range from fog_start to fog_end (default value).
   - 1, exponentiel fog: the fog the fog increase exponentially to fog_density and the distance.
   - 2, exponentiel squared fog: the fog the fog increase exponentially to the square of fog_density and the distance.

 - fog_start: the distance at which the fog begins, if fog_type == 0. Defaults to 10.0.

 - fog_end: the distance at which the fog ends, if fog_type == 0. Defaults to 100.0.

 - fog_density: the fog density, if fog_type > 0. Defaults to 1.0.

 - ambient: the ambient lighting color (an (R, G, B, A) tuple of four floats). Defaults to (0.5, 0.5, 0.5, 1.0).

 - bg_color: the background color of the scene (an (R, G, B, A) tuple of four floats). Defaults to black.
"""

class NoBackgroundAtmosphere(_soya._NoBackgroundAtmosphere, Atmosphere):
  """NoBackgroundAtmosphere

An Atmosphere with no background. It is usefull is you want to render a 3D scene over
another 3D scene."""
  
class NoBackgroundNoDepthCleanAtmosphere(_soya._NoBackgroundNoDepthCleanAtmosphere, Atmosphere):
  """NoBackgroundNoDepthCleanAtmosphere

An Atmosphere with no background, and that does not clean the depth buffer.
It is usefull is you want to render a 3D scene over another 3D scene."""

if hasattr(_soya, "_FixedBackgroundAtmosphere"):
  class FixedBackgroundAtmosphere(_soya._FixedBackgroundAtmosphere, Atmosphere):
    """FixedBackgroundAtmosphere

An Atmosphere that can capture a already-rendered 3D scene, and then restores as a background.
It Captures both colors and depth buffer. Usefull for old-style game with pre-rendered scenes !"""

class SkyAtmosphere(_soya._SkyAtmosphere, Atmosphere):
  """SkyAtmosphere

An Atmosphere with a skybox and/or a sky/cloud effect.

In addition to those of Atmosphere, attributes are :

 - sky_box: the sky box, a tuple of 5 or 6 materials that are displayed on the 6 faces of
   the sky box (which is a cube). Use an empty tuple () to disable the sky box (default value).

 - sky_color: the color of the sky (an (R, G, B, A) tuple of four floats).
   Use a sky_color with an alpha component of 0.0 to disable cloud / sky effet.

 - cloud: the cloud material, which is used to add a cloud-like effect to the sky.
   Coulds move according to the camera.
"""

class Sprite(_soya._Sprite):
  """Sprite

A 2D sprite, displayed as a 3D (e.g. think to very old 3D games).
Today, sprite are usefull for special effect like explosion, or halo.
The Sprite 2D texture always points toward the camera.

Attributes are :

 - material: the material of the Sprite, including the texture.

 - color: the color of the Sprite (defaults to white).

 - width and height: the size of the Sprite, in 3D coordinates values (not pixel values).
   Both defaults to 0.5.

 - lit: if true (default), lighting affects the sprite, and if false, it doesn't."""

class CylinderSprite(_soya._CylinderSprite, Sprite):
  """CylinderSprite

A special kind of Sprite, that points toward the camera only in X and Z dimension, but
not Y. This is usefull e.g. for lightening spell effects, for which using a normal Sprite
would give a poor rendering if seen from top."""

class Particles(_soya._Particles):
  pass

class Portal(_soya._Portal):
  
  # Implement in Python due to the lambda
  def pass_through(self, coordsyst):
    """Portal.pass_though(self, coordsyst)

Makes COORDSYST pass through the portal. If needed (=if coordsyst.parent is self.parent),
it removes COORDSYST from its current parent and add it in the new one,
at the right location.
If coordsyst is a camera, it change the 'to_render' attribute too.

The passing through does NOT occur immediately, but after the beginning of the round
(this is usually what you need, in order to avoid that moving COORDSYST from a parent
to another makes it plays twice)."""
    def do_it():
      if isinstance(coordsyst, Camera) and coordsyst.to_render:
        coordsyst.to_render = self.beyond
      if coordsyst.parent is self.parent:
        self.beyond.add(coordsyst)
    MAIN_LOOP.next_round_tasks.append(do_it)
    
    
class Terrain(_soya._Terrain):
  pass

class TravelingCamera(_soya._TravelingCamera):
  pass

class ThirdPersonTraveling(_soya._ThirdPersonTraveling):
  pass

class FixTraveling(_soya._FixTraveling):
  pass


if hasattr(_soya, "_AnimatedModel"):
  class AnimatedModel(Model, _soya._AnimatedModel):
    DIRNAME = "animated_models"
    SRC_DIRNAMES_EXTS = [("blender", ".blend")]
    _alls = weakref.WeakValueDictionary()
    
    def _export(klass, src, filename):
      if   src.endswith(".blend"):
        if "@" in filename: config_text = "config_text=%s" % filename.split("@")[-1]
        else:               config_text = ""
        do_cmd("blender %s -P %s %s QUALITY=%s%s" % (
          src,
          os.path.join(os.path.dirname(__file__), "converter", "blender2cal3d.py"),
          os.path.join(os.path.dirname(src), os.pardir, AnimatedModel.DIRNAME, filename, filename + ".cfg"),
          _soya.get_quality(),
          config_text,
          ))
    _export = classmethod(_export)
    
    def load(klass, filename):
      filename = filename.replace("/", os.sep)
      ext      = os.sep + filename + ".cfg"
      dirname  = klass._get_directory_for_loading_and_check_export(filename, ext)
      r = parse_cal3d_cfg_file(os.path.join(dirname, klass.DIRNAME, filename, filename + ".cfg"))
      
      if r == "LOD":
        quality = _soya.get_quality()
        if   quality == 0: quality_name = "low"
        elif quality == 1: quality_name = "medium"
        else:              quality_name = "high"
        ext = os.sep + quality_name + ext
        
        dirname  = klass._get_directory_for_loading_and_check_export(filename, ext)
        r = parse_cal3d_cfg_file(os.path.join(dirname, klass.DIRNAME, filename, quality_name, filename + ".cfg"))
        
        
      return r
    load = classmethod(load)
    
  cerealizer.register_class(AnimatedModel, SavedInAPathHandler(AnimatedModel))
  cerealizer.register_class(_soya._AnimatedModelData)
  
  
class CoordSystState(_soya._CoordSystState):
  """CoordSystState

A State that take care of CoordSyst position, rotation and scaling.

CoordSystState extend CoordSyst, and thus have similar method (e.g. set_xyz, rotate_*,
scale, ...)"""
class CoordSystSpeed(_soya._CoordSystSpeed):
  """CoordSystSpeed

A Coordinate System "speed" / derivation, taking into account position, rotation and scaling.

CoordSystSpeed extend CoordSyst, and thus have similar method (e.g. set_xyz, rotate_*,
scale, ...)"""
  
#ODE addition
if hasattr(_soya, "_Mass"):
  class Mass(SavedInAPath, _soya._Mass): pass
  class Joint(_soya._Joint,object): pass
  
if hasattr(_soya, "_Sound"):
  # Has sound / OpenAL support

  class Sound(SavedInAPath, _soya._Sound):
    """Sound

  A sound.

  Use soya.Sound.get("filename.wav") for loading a sound from your data directory.

  Interesting attributes:
    - stereo: 1 if the sound is stereo, 0 otherwise.
  """

    DIRNAME = "sounds"
    _alls = weakref.WeakValueDictionary()

    def save(klass, filename = None): raise NotImplementedError("Soya cannot save sound.")

    def load(klass, filename):
      if ".." in filename: raise ValueError("Cannot have .. in filename (security reason)!", filename)
      filename = filename.replace("/", os.sep)
      
      try:
        import pymedia
        has_pymedia = 1
      except:
        has_pymedia = 0
        
      has_pymedia = 0
        
      for p in path:
        file = os.path.join(p, klass.DIRNAME, filename)
        if os.path.exists(file):
          if has_pymedia:
            sound = PyMediaSound(file)
          else:
            if   file.endswith(".wav"): sound = WAVSound(file)
            elif file.endswith(".ogg"): sound = OGGVorbisSound(file)
            else: raise ValueError("Unsupported sound file format: %s!" % file)
          sound._filename = filename
          return sound
      raise ValueError("No %s named %s" % (klass.__name__, filename))
    load = classmethod(load)
    
    
  class PyMediaSound(_soya._PyMediaSound, Sound):
    """PyMediaSound

  A sound loaded through PyMedia (support WAV, OGG Vorbis, MP3,...).

  Use soya.Sound.get("filename.xxx") for loading a sound from your data directory,
  or soya.PyMediaSound("/full/filename.xxx") for loading a sound from any directory."""

  class WAVSound(_soya._WAVSound, Sound):
    """WAVSound

  A sound in WAV format.

  Use soya.Sound.get("filename.wav") for loading a sound from your data directory,
  or soya.WAVSound("/full/filename.wav") for loading a sound from any directory."""

  class OGGVorbisSound(_soya._OGGVorbisSound, Sound):
    """OGGVorbisSound

  A sound in OGG Vorbis format.

  Use soya.Sound.get("filename.ogg") for loading a sound from your data directory,
  or soya.OGGVorbisSound("/full/filename.ogg") for loading a sound from any directory."""


  class SoundPlayer(_soya._SoundPlayer):
    """SoundPlayer

  A SoundPlayer is a 3D object that play a sound.

  Interesting attributes:
    - sound      : the sound currently played (read-only)
    - loop       : if true, the sound restarts from the beginning when it ends; default is false
    - auto_remove: if true (default), the SoundPlayer is automatically removed when the sound ends (excepted in cases of looping!)
    - gain       : the body (default 1.0)
    - play_in_3D : if true, the sound is played as a 3D sound; if false, as a 2D sound. Notice that OpenAL cannot play stereo sound in 3D.

  Constructor is SoundPlayer(parent = None, sound = None, loop = 0, play_in_3D = 1, gain = 1.0, auto_remove = 1)

  The SoundPlayer.ended method is called when the sound ends, and can be overriden if needed.

  To stop

  """

    def ended(self):
      """SoundPlayer.ended()

  This method is called when the sound is over. It is NOT called if looping.

  The default implementation removes the SoundPlayer, if SoundPlayer.auto_remove is true."""
      # Implemented in Python because of the lambda
      if self.auto_remove:
        MAIN_LOOP.next_round_tasks.append(lambda: self.parent and self.parent.remove(self))
    
  cerealizer.register_class(WAVSound, SavedInAPathHandler(WAVSound))
  cerealizer.register_class(OGGVorbisSound, SavedInAPathHandler(OGGVorbisSound))
  cerealizer.register_class(SoundPlayer)


if hasattr(_soya, "_Font"):
  class Font(SavedInAPath, _soya._Font):
    DIRNAME = "fonts"
    _alls = weakref.WeakValueDictionary()
    
    def __init__(self, filename, width = 20, height = 30):
      _soya._Font.__init__(self, filename, width, height)
      self._filename = ""
      
    def load(klass, filename):
      width  = 20
      height = 30
      p = filename.split("@")
      filename2 = p[0]
      if len(p) > 1:
        width, height = map(int, p[1].split("x"))
      if ".." in filename2: raise ValueError("Cannot have .. in filename (security reason)!", filename2)
      filename2 = filename2.replace("/", os.sep)
      for p in path:
        file = os.path.join(p, klass.DIRNAME, filename2)
        if os.path.exists(file):
          font = Font(file, width, height)
          font._filename = filename
          return font
      raise ValueError("No %s named %s" % (klass.__name__, filename2))
    load = classmethod(load)
    
    def save(klass, filename = None): raise NotImplementedError("Soya cannot save font.")
    
    def availables(klass):
      """SavedInAPath.availables() -> list

  Returns the list of the filename all the objects available in the current path."""
      filenames = dict(klass._alls)
      for p in path:
        for filename in os.listdir(os.path.join(p, klass.DIRNAME)):
          filenames[filename] = 1
      filenames = list(filenames.keys())
      filenames.sort()
      return filenames
    availables = classmethod(availables)
  
  cerealizer.register_class(Font, SavedInAPathHandler(Font))
  


  
  

_soya.Image               = Image
_soya.Material            = Material
_soya.Model               = Model
_soya.VertexBufferedModel = VertexBufferedModel
_soya.Point               = Point
_soya.Vector              = Vector
_soya.Plane               = Plane
_soya.Camera              = Camera
_soya.Light               = Light
_soya.Body                = Body
_soya.World               = World
_soya.AnimatedModel       = AnimatedModel
_soya.Face                = Face
_soya.Atmosphere          = Atmosphere
_soya.Portal              = Portal
_soya.Terrain             = Terrain
_soya.Particles           = Particles
_soya.Mass                = Mass
_soya.Joint               = Joint



cerealizer.register_class(Vertex)
cerealizer.register_class(World, SavedInAPathHandler(World))
cerealizer.register_class(NoBackgroundAtmosphere)
cerealizer.register_class(FixTraveling)
cerealizer.register_class(VertexBufferedModel, SavedInAPathHandler(VertexBufferedModel))
cerealizer.register_class(LODModel, SavedInAPathHandler(LODModel))
cerealizer.register_class(Material, SavedInAPathHandler(Material))
cerealizer.register_class(CylinderSprite)
cerealizer.register_class(Light)
cerealizer.register_class(TravelingCamera)
cerealizer.register_class(CoordSystState)
cerealizer.register_class(CoordSystSpeed)
cerealizer.register_class(Vector)
cerealizer.register_class(Point)
cerealizer.register_class(Image, SavedInAPathHandler(Image))
#cerealizer.register_class(Model, SavedInAPathHandler(Model))
cerealizer.register_class(SkyAtmosphere)
cerealizer.register_class(Portal)
cerealizer.register_class(Terrain)
cerealizer.register_class(Face)
cerealizer.register_class(Atmosphere)
cerealizer.register_class(Particles)
cerealizer.register_class(Sprite)
cerealizer.register_class(Body)
cerealizer.register_class(ThirdPersonTraveling)

cerealizer.register_class(VertexBufferModelBuilder)
cerealizer.register_class(_soya.FlagFirework)
cerealizer.register_class(_soya.Fountain)
cerealizer.register_class(_soya.Smoke)
cerealizer.register_class(_soya.FlagSubFire)
cerealizer.register_class(_soya._VertexBufferedModelData)


DEFAULT_MATERIAL = Material()
DEFAULT_MATERIAL.filename  = "__DEFAULT_MATERIAL__"
DEFAULT_MATERIAL.shininess = 128.0
_soya._set_default_material(DEFAULT_MATERIAL)

PARTICLE_DEFAULT_MATERIAL = Material()
PARTICLE_DEFAULT_MATERIAL.additive_blending = 1
PARTICLE_DEFAULT_MATERIAL.texture = open_image(os.path.join(DATADIR, "fx.png"))
PARTICLE_DEFAULT_MATERIAL.filename = "__PARTICLE_DEFAULT_MATERIAL__"
PARTICLE_DEFAULT_MATERIAL.diffuse = (1.0, 1.0, 1.0, 1.0)
_soya._set_particle_default_material(PARTICLE_DEFAULT_MATERIAL)

_soya._set_default_model_builder(VertexBufferModelBuilder())

opengl = _soya.OpenGL()

inited = 0
quiet = 0


DEBUG_SHADER = 0

from soya3.mini_shader import *
