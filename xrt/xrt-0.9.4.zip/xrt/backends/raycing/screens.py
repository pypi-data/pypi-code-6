# -*- coding: utf-8 -*-
"""
Screens
-------

Module :mod:`~xrt.backends.raycing.screens` defines a flat screen in the class
:class:`Screen` that intercepts a beam and gives its image.
"""
__author__ = "Konstantin Klementiev"
__date__ = "8 Jan 2014"
import numpy as np
from .. import raycing
from . import sources as rs
from . import materials as rm
import os
try:
    import pyopencl as cl
    isOpenCL = True
    os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
except ImportError:
    isOpenCL = False


class Screen(object):
    def __init__(self, bl, name, center=[0, 0, 0], x='auto', z='auto',
                 compressX=None, compressZ=None, targetOpenCL=None):
        """
        *bl*: instance of :class:`~xrt.backends.raycing.BeamLine`.

        *name*: str.

        *center*: tuple of 3 floats, is a 3D point in the global system.

        *x, z*: 3-tuples or 'auto'. Normalized 3D vectors in the global system
            which determine the local x and z axes lying in the screen plane.
            If *x* is 'auto', it is horizontal and perpendicular to the beam
            line. If *z* is 'auto', it is vertical.

        *compressX, compressZ* are multiplicative compression coefficients for
            the corresponding axes.

        *targetOpenCL*:
            If pyopencl is used: a tuple (iPlatform, iDevice) of indices in the
            lists cl.get_platforms() and platform.get_devices(), see the
            section :ref:`calculations_on_GPU`. None, if pyopencl is not
            wanted. Ignored if pyopencl is not installed.

        """
        self.name = name
        self.bl = bl
        bl.screens.append(self)
        self.ordinalNum = len(bl.screens)
        self.center = center
        self.set_orientation(x, z)
        self.compressX = compressX
        self.compressZ = compressZ
        if (targetOpenCL is not None) and not isOpenCL:
            print "pyopencl is not available!"
        if (targetOpenCL is not None) and isOpenCL:
            iPlatform, iDevice = targetOpenCL
            platform = cl.get_platforms()[iPlatform]
            device = platform.get_devices()[iDevice]
            print('    Device - Name:  ' + device.name)
            self.cl_ctx = cl.Context(devices=[device])
            self.cl_queue = cl.CommandQueue(self.cl_ctx)
            cl_file = os.path.join(os.path.dirname(__file__),
                                   'kirchhoff_ij.cl')
            kernelsource = open(cl_file).read()
            self.cl_program = cl.Program(self.cl_ctx, kernelsource).build()
            self.cl_mf = cl.mem_flags
        else:
            self.cl_ctx = None

    def set_orientation(self, x=None, z=None):
        """Determines the local x, y and z in the global system."""
        if x == 'auto':
            self.x = self.bl.cosAzimuth, -self.bl.sinAzimuth, 0.
        elif x is not None:
            self.x = x
        if z == 'auto':
            self.z = 0., 0., 1.
        elif z is not None:
            self.z = z
        assert np.dot(self.x, self.z) == 0, 'x and z must be orthogonal!'
        self.y = np.cross(self.z, self.x)

    def expose(self, beam):
        """Exposes the screen to the beam. *beam* is in the global system, the
        returned beam is in the local system of the screen and represents the
        desired image. Note that you need x and z of it."""
        blo = rs.Beam(copyFrom=beam, withNumberOfReflections=True)  # local
        blo.x[:] = beam.x[:] - self.center[0]
        blo.y[:] = beam.y[:] - self.center[1]
        blo.z[:] = beam.z[:] - self.center[2]
        xyz = blo.x, blo.y, blo.z
        blo.x[:], blo.y[:], blo.z[:] = \
            sum(c*b for c, b in zip(self.x, xyz)),\
            sum(c*b for c, b in zip(self.y, xyz)),\
            sum(c*b for c, b in zip(self.z, xyz))
        abc = beam.a, beam.b, beam.c
        blo.a[:], blo.b[:], blo.c[:] = \
            sum(c*b for c, b in zip(self.x, abc)),\
            sum(c*b for c, b in zip(self.y, abc)),\
            sum(c*b for c, b in zip(self.z, abc))

