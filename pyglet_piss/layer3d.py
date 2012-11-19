
from pyglet.gl import *
from pyglet_piss import Layer

class Layer3d(Layer):
    """A 3-d layer; handles looking into a world and combining the 3d
    rendering with 2d
    """
    
    def onDraw(self):
        self._go3d()
        self.onDraw3d()
        self._go2d()
        
        
    def onDraw3d(self):
        """Here's where we should actually do the 3d rendering"""
        
        
    def _layerInit(self, scene):
        Layer._layerInit(self, scene)
        
        # Set up openGL
        glClearColor(1, 1, 1, 1)
        glColor3f(1, 0, 0)
        
        glEnable(GL_CULL_FACE)
        
        
    def _go2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w = self.window
        gluOrtho2D(0, w.width, 0, w.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        
        
    def _go3d(self):
        glClearDepth(1.0)
        glClear(GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        w = self.window
        gluPerspective(60.0, float(w.width) / w.height, 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        
        
        