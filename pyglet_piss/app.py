
import pyglet

from pyglet_piss.player import JoystickPlayer

class Application(object):
    """Main pyglet_piss application object.  Handles input and layers.
    """
    
    def __init__(self):
        self._scenes = []
        self.players = []
        
        myDisp = pyglet.window.get_platform().get_default_display()
        screen = myDisp.get_default_screen()
        
        width = 1024
        height = width * screen.height / screen.width 
        self.window = pyglet.window.Window(width = width, height = height)

        pyglet.clock.schedule(self.update)
        self.window.set_handler('on_draw', self.onDraw)
        
        # Set up players
        for j in pyglet.input.get_joysticks():
            self.players.append(JoystickPlayer(j))
        
        
    def addScene(self, scene):
        self._scenes.append(scene)
        scene._sceneInit(self)
        
        
    def onDraw(self):
        if len(self._scenes) == 0:
            pyglet.app.exit()
            return
        
        self._scenes[-1]._sceneDraw()
        
        
    def removeScene(self, scene):
        self._scenes.remove(scene)
        
        
    def update(self, dt):
        if len(self._scenes) == 0:
            pyglet.app.exit()
            return
        
        self._scenes[-1]._sceneUpdate(dt)
        

def run(mainScene, **kwargs):
    app = Application(**kwargs)
    app.addScene(mainScene)
    pyglet.app.run()
    