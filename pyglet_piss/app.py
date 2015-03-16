
from pyglet_piss.player import JoystickPlayer, KeyboardPlayer

import pyglet
import six

class _ApplicationWindow(object):
    @property
    def app(self):
        return self._app


    @property
    def height(self):
        return self._window.height


    @property
    def width(self):
        return self._window.width


    @property
    def window(self):
        return self._window


    def __init__(self, app, window, scene):
        self._app = app
        self._window = window
        self._scenes = [ scene ]
        scene._sceneInit(self)


    def addScene(self, scene):
        self._scenes.append(scene)
        scene._sceneInit(self)


    def clear(self, *args, **kwargs):
        self._window.clear(*args, **kwargs)


    def onDraw(self):
        if len(self._scenes) == 0:
            return

        self._scenes[-1]._sceneDraw()


    def removeScene(self, scene):
        self._scenes.remove(scene)



class Application(object):
    """Main pyglet_piss application object.  Handles input and layers.
    """

    @property
    def screens(self):
        """Returns a list of screens available on this computer.  E.g., if there
        are two entries, then there are two monitors, effectively."""
        return pyglet.window.get_platform().get_default_display().get_screens()


    @property
    def windows(self):
        return self._windows


    def __init__(self):
        """Constructor for the instance singleton.  User code entrypoint is run().
        """
        self._windows = []
        self.players = []
        self.conf = None


    def onKeyDown(self, key, modifiers):
        for p in self.players:
            if isinstance(p, KeyboardPlayer):
                p._onPress(key, modifiers)


    def onKeyUp(self, key, modifiers):
        for p in self.players:
            if isinstance(p, KeyboardPlayer):
                p._onRelease(key, modifiers)


    def run(self, config, *scenes, **kwargs):
        """config -- A pyglet_piss.Config instance, representing a section'd
        INI file.

        scenes - A list of scenes.  One window will be created per scene
                specified!
        """
        self.conf = config

        myDisp = pyglet.window.get_platform().get_default_display()
        screen = myDisp.get_default_screen()

        for scene in scenes:
            dispConfig = config.get('display', {})
            fullscreen = dispConfig.get('fullscreen', False)
            if fullscreen:
                width = dispConfig.get('width') or screen.width
                height = dispConfig.get('height') or screen.height
            else:
                width = dispConfig.get('width', 1024)
                height = dispConfig.get('height',
                        int(width * screen.height / screen.width))
            w = pyglet.window.Window(width = width, height = height,
                    fullscreen = fullscreen)
            aw = _ApplicationWindow(self, w, scene)
            self._windows.append(aw)

            w.set_handler('on_draw', aw.onDraw)
            w.set_handler('on_key_press', self.onKeyDown)
            w.set_handler('on_key_release', self.onKeyUp)
        pyglet.clock.schedule(self.update)

        # Any keyboard players?
        joysticks = pyglet.input.get_joysticks()
        possibleKeyboards = []
        for k, mappings in six.iteritems(self.conf):
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
        pyglet.app.run()


    def update(self, dt):
        # Input loop - look for new actions, map them, and reset
        inputScenes = self._windows
        for w in inputScenes:
            if len(w._scenes) == 0:
                pyglet.app.exit()
                return

        for player in self.players:
            player.poll()
            player.update(dt)

            for action in player.actions:
                # Each action must be consumable / stoppable by a True value
                # being returned from a handler.  We have ordered our windows
                # in preference of handling events, so go until we get a True
                for w in inputScenes:
                    if w._scenes[-1]._sceneAction(player, action) is True:
                        break

            player.clearActions()

        for w in self._windows:
            w._scenes[-1]._sceneUpdate(dt)

instance = Application()
