
from __future__ import print_function
import crayola as color
import materials
import numpy as np
from rate_control import *
from IPython.display import HTML
from IPython.display import display, display_html, display_javascript
from IPython.display import Javascript
from IPython.kernel.comm import Comm
from IPython.core.getipython import get_ipython
import time
import math
from time import clock
import os
import IPython.html.nbextensions

ifunc = simulateDelay(delayAvg=0.001)
rate = RateKeeper(interactFunc=ifunc)

display(HTML("""<div id="scene"><div id="glowscript" class="glowscript"></div></div>"""))

package_dir = os.path.dirname(__file__)
IPython.html.nbextensions.install_nbextension(files=[package_dir+"/data/glow.1.0.min.js",package_dir+"/data/glowcomm.js"],overwrite=True,verbose=0)

class baseObj(object):
    txtime = 0.0
    idx = 0
    qSize = 500            # default to 500
    qTime = 0.034          # default to 0.05
    glow = None
    cmds = []
    objCnt = 0
    
    def __init__(self):
        object.__setattr__(self, 'idx', baseObj.objCnt)
        baseObj.incrObjCnt()
        if(idisplay.get_selected() != None):
            idisplay.get_selected().objects.append(self)
        
    def delete(self):
        baseObj.decrObjCnt()
        cmd = {"cmd": "delete", "idx": self.idx}
        baseObj.cmds.append(cmd)
        baseObj.checksend()

    def appendcmd(self,cmd):
        baseObj.cmds.append(cmd)

    @classmethod
    def incrObjCnt(cls):
        cls.objCnt += 1

    @classmethod
    def decrObjCnt(cls):
        cls.objCnt -= 1
        
    @classmethod
    def checksend(cls):
        if ((len(cls.cmds) >= cls.qSize) or (clock() - cls.txtime > cls.qTime)) and (cls.glow != None):
            if (len(cls.cmds) > 0):
                cls.glow.comm.send(cls.cmds)
            cls.cmds = []
            cls.txtime = clock()

    @classmethod
    def qflush(cls):
        if (len(cls.cmds) > 0):
            cls.glow.comm.send(cls.cmds)
        cls.cmds = []
        cls.txtime = clock()

        
class GlowWidget(object):
    
    def __init__(self, comm, msg):
        self.comm = comm
        self.comm.on_msg(self.handle_msg)
        self.comm.on_close(self.handle_close)
        baseObj.glow = self

    
    def handle_msg(self, data):
        baseObj.checksend()
        #self.comm.send([{'cmd': 'heartbeat'}])

    def handle_close(self, data):
        print ("Comm closed")

    def get_execution_count(self):
        return get_ipython().execution_count


get_ipython().comm_manager.register_target('glow', GlowWidget)
#display(Javascript("""console.log("About to call require.undef for glowcom and glow.1.0.min");"""))
display(Javascript("""require.undef("nbextensions/glow.1.0.min");"""))
display(Javascript("""require.undef("nbextensions/glowcomm");"""))
#display(Javascript("""console.log("About to call require for glowcom");"""))
display(Javascript("""require(["nbextensions/glowcomm"], function(){console.log("glowcomm loaded");})"""))

class vector(object):
    'vector class'
    def __init__(self, x = (0.,0.,0.), y = 0., z = 0.):
        if isinstance(x, (int, long, float, complex)):
            self.__dict__['x'] = x
            self.__dict__['y'] = y
            self.__dict__['z'] = z
        else:
            self.__dict__['x'] = x[0]
            self.__dict__['y'] = x[1]
            self.__dict__['z'] = x[2]
        #self.x = x[0] if type(x) is tuple else x[0] if type(x) is list else x[0] if type(x) is np.ndarray else x
        #self.y = x[1] if type(x) is tuple else x[1] if type(x) is list else x[1] if type(x) is np.ndarray else y
        #self.z = x[2] if type(x) is tuple else x[2] if type(x) is list else x[2] if type(x) is np.ndarray else z
        self.__dict__['shape'] = (3L,)
        
    def __str__(self):
        return 'vector (%f, %f, %f)' % (self.x, self.y, self.z)
   
    def __array__(self, dtypes=[None]):
        return np.array((self.x, self.y, self.z), dtype=dtypes[0])

    def __add__(self,other):
        if type(other) is np.ndarray:
            return vector(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            return vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self,other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, (int, long, float, complex)):
            return vector(self.x * other, self.y * other, self.z * other)
        return self
    
    def __rmul__(self, other):
        if isinstance(other, (int, long, float, complex)):
            return vector(self.x * other, self.y * other, self.z * other)
        return self

    def __div__(self, other):
        if isinstance(other, (int, long, float, complex)):
            return vector(self.x / other, self.y / other, self.z / other)
        return self
    
    def __truediv__(self, other):
        if isinstance(other, (int, long, float, complex)):
            return vector(self.x / other, self.y / other, self.z / other)
        return self

    def __neg__(self):
        return vector(-1.*self.x, -1.*self.y, -1.*self.z)

    def __getitem__(self,key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            return

    def __setitem__(self,key,value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value

    def mag(self):
        return np.linalg.norm(np.array([self.x,self.y,self.z]))

    def mag2(self):
        return self.mag()*self.mag()

    def norm(self):
        return self / self.mag()

    def dot(self,other):
        if type(other) is np.ndarray:
            return np.dot(np.array([self.x,self.y,self.z]),other)
        else:
            return np.dot(np.array([self.x,self.y,self.z]),np.array([other.x,other.y,other.z]))

    def cross(self,other):
        if type(other) is np.ndarray:
            return vector(np.cross(np.array([self.x,self.y,self.z]),other))
        elif (type(other) is tuple) or (type(other) is list):
            return vector(np.cross(np.array([self.x,self.y,self.z]),np.array(other)))
        else:
            return vector(np.cross(np.array([self.x,self.y,self.z]),np.array([other.x,other.y,other.z])))

    def proj(self,other):
        normB = other.norm()
        return self.dot(normB) * normB

    def comp(self,other):
        normB = other.norm()
        return self.dot(normB) * normB

    def diff_angle(self, other):
        angle = np.arccos(np.clip(self.norm().dot(other.norm()),-1.,1.))
        return angle

    def rotate(self,angle=0.,axis=(0,0,1)):
        if type(axis) is np.ndarray:
            axis = axis/math.sqrt(np.dot(axis,axis))
        elif (type(axis) is tuple) or (type(axis) is list):
            axis = np.array(axis)
            axis = axis/math.sqrt(np.dot(axis,axis))
        else:
            axis = axis/math.sqrt(axis.dot(axis))
            axis = np.array([axis.x,axis.y,axis.z])
            
        a = math.cos(angle/2)
        b,c,d = -axis*math.sin(angle/2)
        mat = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                         [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                         [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])
        v = np.array([self.x,self.y,self.z])
        res = np.dot(mat,v)
        self.x = res[0]
        self.y = res[1]
        self.z = res[2]
    
    def astuple(self):
        return (self.x,self.y,self.z)
  
    def keys(self):
        return [0,1,2]
    
    def values(self):
        return [self.x,self.y,self.z]

    def __setattr__(self, name, value):
        if name in ['mag','mag2']:
            normA = self.norm()
            if name == 'mag':
                self.__dict__['x'] = value * normA.x
                self.__dict__['y'] = value * normA.y
                self.__dict__['z'] = value * normA.z
            elif name == 'mag2':
                self.__dict__['x'] = math.sqrt(value) * normA.x
                self.__dict__['y'] = math.sqrt(value) * normA.y
                self.__dict__['z'] = math.sqrt(value) * normA.z
        elif name in ['x','y','z']:
            self.__dict__[name] = value
        
            
def mag(A):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).mag()
    else:
        return A.mag()
    
def mag2(A):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).mag2()
    else:
        return A.mag2()

def norm(A):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).norm()
    else:
        return A.norm()

def dot(A,B):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).dot(B)
    else:
        return A.dot(B)

def cross(A,B):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).cross(B)
    else:
        return A.cross(B)

def proj(A,B):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).proj(B)
    else:
        return A.proj(B)

def comp(A,B):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).comp(B)
    else:
        return A.comp(B)

def diff_angle(A,B):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).diff_angle(B)
    else:
        return A.diff_angle(B)

