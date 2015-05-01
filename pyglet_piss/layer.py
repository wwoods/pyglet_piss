
import pyglet.gl as gl

class Layer(object):
    """A renderable, updateable, input-handling segment of the display.

    Where stuff gets rendered depends on both localBounds and scissor().
    """

    localBounds = None
    localBounds_doc = """Maps the screen's left, bottom, right, and top as these
            coordinates locally, with the caveat that the result is always
            uniform (10 pixels in the X-dimension covers the same distance as
            10 pixels in the Y-dimension).  Defaults to None, meaning pixel
            coordinates are used.  Otherwise, must be a 4-tuple: (left, bottom,
            right, top).

            Note that the scissorMode tranform denotes how any discrepency
            is handled between the specified system's aspect and the scene's
            aspect ratio.  If not None, and SCISSOR_CLIP is specified, then
            an exception is raised.
            """


    SCISSOR_STRETCH = "scissor-stretch"
    SCISSOR_SCALE_BIG = "scissor-scale-big"
    SCISSOR_SCALE_SMALL = "scissor-scale-small"
    SCISSOR_SCALE_WIDTH = "scissor-scale-width"
    SCISSOR_SCALE_HEIGHT = "scissor-scale-height"
    SCISSOR_CLIP = "scissor-clip"
    scissorMode = SCISSOR_SCALE_BIG
    scissorMode_doc = """The way that calling self.scissor() affects this
            layer's rendering.  Scissoring never affects the layer's local
            origin (0, 0).  However, the behavior across the width and height
            of the scene depends on the scissorMode parameter:

            Layer.SCISSOR_STRETCH will cause display
            coordinates to not be modified, but causes distortion if the
            scissor box's aspect ratio does not match the scene.

            Layer.SCISSOR_SCALE_BIG will keep the layer's center in the middle of
            the center box, again not modifying display coordinates within the
            layer.  However, the new scale will be uniform, and will clip the
            smaller aspect dimension.

            Layer.SCISSOR_SCALE_SMALL is like SCISSOR_SCALE_BIG except the layer
            will not be clipped at all, it will just have blank areas at either
            extreme.

            Layer.SCISSOR_SCALE_WIDTH always scales the display width, clipping
            or adding blank space as needed to preserve uniformity with height.

            Layer.SCISSOR_SCALE_HEIGHT always scales the display height,
            clipping or adding blank space as needed to preserve uniformity with
            width.

            Layer.SCISSOR_CLIP sets the local coordinates to the same size as
            its renderable area, and makes the layer responsible for any
            view scaling.  This is useful for preserving pixel-perfect behavior.
            Use self.left, self.top, self.right, and self.bottom to determine
            the range of displayed pixels.
            """

    suspendsLower = False
    suspendsLower_doc = """True if any lower layers' update functions
            should not be called (drawing still occurs)."""


    @property
    def bottom(self):
        """Returns the local-space bottom boundary of this layer."""
        return self.coordsLocal[1]


    @property
    def center(self):
        """Returns the local-space center of this layer."""
        cl = self.coordsLocal
        return (cl[0] + cl[2] * 0.5, cl[1] + cl[3] * 0.5)


    @property
    def coordsLocal(self):
        """Returns (left, bottom, w, h) for local-space."""
        # Calculate our centers and half-dimensions, and the screen aspect
        # ratio that has been assigned to us
        lx = 0
        ly = 0
        lw = 0
        lh = 0
        if self._scissorBox is None:
            if self.localBounds is None:
                return (0, 0, self.scene.width, self.scene.height)
            sa = self.scene.width * 1.0 / self.scene.height
        else:
            sa = self._scissorBox[2] * 1.0 / self._scissorBox[3]

        if self.localBounds is None:
            lx = self.scene.width * 0.5
            ly = self.scene.height * 0.5
            lw = lx
            lh = ly
        else:
            lw = (self.localBounds[2] - self.localBounds[0]) * 0.5
            lh = (self.localBounds[3] - self.localBounds[1]) * 0.5
            lx = self.localBounds[0] + lw
            ly = self.localBounds[1] + lh

        # Now, we have our coordinates and the screen aspect ratio.  Do some
        # processing
        if self.scissorMode == Layer.SCISSOR_CLIP:
            if self.localBounds is not None:
                raise ValueError("Layer.SCISSOR_CLIP cannot be used with "
                        "Layer.localBounds")

            # Special case, return our scissor box clipped to
            return (0, 0, self._scissorBox[2], self._scissorBox[3])
        elif self.scissorMode == Layer.SCISSOR_STRETCH:
            # Another special case, just leave our local zone as-is
            pass
        elif self.scissorMode == Layer.SCISSOR_SCALE_BIG:
            la = lw / lh
            if la > sa:
                lw = lh * sa
            else:
                lh = lw / sa
        elif self.scissorMode == Layer.SCISSOR_SCALE_SMALL:
            la = lw / lh
            if la > sa:
                lh = lw / sa
            else:
                lw = lh * sa
        elif self.scissorMode == Layer.SCISSOR_SCALE_HEIGHT:
            lw = lh * sa
        elif self.scissorMode == Layer.SCISSOR_SCALE_WIDTH:
            lh = lw * sa
        else:
            raise NotImplementedError()

        if self.localBounds is None:
            lx = lw
            ly = lh
        return (lx - lw, ly - lh, lw * 2.0, lh * 2.0)


    @property
    def coordsScreen(self):
        """Returns (left, bottom, w, h) for screen-space."""
        if self._scissorBox is None:
            return (0, 0, self.scene.width, self.scene.height)
        return self._scissorBox


    @property
    def height(self):
        """Returns the local-space height of this layer."""
        return self.coordsLocal[3]


    @property
    def left(self):
        """Returns local-space left boundary of this layer."""
        return self.coordsLocal[0]


    @property
    def players(self):
        return self.scene.window.app.players


    @property
    def right(self):
        """Returns local-space right boundary of this layer."""
        cl = self.coordsLocal
        return cl[0] + cl[2]


    @property
    def screenHeight(self):
        """Returns screen-space height of this layer."""
        if self._scissorBox is None:
            return self.scene.height
        return self._scissorBox[3]


    @property
    def screenScale(self):
        """Returns the scale from local to screen coordinates."""
        cl = self.coordsLocal
        cs = self.coordsScreen
        return max(cs[2] / cl[2], cs[3] / cl[3])


    @property
    def screenWidth(self):
        """Returns screen-space width of this layer."""
        if self._scissorBox is None:
            return self.scene.width
        return self._scissorBox[2]


    @property
    def top(self):
        """Returns the local-space top boundary of this layer."""
        cl = self.coordsLocal
        return cl[1] + cl[3]


    @property
    def width(self):
        """Returns the render-space width of this layer."""
        return self.coordsLocal[2]


    @property
    def window(self):
        return self.scene.window


    def __init__(self):
        self.__isInit = False
        self.scene = None
        self._scissorBox = None


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


    def preDraw(self):
        """Called right before this layer draws; establishes e.g. scissor box
        and scaling."""
        if self._scissorBox is not None:
            gl.glEnable(gl.GL_SCISSOR_TEST)
            gl.glScissor(*self._scissorBox)

        self._layerProjectLocalToScreen()


    def postDraw(self):
        """Called right after this layer draws; should revert any changes from
        preDraw()."""
        self._layerProjectLocalToScreenUndo()

        if self._scissorBox is not None:
            gl.glDisable(gl.GL_SCISSOR_TEST)


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


    def scissor(self, x = None, y = None, width = None, height = None):
        """In window coordinates, declares a scissor box to constrain this layer to.
        The Layer property scissorMode (from Layer.SCISSOR_STRETCH or
        Layer.SCISSOR_CLIP) determines how the layer's rendering code reacts to
        this.  If all parameters are None, then scissoring is turned off.  If
        any parameters are not None, then x and y default to 0, and width and
        height default to the scene width and height."""
        if x is None and y is None and width is None and height is None:
            self._scissorBox = None
        else:
            x = int(x) if x is not None else 0
            y = int(y) if y is not None else 0
            width = int(width) if width is not None else self.scene.width - x
            height = int(height) if height is not None else self.scene.height - y
            self._scissorBox = (x, y, width, height)


    def quitScene(self):
        """Looking at the app's layers, remove everything after and including
        the uppermost scene.
        """
        self.scene.quitScene()


    def translateForPixels(self, x, y):
        """Returns a context manager that translates to x, y in local coords and
        then changes the scaling so that subsequent rendering happens in
        pixel space.  Useful to get around scaling."""
        cl = self.coordsLocal
        cs = (0, 0, self.scene.width, self.scene.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.gluOrtho2D(cs[0], cs[2], cs[1], cs[3])
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        s = self._layerMapToScreen(x, y)
        gl.glTranslatef(s[0], s[1], 0.0)
        return _RestoreProjectionAndModelview()


    def _layerInit(self, scene):
        """Called when added to application (added to scene) for first
        time.
        """
        if self.__isInit:
            # Already initialized and added, all is well
            raise RuntimeError("Cannot add layer twice")

        self.__isInit = True
        self.scene = scene


    def _layerProjectLocalToScreen(self):
        """Maps self.coordLocal to self.coordScreen within OpenGL."""
        if self._scissorBox is None and self.localBounds is None:
            return
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        # gluOrtho2D declares the render space for the corners of the window.
        # So, we want to set it up in such a way that our layer renders in
        # the right place.  In other words, determine window corners that
        # map cl -> cs.  All clipping, etc is already handled by the coordsLocal
        # getter.
        cs = self.coordsScreen
        cl = self.coordsLocal
        sw = self.scene.width
        sh = self.scene.height

        # Determine the window width and height.  We want a local-sized chunk
        # of this to correspond to a screen-sized chunk of the screen.  That is,
        # cl[2] / ww == cs[2] / sw
        ww = cl[2] * sw / cs[2]
        wh = cl[3] * sh / cs[3]

        # cs[0] / sw = (x - nx) / ww
        nx = cl[0] - cs[0] * ww / sw
        ny = cl[1] - cs[1] * wh / sh
        gl.gluOrtho2D(nx, nx+ww, ny, ny+wh)
        gl.glMatrixMode(gl.GL_MODELVIEW)


    def _layerProjectLocalToScreenUndo(self):
        """Undoes the _layerProjectLocalToScreen() operation."""
        if self._scissorBox is None and self.localBounds is None:
            return
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)


    def _layerMapToScreen(self, localX, localY):
        """maps a local x and y to screen coords."""
        cl = self.coordsLocal
        cs = self.coordsScreen

        interpX = (localX - cl[0]) / cl[2]
        interpY = (localY - cl[1]) / cl[3]
        return (cs[0] + interpX * cs[2], cs[1] + interpY * cs[3])



class _RestoreProjectionAndModelview(object):
    def __enter__(self):
        return self


    def __exit__(self, typ, val, tb):
        if typ is None:
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPopMatrix()
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPopMatrix()
