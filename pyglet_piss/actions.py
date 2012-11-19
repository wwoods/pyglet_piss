
class Actions(object):
    """Static class to hold all of the available actions"""
    
    ACTION_STOP_MASK = 0x8000
    
    BTN_BASE = 0x0001 # First ID of button
    BTN1 = 0x0001
    BTN1_UP = BTN1 | ACTION_STOP_MASK
    BTN2 = 0x0002
    BTN2_UP = BTN2 | ACTION_STOP_MASK
    BTN3 = 0x0003
    BTN3_UP = BTN3 | ACTION_STOP_MASK
    BTN4 = 0x0004
    BTN4_UP = BTN4 | ACTION_STOP_MASK
    BTN5 = 0x0005
    BTN5_UP = BTN5 | ACTION_STOP_MASK
    
    TAP_LEFT = 0x0201
    TAP_UP = 0x0202
    TAP_RIGHT = 0x0203
    TAP_DOWN = 0x0204
    
    RECURRING_doc = """Any actions in this list will automatically be 
            "recurred" at RECURRING_INTERVAL.  For instance, when you press
            an arrow key on the keyboard, after a little bit, applications act
            like the arrow key is being pressed more times.  This creates that
            behavior."""
    RECURRING_INTERVAL = 0.1 # seconds
    RECURRING_MINIMUM = 0.5 # seconds before recurring
    