def rotate(A,angle=0.,axis=(0,0,1)):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).rotate(angle,axis)
    else:
        return A.rotate(angle,axis)

def astuple(A):
    if (type(A) is np.ndarray) or (type(A) is tuple) or (type(A) is list):
        return vector(A).astuple()
    else:
        return A.astuple()

def array(arr_obj, dtype=None, copy=True, order=None, subok=False, ndmin=0):
  return np.array(arr_obj,dtype,copy,order,subok,ndmin)

class baseAttrs(baseObj):
    pos = vector(0.,0.,0.)
    x = 0.
    y = 0.
    z = 0.
    size = vector(1.,1.,1.)
    axis = vector(1.,0.,0.)
    up = vector(0.,1.,0.)
    red = 1.
    green = 1.
    blue = 1.
    visible = False
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., frame = None, display = None):
        super(baseAttrs, self).__init__()
        if (x != 0.) or (y != 0.) or (z != 0.):
            pos = vector(x,y,z) if type(pos) is tuple else pos
        else:
            x = pos[0]
            y = pos[1]
            z = pos[2]
        if (red != 1.) or (green != 1.) or (blue != 1.):
            color = (red,green,blue)
        else:
            red = color[0]
            green = color[1]
            blue = color[2]
        
        object.__setattr__(self, 'pos', vector(pos) if type(pos) is tuple else pos )
        object.__setattr__(self, 'x', x)
        object.__setattr__(self, 'y', y)
        object.__setattr__(self, 'z', z)        
        object.__setattr__(self, 'axis', vector(axis) if type(axis) is tuple else axis)
        object.__setattr__(self, 'size', vector(size) if type(size) is tuple else size)
        object.__setattr__(self, 'up', vector(up) if type(up) is tuple else up)
        object.__setattr__(self, 'color', color)
        object.__setattr__(self, 'red', red)
        object.__setattr__(self, 'green', green)
        object.__setattr__(self, 'blue', blue)        
        object.__setattr__(self, 'visible', True)
        object.__setattr__(self, 'display', display)
        object.__setattr__(self, 'frame', frame)

    def __setattr__(self, name, value):
        # print('attribute : ', name,' value changed to ',value)
        if name in ['pos','size','axis','up','visible','x','y','z','red','green','blue']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
            cmd = {}
            if name == 'x':
                self.__dict__['pos'][0] = value
                cmd = {"idx": self.idx, "attr": "pos", "val": self.pos.values()}            
            elif name == 'y':
                self.__dict__['pos'][1] = value
                cmd = {"idx": self.idx, "attr": "pos", "val": self.pos.values()}            
            elif name == 'z':
                self.__dict__['pos'][2] = value
                cmd = {"idx": self.idx, "attr": "pos", "val": self.pos.values()}            
            elif name == 'pos':
                self.__dict__['x'] = value[0]
                self.__dict__['y'] = value[1]
                self.__dict__['z'] = value[2]
                cmd = {"idx": self.idx, "attr": name, "val": self.pos.values()}            
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
            elif name == 'size':
                cmd = {"idx": self.idx, "attr": name, "val": self.size.values()}            
            elif name == 'up':
                cmd = {"idx": self.idx, "attr": name, "val": self.up.values()}            
            elif name == 'visible':
                cmd = {"idx": self.idx, "attr": name, "val": self.visible}            
            elif name == 'red':
                self.__dict__['color'] = (self.red,self.green,self.blue)
                cmd = {"idx": self.idx, "attr": "color", "val": list(self.color)}            
            elif name == 'green':
                self.__dict__['color'] = (self.red,self.green,self.blue)
                cmd = {"idx": self.idx, "attr": "color", "val": list(self.color)}            
            elif name == 'blue':
                self.__dict__['color'] = (self.red,self.green,self.blue)
                cmd = {"idx": self.idx, "attr": "color", "val": list(self.color)} 
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
        elif name == 'color':
            self.__dict__[name] = value
            self.__dict__['red'] = value[0]
            self.__dict__['green'] = value[1]
            self.__dict__['blue'] = value[2]
            cmd = {"idx": self.idx, "attr": name, "val": list(self.color)}            
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
                
        else:
            super(baseAttrs, self).__setattr__(name, value)

    def rotate(self, angle=math.pi/4, axis=axis, origin=pos):
        axis = vector(axis) if type(axis) is tuple else axis
        origin = vector(origin) if type(origin) is tuple else origin
        cmd = {"cmd": "rotate", "idx": self.idx,
               "attrs": [{"attr": "pos", "value": origin.values()},
                        {"attr": "axis", "value": axis.values()},
                        {"attr": "angle", "value": angle}]}
        baseObj.cmds.append(cmd)
        baseObj.checksend()

        
class baseAttrs2(baseAttrs):
    texture = None
    opacity = 1.0
    shininess = 0.6
    emissive = False
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., frame = None, display = None, material = None,
                 opacity = 1.0):
        super(baseAttrs2, self).__init__(pos=pos,axis=axis,size=size,up=up,color=color,red=red,green=green,blue=blue,x=x,y=y,z=z,frame=frame,display=display)
        object.__setattr__(self, 'texture', None )
        object.__setattr__(self, 'opacity', opacity )
        object.__setattr__(self, 'shininess', 0.6)
        object.__setattr__(self, 'emissive', False)
        if (material != None):
            if (material == materials.emissive):
                object.__setattr__(self, 'emissive', True)
            elif (material == materials.plastic):
                object.__setattr__(self, 'emissive', False)
            else:
                pass
        
    def __setattr__(self, name, value):
        if name in ['material','opacity']:
            if name == 'material':
                cmd = {}
                if (value == materials.emissive):
                    object.__setattr__(self, 'emissive', True)
                    cmd = {"idx": self.idx, "attr": 'emissive', "val": self.emissive}            
                elif (value == materials.plastic):
                    object.__setattr__(self, 'emissive', False)
                    cmd = {"idx": self.idx, "attr": 'emissive', "val": self.emissive}            
                else:
                    object.__setattr__(self, 'emissive', False)
                    cmd = {"idx": self.idx, "attr": 'emissive', "val": self.emissive}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'opacity':
                self.__dict__[name] = value
                cmd = {"idx": self.idx, "attr": name, "val": self.opacity}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
                
        else:
            super(baseAttrs2, self).__setattr__(name, value)
        
class trailAttrs(baseAttrs2):
    make_trail = False
    trail_type = "curve"
    interval = 10
    retain = 50
    trail_object = None
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., frame = None, display = None, material = None,
                 opacity = 1.0, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        super(trailAttrs, self).__init__(pos=pos,axis=axis,size=size,up=up,color=color,red=red,green=green,blue=blue,x=x,y=y,z=z,frame=frame,display=display)
        object.__setattr__(self, 'make_trail', make_trail )
        object.__setattr__(self, 'trail_type', trail_type )
        object.__setattr__(self, 'interval', interval)
        object.__setattr__(self, 'retain', retain)
        #object.__setattr__(self, 'trail_object', curve() if self.trail_type == "curve" else points())

    def __setattr__(self, name, value):
        if name in ['make_trail','trail_type','interval','retain']:
            self.__dict__[name] = value
            if name == 'make_trail':
                cmd = {"idx": self.idx, "attr": name, "val": self.make_trail}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'trail_type':
                cmd = {"idx": self.idx, "attr": name, "val": self.trail_type}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'interval':
                cmd = {"idx": self.idx, "attr": name, "val": self.interval}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'retain':
                cmd = {"idx": self.idx, "attr": name, "val": self.retain}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
                
        else:
            super(trailAttrs, self).__setattr__(name, value)
        

