
from __future__ import print_function
#import ivisual
import crayola as color
import materials
import numpy as np
from rate_control import *
from IPython.display import HTML
from IPython.display import display
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

display(HTML("""<div id="glowscript" class="glowscript">"""))

package_dir = os.path.dirname(np.__file__)
IPython.html.nbextensions.install_nbextension(files=[package_dir+"/../ivisual/data/glow.1.0.min.js",package_dir+"/../ivisual/data/glowcomm.js"],overwrite=True)
#IPython.html.nbextensions.install_nbextension(files=[package_dir+"/data/glow.1.0.min.js",package_dir+"/data/glowcomm.js"],overwrite=True)

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
    def __init__(self, x = 0., y = 0., z = 0.):
        self.x = x[0] if type(x) is tuple else x
        self.y = x[1] if type(x) is tuple else y
        self.z = x[2] if type(x) is tuple else z

    def __str__(self):
        return 'vector (%f, %f, %f)' % (self.x, self.y, self.z)
   
    def __add__(self,other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self,other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if type(other) is float:
            return vector(self.x * other, self.y * other, self.z * other)
        return self
    
    def __rmul__(self, other):
        if type(other) is float:
            return vector(self.x * other, self.y * other, self.z * other)
        return self

    def __div__(self, other):
        if type(other) is float:
            return vector(self.x / other, self.y / other, self.z / other)
        return self
    
    def __truediv__(self, other):
        if type(other) is float:
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

    def norm(self):
        return self / self.mag()

    def keys(self):
        return [0,1,2]
    
    def values(self):
        return [self.x,self.y,self.z]


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
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.):
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

    def __setattr__(self, name, value):
        # print('attribute : ', name,' value changed to ',value)
        if name in ['pos','size','axis','up','visible','x','y','z','red','green','blue']:
            self.__dict__[name] = vector(value) if type(value) is tuple else value
            cmd = {}
            if name == 'x':
                self.__dict__['pos'][0] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.pos.values()}            
            elif name == 'y':
                self.__dict__['pos'][1] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.pos.values()}            
            elif name == 'z':
                self.__dict__['pos'][2] = value
                cmd = {"idx": self.idx, "attr": "size", "val": self.pos.values()}            
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
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None,
                 opacity = 1.0):
        super(baseAttrs2, self).__init__(pos=pos,axis=axis,size=size,up=up,color=color,red=red,green=green,blue=blue,x=x,y=y,z=z)
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
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None,
                 opacity = 1.0, make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        super(trailAttrs, self).__init__(pos=pos,axis=axis,size=size,up=up,color=color,red=red,green=green,blue=blue,x=x,y=y,z=z)
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
                 frame = None, material = None, opacity = 1.0, 
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        sz = size
        if (length != 1.0) or (width != 1.0) or (height != 1.0):
            sz = vector(length,height,width) if type(size) is tuple else size
        else:
            length = size[0]
            height = size[1]
            width = size[2]
        super(box, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=sz, up=up,color=color,red=red,green=green,blue=blue,
                                  material=material,opacity=opacity,
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (length == -1.0):
            length = axis[0]
        size = vector(length,radius*2,radius*2)
        super(cone, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                   material=material,opacity=opacity,
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
    # xx = x.tolist()    # create a list from an array
    # xx = list(x)       # create a list from an array
    def __init__(self, pos = [], x = [], y = [], z = [], axis = (1.,0.,0.), radius = 0.,
                 up = (0.,1.,0.), color = [(1.,1.,1.)], red = [1.], green = [1.], blue = [1.], material = None):
        posns = np.array(pos, dtype=('f4,f4,f4')) if type(pos) is list else pos
        xs = np.array(x, float) if type(x) is list else np.array([x], float) if type(x) is float or int else x
        ys = np.array(y, float) if type(y) is list else np.array([y], float) if type(y) is float or int else y
        zs = np.array(z, float) if type(z) is list else np.array([z], float) if type(z) is float or int else z
        colors = np.array(color, dtype=('f4,f4,f4')) if type(color) is list else np.array([color], dtype=('f4,f4,f4')) if type(color) is tuple else color
        reds = np.array(red, float) if type(red) is list else np.array([red], float) if type(red) is float or int else red
        greens = np.array(green, float) if type(green) is list else np.array([green], float) if type(green) is float or int else green
        blues = np.array(blue, float) if type(blue) is list else np.array([blue], float) if type(blue) is float or int else blue
        
        super(curve, self).__init__(axis=axis, up=up, material=material)
        object.__setattr__(self, 'radius', radius)
        object.__setattr__(self, 'colors', colors)
        """
        cmd = {"cmd": "curve", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         #{"attr": "radius", "value": self.radius if self.radius != 0. else 0.001 if idisplay.get_selected() == None else 0.001*idisplay.get_selected().range},
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        
        points = [{"pos": [0, 0, 0]}, {"pos": [1, 0, 0]}]
        points.append({"pos": list((1,1,0)), "color": list((1,1,0))})
        points.append({"pos": list((0,1,0)), "color": list((0,1,0))})
        pointsa = np.array(points)
        """
        
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}

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
        if name in ['radius','axis']:
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
            super(curve, self).__setattr__(name, value)

    def append(self, pos = None, color = None, red = None, green = None, blue = None):
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
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None):
        if (length == -1.0):
            length = axis[0]
        if (thickness == 0.):
            thickness = radius/20.
        size = vector(length,radius*2,radius*2)
        super(helix, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                   material=material)
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}

        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
        if name in ['length','radius','thickness','coils','axis']:
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
            elif name == 'thickness':
                cmd = {"idx": self.idx, "attr": name, "val": self.thickness}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
            elif name == 'axis':
                cmd = {"idx": self.idx, "attr": name, "val": self.axis.values()}            
                baseObj.cmds.append(cmd)
                baseObj.checksend()
        else:
            super(helix, self).__setattr__(name, value)

