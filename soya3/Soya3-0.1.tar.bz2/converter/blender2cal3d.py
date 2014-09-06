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

import sys, os, os.path, glob, math
import bpy, mathutils
from collections import *
from itertools   import *

__author__    = "Jeremy Moles, Palle Raabjerg, Jean-Baptiste Lamy"
__email__     = "jeremy@emperorlinux.com, palle@user-friendly.dk, jibalamy@free.fr"
__url__       = "http://gna.org/projects/cal3d"
__bpydoc__    = """
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Known problems:
 * None yet !

"""

print(sys.argv)
FILENAME        = sys.argv[sys.argv.index("-P") + 2]
AUTHOR          = ""
PREPEND         = ""
XMLINDENT       = 2
FLOATPRE        = 5
ANIMFPS         = 25.0
EXPORTGL        = True
LOD             = False
EXTRADATA       = False
SCALE           = 1.0
MAX_FACE_ANGLE  = 80.0
ADDITIONAL_CFG  = ""
MATERIAL_MAP    = {}
MIN_INFLUENCE   = 0.05 # Minimum influence weight for a bone on a vertex -- any influence below this value will be discarded
INFLUENCE_POWER = 1 # Power applied to influence weight (weight => weight ** INFLUENCE_POWER). Usefull when using Subsurf. I suggest 1 for octopus like creature, and 2 (or higher) for Human creature

# Soya specific stuff
QUALITY         = -1 # 0 low, 1 medium, 2 high, -1 disable -- for Subsurf with Soya
LOD_LOW = LOD_MEDIUM = LOD_HIGH = -1 # Subsurf values for the 3 quality levels

if EXPORTGL:
  ROT90X    = mathutils.Matrix.Rotation(math.radians(90), 4, "X")
  IROT90X   = ROT90X.inverted()
  VECTOR2GL = lambda v: IROT90X * v
  MATRIX2GL = lambda m: IROT90X * m * ROT90X
else:
  VECTOR2GL = lambda v: v
  MATRIX2GL = lambda m: m
  
CONCAT      = lambda s, j = "": j.join([str(v) for v in s])
STRFLT      = lambda f: "%%.%df" % FLOATPRE % f