class box(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 length = 1., width = 1., height = 1., up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.,
                 frame = None, material = None, opacity = 1.0, display = None,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        sz = size
        if (length != 1.0) or (width != 1.0) or (height != 1.0):
            sz = vector(length,height,width) if type(size) is tuple else size
        else:
            length = size[0]
            height = size[1]
            width = size[2]
        super(box, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=sz, up=up,color=color,red=red,green=green,blue=blue,
                                  material=material,opacity=opacity,frame=frame,display=display,
                                  make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'width', width)
        object.__setattr__(self, 'height', height)
        cmd = {"cmd": "box", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        """
        cmd = {"cmd": "box", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "texture", "value": self.texture},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive}]}
        """
        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','width','height','size']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'height':
                self.__dict__['size'][1] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'width':
                self.__dict__['size'][2] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'size':
                self.__dict__['length'] = value[0]
                self.__dict__['height'] = value[1]
                self.__dict__['width'] = value[2]
                cmd = {"idx": self.idx, "attr": name, "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
                
        else:
            super(box, self).__setattr__(name, value)


class cone(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), length = -1., radius = 1.,
                 frame = None, up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None, opacity = 1.0,
                 display = None, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (length == -1.0):
            length = axis[0]
        size = vector(length,radius*2,radius*2)
        super(cone, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                   material=material,opacity=opacity,frame=frame,display=display,
                                   make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'radius', radius)
        cmd = {"cmd": "cone", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','radius','axis']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'radius':
                self.__dict__['size'][1] = 2*value
                self.__dict__['size'][2] = 2*value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(cone, self).__setattr__(name, value)

class curve(baseAttrs2):
    xs = np.array([],float)
    ys = np.array([],float)
    zs = np.array([],float)
    def __init__(self, pos = [], x = [], y = [], z = [], axis = (1.,0.,0.), radius = 0., display = None,
                 up = (0.,1.,0.), color = [], red = [], green = [], blue = [], frame = None, material = None):
        posns = np.array(pos, dtype=('f4,f4,f4')) if type(pos) is list and (len(pos) == 0 or len(pos[0]) == 3) else np.array(pos, dtype=('f4,f4')) if type(pos) is list and len(pos[0]) == 2 else pos
        if len(posns) > 0:
            xs = posns['f0']
            ys = posns['f1']
            if(len(posns[0]) == 3):
                zs = posns['f2']
            else:
                zs = np.zeros(len(posns))
        elif (len(x) > 0) or (len(y) > 0) or (len(z) > 0):
            lsz = max(len(x),len(y),len(z))
            if len(x) < lsz:
                if len(x) > 0:
                    a = np.array(x, float) if type(x) is list or tuple else np.array([x], float) if type(x) is float or int else x
                    b = np.zeros(lsz-len(a))
                    x = np.concatenate(a,b)
                else:
                    x = np.zeros(lsz)
            if len(y) < lsz:
                if len(y) > 0:
                    a = np.array(y, float) if type(y) is list or tuple else np.array([y], float) if type(y) is float or int else y
                    b = np.zeros(lsz-len(a))
                    y = np.concatenate(a,b)
                else:
                    y = np.zeros(lsz)
            if len(z) < lsz:
                if len(z) > 0:
                    a = np.array(z, float) if type(z) is list or tuple else np.array([z], float) if type(z) is float or int else z
                    b = np.zeros(lsz-len(a))
                    z = np.concatenate(a,b)
                else:
                    z = np.zeros(lsz)
            posns = np.zeros(lsz, dtype=('f4,f4,f4'))
            posns['f0'] = x
            posns['f1'] = y
            posns['f2'] = z
        xs = np.array(x, float) if type(x) is list or tuple else np.array([x], float) if type(x) is float or int else x
        ys = np.array(y, float) if type(y) is list or tuple else np.array([y], float) if type(y) is float or int else y
        zs = np.array(z, float) if type(z) is list or tuple else np.array([z], float) if type(z) is float or int else z

        colors = np.array(color, dtype=('f4,f4,f4')) if type(color) is list else np.array([color], dtype=('f4,f4,f4')) if type(color) is tuple else color
        if len(colors) > 0:
            reds = colors['f0']
            greens = colors['f1']
            blues = colors['f2']
        elif (len(red) > 0) or (len(green) > 0) or (len(blue) > 0):
            lsz = max(len(red),len(green),len(blue))
            if len(red) < lsz:
                if len(red) > 0:
                    a = np.array(red, float) if type(red) is list or tuple else np.array([red], float) if type(red) is float or int else red
                    b = np.zeros(lsz-len(a))
                    red = np.concatenate(a,b)
                else:
                    red = np.zeros(lsz)
            if len(green) < lsz:
                if len(green) > 0:
                    a = np.array(green, float) if type(green) is list or tuple else np.array([green], float) if type(green) is float or int else green
                    b = np.zeros(lsz-len(a))
                    green = np.concatenate(a,b)
                else:
                    green = np.zeros(lsz)
            if len(blue) < lsz:
                if len(blue) > 0:
                    a = np.array(blue, float) if type(blue) is list or tuple else np.array([blue], float) if type(blue) is float or int else blue
                    b = np.zeros(lsz-len(a))
                    blue = np.concatenate(a,b)
                else:
                    blue = np.zeros(lsz)
            colors = np.zeros(lsz, dtype=('f4,f4,f4'))
            colors['f0'] = red
            colors['f1'] = green
            colors['f2'] = blue
        else:
            colors = np.ones(1, dtype=('f4,f4,f4'))
            reds = colors['f0']
            greens = colors['f1']
            blues = colors['f2']

        reds = np.array(red, float) if type(red) is list or tuple else np.array([red], float) if type(red) is float or int else red
        greens = np.array(green, float) if type(green) is list or tuple else np.array([green], float) if type(green) is float or int else green
        blues = np.array(blue, float) if type(blue) is list or tuple else np.array([blue], float) if type(blue) is float or int else blue
        
        points = []
        cols = []
        if len(posns) > 0:
            i = 0
            col = colors[-1]
            for posn in posns:
                col = colors[i] if len(colors) > i else colors[-1]
                if i >= len(colors):
                    cols.append(col)
                if (len(posn) == 3):
                    points.append({"pos": posn.tolist(), "color": col.tolist()})
                elif(len(posn) == 2):
                    p3 = list(posn)
                    p3.append(0.0)
                    p3a = np.array([tuple(p3)], dtype=('f4,f4,f4'))
                    points.append({"pos": p3a[0].tolist(), "color": col.tolist()})
                    
                i += 1
            if len(cols) > 0:
                colors = np.append(colors, np.array(cols, dtype=colors.dtype))

        super(curve, self).__init__(axis=axis, up=up, material=material, frame=frame, display=display)
        object.__setattr__(self, 'radius', radius)
        object.__setattr__(self, 'color', colors)
        object.__setattr__(self, 'pos', posns)
        object.__setattr__(self, 'x', xs)
        object.__setattr__(self, 'y', ys)
        object.__setattr__(self, 'z', zs)
        object.__setattr__(self, 'red', reds)
        object.__setattr__(self, 'green', greens)
        object.__setattr__(self, 'blue', blues)
        cmd = {"cmd": "curve", "idx": self.idx, 
               "attrs": [#{"attr": "pos", "value": self.pos.values()},
                         #{"attr": "axis", "value": self.axis.values()},
                         #{"attr": "size", "value": self.size.values()},
                         #{"attr": "up", "value": self.up.values()},
                         #{"attr": "color", "value": list(self.color)},
                         #{"attr": "shininess", "value": self.shininess},
                         #{"attr": "emissive", "value": self.emissive},
                         #{"attr": "points", "value": [{"pos": [0, 0, 0]}, {"pos": [1, 0, 0]}]},
                         #{"attr": "points", "value": pointsa.tolist()},
                         {"attr": "points", "value": points},
                         {"attr": "radius", "value": self.radius},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['pos','color','x','y','z','red','green','blue','radius','axis']:
        
            if name == 'radius':
                self.__dict__[name] = vector(value) if type(value) is tuple else value
                cmd = {"idx": self.idx, "attr": "radius", "val": self.radius}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'axis':
                self.__dict__[name] = vector(value) if type(value) is tuple else value
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'pos':
                self.__dict__[name] = np.array(value, dtype=('f4,f4,f4')) if type(value) is list and (len(value) == 0 or len(value[0]) == 3) else np.array(value, dtype=('f4,f4')) if type(value) is list and len(value[0]) == 2 else value
                self.__dict__['x'] = self.pos['f0']
                self.__dict__['y'] = self.pos['f1']
                if len(value[0]) == 3:
                    self.__dict__['z'] = self.pos['f2']
                    cmd = {"cmd": "modify", "idx": self.idx, 
                        "attrs":[{"attr": 'posns', "value": self.pos.tolist()}]}
                    baseObj.cmds.append(cmd)
                    baseObj.checksend()
                else:
                    posns = []
                    if len(self.pos) > 0:
                        for posn in self.pos:
                            p3 = list(posn)
                            p3.append(0.0)
                            posns.append(tuple(p3))
                        posns2 = np.array(posns, dtype=('f4,f4,f4'))
                        cmd = {"cmd": "modify", "idx": self.idx, 
                            "attrs":[{"attr": 'posns', "value": posns2.tolist()}]}
                        baseObj.cmds.append(cmd)
                        baseObj.checksend()
                    
            elif name == 'x':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f0'] = self.x
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.x.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'y':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f1'] = self.y
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.y.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'z':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f2'] = self.z
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.z.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'red':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f0'] = self.red
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.red.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'green':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f1'] = self.green
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.green.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'blue':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f2'] = self.blue
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.blue.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'color':
                self.__dict__[name] = np.array(value, dtype=('f4,f4,f4')) if type(value) is list and (len(value) == 0 or len(value[0]) == 3) else np.array(value, dtype=('f4,f4')) if type(value) is list and len(value[0]) == 2 else value
                self.__dict__['red'] = self.color['f0']
                self.__dict__['green'] = self.color['f1']
                self.__dict__['blue'] = self.color['f2']
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": 'colors', "value": self.color.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(curve, self).__setattr__(name, value)

    def append(self, pos = None, color = None, red = None, green = None, blue = None):

        if (red is not None) and (green is not None) and (blue is not None):
            color = (red,green,blue)

        if (pos is not None) and (color is not None):
            self.__dict__['pos'] = np.append(self.pos, np.array([pos], dtype=self.pos.dtype))
            self.__dict__['color'] = np.append(self.color, np.array([color], dtype=self.color.dtype))
            pos = list(pos)
            if len(pos) == 2:
                pos.append(0.0)
            cmd = {"cmd": "push", "idx": self.idx, 
                    "attrs":[{"attr": "pos", "value": pos},{"attr": "color", "value": list(color)}]}
            baseObj.cmds.append(cmd)
            baseObj.checksend()
        elif (pos is not None):
            self.__dict__['pos'] = np.append(self.pos, np.array([pos], dtype=self.pos.dtype))
            color = self.color[-1]
            self.__dict__['color'] = np.append(self.color, np.array([color], dtype=self.color.dtype))
            pos = list(pos)
            if len(pos) == 2:
                pos.append(0.0)
            cmd = {"cmd": "push", "idx": self.idx, 
                    "attrs":[{"attr": "pos", "value": pos},{"attr": "color", "value": self.color[-1].tolist()}]}
            baseObj.cmds.append(cmd)
            baseObj.checksend()

class faces(baseAttrs2):
    xs = np.array([],float)
    ys = np.array([],float)
    zs = np.array([],float)
    def __init__(self, pos = [], x = [], y = [], z = [], axis = (1.,0.,0.), radius = 0., display = None,
                 up = (0.,1.,0.), color = [], red = [], green = [], blue = [], normal = [], frame = None, material = None):
        posns = np.array(pos, dtype=('f4,f4,f4')) if type(pos) is list and (len(pos) == 0 or len(pos[0]) == 3) else np.array(pos, dtype=('f4,f4')) if type(pos) is list and len(pos[0]) == 2 else pos
        if len(posns) > 0:
            xs = posns['f0']
            ys = posns['f1']
            if(len(posns[0]) == 3):
                zs = posns['f2']
            else:
                zs = np.zeros(len(posns))
        elif (len(x) > 0) or (len(y) > 0) or (len(z) > 0):
            lsz = max(len(x),len(y),len(z))
            if len(x) < lsz:
                if len(x) > 0:
                    a = np.array(x, float) if type(x) is list or tuple else np.array([x], float) if type(x) is float or int else x
                    b = np.zeros(lsz-len(a))
                    x = np.concatenate(a,b)
                else:
                    x = np.zeros(lsz)
            if len(y) < lsz:
                if len(y) > 0:
                    a = np.array(y, float) if type(y) is list or tuple else np.array([y], float) if type(y) is float or int else y
                    b = np.zeros(lsz-len(a))
                    y = np.concatenate(a,b)
                else:
                    y = np.zeros(lsz)
            if len(z) < lsz:
                if len(z) > 0:
                    a = np.array(z, float) if type(z) is list or tuple else np.array([z], float) if type(z) is float or int else z
                    b = np.zeros(lsz-len(a))
                    z = np.concatenate(a,b)
                else:
                    z = np.zeros(lsz)
            posns = np.zeros(lsz, dtype=('f4,f4,f4'))
            posns['f0'] = x
            posns['f1'] = y
            posns['f2'] = z
        xs = np.array(x, float) if type(x) is list or tuple else np.array([x], float) if type(x) is float or int else x
        ys = np.array(y, float) if type(y) is list or tuple else np.array([y], float) if type(y) is float or int else y
        zs = np.array(z, float) if type(z) is list or tuple else np.array([z], float) if type(z) is float or int else z

        colors = np.array(color, dtype=('f4,f4,f4')) if type(color) is list else np.array([color], dtype=('f4,f4,f4')) if type(color) is tuple else color
        if len(colors) > 0:
            reds = colors['f0']
            greens = colors['f1']
            blues = colors['f2']
        elif (len(red) > 0) or (len(green) > 0) or (len(blue) > 0):
            lsz = max(len(red),len(green),len(blue))
            if len(red) < lsz:
                if len(red) > 0:
                    a = np.array(red, float) if type(red) is list or tuple else np.array([red], float) if type(red) is float or int else red
                    b = np.zeros(lsz-len(a))
                    red = np.concatenate(a,b)
                else:
                    red = np.zeros(lsz)
            if len(green) < lsz:
                if len(green) > 0:
                    a = np.array(green, float) if type(green) is list or tuple else np.array([green], float) if type(green) is float or int else green
                    b = np.zeros(lsz-len(a))
                    green = np.concatenate(a,b)
                else:
                    green = np.zeros(lsz)
            if len(blue) < lsz:
                if len(blue) > 0:
                    a = np.array(blue, float) if type(blue) is list or tuple else np.array([blue], float) if type(blue) is float or int else blue
                    b = np.zeros(lsz-len(a))
                    blue = np.concatenate(a,b)
                else:
                    blue = np.zeros(lsz)
            colors = np.zeros(lsz, dtype=('f4,f4,f4'))
            colors['f0'] = red
            colors['f1'] = green
            colors['f2'] = blue
        else:
            colors = np.ones(1, dtype=('f4,f4,f4'))
            reds = colors['f0']
            greens = colors['f1']
            blues = colors['f2']

        reds = np.array(red, float) if type(red) is list or tuple else np.array([red], float) if type(red) is float or int else red
        greens = np.array(green, float) if type(green) is list or tuple else np.array([green], float) if type(green) is float or int else green
        blues = np.array(blue, float) if type(blue) is list or tuple else np.array([blue], float) if type(blue) is float or int else blue

        normals = np.array(normal, dtype=('f4,f4,f4')) if type(normal) is list and (len(normal) == 0 or len(normal[0]) == 3) else np.array(normal, dtype=('f4,f4')) if type(normal) is list and len(normal[0]) == 2 else normal
        
        points = []
        cols = []
        if len(posns) > 0:
            i = 0
            col = colors[-1]
            for posn in posns:
                col = colors[i] if len(colors) > i else colors[-1]
                if i >= len(colors):
                    cols.append(col)
                if (len(posn) == 3):
                    points.append({"pos": posn.tolist(), "color": col.tolist()})
                elif(len(posn) == 2):
                    p3 = list(posn)
                    p3.append(0.0)
                    p3a = np.array([tuple(p3)], dtype=('f4,f4,f4'))
                    points.append({"pos": p3a[0].tolist(), "color": col.tolist()})
                    
                i += 1
            if len(cols) > 0:
                colors = np.append(colors, np.array(cols, dtype=colors.dtype))

        super(faces, self).__init__(axis=axis, up=up, material=material, display=display)
        object.__setattr__(self, 'radius', radius)
        object.__setattr__(self, 'color', colors)
        object.__setattr__(self, 'pos', posns)
        object.__setattr__(self, 'normal', posns)
        object.__setattr__(self, 'x', xs)
        object.__setattr__(self, 'y', ys)
        object.__setattr__(self, 'z', zs)
        object.__setattr__(self, 'red', reds)
        object.__setattr__(self, 'green', greens)
        object.__setattr__(self, 'blue', blues)
        object.__setattr__(self, 'frame', frame)
        cmd = {"cmd": "faces", "idx": self.idx, 
               "attrs": [#{"attr": "pos", "value": self.pos.values()},
                         #{"attr": "axis", "value": self.axis.values()},
                         #{"attr": "size", "value": self.size.values()},
                         #{"attr": "up", "value": self.up.values()},
                         #{"attr": "color", "value": list(self.color)},
                         #{"attr": "shininess", "value": self.shininess},
                         #{"attr": "emissive", "value": self.emissive},
                         #{"attr": "points", "value": [{"pos": [0, 0, 0]}, {"pos": [1, 0, 0]}]},
                         #{"attr": "points", "value": pointsa.tolist()},
                         {"attr": "points", "value": points},
                         {"attr": "radius", "value": self.radius},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        """
        self.appendcmd(cmd)
        baseObj.checksend()
        """
        
    def __setattr__(self, name, value):
        if name in ['pos','color','x','y','z','red','green','blue','radius','axis']:
        
            if name == 'radius':
                self.__dict__[name] = vector(value) if type(value) is tuple else value
                cmd = {"idx": self.idx, "attr": "radius", "val": self.radius}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'axis':
                self.__dict__[name] = vector(value) if type(value) is tuple else value
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'pos':
                self.__dict__[name] = np.array(value, dtype=('f4,f4,f4')) if type(value) is list and (len(value) == 0 or len(value[0]) == 3) else np.array(value, dtype=('f4,f4')) if type(value) is list and len(value[0]) == 2 else value
                self.__dict__['x'] = self.pos['f0']
                self.__dict__['y'] = self.pos['f1']
                if len(value[0]) == 3:
                    self.__dict__['z'] = self.pos['f2']
                    cmd = {"cmd": "modify", "idx": self.idx, 
                        "attrs":[{"attr": 'posns', "value": self.pos.tolist()}]}
                    baseObj.cmds.append(cmd)
                    baseObj.checksend()
                else:
                    posns = []
                    if len(self.pos) > 0:
                        for posn in self.pos:
                            p3 = list(posn)
                            p3.append(0.0)
                            posns.append(tuple(p3))
                        posns2 = np.array(posns, dtype=('f4,f4,f4'))
                        cmd = {"cmd": "modify", "idx": self.idx, 
                            "attrs":[{"attr": 'posns', "value": posns2.tolist()}]}
                        baseObj.cmds.append(cmd)
                        baseObj.checksend()
                    
            elif name == 'x':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f0'] = self.x
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.x.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'y':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f1'] = self.y
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.y.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'z':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['pos']['f2'] = self.z
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.z.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'red':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f0'] = self.red
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.red.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'green':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f1'] = self.green
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.green.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'blue':
                self.__dict__[name] = np.array(value, float) if type(value) is list or tuple else np.array([value], float) if type(value) is float or int else value
                self.__dict__['color']['f2'] = self.blue
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": name, "value": self.blue.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'color':
                self.__dict__[name] = np.array(value, dtype=('f4,f4,f4')) if type(value) is list and (len(value) == 0 or len(value[0]) == 3) else np.array(value, dtype=('f4,f4')) if type(value) is list and len(value[0]) == 2 else value
                self.__dict__['red'] = self.color['f0']
                self.__dict__['green'] = self.color['f1']
                self.__dict__['blue'] = self.color['f2']
                cmd = {"cmd": "modify", "idx": self.idx, 
                    "attrs":[{"attr": 'colors', "value": self.color.tolist()}]}
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(faces, self).__setattr__(name, value)

    def append(self, pos = None, normal = None, color = None, red = None, green = None, blue = None):
        """
        Usage:
        f.append(pos=(x,y,z))
        f.append(pos=(x,y,z), normal=(nx,ny,nz))
        f.append(pos=(x,y,z), normal=(nx,ny,nz), color=(r,g,b))
        f.append(pos=(x,y,z), normal=(nx,ny,nz), red=r, green=g, blue=b)                    
        """
        
        if (red is not None) and (green is not None) and (blue is not None):
            color = (red,green,blue)

        if (pos is not None) and (normal is not None) and (color is not None):
            self.__dict__['pos'] = np.append(self.pos, np.array([pos], dtype=self.pos.dtype))
            self.__dict__['normal'] = np.append(self.normal, np.array([normal], dtype=self.normal.dtype))
            self.__dict__['color'] = np.append(self.color, np.array([color], dtype=self.color.dtype))
            #cmd = {"cmd": "push", "idx": self.idx, 
            #        "attrs":[{"attr": "pos", "value": list(pos)},{"attr": "normal", "value": list(normal)},{"attr": "color", "value": list(color)}]}
            #baseObj.cmds.append(cmd)
            #baseObj.checksend()
        elif (pos is not None) and (normal is not None):
            self.__dict__['pos'] = np.append(self.pos, np.array([pos], dtype=self.pos.dtype))
            self.__dict__['normal'] = np.append(self.normal, np.array([normal], dtype=self.normal.dtype))
            #color = self.color[-1]
            #self.__dict__['color'] = np.append(self.color, np.array([color], dtype=self.color.dtype))
            #cmd = {"cmd": "push", "idx": self.idx, 
            #        "attrs":[{"attr": "pos", "value": list(pos)},{"attr": "normal", "value": list(normal)},{"attr": "color", "value": self.color[-1].tolist()}]}
            #baseObj.cmds.append(cmd)
            #baseObj.checksend()
        elif (pos is not None):
            self.__dict__['pos'] = np.append(self.pos, np.array([pos], dtype=self.pos.dtype))

    def make_normals(self):
        # for triangle with vertices abc, (b-a).cross(c-b).norm() will be perpendicular to triangle
        pass

    def make_twosided(self):
        pass

    def smooth(self, angle = 0.95):
        pass

class faces2(baseAttrs2):

    def __init__(self, pos = [], color = [], normal = [], red = [1.], green = [1.], blue = [1.], material = None, frame = None, display = None):
        posns = np.array(pos, dtype=('f4,f4,f4')) if type(pos) is list else pos
        normals = np.array(normal, dtype=('f4,f4,f4')) if type(pos) is list else normal
        colors = np.array(color, dtype=('f4,f4,f4')) if type(color) is list else np.array([color], dtype=('f4,f4,f4')) if type(color) is tuple else color
        reds = np.array(red, float) if type(red) is list else np.array([red], float) if type(red) is float or int else red
        greens = np.array(green, float) if type(green) is list else np.array([green], float) if type(green) is float or int else green
        blues = np.array(blue, float) if type(blue) is list else np.array([blue], float) if type(blue) is float or int else blue
        
        super(faces, self).__init__()
        object.__setattr__(self, 'frame', frame)
        object.__setattr__(self, 'display', display)
        
        points = []
        if len(posns) > 0:
            i = 0
            #col = np.array([(1.,1.,1.)], dtype=('f4,f4,f4'))[-1]
            col = colors[-1]
            for posn in posns:
                col = colors[i] if len(colors) > i else col
                """
                if len(colors) > i:
                    points.append({"pos": posn.tolist(), "color": col.tolist()})
                else:
                    points.append({"pos": posn.tolist()})
                """
                points.append({"pos": posn.tolist(), "color": col.tolist()})
                i += 1
        
        cmd = {"cmd": "faces", "idx": self.idx, 
               "attrs": [#{"attr": "pos", "value": self.pos.values()},
                         #{"attr": "axis", "value": self.axis.values()},
                         #{"attr": "size", "value": self.size.values()},
                         #{"attr": "up", "value": self.up.values()},
                         #{"attr": "color", "value": list(self.color)},
                         #{"attr": "shininess", "value": self.shininess},
                         #{"attr": "emissive", "value": self.emissive},
                         #{"attr": "points", "value": [{"pos": [0, 0, 0]}, {"pos": [1, 0, 0]}]},
                         #{"attr": "points", "value": pointsa.tolist()},
                         {"attr": "points", "value": points},
                         {"attr": "radius", "value": self.radius},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}

        self.appendcmd(cmd)
        #baseObj.checksend()
        """
        if len(posns) > 0:
            i = 0
            col = (1.,1.,1.)
            for posn in posns:
                col = colors[i] if len(colors) > i else col
                cmd2 = {"cmd": "push", "idx": self.idx, 
                       "attrs":[{"attr": "pos", "value": list(posn)},
                                {"attr": "color", "value": list(col)}]}
                i += 1
                self.appendcmd(cmd2)
                #baseObj.cmds.append(cmd)
                #baseObj.checksend()
        """
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['frame','display']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'radius':
                cmd = {"idx": self.idx, "attr": "radius", "val": self.radius}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(faces, self).__setattr__(name, value)

    def append(self, pos = None, color = None, normal = None, red = None, green = None, blue = None):
        # need to implement this

        if (red is not None) and (green is not None) and (blue is not None):
            color = (red,green,blue)

        if (pos is not None) and (color is not None):
            # self.__dict__['colors'] = np.append(self.colors,np.array([color], dtype=('f4,f4,f4'))[0],axis=0)
            #y = np.append(self.colors, np.array([color], dtype=self.colors.dtype))
            #self.colors = y
            self.colors = np.append(self.colors, np.array([color], dtype=self.colors.dtype))
            cmd = {"cmd": "push", "idx": self.idx, 
                    "attrs":[{"attr": "pos", "value": list(pos)},{"attr": "color", "value": list(color)}]}
            baseObj.cmds.append(cmd)
            baseObj.checksend()
        elif (pos is not None):
            cmd = {"cmd": "push", "idx": self.idx, 
                    "attrs":[{"attr": "pos", "value": list(pos)},{"attr": "color", "value": self.colors[-1].tolist()}]}
            #"attrs":[{"attr": "pos", "value": list(pos)}]}
            baseObj.cmds.append(cmd)
            baseObj.checksend()


class helix(baseAttrs2):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), length = -1., radius = 1., thickness = 0., coils = 5,
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., frame = None, display = None, material = None):
        if (length == -1.0):
            length = axis[0]
        if (thickness == 0.):
            thickness = radius/20.
        size = vector(length,radius*2,radius*2)
        super(helix, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                   material=material,frame=frame,display=display)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'radius', radius)
        object.__setattr__(self, 'thickness', thickness)
        object.__setattr__(self, 'coils', coils)
        cmd = {"cmd": "helix", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "thickness", "value": self.thickness},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['length','radius','thickness','coils','axis','size']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                self.__dict__['axis'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
                cmd = {"idx": self.idx, "attr": "axis", "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'radius':
                self.__dict__['size'][1] = 2*value
                self.__dict__['size'][2] = 2*value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
                self.__dict__['axis'][1] = 2*value
                self.__dict__['axis'][2] = 2*value
                cmd = {"idx": self.idx, "attr": "axis", "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
            elif name == 'thickness':
                cmd = {"idx": self.idx, "attr": name, "val": self.thickness}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
                self.__dict__['size'][0] = value[0]
                self.__dict__['length'] = value[0]
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'size':
                """VPython helix does not hava a size attribute but Glowscript helix does"""
                pass
        else:
            super(helix, self).__setattr__(name, value)

class arrow(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), length = -1., shaftwidth = 0., headwidth = 0., headlength = 0., fixedwidth = False,
                 frame = None, up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None, opacity = 1.0,
                 display = None, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        axis = vector(axis) if type(axis) is tuple else axis
        if (length == -1.0):
            length = axis.mag()
        if (shaftwidth == 0.):
            shaftwidth = 0.1*length
        if (headwidth == 0.):
            headwidth = 2.*shaftwidth
        if (headlength == 0.):
            headlength = 3.*shaftwidth
        super(arrow, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, up=up, color=color, red=red,
                                    green=green,blue=blue,material=material,opacity=opacity,frame=frame,display=display,
                                   make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'shaftwidth', shaftwidth)
        object.__setattr__(self, 'headwidth', headwidth)
        object.__setattr__(self, 'headlength', headlength)
        cmd = {"cmd": "arrow", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis_and_length", "value": self.axis.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shaftwidth", "value": self.shaftwidth},
                         {"attr": "headwidth", "value": self.headwidth},
                         {"attr": "headlength", "value": self.headlength},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','axis','shaftwidth','headwidth','headlength','fixedwidth']:
            self.__dict__[name] = vector(value) if type(value) is tuple else vector(tuple(value.tolist())) if type(value) is np.ndarray else value
        
            if name == 'length':
                tmp = self.axis.norm() * self.length
                cmd = {"idx": self.idx, "attr": "axis_and_length", "val": tmp.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'axis':
                tmp = self.axis.norm() * self.length
                cmd = {"idx": self.idx, "attr": "axis_and_length", "val": tmp.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'shaftwidth':
                cmd = {"idx": self.idx, "attr": name, "val": self.shaftwidth}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
            elif name == 'headwidth':
                cmd = {"idx": self.idx, "attr": name, "val": self.headwidth}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
            elif name == 'headlength':
                cmd = {"idx": self.idx, "attr": name, "val": self.headlength}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
                
        else:
            super(arrow, self).__setattr__(name, value)

class cylinder(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), length = -1., radius = 1.,
                 frame = None, up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None, opacity = 1.0,
                 display = None, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (length == -1.0):
            length = axis[0]
        size = vector(length,radius*2,radius*2)
        super(cylinder, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                       material=material,opacity=opacity,frame=frame,display=display,
                                       make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'radius', radius)
        cmd = {"cmd": "cylinder", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','radius','axis']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'radius':
                self.__dict__['size'][1] = 2*value
                self.__dict__['size'][2] = 2*value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                                           
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(cylinder, self).__setattr__(name, value)
 
class pyramid(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 length = 1., width = 1., height = 1., up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.,
                 frame = None, material = None, opacity = 1.0, display = None,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        sz = size
        if (length != 1.0) or (width != 1.0) or (height != 1.0):
            sz = vector(length,height,width) if type(size) is tuple else size
        else:
            length = size[0]
            height = size[1]
            width = size[2]
        super(pyramid, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=sz, up=up,color=color,red=red,green=green,blue=blue,
                                      material=material,opacity=opacity,frame=frame,display=display,
                                      make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'width', width)
        object.__setattr__(self, 'height', height)
        cmd = {"cmd": "pyramid", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','width','height','size']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'height':
                self.__dict__['size'][1] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'width':
                self.__dict__['size'][2] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'size':
                self.__dict__['length'] = value[0]
                self.__dict__['height'] = value[1]
                self.__dict__['width'] = value[2]
                cmd = {"idx": self.idx, "attr": name, "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
                
        else:
            super(pyramid, self).__setattr__(name, value)

class sphere(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.),x = 0., y = 0., z = 0., axis = (1.,0.,0.), radius = 1.0,
                 frame = None, up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None, opacity = 1.0,
                 display = None, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        size = vector(radius*2,radius*2,radius*2)
        super(sphere, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                     material=material,opacity=opacity,frame=frame,display=display,
                                     make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'radius', radius )
        object.__setattr__(self, 'display', display )

        cmd = {"cmd": "sphere", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}
        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):        
        if name == 'radius':
            self.__dict__[name] = value
            self.__dict__['size'][0] = value*2
            self.__dict__['size'][1] = value*2
            self.__dict__['size'][2] = value*2
            cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
            baseObj.cmds.append(cmd)
            baseObj.checksend()                
        else:
            super(sphere, self).__setattr__(name, value)

class ellipsoid(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), size = (1.,1.,1.),
                 length = 1., width = 1., height = 1., up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.,
                 frame = None, material = None, opacity = 1.0, display = None,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        sz = size
        if (length != 1.0) or (width != 1.0) or (height != 1.0):
            sz = vector(length,height,width) if type(size) is tuple else size
        else:
            length = size[0]
            height = size[1]
            width = size[2]
        super(ellipsoid, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=sz, up=up,color=color,red=red,green=green,blue=blue,
                                  material=material,opacity=opacity,frame=frame,display=display,
                                  make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'width', width)
        object.__setattr__(self, 'height', height)
        cmd = {"cmd": "ellipsoid", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['length','width','height','size']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'length':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            elif name == 'height':
                self.__dict__['size'][1] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'width':
                self.__dict__['size'][2] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'size':
                self.__dict__['length'] = value[0]
                self.__dict__['height'] = value[1]
                self.__dict__['width'] = value[2]
                cmd = {"idx": self.idx, "attr": name, "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
                
        else:
            super(ellipsoid, self).__setattr__(name, value)


class ring(baseAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.),
                 length = 1., radius = 1., thickness = 0.0, frame = None, display = None,
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (thickness == 0.0):
            thickness = radius/10.0
        size = vector(thickness,radius,radius)
        super(ring, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,frame=frame,display=display)
        object.__setattr__(self, 'length', length)
        object.__setattr__(self, 'radius', radius)
        object.__setattr__(self, 'thickness', thickness)
        object.__setattr__(self, 'make_trail', make_trail )
        object.__setattr__(self, 'trail_type', trail_type )
        object.__setattr__(self, 'interval', interval)
        object.__setattr__(self, 'retain', retain)
        #object.__setattr__(self, 'trail_object', curve() if self.trail_type == "curve" else points())
        cmd = {"cmd": "ring", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
                         {"attr": "make_trail", "value": self.make_trail},
                         {"attr": "type", "value": 'curve' if self.trail_type == 'curve' else 'spheres'},
                         {"attr": "interval", "value": self.interval},
                         {"attr": "retain", "value": self.retain}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['make_trail','trail_type','interval','retain','length','radius','thickness']:
            self.__dict__[name] = value
            if name == 'make_trail':
                cmd = {"idx": self.idx, "attr": name, "val": self.make_trail}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'trail_type':
                cmd = {"idx": self.idx, "attr": name, "val": self.trail_type}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'interval':
                cmd = {"idx": self.idx, "attr": name, "val": self.interval}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'retain':
                cmd = {"idx": self.idx, "attr": name, "val": self.retain}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
            elif name == 'radius':
                self.__dict__['size'][1] = value
                self.__dict__['size'][2] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'thickness':
                self.__dict__['size'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.size.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                           
                
        else:
            super(ring, self).__setattr__(name, value)

class label(baseAttrs2):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., color = (1.,1.,1.), red = 1., green = 1., blue = 1., opacity = 0.66, 
                 xoffset = 20., yoffset = 12., text = "", font = "sans", height = 13, background = (0.,0.,0.),
                 border = 5, box = True, line = True, linecolor = (0.,0.,0.), space = 0., display = None, frame = None):  
        # backgraound = scene.background   # default background color
        # color = scene.foreground  # default color
        super(label, self).__init__(pos=pos, x=x, y=y, z=z, color=color, red=red, green=green,blue=blue, opacity=opacity, frame=frame, display=display)

        object.__setattr__(self, 'xoffset', xoffset)
        object.__setattr__(self, 'yoffset', yoffset)
        object.__setattr__(self, 'text', text)
        object.__setattr__(self, 'font', font)
        object.__setattr__(self, 'height', height)
        object.__setattr__(self, 'background', background)
        object.__setattr__(self, 'border', border)
        object.__setattr__(self, 'box', box)
        object.__setattr__(self, 'line', line)
        object.__setattr__(self, 'linecolor', linecolor)
        object.__setattr__(self, 'space', space)
        cmd = {"cmd": "label", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "text", "value": self.text},
                         #{"attr": "align", "value": 'center'},
                         {"attr": "xoffset", "value": self.xoffset},
                         {"attr": "yoffset", "value": self.yoffset},
                         #{"attr": "font", "value": self.font},
                         #{"attr": "height", "value": self.height},
                         #{"attr": "color", "value": list(self.color)},
                         #{"attr": "background", "value": list(self.background)},
                         #{"attr": "opacity", "value": self.opacity},
                         #{"attr": "border", "value": self.border},
                         #{"attr": "box", "value": self.box},
                         #{"attr": "line", "value": self.line},
                         #{"attr": "linecolor", "value": list(self.linecolor)},
                         ##{"attr": "linewidth", "value": self.linewidth},
                         #{"attr": "space", "value": self.space},
                         #{"attr": "pixel_pos", "value": False},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
                         ]}

        self.appendcmd(cmd)
        baseObj.checksend()
        if (frame != None):
            frame.objects.append(self)
            frame.update_obj_list()
        
    def __setattr__(self, name, value):
        if name in ['xoffset','yoffset','text','font','height','background',
                    'border','box','line','linecolor','space']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
            if name == 'background':
                cmd = {"idx": self.idx, "attr": "axis_and_length", "val": self.background.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()                
            else:
                cmd = {"idx": self.idx, "attr": name, "val": value}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
                
        else:
            super(label, self).__setattr__(name, value)

            
class frame(baseAttrs):
    objects = []
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), display = None,
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.):
        super(frame, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, up=up, color=color, red=red, green=green, blue=blue, display=display)
        object.__setattr__(self, 'objects', [])
        cmd = {"cmd": "compound", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        
        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        super(frame, self).__setattr__(name, value)

    def frame_to_world(self, pos):
        # need to implement this
        return pos

    def world_to_frame(self, pos):
        # need to implement this
        return pos

    def update_obj_list(self):
        # self.visible = False     # we are going to create a new compound in glowscript so remove current one
        obj_idxs = []
        for obj in self.objects:
            obj_idxs.append(obj.idx)
        cmd = {"cmd": "compound", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "obj_idxs", "value": obj_idxs},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        
        self.appendcmd(cmd)
        baseObj.checksend()
        #self.visible = True

class sceneObj(baseObj):
    foreground = (1,1,1)
    background = (0,0,0)
    ambient = color.gray(0.2)
    lights = []
    objects = []
    stereo = 'redcyan'
    stereodepth = 1.
    x = 0.
    y = 0.
    height = 500
    width = 800
    title = ""
    fullscreen = False
    exit = True
    center = (0,0,0)
    autocenter = True
    forward = (0,0,-1)
    fov = math.pi/3.
    range = (1.,1.,1.)
    scale = (1.,1.,1.)
    autoscale = True
    userzoom = True
    userspin = True

    def __init__(self, foreground = (1,1,1), background = (0,0,0), ambient = color.gray(0.2), stereo = 'redcyan',
                    stereodepth = 1., x = 0., y = 0., height = 480, width = 640, title = "", fullscreen = False,
                    exit = True, center = (0,0,0), autocenter = True, forward = (0,0,-1), fov = math.pi/3.,
                    range = (1.,1.,1.), scale = (1.,1.,1.), autoscale = True, userzoom = True, userspin = True):
        super(sceneObj, self).__init__()
        if isinstance(range, (int, long, float)):
            range = (range,range,range)
        if isinstance(scale, (int, long, float)):
            scale = (scale,scale,scale)
        if (range[0] != 1.) and (range[0] != 0.):
            scale[0] = 1./range[0]
        if (scale[0] != 1.) and (scale[0] != 0.):
            range[0] = 1./scale[0]
        object.__setattr__(self, 'objects', [])
        object.__setattr__(self, 'foreground', foreground)
        object.__setattr__(self, 'background', background)
        object.__setattr__(self, 'ambient', ambient)
        object.__setattr__(self, 'stereo', stereo)
        object.__setattr__(self, 'stereodepth', stereodepth)
        object.__setattr__(self, 'x', x)
        object.__setattr__(self, 'y', y)
        object.__setattr__(self, 'height', height)
        object.__setattr__(self, 'width', width)
        object.__setattr__(self, 'title', title)
        object.__setattr__(self, 'fullscreen', fullscreen)
        object.__setattr__(self, 'exit', exit)
        object.__setattr__(self, 'center', vector(center) if type(center) is tuple else center)
        object.__setattr__(self, 'autocenter', autocenter)
        object.__setattr__(self, 'forward', vector(forward) if type(forward) is tuple else forward)
        object.__setattr__(self, 'fov', fov)
        object.__setattr__(self, 'range', vector(range) if type(range) is tuple else range)
        object.__setattr__(self, 'scale', vector(scale) if type(scale) is tuple else scale)
        object.__setattr__(self, 'autoscale', autoscale)
        object.__setattr__(self, 'userzoom', userzoom)
        object.__setattr__(self, 'userspin', userspin)
        
    def __setattr__(self, name, value):
        if name in ['foreground','background','ambient','stereo','stereodepth','x','y',
                    'height','width','title','fullscreen','exit','center','autocenter',
                    'forward','fov','range','scale','autoscale','userzoom','userspin']:
            if name in ['foreground','background','ambient']:
                self.__dict__[name] = value
            else:
                self.__dict__[name] = vector(value) if type(value) is tuple else value
            if name in ['background','ambient','height','width','center',
                    'forward','fov','range','scale','autoscale','userzoom','userspin']:
                cmd = {}
                if name == 'background':
                    cmd = {"idx": self.idx, "attr": name, "val": list(self.background)}            
                elif name == 'ambient':
                    cmd = {"idx": self.idx, "attr": name, "val": list(self.ambient)}            
                elif name == 'center':
                    cmd = {"idx": self.idx, "attr": name, "val": self.center.values()}            
                elif name == 'forward':
                    cmd = {"idx": self.idx, "attr": name, "val": self.forward.values()}            
                elif name == 'range':
                    cmd = {"idx": self.idx, "attr": name, "val": self.range[0]}            
                elif name == 'scale':
                    cmd = {"idx": self.idx, "attr": name, "val": self.scale[0]}            
                else:
                    cmd = {"idx": self.idx, "attr": name, "val": value}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(sceneObj, self).__setattr__(name, value)
        
class idisplay(sceneObj):
    sceneCnt = 0
    selected_display = -1
    displays = []
    display_idx = 0
    def __init__(self, foreground = (1,1,1), background = (0,0,0), ambient = color.gray(0.2), stereo = 'redcyan',
                    stereodepth = 1., x = 0., y = 0., height = 480, width = 640, title = "", fullscreen = False,
                    exit = True, center = (0,0,0), autocenter = True, forward = (0,0,-1), fov = math.pi/3.,
                    range = 1., scale = 1., autoscale = True, userzoom = True, userspin = True):
        # display(Javascript("""$.getScript("glowcomm.js");"""))        
        super(idisplay, self).__init__(foreground=foreground, background=background, ambient=ambient, stereo=stereo,
                                       stereodepth=stereodepth, x=x, y=y, height=height, width=width, title=title, fullscreen=fullscreen,
                                       exit=exit, center=center, autocenter=autocenter, forward=forward, fov=fov, 
                                       range=range, scale=scale, autoscale=autoscale, userzoom=userzoom)
        object.__setattr__(self, 'display_index', idisplay.display_idx)
        idisplay.displays.append(self)
        idisplay.selected_display = idisplay.display_idx
        idisplay.display_idx += 1
        idisplay.sceneCnt += 1
        object.__setattr__(self, 'sceneId', "scene%d" % (idisplay.sceneCnt))
        display(HTML("""<div id="%s"><div id="glowscript" class="glowscript"></div></div>""" % (self.sceneId)))
        display(Javascript("""window.__context = { glowscript_container: $("#glowscript").removeAttr("id")}"""))

        #cmd = {"cmd": "canvas", "idx": self.idx, 
        #       "attrs": [{"attr": "title", "value": self.title}]}
        cmd = {"cmd": "canvas", "idx": self.idx, 
               "attrs": [{"attr": "title", "value": self.title},
                         #{"attr": "background", "value": list(self.background)},
                         #{"attr": "ambient", "value": list(self.ambient)},
                         {"attr": "height", "value": self.height},
                         {"attr": "width", "value": self.width},
                         #{"attr": "center", "value": self.center.values()},
                         #{"attr": "forward", "value": self.forward.values()},
                         {"attr": "fov", "value": self.fov},
                         {"attr": "range", "value": self.range[0]},
                         {"attr": "autoscale", "value": self.autoscale},
                         {"attr": "userzoom", "value": self.userzoom},
                         {"attr": "userspin", "value": self.userspin}
                         ]}

        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
            super(idisplay, self).__setattr__(name, value)

    def select(self):
        idisplay.selected_display = self.display_index

    @classmethod
    def get_selected(cls):
        return cls.displays[cls.selected_display] if cls.selected_display >= 0 else None

    def _ipython_display_(self):
        #display(HTML("""<div id="glowscript2" class="glowscript"></div>"""))
        display_html('<div id="glowscript2" ><div id="glowscript" class="glowscript"></div></div>', raw=True)
        #display(Javascript("""$('#glowscript2').replaceWith($('#scene1'));"""))
        #display(Javascript("""document.getElementById('glowscript2').appendChild(document.getElementById('%s'));""" % (self.sceneId)))
        #display(Javascript("""$('#glowscript2').replaceWith(document.getElementById('%s'));""" % (self.sceneId)))
        #display_javascript("""$('#glowscript2').replaceWith(document.getElementById('%s'));""" % (self.sceneId),raw=True)
        #display_javascript("""var c = document.getElementById('%s'); if (c !== null) {$('#glowscript2').replaceWith(c);}else{console.log("scene object is null");}""" % (self.sceneId),raw=True)
        #display(Javascript("""$('#glowscript2').replaceWith(document.getElementById('scene1'));"""))      #display(Javascript("""$('#glowscript2').replaceWidth($('#%s'));"""%(self.sceneId)))
        #display(Javascript("""window.__context = { glowscript_container: $("#glowscript2")}"""))
        #display(HTML("""<div id="glowscript2" class="glowscript"></div>"""))
        cmd = {"cmd": "redisplay", "idx": self.idx, "sceneId": self.sceneId}        
        self.appendcmd(cmd)
        baseObj.checksend()
    
class defaultscene(sceneObj):

    def __init__(self):
        super(defaultscene, self).__init__()
        cmd = {"cmd": "scene", "idx": self.idx}        
        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        cmd = {"cmd": "scene", "idx": self.idx}        
        self.appendcmd(cmd)
        baseObj.checksend()
        
        super(defaultscene, self).__setattr__(name, value)
    
class local_light(baseObj):
    def __init__(self, pos = (0.,0.,0.), color = (1.,1.,1.), frame = None, display = None):
        # display(Javascript("""$.getScript("glowcomm.js");"""))        
        super(local_light, self).__init__()
        object.__setattr__(self, 'pos', vector(pos) if type(pos) is tuple else pos)
        object.__setattr__(self, 'color', color)
        object.__setattr__(self, 'display', display)
        object.__setattr__(self, 'frame', frame)
        cmd = {"cmd": "local_light", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
                         ]}
        if (idisplay.get_selected() != None):
            idisplay.get_selected().lights.append(self)
        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['pos']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
            cmd = {}
            if name == 'pos':
                cmd = {"idx": self.idx, "attr": name, "val": self.pos.values()}            
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
        elif name == 'color':
            self.__dict__[name] = value
            cmd = {"idx": self.idx, "attr": name, "val": list(self.color)}            
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
                
        else:
            super(local_light, self).__setattr__(name, value)
        
class distant_light(baseObj):
    def __init__(self, direction = (0.,0.,0.), color = (1.,1.,1.), frame = None, display = None):
        # display(Javascript("""$.getScript("glowcomm.js");"""))        
        super(distant_light, self).__init__()
        object.__setattr__(self, 'direction', vector(direction) if type(direction) is tuple else direction)
        object.__setattr__(self, 'color', color)
        object.__setattr__(self, 'display', display)
        object.__setattr__(self, 'frame', frame)
        cmd = {"cmd": "distant_light", "idx": self.idx, 
               "attrs": [{"attr": "direction", "value": self.direction.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": self.display.idx if self.display != None else idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
                         ]}
        if (idisplay.get_selected() != None):
            idisplay.get_selected().lights.append(self)
        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['direction']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
            cmd = {}
            if name == 'direction':
                cmd = {"idx": self.idx, "attr": name, "val": self.direction.values()}            
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
        elif name == 'color':
            self.__dict__[name] = value
            cmd = {"idx": self.idx, "attr": name, "val": list(self.color)}            
                
            baseObj.cmds.append(cmd)
            baseObj.checksend()                           
                
        else:
            super(distant_light, self).__setattr__(name, value)

scene = defaultscene()