
import pyglet

from pyglet_piss.player import JoystickPlayer, KeyboardPlayer

class Application(object):
    """Main pyglet_piss application object.  Handles input and layers.
    """
    
    def __init__(self, config):
        """config -- A pyglet_piss.Config instance, representing a section'd
        INI file.
        """
        self._scenes = []
        self.players = []
        self.conf = config
        
        myDisp = pyglet.window.get_platform().get_default_display()
        screen = myDisp.get_default_screen()
        
        dispConfig = config.get('display', {})
        fullscreen = dispConfig.get('fullscreen', False)
        if fullscreen:
            width = dispConfig.get('width') or screen.width
            height = dispConfig.get('height') or screen.height
        else:
            width = 1024
            height = width * screen.height / screen.width
        self.window = pyglet.window.Window(width = width, height = height,
                fullscreen = fullscreen)

        pyglet.clock.schedule(self.update)
        self.window.set_handler('on_draw', self.onDraw)
        self.window.set_handler('on_key_press', self.onKeyDown)
        self.window.set_handler('on_key_release', self.onKeyUp)
        
        # Any keyboard players?
        joysticks = pyglet.input.get_joysticks()
        possibleKeyboards = []
        for k, mappings in self.conf.iteritems():
            if k.startswith('keyboard_player_'):
                replaceWithJoystick = mappings.pop('replaceWithJoystick', True)
                if replaceWithJoystick:
                    # Will be defined as joystick player, if possible
                    possibleKeyboards.append(mappings)
                    continue 
                # Keyboard player definition
                self.players.append(KeyboardPlayer(mappings))
                
        # Do we need to add the possibles?
        usePossibles = len(possibleKeyboards) - len(joysticks)
        while usePossibles > 0:
            next = possibleKeyboards.pop(0)
            self.players.append(KeyboardPlayer(next))
            usePossibles -= 1
        
        # Set up joystick players
        for j in joysticks:
            self.players.append(JoystickPlayer(j))
        
        
    def addScene(self, scene):
        self._scenes.append(scene)
        scene._sceneInit(self)
        
        
    def onDraw(self):
        if len(self._scenes) == 0:
            pyglet.app.exit()
            return
        
        self._scenes[-1]._sceneDraw()
        
        
    def onKeyDown(self, key, modifiers):
        for p in self.players:
            if isinstance(p, KeyboardPlayer):
                p._onPress(key, modifiers)
                
                
    def onKeyUp(self, key, modifiers):
        for p in self.players:
            if isinstance(p, KeyboardPlayer):
                p._onRelease(key, modifiers)
        
        
    def removeScene(self, scene):
        self._scenes.remove(scene)
        
        
    def update(self, dt):
        if len(self._scenes) == 0:
            pyglet.app.exit()
            return
        
        self._scenes[-1]._sceneUpdate(dt)
        

def run(config, mainScene, **kwargs):
    app = Application(config, **kwargs)
    app.addScene(mainScene)
    pyglet.app.run()
    
