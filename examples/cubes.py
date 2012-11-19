
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import pyglet
import pyglet_piss

from pyglet_piss import Actions

image = pyglet.image.create(32, 32, pyglet.image.SolidColorImagePattern(
        color = (255,0,0,255)))
square = pyglet.sprite.Sprite(image, x = 10, y = 10)

class GameScene(pyglet_piss.Scene):
    def __init__(self):
        pyglet_piss.Scene.__init__(self)
        self.addLayer(CubeLayer())
        self.addLayer(PlayerLayer())
        
    def onAction(self, player, action):
        raise NotImplementedError("Shouldn't be called")
    
    def onDraw(self):
        self.window.clear()


class CubeLayer(pyglet_piss.Layer3d):
    
    def __init__(self):
        pyglet_piss.Layer3d.__init__(self)
        self.x = 0.0
        self.y = 0.0
        
    def onAction(self, player, action):
        if action == Actions.TAP_LEFT:
            self.x -= 30.0
        elif action == Actions.TAP_RIGHT:
            self.x += 30.0
        elif action == Actions.TAP_UP:
            self.y += 30
        elif action == Actions.TAP_DOWN:
            self.y -= 30
            
        # Prevent onAction from being called in GameScene
        return True
    
    def onDraw3d(self):
        # Draw a 3d square at x, y
        from pyglet.gl import *
        glTranslatef(self.x, self.y, -100)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 100, 0)
        glVertex3f(100, 100, 0)
        glVertex3f(100, 0, 0)
        glEnd()
        glTranslatef(self.x, 0, -300)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 100, 0)
        glVertex3f(100, 100, 0)
        glVertex3f(100, 0, 0)
        glEnd()
        
    def onUpdate(self, dt):
        self.x += dt * 9.0
    

class PlayerLayer(pyglet_piss.Layer):
    PLAYER_HUD_WIDTH = 50
    PLAYER_HUD_HEIGHT = 32
    
    def __init__(self):
        pyglet_piss.Layer.__init__(self)
        self.label = pyglet.text.Label("LABEL", x = 0, y = 0)
    
    def onAction(self, player, action):
        if action == Actions.BTN1:
            self.quitScene()
        elif action == Actions.BTN2:
            self.suspendsLower = True
        elif action == Actions.BTN2_UP:
            self.suspendsLower = False
        else:
            return False
        return True
            
    def onDraw(self):
        px = 0
        for p in self.players:
            self.label.x = px
            self.label.text = "Player " + str(p.id)
            self.label.draw()
            px += 100


if __name__ == '__main__':
    pyglet_piss.app.run(GameScene())
    