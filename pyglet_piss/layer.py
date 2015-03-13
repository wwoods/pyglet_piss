
class Layer(object):
    """A renderable, updateable, input-handling segment of the display.
    """
    
    suspendsLower = False
    suspendsLower_doc = """True if any lower layers' update functions
            should not be called (drawing still occurs)."""

    scissorBox_doc = """Tuple of (x, y, w, h) in gl window coordinates.  Scissor
            test will be applied if this is set.  It is up to the scene to adjust
            its rendering process to self.scissorBox as desired."""
            
    @property
    def players(self):
        return self.scene.app.players
        
    @property
    def window(self):
        return self.scene.app.window


    def __init__(self):
        self.__isInit = False
        self.scene = None
        self.scissorBox = None
        
    
    def onAction(self, player, action):
        """Called when this layer has access to input and a player performs
        an action that was not handled by a higher layer.  Should return
        True if the event was handled."""
        return False
    
    
    def onDraw(self):
        """Called when this layer should draw."""
        
        
    def onUpdate(self, dt):
        """Called when this layer should update its members; dt is the number
        of seconds since the last update (multiply any action with quantity
        by this to regulate game speed)."""
        
        
    def pushLayer(self, layer):
        """Push a layer on top of this one; if this layer is not yet added
        to the hierarchy, the new layer will be added after this one once
        this layer is added."""
        if self.scene is None:
            self.__layers.append(layer)
        else:
            self.scene.addLayer(layer)
        
    
    def remove(self):
        """Removes self from app's layers.
        """
        self.scene.removeLayer(self)
        
    
    def quitScene(self):
        """Looking at the app's layers, remove everything after and including
        the uppermost scene.
        """
        self.scene.quitScene()
        
            
    def _layerInit(self, scene):
        """Called when added to application (added to scene) for first
        time.
        """
        if self.__isInit:
            # Already initialized and added, all is well
            raise RuntimeError("Cannot add layer twice")
        
        self.__isInit = True
        self.scene = scene

