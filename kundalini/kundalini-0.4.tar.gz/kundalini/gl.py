from pygame.surface import Surface
from OpenGL.GL import *
from OpenGL.GLU import *


#-----------------------------------------------------------------------
def init() -> None:
    glEnable(GL_DEPTH_TEST)
    glClearColor(1., 1., 1., 0.)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLight(GL_LIGHT0, GL_POSTION, (0, 1, 1, 0))


#-----------------------------------------------------------------------
def resize(screen:Surface, perspective:float=60.) -> None:
    width, height = screen.get_size()
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(perspective, float(width) / height, 1., 10000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