#*** if path at the screen is needed *******
#        maxa = np.max(abs(blo.a))
#        maxb = np.max(abs(blo.b))
#        maxc = np.max(abs(blo.c))
#        maxMax = max(maxa, maxb, maxc)
#        if maxMax == maxa:
#            blo.path[:] = -blo.x / blo.a
#        elif maxMax == maxb:
#            blo.path[:] = -blo.y / blo.b
#        else:
#            blo.path[:] = -blo.z / blo.c
#end if path at the screen is needed *******

        blo.y[:] /= blo.b
        blo.x[:] -= blo.a * blo.y
        blo.z[:] -= blo.c * blo.y
        blo.y[:] = 0

        if self.compressX:
            blo.x[:] *= self.compressX
        if self.compressZ:
            blo.z[:] *= self.compressZ

        return blo

    def expose_Kirchhoff(self, beamOEin, oe, beamOEglo, beamOEloc, xloc, zloc):
        if self.cl_ctx is None:
            return self._expose_Kirchhoff_conv(
                beamOEin, oe, beamOEglo, beamOEloc, xloc, zloc)
        else:
            return self._expose_Kirchhoff_CL(
                beamOEin, oe, beamOEglo, beamOEloc, xloc, zloc)

    def _expose_Kirchhoff_conv(
            self, beamOEin, oe, beamOEglo, beamOEloc, xloc, zloc):
        n = oe.local_n(beamOEloc.x, beamOEloc.y)
        cosGamma = (beamOEloc.a*n[-3] + beamOEloc.b*n[-2] + beamOEloc.c*n[-1])
#rotate the normal to virgin local system:
        ng = rs.Beam(0)
        ng.a, ng.b, ng.c = n[-3], n[-2], n[-1]
#        print 'ncos', np.degrees(np.arccos(ng.c))
        raycing.rotate_beam(ng, way=-1, pitch=oe.pitch, roll=oe.roll +
                            oe.positionRoll, yaw=oe.yaw, skip_xyz=True)
#        print 'ncos', np.degrees(np.arccos(ng.c))
#rotate the normal from virgin local to global system:
        a0, b0 = oe.bl.sinAzimuth, oe.bl.cosAzimuth
        if a0 != 0:
            ng.a, ng.b = raycing.rotate_z(ng.a, ng.b, b0, -a0)
        jk = 1j * beamOEglo.E[0] / rm.chbar * 1e7  # [mm^-1]

        blo = rs.Beam(nrays=len(zloc))  # local
        blo.x = np.asarray(xloc)
        blo.z = np.asarray(zloc)
        xglo = (self.center[0] + self.x[0]*blo.x +
                self.z[0]*blo.z)[:, np.newaxis]
        yglo = (self.center[1] + self.x[1]*blo.x +
                self.z[1]*blo.z)[:, np.newaxis]
        zglo = (self.center[2] + self.x[2]*blo.x +
                self.z[2]*blo.z)[:, np.newaxis]
        print self.center
        print self.x
        print self.z
        #aglo = self.center[0]
        #bglo = self.center[1] - oe.center[1]
        #cglo = self.center[2]
#        print 'aglo ', aglo
#        print 'bglo ', bglo
#        print 'cglo ', cglo
#        print 'ncos', np.degrees(np.arccos(ng.c))
        #pathAfter = (aglo**2 + bglo**2 + cglo**2)**0.5
        #print pathAfter.shape
        #cosAlpha = (aglo*ng.a + bglo*ng.b + cglo*ng.c) / pathAfter
#        print 'pi/2-alpha ', np.degrees(np.arcsin(cosAlpha))

#        print 'beamOEglo.x ', beamOEglo.x.min(), beamOEglo.x.max()
#        print 'beamOEglo.y ', beamOEglo.y.min(), beamOEglo.y.max()
#        print 'beamOEglo.z ', beamOEglo.z.min(), beamOEglo.z.max()
        aglo = xglo - beamOEglo.x
        bglo = yglo - beamOEglo.y
        cglo = zglo - beamOEglo.z

        #print aglo.shape
