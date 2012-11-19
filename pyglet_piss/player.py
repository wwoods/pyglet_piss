
import pyglet
from pyglet_piss.actions import Actions

class Player(object):
    """A base-class representation of a player as a distinct input system.
    """
    
    _base_id = 1
    _base_id_doc = """Incrementing series ID for each player"""
    
    def __init__(self):
        self.id = Player._base_id
        Player._base_id += 1
        self.actions = []
        self.actions_doc = """Actions queued and waiting processing"""
        self._recurring = {}
        self._recurring_doc = """Map of { action: Time till recur }"""
        self._buttonMap = {}
        self._buttonMap_doc = """Map of { inputId: Action.BTN id }"""
        self.x = 0.0
        self.y = 0.0
        
        
    def clearActions(self):
        """Clear all current actions, they have all been processed by UI.
        """
        self.actions = []
        
        
    def poll(self):
        """Update input system via polling, if needed (especially x and y)"""
        
        
    def startAction(self, action):
        """Issue action and set a timer for its recurring, even if it was
        already registered as recurring.  In other words, if the player can
        press a button faster than recurring, let them."""
        self.actions.append(action)
        self._recurring[action] = Actions.RECURRING_MINIMUM
        
        
    def stopAction(self, action):
        """Issue the stop message for action, and take it out of the
        recurring keys.  Skip this step if action is not currently part
        of the recurring step; this is only for convenience."""
        self.actions.append(action | Actions.ACTION_STOP_MASK)
        self._recurring.pop(action, None)
        
        
    def update(self, dt):
        """See if we need to recur anything"""
        for action, time in self._recurring.items():
            time -= dt
            if time < 0:
                time += Actions.RECURRING_INTERVAL
                self.actions.append(action)
            self._recurring[action] = time
    
        

class JoystickPlayer(Player):
    """Joystick input!"""
    
    TAP_THRESHOLD = 0.8
    
    def __init__(self, pygletJoystick):
        Player.__init__(self)
        self._joystick = pygletJoystick
        self._joystick.open()
        
        self._joystick.set_handler('on_joyaxis_motion', self._onMove)
        self._joystick.set_handler('on_joybutton_press', self._onPress)
        self._joystick.set_handler('on_joybutton_release', self._onRelease)
        
        
    def _onMove(self, joystick, axis, val):
        if axis == 'x':
            o = self.x
            self.x = val
            if val >= self.TAP_THRESHOLD:
                # Possible tap right?
                if o < self.TAP_THRESHOLD:
                    self.startAction(Actions.TAP_RIGHT)
            else:
                # No longer 
                self.stopAction(Actions.TAP_RIGHT)
                
            if val <= -self.TAP_THRESHOLD:
                # Possible tap left?
                if o > -self.TAP_THRESHOLD:
                    self.startAction(Actions.TAP_LEFT)
            else:
                # No longer 
                self.stopAction(Actions.TAP_LEFT)
        elif axis == 'y':
            o = self.y
            self.y = val
            if val >= self.TAP_THRESHOLD:
                # Possible tap down?
                if o < self.TAP_THRESHOLD:
                    self.startAction(Actions.TAP_DOWN)
            else:
                # No longer 
                self.stopAction(Actions.TAP_DOWN)
                
            if val <= -self.TAP_THRESHOLD:
                # Possible tap up?
                if o > -self.TAP_THRESHOLD:
                    self.startAction(Actions.TAP_UP)
            else:
                # No longer 
                self.stopAction(Actions.TAP_UP)
    
    
    def _onPress(self, joystick, button):
        realBtn = self._buttonMap.get(button, Actions.BTN_BASE + button)
        self.startAction(realBtn)
        
        
    def _onRelease(self, joystick, button):
        realBtn = self._buttonMap.get(button, Actions.BTN_BASE + button)
        self.stopAction(realBtn)