class arrow(trailAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.), length = -1., shaftwidth = 0., headwidth = 0., headlength = 0., fixedwidth = False,
                 frame = None, up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1., material = None, opacity = 1.0,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
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
                                    green=green,blue=blue,material=material,opacity=opacity,
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
            self.__dict__[name] = vector(value) if type(value) is tuple else value
        
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
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (length == -1.0):
            length = axis[0]
        size = vector(length,radius*2,radius*2)
        super(cylinder, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                       material=material,opacity=opacity,
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
                 frame = None, material = None, opacity = 1.0,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        sz = size
        if (length != 1.0) or (width != 1.0) or (height != 1.0):
            sz = vector(length,height,width) if type(size) is tuple else size
        else:
            length = size[0]
            height = size[1]
            width = size[2]
        super(pyramid, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=sz, up=up,color=color,red=red,green=green,blue=blue,
                                      material=material,opacity=opacity,
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        size = vector(radius*2,radius*2,radius*2)
        super(sphere, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue,
                                     material=material,opacity=opacity,
                                     make_trail=make_trail,trail_type=trail_type,interval=interval,retain=retain)
        object.__setattr__(self, 'radius', radius )

        cmd = {"cmd": "sphere", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "size", "value": self.size.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "opacity", "value": self.opacity},
                         {"attr": "shininess", "value": self.shininess},
                         {"attr": "emissive", "value": self.emissive},
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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

class ring(baseAttrs):
    
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.),
                 length = 1., radius = 1., thickness = 0.0,
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.,
                 make_trail = False, trail_type = "curve", interval = 10, retain = 50):
        if (thickness == 0.0):
            thickness = radius/10.0
        size = vector(thickness,radius,radius)
        super(ring, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, size=size, up=up,color=color,red=red,green=green,blue=blue)
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1},
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
                 border = 5, box = True, line = True, linecolor = (0.,0.,0.), space = 0., frame = None):  
        # backgraound = scene.background   # default background color
        # color = scene.foreground  # default color
        super(label, self).__init__(pos=pos, x=x, y=y, z=z, color=color, red=red, green=green,blue=blue, opacity=opacity)

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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
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
    def __init__(self, pos = (0.,0.,0.), x = 0., y = 0., z = 0., axis = (1.,0.,0.),
                 up = (0.,1.,0.), color = (1.,1.,1.), red = 1., green = 1., blue = 1.):
        super(frame, self).__init__(pos=pos, x=x, y=y, z=z, axis=axis, up=up, color=color, red=red, green=green, blue=blue)
        object.__setattr__(self, 'objects', [])
        cmd = {"cmd": "compound", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "axis", "value": self.axis.values()},
                         {"attr": "up", "value": self.up.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        
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
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}]}
        
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
    range = 1.
    scale = 1.
    autoscale = True
    userzoom = True
    userspin = True

    def __init__(self, foreground = (1,1,1), background = (0,0,0), ambient = color.gray(0.2), stereo = 'redcyan',
                    stereodepth = 1., x = 0., y = 0., height = 500, width = 800, title = "", fullscreen = False,
                    exit = True, center = (0,0,0), autocenter = True, forward = (0,0,-1), fov = math.pi/3.,
                    range = 1., scale = 1., autoscale = True, userzoom = True, userspin = True):
        super(sceneObj, self).__init__()
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
        object.__setattr__(self, 'center', center)
        object.__setattr__(self, 'autocenter', autocenter)
        object.__setattr__(self, 'forward', forward)
        object.__setattr__(self, 'fov', fov)
        object.__setattr__(self, 'range', range)
        object.__setattr__(self, 'scale', scale)
        object.__setattr__(self, 'autoscale', autoscale)
        object.__setattr__(self, 'userzoom', userzoom)
        object.__setattr__(self, 'userspin', userspin)
        
    def __setattr__(self, name, value):
        if name in ['foreground','background','ambient','stereo','stereodepth','x','y',
                    'height','width','title','fullscreen','exit','center','autocenter',
                    'forward','fov','range','scale','autoscale','userzoom','userspin']:
            self.__dict__[name] = value
            if name in ['background','ambient','height','width','center','autocenter',
                    'forward','fov','range','scale','userzoom','userspin']:
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
                    stereodepth = 1., x = 0., y = 0., height = 500, width = 800, title = "", fullscreen = False,
                    exit = True, center = (0,0,0), autocenter = True, forward = (0,0,-1), fov = math.pi/3.,
                    range = 1., scale = 1., autoscale = True, userzoom = True, userspin = True):
        display(HTML("""<div id="glowscript" class="glowscript">"""))
        display(Javascript("""window.__context = { glowscript_container: $("#glowscript").removeAttr("id")}"""))
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
        cmd = {"cmd": "canvas", "idx": self.idx, 
               "attrs": [{"attr": "title", "value": self.title}]}
        
        self.appendcmd(cmd)
        baseObj.checksend()
        
    def __setattr__(self, name, value):
            super(idisplay, self).__setattr__(name, value)

    def select(self):
        idisplay.selected_display = self.display_index

    @classmethod
    def get_selected(cls):
        return cls.displays[cls.selected_display] if cls.selected_display >= 0 else None

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
    def __init__(self, pos = (0.,0.,0.), color = (1.,1.,1.)):
        # display(Javascript("""$.getScript("glowcomm.js");"""))        
        super(local_light, self).__init__()
        object.__setattr__(self, 'pos', vector(pos) if type(pos) is tuple else pos)
        object.__setattr__(self, 'color', color)
        cmd = {"cmd": "local_light", "idx": self.idx, 
               "attrs": [{"attr": "pos", "value": self.pos.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
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
    def __init__(self, direction = (0.,0.,0.), color = (1.,1.,1.)):
        # display(Javascript("""$.getScript("glowcomm.js");"""))        
        super(distant_light, self).__init__()
        object.__setattr__(self, 'direction', vector(direction) if type(direction) is tuple else direction)
        object.__setattr__(self, 'color', color)
        cmd = {"cmd": "distant_light", "idx": self.idx, 
               "attrs": [{"attr": "direction", "value": self.direction.values()},
                         {"attr": "color", "value": list(self.color)},
                         {"attr": "canvas", "value": idisplay.get_selected().idx if idisplay.get_selected() != None else -1}
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

if (idisplay.sceneCnt > 0):
    display(HTML("""<div id="glowscript" class="glowscript">"""))
    #display(Javascript("""$.getScript("glowcomm.js");"""))
    display(Javascript("""require.undef("nbextensions/glow.1.0.min");"""))
    display(Javascript("""require(["nbextensions/glow.1.0.min"], function(){console.log("test2");})"""))
    #display(Javascript("""require(["nbextensions/glowcomm"], function(){console.log("glowscript 3");})"""))
    #display(Javascript("""require(["glowcomm"], function(){console.log("glowscript 3a");})"""))
    scene = defaultscene()

idisplay.sceneCnt += 1