#        print 'aglo ', aglo.min(), aglo.max()
#        print 'bglo ', bglo.min(), bglo.max()
#        print 'cglo ', cglo.min(), cglo.max()
        pathAfter = (aglo**2 + bglo**2 + cglo**2)**0.5
        #print pathAfter.shape
        cosAlpha = (aglo*ng.a + bglo*ng.b + cglo*ng.c) / pathAfter
        print cosAlpha.shape
#        print 'pi/2-alpha ', np.degrees(np.arcsin(cosAlpha.min())),\
#            np.degrees(np.arcsin(cosAlpha.max()))
        path = beamOEloc.path + pathAfter
        #print "path.shape", path.shape
# averaged path:
        blo.path = np.sum(path, axis=1) / path.shape[1]
        c = (cosGamma+cosAlpha) * np.exp(jk*path) / (beamOEin.Jss+beamOEin.Jpp)
        blo.fieldKirchhoffS = np.sum(c * beamOEloc.Jss**0.5, axis=1)
        blo.fieldKirchhoffP = np.sum(c * beamOEloc.Jpp**0.5, axis=1)
        blo.fieldKirchhoffN = np.sum(c, axis=1)
        print "c.shape", c.shape
        blo.Jss[:] = abs(blo.fieldKirchhoffS)**2
        blo.Jpp[:] = abs(blo.fieldKirchhoffP)**2
        blo.E[:] = beamOEglo.E[0]
        blo.state[:] = 1
        #print (blo.E).shape
#        raise
        return blo

    def _expose_Kirchhoff_CL(
            self, beamOEin, oe, beamOEglo, beamOEloc, xloc, zloc):
        n = oe.local_n(beamOEloc.x, beamOEloc.y)
        cosGamma = (beamOEloc.a*n[-3] + beamOEloc.b*n[-2] + beamOEloc.c*n[-1])
#rotate the normal to virgin local system:
        ng = rs.Beam(0)
        ng.a, ng.b, ng.c = n[-3], n[-2], n[-1]
#        print 'ncos', np.degrees(np.arccos(ng.c))
        raycing.rotate_beam(ng, way=-1, pitch=oe.pitch, roll=oe.roll +
                            oe.positionRoll, yaw=oe.yaw, skip_xyz=True)
#        print 'ncos', np.degrees(np.arccos(ng.c))
#rotate the normal from virgin local to global system:
        a0, b0 = oe.bl.sinAzimuth, oe.bl.cosAzimuth
        if a0 != 0:
            ng.a, ng.b = raycing.rotate_z(ng.a, ng.b, b0, -a0)