# Blender.Mathutils.AngleBetweenVecs seems bugged ??
def vector_length(v):         return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
def vector_dot_product(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def vector_angle(a, b):
  s = vector_length(a) * vector_length(b)
  if s == 0.0: return 0.0
  f = vector_dot_product(a, b) / s
  if f >=  1.0: return   0.0
  if f <= -1.0: return 180.0
  return (math.atan(-f / math.sqrt(1.0 - f * f)) + math.pi / 2) / math.pi * 180.0

# Blender matrix multiplication behaves strangely!
def matrix_multiply(matrix1, matrix2): return matrix2 * matrix1

# def matrix_multiply(b, a):
#   r[ 0] = a[ 0] * b[0] + a[ 1] * b[4] + a[ 2] * b[ 8]
#   r[ 4] = a[ 4] * b[0] + a[ 5] * b[4] + a[ 6] * b[ 8]
#   r[ 8] = a[ 8] * b[0] + a[ 9] * b[4] + a[10] * b[ 8]
#   r[12] = a[12] * b[0] + a[13] * b[4] + a[14] * b[ 8] + b[12]
#   r[ 1] = a[ 0] * b[1] + a[ 1] * b[5] + a[ 2] * b[ 9]
#   r[ 5] = a[ 4] * b[1] + a[ 5] * b[5] + a[ 6] * b[ 9]
#   r[ 9] = a[ 8] * b[1] + a[ 9] * b[5] + a[10] * b[ 9]
#   r[13] = a[12] * b[1] + a[13] * b[5] + a[14] * b[ 9] + b[13]
#   r[ 2] = a[ 0] * b[2] + a[ 1] * b[6] + a[ 2] * b[10]
#   r[ 6] = a[ 4] * b[2] + a[ 5] * b[6] + a[ 6] * b[10]
#   r[10] = a[ 8] * b[2] + a[ 9] * b[6] + a[10] * b[10]
#   r[14] = a[12] * b[2] + a[13] * b[6] + a[14] * b[10] + b[14]
#   r[ 3] = 0.0
#   r[ 7] = 0.0
#   r[11] = 0.0
#   r[15] = 1.0
#   r[16] = a[16] * b[16]
#   r[17] = a[17] * b[17]
#   r[18] = a[18] * b[18]
#   return r

def parse_args(args):
  global MATERIAL_MAP, LOD, SCALE, MAX_FACE_ANGLE, INFLUENCE_POWER, MIN_INFLUENCE, LOD_LOW, LOD_MEDIUM, LOD_HIGH, QUALITY, ADDITIONAL_CFG
  
  for arg in args:
    if "=" in arg:
      attr, val = arg.split("=")
      attr = attr.lower()
      try: val = int(val)
      except:
        try: val = float(val)
        except: pass
        
    if   attr.startswith("material_"): # A material map
      MATERIAL_MAP[attr[len("material_"):]] = val
      
    elif attr == "lod":
      LOD = val
      
    elif attr == "config_text": # Config text
      sys.stderr.write("(reading config text %s)\n" % val)
      parse_buffer(val)
      
    elif attr == "config_file": # Config file
      sys.stderr.write("(reading config file %s)\n" % val)
      parse_args(open(val).read().split("\n"))
      
    elif attr == "scale":           SCALE           = val
    elif attr == "max_face_angle":  MAX_FACE_ANGLE  = val
    elif attr == "min_influence":   MIN_INFLUENCE   = val
    elif attr == "influence_power": INFLUENCE_POWER = val
    elif attr == "lod_low":         LOD_LOW         = val
    elif attr == "lod_medium":      LOD_MEDIUM      = val
    elif attr == "lod_high":        LOD_HIGH        = val
    elif attr == "lod_collision":   pass # Not yet supported
    elif attr == "quality":         QUALITY         = val
    
    else:
      ADDITIONAL_CFG += arg + "\n"
      
def parse_buffer(name):
  text = bpy.data.texts.get(name)
  if text: parse_args(text.as_string().split("\n"))
  #try: args = bpy.data.texts[name].as_string().split("\n")
  #except: print("Problem with text buffer %s !" % name)
  #else: parse_args(args)




class Cal3DObject(object):
  # Children of this class must
  # define a method called XML which should build and return an XML representation
  # of the object. Furthermore, children that pass a value in the constructor
  # for the magic parameter are treated as top-level XML files and preprend
  # the appropriate headers.
  def __init__(self, magic = None): self.magic = magic

  def __repr__(self):
    ret = ""
    if self.magic:
      ret += """<?xml version="1.0"?>\n"""
      ret += """<HEADER MAGIC="%s" VERSION="1200"/>\n""" % self.magic
    return ret + self.XML().replace("\t", "").replace("#", " " * XMLINDENT)

  def __str__(self): return self.__repr__()


class Material(Cal3DObject):
  MATERIALS  = {}
  
  def __init__(self, name, ambient = None, diffuse = None, specular = None, mapnames = None):
    Cal3DObject.__init__(self, "XRF")
    self.name      = name
    self.ambient   = ambient  or [255] * 4
    self.diffuse   = diffuse  or [255] * 4
    self.specular  = specular or [255] * 4
    self.shininess = 1.0
    self.mapnames  = []
    self.id        = len(Material.MATERIALS)
    if mapnames: self.mapnames.extend(mapnames)
    Material.MATERIALS[self.name] = self
    
  def XML(self):
    mapXML = ""
    for mapname in self.mapnames: mapXML += "#<MAP>%s</MAP>\n" % mapname
    return """\
<MATERIAL NUMMAPS="%s">
#<AMBIENT>%s %s %s %s</AMBIENT>
#<DIFFUSE>%s %s %s %s</DIFFUSE>
#<SPECULAR>%s %s %s %s</SPECULAR>
#<SHININESS>%s</SHININESS>
%s</MATERIAL>
""" % (len(self.mapnames),
       self.ambient [0], self.ambient [1], self.ambient [2], self.ambient [3],
       self.diffuse [0], self.diffuse [1], self.diffuse [2], self.diffuse [3],
       self.specular[0], self.specular[1], self.specular[2], self.specular[3],
       self.shininess, mapXML)


class Mesh(Cal3DObject):
  def __init__(self, name):
    Cal3DObject.__init__(self, "XMF")
    self.name      = name.replace(".", "_")
    self.submeshes = []
    
  def XML(self):
    return """\
<MESH NUMSUBMESH="%s">
%s</MESH>
""" % (len(self.submeshes), CONCAT(self.submeshes))

class SubMesh(Cal3DObject):
  def __init__(self, mesh, material):
    Cal3DObject.__init__(self)
    self.material     = material
    self.vertices     = []
    self.faces        = []
    self.springs      = []
    self.mesh         = mesh
    self.num_lodsteps = 0
    mesh.submeshes.append(self)
    if not material: self.material = Material("Default")
    
  # These are all small classes for the creation of a very specific,
  # temporary data structure for LOD calculations. The entire submesh
  # will be temporarily copied into this structure, to allow more freedom
  # in on-the-fly refactorizations and manipulations.
  class LODVertex:
    """We need to factor in some other information, compared
    to standard vertices, like edges and faces. On the other hand,
    we don't really need stuff like UVs when we do this. Doing another
    small, inner Vertex class for this, will hopefully not be
    seen as a total waste."""
    def __init__(self, origindex, loc, cloned):
      self.id             = origindex
      self.loc            = mathutils.Vector(loc)
      self.edges          = {}
      self.faces          = {}
      self.cloned         = cloned
      self.col_to         = None
      self.col_from       = None
      self.face_collapses = 0
      self.deathmarked    = False
      
    def colto(self):
      if self.col_to:
        cvert = self.col_to
        while cvert.col_to: cvert = cvert.col_to
        return cvert
      else:
        return self

    def colfrom(self):
      if self.col_from:
        cvert = self.col_from
        while cvert.col_from: cvert = cvert.col_from
        return cvert
      else:
        return self

    def getid (self): return self.colto().id
    def getloc(self): return self.colto().loc
    
    def getfaces(self, facel = None):
      if not facel: facelist = []
      else:         facelist = facel

      for face in self.faces.values():
        if (not face.dead) and (not facelist.__contains__(face)): facelist.append(face)
      if self.col_from: facelist = self.col_from.getfaces(facelist)
      return facelist

    def getedges(self, edgel = None):
      if not edgel: edgelist = []
      else:         edgelist = edgel

      for edge in self.edges.values():
        if (not edge.dead) and (not edgelist.__contains__(edge)): edgelist.append(edge)
      if self.col_from: edgelist = self.col_from.getedges(edgelist)
      return edgelist

  class LODFace:
    def __init__(self, verts, fid):
      self.verts = verts
      vertset    = frozenset((self.verts[0].id, self.verts[1].id, self.verts[2].id))
      for vert in self.verts: vert.faces[self.getHashableSet()] = self
      
      self.id    = fid
      self.edges = []
      self.RefactorArea()

      self.dead = False
      
    def replaceVert(self, replacev, withv):
      i = self.verts.index(replacev)
      self.verts[i] = withv
      
    def RefactorArea(self):
      crossp = (self.verts[1].getloc() - self.verts[2].getloc()).cross(self.verts[0].getloc() - self.verts[2].getloc())
      self.area = (1./2.)*((crossp.x**2 + crossp.y**2 + crossp.z**2)**(1./2.))
      
    def getHashableSet(self):
      return frozenset((self.verts[0].id, self.verts[1].id, self.verts[2].id))
    
  class LODEdge:
    """Extra, inner class used for the temporary LOD datastructure"""
    def __init__(self, v1, v2):
      self.v1 = v1
      self.v2 = v2
      vertset = frozenset((self.v1.id, self.v2.id))
      self.v1.edges[vertset] = self
      self.v2.edges[vertset] = self
      self.faces             = []
      self.collapsed_faces   = {}

      self.RefactorLength()

      self.dead = False

    def getOtherVert(self, vertex):
      if   vertex == self.v1: return self.v2
      elif vertex == self.v2: return self.v1

    def Refactor(self):
      self.RefactorLength()
      self.RefactorWeight()

    def RefactorLength(self): self.length = (self.v2.getloc() - self.v1.getloc()).length

    def RefactorWeight(self):
      # Determine which vert to collapse to which,
      # using jiba's method of basing this decision on
      # The number of edges connected to each vertex
      # I.e.: Collapse the edge with least amount of edges.
      # The order of the vertices in v1, v2 do not matter in
      # any other respect, so we simply use this order, and
      # say we collapse v1 into v2.
      if len(self.v1.getedges()) > len(self.v2.getedges()): self.v1, self.v2 = self.v2, self.v1
      
      # Get total area of faces surrounding edge
      area = 0
      for face in self.faces: area += face.area
      
      proportional_area   = area / avg_area
      proportional_length = self.length / avg_length
      
      # Get dot products (angle sharpness) of edges connected to v1
      edgeverts_factor = 0
      
      self_vec = self.v2.getloc() - self.v1.getloc()
      self_vec.normalize()
      for edge in self.v1.edges.values():
        if edge != self:
          edgevert = edge.getOtherVert(self.v1)
          edge_vec = edgevert.getloc() - self.v1.getloc()
          edge_vec.normalize()
          edgeverts_factor += (1 - self_vec.dot(edge_vec))/2
          
      # Get dot products of edges connected to v2. Wohoo, copy-paste!
      self_vec = self.v1.getloc() - self.v2.getloc()
      self_vec.normalize()
      for edge in self.v2.edges.values():
        if edge != self:
          edgevert = edge.getOtherVert(self.v2)
          edge_vec = edgevert.getloc() - self.v2.getloc()
          edge_vec.normalize()
          edgeverts_factor += (1 - self_vec.dot(edge_vec))/2
          
      # Error metric, or magic formula. Whatever you like to call it.
      # This calculates the weight of the edge, based on the
      # information we have now gathered. We can change this at
      # any time to try and get better results.
      self.weight = proportional_area * proportional_length * edgeverts_factor
      
      return self.weight
    
    def getHashableSet(self): return frozenset((self.v1.id, self.v2.id))

    def collapse(self):
      if self.v1.col_to or self.v2.col_to: return False
      if self.v1.cloned or self.v2.cloned: return False
      if len(self.faces) < 2:              return False
      self.dead = True

      # Mark all faces as dead and the two
      # collapsed edges as dead
      for face in filter(self.v1.getfaces().__contains__, self.v2.getfaces()):
        # If not dead, add to dict of faces to collapse with this edge
        if not face.dead:
          self.collapsed_faces[face.getHashableSet()] = face
          self.v1.face_collapses += 1
          face.dead = True
        # Mark collapsed edges as dead. Edges that don't share
        # a vertex with this edge's v2 dies.
        for edge in face.edges:
          if (edge.v1 != self.v2) and (edge.v2 != self.v2): edge.dead = True


      # Refactor area of all non-dead faces on vertex 1
      for face in self.v1.getfaces():
        if not face.dead: face.RefactorArea()

      # Refactor lengths and weights of all non-dead
      # edges on vertex 1
      for edge in self.v1.getedges():
        if not edge.dead: edge.Refactor()

      self.v2.colfrom().col_from = self.v1
      self.v1.col_to             = self.v2
      
      return True
      

  def LOD(self):
    global avg_area, avg_length
    
    # Step one. Build temporary data structure suited for weight calculations.
    # Vertices are the only ones that can be/needs to be ordered.
    # Faces and edges are dicts, with Immutable Sets (containing Vertex indices) as keys.
    LODverts = []
    LODfaces = {}
    LODedges = {}
    
    # Create vertices
    progressbar.setup(len(self.vertices), "Creating LODverts")
    for vertex in self.vertices:
      progressbar.increment()
      LODverts.append(self.LODVertex(vertex.id, vertex.loc, vertex.cloned))

    # Create faces
    num_faces  = 0
    avg_area   = 0
    total_area = 0
    progressbar.setup(len(self.faces), "Creating LODfaces")
    for face in self.faces:
      progressbar.increment()
      lface = self.LODFace([LODverts[face.vertices[0].id], LODverts[face.vertices[1].id], LODverts[face.vertices[2].id]], num_faces)
      LODfaces[lface.getHashableSet()] = lface
      total_area += lface.area
      num_faces  += 1
    if num_faces: avg_area = total_area / float(num_faces)

    # Create edges
    num_edges    = 0
    avg_length   = 0
    total_length = 0
    progressbar.setup(len(LODfaces), "Creating LODedges")
    for lodface in LODfaces.values():
      progressbar.increment()
      #Create the three edges from this face
      for e in [(0, 1), (0, 2), (1, 2)]:
        imset = frozenset((lodface.verts[e[0]].id, lodface.verts[e[1]].id))
        if not imset in LODedges:
          #Create edge
          lodedge = self.LODEdge(lodface.verts[e[0]], lodface.verts[e[1]])
          LODedges[imset] = lodedge
          lodface.edges.append(lodedge)
          lodedge.faces.append(lodface)
          total_length += lodedge.length
          num_edges    += 1
        else:
          lodedge = LODedges[imset]
          lodface.edges.append(lodedge)
          lodedge.faces.append(lodface)

    if num_edges: avg_length = total_length / float(num_edges)

    # Step two. Calculate initial weights of all edges.
    progressbar.setup(len(LODedges), "Calculating weights")
    for edge in LODedges.values():
      progressbar.increment()
      edge.RefactorWeight()

    # Order edges in list after weights
    LODedgelist = LODedges.values()
    LODedgelist.sort(self.compareweights)
    weight = LODedgelist[0].weight

    percentage    = len(LODedgelist) * 0.6
    count         = 0
    collapse_list = []

    progressbar.setup(percentage, "Calculating LOD")
    while count < percentage:
      edge = LODedgelist.pop(0)
      if not edge.dead:
        if edge.collapse():
          LODedgelist.sort(self.compareweights)
          collapse_list.append((edge.v1, edge.collapsed_faces))
      count += 1
      progressbar.increment()

    self.num_lodsteps = len(collapse_list)
    newvertlist = []
    newfacelist = []
    # The list should be in reverse order, with the most
    # important ones first.
    collapse_list.reverse()

    for vertex, faces in collapse_list: vertex.col_to = self.vertices[vertex.col_to.id]
    
    for vertex in LODverts:
      if not vertex.col_to:
        cvert = self.vertices[vertex.id]
        cvert.id = len(newvertlist)
        newvertlist.append(cvert)

    for face in LODfaces.values():
      if not face.dead: newfacelist.append(self.faces[face.id])
 
    for vertex, faces in collapse_list:
      for face in faces.values():
        newfacelist.append(self.faces[face.id])
      cvert = self.vertices[vertex.id]
      cvert.id = len(newvertlist)
      cvert.collapse_to = vertex.col_to
      cvert.num_faces = vertex.face_collapses
      newvertlist.append(cvert)

    self.vertices = newvertlist
    self.faces    = newfacelist

  def compareweights(self, x, y):
    result = x.weight - y.weight
    if   result < 0: return -1
    elif result > 0: return  1
    else:            return  0

  def XML(self):
    return """\
#<SUBMESH
##NUMVERTICES="%s"
##NUMFACES="%s"
##MATERIAL="%s"
##NUMLODSTEPS="%s"
##NUMSPRINGS="%s"
##NUMTEXCOORDS="%s"
#>
%s%s%s#</SUBMESH>
""" % (len(self.vertices),
       len(self.faces),
       self.material.id,
       self.num_lodsteps,
       len(self.springs),
       len(self.material.mapnames),
       CONCAT(self.vertices), CONCAT(self.springs),CONCAT(self.faces))



class Map(Cal3DObject):
  def __init__(self, uv):
    Cal3DObject.__init__(self)
    self.uv = mathutils.Vector(uv)
    
  def XML(self):
    return "###<TEXCOORD>%s %s</TEXCOORD>\n" % (STRFLT(self.uv.x), STRFLT(-self.uv.y))
  
class Vertex(Cal3DObject):
  # An interesting note about this class is that we keep Blender objects
  # as self.loc and self.normal. Of note is how we "wrap" the existing
  # instances with our own copies, since I was experiencing bugs where
  # the existing ones would go out of scope.
  def __init__(self, submesh, hv):
    Cal3DObject.__init__(self)
    
    self.loc         = mathutils.Vector(hv.co)
    self.normal      = mathutils.Vector(hv.normal)
    self.influences  = []
    self.submesh     = submesh
    self.id          = len(submesh.vertices)
    self.cloned      = 0 # XXX ???
    self.collapse_to = None
    self.num_faces   = 0
    
    if submesh.material.mapnames and (not hv.uv[0] is None):
      self.maps = [Map(hv.uv) for i in range(len(submesh.material.mapnames))]
    else:
      self.maps = []
      
    submesh.vertices.append(self)

    hv.cal3d_vertex      = self
    self.hashable_vertex = hv
    
  def XML(self):
    loc    = VECTOR2GL(self.loc)
    normal = VECTOR2GL(self.normal)
    
    collapse = ""
    # Note: collapse_to is an index, and _can_ be 0
    if self.collapse_to != None:
      collapse = """\
###<COLLAPSEID>%s</COLLAPSEID>
###<COLLAPSECOUNT>%s</COLLAPSECOUNT>
""" % (str(self.collapse_to.id), str(self.num_faces))

    loc    *= SCALE
    normal *= SCALE

    return """\
##<VERTEX ID="%s" NUMINFLUENCES="%s">
###<POS>%s %s %s</POS>
###<NORM>%s %s %s</NORM>
%s%s%s##</VERTEX>
""" % (self.id, len(self.influences),
       STRFLT(loc.x), STRFLT(loc.y), STRFLT(loc.z),
       STRFLT(normal.x), STRFLT(normal.y), STRFLT(normal.z),
       collapse,
       len(self.maps)  and CONCAT(self.maps)       or "",
       self.influences and CONCAT(self.influences) or "")


class Influence(Cal3DObject):
  def __init__(self, bone, weight):
    Cal3DObject.__init__(self)
    self.bone           = bone
    self.weight         = weight
    
  def XML(self): return """###<INFLUENCE ID="%s">%s</INFLUENCE>\n""" % (self.bone.id, STRFLT(self.weight))

  
 
class Face(Cal3DObject):
  def __init__(self, submesh, v1, v2, v3):
    Cal3DObject.__init__(self)
    self.vertices = (v1, v2, v3)
    self.submesh  = submesh
    submesh.faces.append(self)
    
  def XML(self):
    return """##<FACE VERTEXID="%s %s %s"/>\n""" % (self.vertices[0].id, self.vertices[1].id, self.vertices[2].id)
  

class Skeleton(Cal3DObject):
  ARMATURE = None

  def __init__(self):
    Cal3DObject.__init__(self, "XSF")
    self.bones = []
  
  def XML(self):
    return """\
<SKELETON NUMBONES="%s">
%s</SKELETON>
""" % (len(self.bones), CONCAT(self.bones))


class Bone(Cal3DObject):
  BONES = {}

  def __init__(self, skeleton, parent, name, matrix):
    Cal3DObject.__init__(self)
    
    self.parent   = parent
    self.name     = name
    self.invert   = mathutils.Matrix(matrix).inverted()
    if not parent: self.local  = matrix
    else:          self.local  = matrix_multiply(matrix, parent.invert)
    self.children = []
    self.skeleton = skeleton
    self.id       = len(skeleton.bones)
    
    if self.parent: self.parent.children.append(self)
    skeleton.bones.append(self)
    Bone.BONES[self.name] = self
    
  def XML(self):
    # TRANSLATION and ROTATION are relative to the parent bone.
    # They are virtually useless since the animations (.XAF .CAF)
    # will always override them.
    #
    # LOCALTRANSLATION and LOCALROTATION are the invert of the cumulated
    # TRANSLATION and ROTATION (see above). It is used to calculate the
    # delta between an animated bone and the original non animated bone.
    # This delta will be applied to the influenced vertexes.
    #
    # Negate the rotation because blender rotations are clockwise
    # and cal3d rotations are counterclockwise
    
    local     = MATRIX2GL(self.local)
    local     = local * SCALE
    localloc  = local.to_translation()
    localrot  = local.to_quaternion()
    
    invert    = MATRIX2GL(self.invert)
    invertloc = invert.to_translation()
    invertloc = invertloc * SCALE
    invertrot = invert.to_quaternion()
    
    return """\
#<BONE ID="%s" NAME="%s" NUMCHILD="%s">
##<TRANSLATION>%s %s %s</TRANSLATION>
##<ROTATION>%s %s %s %s</ROTATION>
##<LOCALTRANSLATION>%s %s %s</LOCALTRANSLATION>
##<LOCALROTATION>%s %s %s %s</LOCALROTATION>
##<PARENTID>%s</PARENTID>
%s#</BONE>
""" % (self.id, self.name, len(self.children),
       STRFLT(localloc.x), STRFLT(localloc.y), STRFLT(localloc.z),
       STRFLT(localrot.x), STRFLT(localrot.y), STRFLT(localrot.z), STRFLT(-localrot.w),
       STRFLT(invertloc.x), STRFLT(invertloc.y), STRFLT(invertloc.z),
       STRFLT(invertrot.x), STRFLT(invertrot.y), STRFLT(invertrot.z), STRFLT(-invertrot.w),
       self.parent and "%d" % self.parent.id or "-1",
       "".join(["##<CHILDID>%s</CHILDID>\n" % c.id for c in self.children]))


class Animation(Cal3DObject):
  def __init__(self, name, duration = 1.0):
    Cal3DObject.__init__(self, "XAF")
    self.name     = name.replace(".", "_")
    self.duration = duration
    self.tracks   = {}
  
  def XML(self):
    return """\
<ANIMATION DURATION="%s" NUMTRACKS="%s">
%s</ANIMATION>
""" % (self.duration or 1.0, len(self.tracks), CONCAT(self.tracks.values()))

    
class Track(Cal3DObject):
  def __init__(self, animation, bone):
    Cal3DObject.__init__(self)
    
    self.bone      = bone
    self.keyframes = []
    self.animation = animation
    
    animation.tracks[bone.name] = self
    
  def XML(self):
    return """\
#<TRACK BONEID="%s" NUMKEYFRAMES="%s"> <!-- Bone name %s -->
%s#</TRACK>
""" % (self.bone.id, len(self.keyframes), self.bone.name, CONCAT(self.keyframes))


class KeyFrame(Cal3DObject):
  def __init__(self, track, time, loc, rot):
    Cal3DObject.__init__(self)
  
    self.time  = time
    self.loc   = mathutils.Vector(loc)
    self.rot   = mathutils.Quaternion(rot)
    self.track = track
    
    track.keyframes.append(self)
    
  def XML(self):
    self.loc *= SCALE
    
    return """\
##<KEYFRAME TIME="%s">
###<TRANSLATION>%s %s %s</TRANSLATION>
###<ROTATION>%s %s %s %s</ROTATION>
##</KEYFRAME>
""" % (STRFLT(self.time),
       STRFLT(self.loc.x), STRFLT(self.loc.y), STRFLT(self.loc.z),
       STRFLT(self.rot.x), STRFLT(self.rot.y), STRFLT(self.rot.z), STRFLT(-self.rot.w))





def skeleton_data():
  # This function returns a single Skeleton instance
  # and sets Skeleton.ARMATURE to the appropriate Blender
  # object. For the time being we ony support a single skeleton (although, this
  # could be changed later), so it only makes sense to return a single Skeleton.
  # The ARMATURE variable is set for use later in retrieving the animations
  # tied to the Armature.

  skeleton = Skeleton()

  # A recursive function that operates on a single root bone and creates
  # Bone instances appropriately. It might be possible to totally
  # get rid of this function and just use bone.getAllChildren() instead.
  def recurse_bone(bone, matrix, parent = None):
    bone_matrix = matrix_multiply(bone.matrix_local, matrix)
    cbone = Bone(skeleton, parent, bone.name.replace(".", "_"), bone_matrix)
    for c in bone.children: recurse_bone(c, matrix, cbone)
    
  for obj in bpy.data.objects:
    if (obj.type != "ARMATURE") or obj.name.startswith("_"): continue
    rootbones = [b for b in obj.data.bones if b.parent is None]
    for rootbone in rootbones: recurse_bone(rootbone, obj.matrix_world)
    
    # Set the ARMATURE variable for use later in Animations.
    Skeleton.ARMATURE = obj
    
  return skeleton


def mesh_data():
  # This function returns a list of Mesh objects, one for
  # each mesh in your Blender scene. The Cal3D notion of a Mesh is actually more
  # like a container whose purpose it is to hold other SubMeshes, which are
  # what hold the vertex, weight, and material data. As it is now, there is always
  # one Mesh+SubMesh combo per item in the list, though it would also be possible
  # to have all meshes in the scene be SubMeshes of a single Mesh returned
  # by this function.

  meshes = []

  # This class serves as a kind of "temporary" vertex class that we will use
  # to create both the vertex list and the index list for later iteration. The
  # only reason we have to do this is due to the fact that Blender doesn't
  # pre-sanitize vertex data such that each vertex is TRULY unique, i.e. in 
  # location, normal, and UV coords.
  #
  # TODO: There are special methods (__hash__, __cmp__, and __eq__) we could
  # use instead for implicit comparison rather than having to call MakeKey()
  # directly. I'll need to research that a bit...

  
  class HashableVertex(object):
    def __init__(self, obj_mesh, face, vertex_ids, i):
      self.obj_mesh   = obj_mesh
      self.face       = face
      self.vertex_ids = vertex_ids
      self.vertex_id  = face.vertices[i]
      self.v          = obj_mesh.vertices[self.vertex_id]
      self.co         = self.v.co
      self.normal     = self.v.normal
      self.index      = i
      #self.reference_vertices   = {}
      self.reference_vertices   = defaultdict(lambda :  self )
      self.referenced_verticess = defaultdict(lambda : {self})
      # For unknown reason, defaultdict behaves differently ???
      #self.reference_vertices   = { "loc" :  self , "locnorm" :  self , "locnormuv" :  self  }
      #self.referenced_verticess = { "loc" : {self}, "locnorm" : {self}, "locnormuv" : {self} }
      
      if len(obj_mesh.tessface_uv_textures) > 0:
        tessface_uv_texture = obj_mesh.tessface_uv_textures[0].data[face.index]
        self.uv = list(getattr(tessface_uv_texture, "uv%s" % (i + 1)))
      else:
        self.uv = 0.0, 0.0
        
    def hash_location(self): return self.vertex_id
    def hash_all     (self): return self.vertex_id, self.uv[0], self.uv[1]

    # def set_reference_vertex(self, category, ivertex):
    #   self.reference_vertices[category] = ivertex
    #   ivertex.referenced_verticess[category].append(self)
      
    #   if self.referenced_verticess[category]:
    #     for vertex in self.referenced_verticess[category]:
    #       if not vertex is self: vertex.set_reference_vertex(category, ivertex)
    #     del self.referenced_verticess[category]
        
    def is_reference_vertex    (self, category): return self is self.reference_vertices[category]
    def get_reference_vertex   (self, category): return self.reference_vertices[category]
    def get_referenced_vertices(self, category): return self.referenced_verticess[category]
    def set_reference_vertex   (self, category, reference_vertex):
      assert reference_vertex.is_reference_vertex(category)
      self.reference_vertices[category].referenced_verticess[category].discard(self)
      self.reference_vertices[category] = reference_vertex
      reference_vertex.referenced_verticess[category].add(self)
      
      for vertex in frozenset(self.referenced_verticess[category]):
        if not vertex is self: vertex.set_reference_vertex(category, reference_vertex)
        
    def angle_at(self):
      index = self.vertex_ids.index(self.vertex_id)
      if index < 3: vertex_ids = self.vertex_ids[:3]
      else:         vertex_ids = self.vertex_ids[3:]; index = index - 3
      a = self.obj_mesh.vertices[vertex_ids[(index + 1) % 3]]
      b = self.obj_mesh.vertices[vertex_ids[ index - 1     ]]
      vec1 = mathutils.Vector([a.co[0] - self.co[0], a.co[1] - self.co[1], a.co[2] - self.co[2]])
      vec2 = mathutils.Vector([b.co[0] - self.co[0], b.co[1] - self.co[1], b.co[2] - self.co[2]])
      return vector_angle(vec1, vec2)
    
  # A function to split our faces into triangles and convert the vertices into our HashableVert class.
  def tri_faces(obj_mesh, face):
    if len(face.vertices) == 4: indices = [0, 1, 2, 2, 3, 0]
    else:                       indices = [0, 1, 2]
    vertex_ids = [face.vertices[i] for i in indices]
    return [HashableVertex(obj_mesh, face, vertex_ids, i) for i in indices]
  
  
  def get_face_mapnames(obj_mesh, face):
    mapnames = []
    for uv_texture in obj_mesh.tessface_uv_textures:
      tessface_uv_texture = uv_texture.data[face.index]
      if tessface_uv_texture.image:
        mapnames.append(tessface_uv_texture.image.name)
    return mapnames
    #if "." in material_filename: material_filename = material_filename[:material_filename.find(".")]
  
  _MATERIALS = {}
  def get_face_material(obj_mesh, face):
    mapnames = get_face_mapnames(obj_mesh, face)
    if obj_mesh.materials:
      blender_material      = obj_mesh.materials[face.material_index]
      blender_material_name = blender_material.name
    else:
      blender_material      = None
      blender_material_name = "Default"
    material = _MATERIALS.get((blender_material_name, frozenset(mapnames)))
    if not material:
      material = _MATERIALS[blender_material_name, frozenset(mapnames)] = Material(
        "_".join([blender_material_name] + mapnames),
        mapnames = mapnames)
      if blender_material:
        material.diffuse   = [blender_material.diffuse_color [0] * 255, blender_material.diffuse_color [1] * 255, blender_material.diffuse_color [2] * 255, blender_material.alpha          * 255]
        material.specular  = [blender_material.specular_color[0] * 255, blender_material.specular_color[1] * 255, blender_material.specular_color[2] * 255, blender_material.specular_alpha * 255]
        material.shininess = blender_material.specular_intensity
    return material
  

  def create_vertices(obj_mesh, material):
    vertices = []
    for face in obj_mesh.tessfaces:
      if not get_face_material(obj_mesh, face) is material: continue
      vertices.extend(tri_faces(obj_mesh, face))
    print ("* blender2cal3d * Found %s vertices" % len(vertices))
    
    loc_reference_vertices = {}
    for v in vertices:
      v.set_reference_vertex("loc", loc_reference_vertices.setdefault(v.hash_location(), v))
    loc_reference_vertices = [v for v in vertices if v.is_reference_vertex("loc")]
    print ("* blender2cal3d * Found %s loc reference vertices" % len(loc_reference_vertices))

    
    for loc_reference_vertex in loc_reference_vertices:
      pairs = []
      for v1, v2 in combinations(loc_reference_vertex.get_referenced_vertices("loc"), 2):
        angle = vector_angle(v1.face.normal, v2.face.normal)
        if angle != 0.0 and not(v1.face.use_smooth or v2.face.use_smooth): angle = 360.0
        pairs.append((angle, v1, v2))
      pairs.sort(key = lambda pair: pair[0])
      
      for angle, v1, v2 in pairs:
        if angle > MAX_FACE_ANGLE: break
        v2.set_reference_vertex("locnorm", v1.get_reference_vertex("locnorm"))
        
    locnorm_reference_vertices = [v for v in vertices if v.is_reference_vertex("locnorm")]
    print ("* blender2cal3d * Found %s loc+norm reference vertices" % len(locnorm_reference_vertices))

    
    for reference_vertex in locnorm_reference_vertices:
      normal = [0.0, 0.0, 0.0]
      for vertex in reference_vertex.get_referenced_vertices("locnorm"):
        angle = vertex.angle_at()
        normal = [normal[0] + angle * vertex.face.normal[0],
                  normal[1] + angle * vertex.face.normal[1],
                  normal[2] + angle * vertex.face.normal[2]]
      normal = mathutils.Vector(normal)
      normal.normalize()
      for vertex in reference_vertex.get_referenced_vertices("locnorm"):
        vertex.normal = reference_vertex.normal


    for reference_vertex in locnorm_reference_vertices:
      locnormuv_verticess = []
      for v in reference_vertex.get_referenced_vertices("locnorm"):
        for locnormuv_vertices in locnormuv_verticess:
          uv2 = locnormuv_vertices[0].uv
          if abs(v.uv[0] - uv2[0]) + abs(v.uv[1] - uv2[1]) < 0.05:
            locnormuv_vertices.append(v)
            break
        else:
          locnormuv_verticess.append([v])
          
      for locnormuv_vertices in locnormuv_verticess:
        locnormuv_vertices = list(locnormuv_vertices)
        for v in locnormuv_vertices:
          if v.is_reference_vertex("locnorm"):
            locnormuv_reference_vertex = v
            break
        else: locnormuv_reference_vertex = locnormuv_vertices[0]
        for v in locnormuv_vertices:
          v.set_reference_vertex("locnormuv", locnormuv_reference_vertex)
          
    locnormuv_reference_vertices = [v for v in vertices if v.is_reference_vertex("locnormuv")]
    
    
    print ("* blender2cal3d * Found %s loc+norm+uv reference vertices" % len(locnormuv_reference_vertices))
    
    return vertices, loc_reference_vertices, locnorm_reference_vertices, locnormuv_reference_vertices
  

  def create_sub_meshes(mesh, obj):
    #obj_mesh = obj.data
    #obj_mesh.update(1, 1)
    
    # Hide Armature's modifiers, because the deformation caused by animation and armature will be added later
    for modifier in obj.modifiers:
      if modifier.type == "ARMATURE": modifier.show_viewport = False
      
    obj_mesh = obj.to_mesh(bpy.context.scene, True, "PREVIEW")
    obj_mesh.update(1, 1)
    
    obj_mesh.transform(obj.matrix_world)
          
    materials = list(set(get_face_material(obj_mesh, face) for face in obj_mesh.tessfaces))
    
    for material in materials:
      submesh = SubMesh(mesh, material)
      
      hashable_vertices, loc_reference_vertices, locnorm_reference_vertices, locnormuv_reference_vertices = create_vertices(obj_mesh, material)
      
      vertices = []
      for v in locnormuv_reference_vertices:
        vertices.append(Vertex(submesh, v))
        
      faces = []
      for v1, v2, v3 in zip(*[iter(hashable_vertices)] * 3):
        faces.append(Face(submesh, v1.get_reference_vertex("locnormuv").cal3d_vertex, v2.get_reference_vertex("locnormuv").cal3d_vertex, v3.get_reference_vertex("locnormuv").cal3d_vertex))
      
      
      for v in locnormuv_reference_vertices:
        total_weight0 = sum(group.weight ** INFLUENCE_POWER for group in v.v.groups)
        total_weight = 0.0
        groups       = []
        
        for group in v.v.groups:
          weight = (group.weight ** INFLUENCE_POWER) / total_weight0
          if weight >= MIN_INFLUENCE:
            total_weight += (group.weight ** INFLUENCE_POWER)
            groups.append(group)
            
        for group in groups:
          bone_name = obj.vertex_groups[group.group].name.replace(".", "_")
          weight = (group.weight ** INFLUENCE_POWER) / total_weight
          
          v.cal3d_vertex.influences.append(Influence(Bone.BONES[bone_name], weight))
          
      if LOD: submesh.LOD()
      
      
  for obj in bpy.data.objects:
    if (obj.type == "MESH") and (len(obj.data.polygons) > 0):
      mesh = Mesh(obj.name)
      meshes.append(mesh)
      create_sub_meshes(mesh, obj)
    
  return meshes


def animation_data():
  animations = []
  
  for obj_armature in bpy.data.objects:
    if obj_armature.type == "ARMATURE": break
    
  for action in bpy.data.actions:
    animation = Animation(action.name)
    animations.append(animation)
    
    obj_armature.animation_data.action = action
    bpy.context.scene.update()
    
    frames = sorted(list(set([keyframe_point.co[0] for fcurve in action.fcurves for keyframe_point in fcurve.keyframe_points])))
    if not frames: continue
    
    bone_2_track       = {}
    animation.duration = (frames[-1] / ANIMFPS)
    
    for frame in frames:
      bpy.context.scene.frame_set(frame)
      
      for pose_bone in obj_armature.pose.bones:
        bone_name = pose_bone.bone.name.replace(".", "_")
        bone      = Bone.BONES[bone_name]
        matrix    = pose_bone.matrix_basis
        matrix    = matrix_multiply(matrix, bone.local)
        matrix    = MATRIX2GL(matrix)
            
          
        track = bone_2_track.get(bone)
        if not track: track = bone_2_track[bone] = Track(animation, bone)
        KeyFrame(track, frame / ANIMFPS, matrix.to_translation(), matrix.to_quaternion())
        
  return animations



def cal3D_export(filename, prefix = ""):
  # Reset globals, in case the script is executed multiple times from the gui
  Material.MATERIALS = {}
  Skeleton.ARMATURE  = None
  Bone    .BONES     = {}
  
  if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode = "OBJECT") # Close edit mode (required, else some Blender data are not available).
    
  if LOD_LOW != -1:
    if   QUALITY == 0: subsurf_level = LOD_LOW
    elif QUALITY == 1: subsurf_level = LOD_MEDIUM
    else:              subsurf_level = LOD_HIGH
    for obj in bpy.data.objects:
      for mod in obj.modifiers:
        if mod.type == "SUBSURF": mod.levels = subsurf_level
        
  skeldata = skeleton_data()
  meshdata = mesh_data()
  animdata = animation_data()
  
  dirname  = os.path.dirname(filename)
  basename = os.path.splitext(os.path.basename(filename))[0]
  
  if LOD_LOW != -1:
    try: os.makedirs(dirname)
    except OSError as e: pass
    
    cfg = open(os.path.join(dirname, "%s.cfg" % basename), "w")
    cfg.write("LOD")
    cfg.close()
    
    if   QUALITY == 0: dirname  = os.path.join(dirname, "low")
    elif QUALITY == 1: dirname  = os.path.join(dirname, "medium")
    else:              dirname  = os.path.join(dirname, "high")
    
  try: os.makedirs(dirname)
  except OSError as e: pass

  cfg = open(os.path.join(dirname, "%s.cfg" % basename), "w")
  
  cfg.write("# Cal3D model exported from Blender with blender2cal3d.py\n")
  cfg.write("skeleton=%s.xsf\n" % basename)
  with open(os.path.join(dirname, "%s.xsf" % basename), "w") as f:
    f.write(skeldata.XML())
  
  for animation in animdata:
    if not animation.name.startswith("_"):
      animfile = "%s%s.xaf" % (prefix, animation.name)
      with open(os.path.join(dirname, animfile), "w") as f:
        f.write(animation.XML())
      cfg.write("animation=%s\n" % animfile)
      
  for mesh in meshdata:
    if not mesh.name.startswith("_"):
      meshfile = "%s%s.xmf" % (prefix, mesh.name)
      with open(os.path.join(dirname, meshfile), "w") as f:
        f.write(mesh.XML())
      cfg.write("mesh=%s\n" % meshfile)
      
  materials = list(Material.MATERIALS.values())
  materials.sort(key = lambda o: o.id)
  
  for material in materials:
    matfile = "%s.xrf" % material.name
    with open(os.path.join(dirname, matfile), "w") as f:
      xml = material.XML()
      if MATERIAL_MAP:
        for old, new in MATERIAL_MAP.items(): xml = xml.replace(old, new)
      f.write(xml)
    cfg.write("material=%s\n" % matfile)
    
  if ADDITIONAL_CFG: cfg.write("\n%s" % ADDITIONAL_CFG)
      

if __name__ == "__main__":
  parse_buffer("soya_params")
  parse_args(sys.argv[sys.argv.index("-P") + 3:])
  #if sys.argv[-1] != "-": parse_buffer(sys.argv[-1])
  
  cal3D_export(FILENAME)
  
  bpy.ops.wm.quit_blender()

