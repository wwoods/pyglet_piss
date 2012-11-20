
import pyglet
from pyglet_piss.layer import Layer

class Scene(object):
    """A scene is a collection of layers that make up a single user experience.
    """
    
    showFps = False
    showFps_doc = """Set to True to show the FPS in the lower-left corner"""
    
    @property
    def window(self):
        return self.app.window
    
    def __init__(self):
        self._layers = []
        self._isInit = False
        
        
    def addLayer(self, layer):
        self._layers.append(layer)
        layer._layerInit(self)
        
        
    def onDraw(self):
        """Called when we draw the scene, before any layers are drawn."""
        
        
    def onUpdate(self, dt):
        """Called when this scene should be updated; called before any layers
        have their onUpdate() called."""
        
        
    def quitScene(self):
        """Close this scene"""
        self.app.removeScene(self)
        
        
    def _sceneAction(self, player, action):
        """Call onAction() for each layer until one returns True.
        """
        i = len(self._layers)
        while i > 0:
            i -= 1
            r = self._layers[i].onAction(player, action)
            if r is True:
                break
        
        
    def _sceneDraw(self):
        """Draw self, then all layers"""
        self.onDraw()
        for l in self._layers:
            l.onDraw()
            
        if self.showFps:
            self.__fps.draw()
        
    
    def _sceneInit(self, app):
        """Called when added to an app"""
        if self._isInit:
            raise RuntimeError("Cannot be added to application twice")
        
        self._isInit = True
        self.app = app
        self.__fps = pyglet.clock.ClockDisplay()
        
        
    def _sceneUpdate(self, dt):
        """Calculate input, trigger actions, and then do any necessary updates.
        """
        # Input loop - look for new actions, map them, and reset
        for player in self.app.players:
            player.poll()
            player.update(dt)
            for action in player.actions:
                self._sceneAction(player, action)
            player.clearActions()
        
        # Run update methods
        firstLayer = None
        for i, l in reversed(list(enumerate(self._layers))):
            if l.suspendsLower:
                firstLayer = i
                break
            
        if firstLayer is None:
            self.onUpdate(dt)
            for l in self._layers:
                l.onUpdate(dt)
        else:
            for l in self._layers[i:]:
                l.onUpdate(dt)
        