#        jk = 1j * beamOEglo.E[0] / rm.chbar * 1e7  # [mm^-1]

        pic_dim = len(zloc)*len(xloc)
        blo = rs.Beam(nrays=pic_dim)  # local

        imax = np.int32(len(xloc))
        jmax = np.int32(len(zloc))

        nrays = np.int32(len(beamOEglo.E))

        center = np.float64(self.center)

        x = np.float64(self.x)
        z = np.float64(self.z)
        xloc_loc = np.float64(xloc)
        zloc_loc = np.float64(zloc)

        cosgamma_loc = cosGamma
        Jss_in_loc = beamOEin.Jss
        Jpp_in_loc = beamOEin.Jpp

        Jss_loc = beamOEloc.Jss
        Jpp_loc = beamOEloc.Jpp

        k_wave = beamOEglo.E / rm.chbar * 1e7

        bOEglo_coord = np.array([beamOEglo.x,
                                 beamOEglo.y,
                                 beamOEglo.z,
                                 0.*beamOEglo.x], order='F')
        surface_normal = np.array([ng.a, ng.b, ng.c, 0.*ng.c], order='F')

        bOEpath = beamOEloc.path
        blox_local = np.zeros(pic_dim, dtype=np.float64)
        bloz_local = np.zeros(pic_dim, dtype=np.float64)

        path_local = np.zeros(pic_dim, dtype=np.float64)

        KirchN_local = np.zeros(pic_dim, dtype=np.complex128)
        KirchS_local = np.zeros(pic_dim, dtype=np.complex128)
        KirchP_local = np.zeros(pic_dim, dtype=np.complex128)

        center_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=center)
        x_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                          self.cl_mf.COPY_HOST_PTR, hostbuf=x)
        z_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                          self.cl_mf.COPY_HOST_PTR, hostbuf=z)
        cosgamma_buf = cl.Buffer(
            self.cl_ctx, self.cl_mf.READ_ONLY |
            self.cl_mf.COPY_HOST_PTR, hostbuf=cosgamma_loc)
        xloc_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                             self.cl_mf.COPY_HOST_PTR, hostbuf=xloc_loc)
        zloc_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                             self.cl_mf.COPY_HOST_PTR, hostbuf=zloc_loc)
        Jss_in_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=Jss_in_loc)
        Jpp_in_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=Jpp_in_loc)
        Jss_loc_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                                self.cl_mf.COPY_HOST_PTR, hostbuf=Jss_loc)
        Jpp_loc_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                                self.cl_mf.COPY_HOST_PTR, hostbuf=Jpp_loc)
        k_wave_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_ONLY |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=k_wave)
        beamOEglo_buf = cl.Buffer(
            self.cl_ctx, self.cl_mf.READ_ONLY |
            self.cl_mf.COPY_HOST_PTR, hostbuf=bOEglo_coord)
        oe_surface_normal_buf = cl.Buffer(
            self.cl_ctx, self.cl_mf.READ_ONLY |
            self.cl_mf.COPY_HOST_PTR, hostbuf=surface_normal)
        beam_OE_loc_path_buf = cl.Buffer(
            self.cl_ctx, self.cl_mf.READ_ONLY |
            self.cl_mf.COPY_HOST_PTR, hostbuf=bOEpath)

        path_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                             self.cl_mf.COPY_HOST_PTR, hostbuf=path_local)
        blox_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                             self.cl_mf.COPY_HOST_PTR, hostbuf=blox_local)
        bloz_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                             self.cl_mf.COPY_HOST_PTR, hostbuf=bloz_local)
        KirchS_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=KirchS_local)
        KirchP_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=KirchP_local)
        KirchN_buf = cl.Buffer(self.cl_ctx, self.cl_mf.READ_WRITE |
                               self.cl_mf.COPY_HOST_PTR, hostbuf=KirchN_local)

        global_size = KirchN_local.shape
        local_size = None

        self.cl_program.integrate_kirchhoff(self.cl_queue,
                                            global_size,
                                            local_size,
                                            imax, jmax, nrays,
                                            center_buf, x_buf, z_buf,
                                            cosgamma_buf,
                                            xloc_buf, zloc_buf,
                                            Jss_in_buf, Jpp_in_buf,
                                            Jss_loc_buf, Jpp_loc_buf,
                                            k_wave_buf, beamOEglo_buf,
                                            oe_surface_normal_buf,
                                            beam_OE_loc_path_buf,
                                            path_buf, blox_buf, bloz_buf,
                                            KirchS_buf, KirchP_buf,
                                            KirchN_buf
                                            ).wait()

        cl.enqueue_read_buffer(self.cl_queue,
                               path_buf,
                               path_local).wait()
        cl.enqueue_read_buffer(self.cl_queue,
                               blox_buf,
                               blox_local).wait()
        cl.enqueue_read_buffer(self.cl_queue,
                               bloz_buf,
                               bloz_local).wait()
        cl.enqueue_read_buffer(self.cl_queue,
                               KirchS_buf,
                               KirchS_local).wait()
        cl.enqueue_read_buffer(self.cl_queue,
                               KirchP_buf,
                               KirchP_local).wait()
        cl.enqueue_read_buffer(self.cl_queue,
                               KirchN_buf,
                               KirchN_local).wait()

        blo.path = path_local
        blo.x = blox_local
        blo.z = bloz_local

        blo.fieldKirchhoffS = KirchS_local
        blo.fieldKirchhoffP = KirchP_local
        blo.fieldKirchhoffN = KirchN_local

        blo.Jss[:] = abs(blo.fieldKirchhoffS*np.conj(blo.fieldKirchhoffS))
        blo.Jpp[:] = abs(blo.fieldKirchhoffP*np.conj(blo.fieldKirchhoffP))

        blo.E[:] = beamOEglo.E[0]
        blo.state[:] = 1

#        raise
        return blo
