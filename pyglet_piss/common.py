
import functools

def frameCachedProperty(f):
    # Decorates a property getter, that clears out every frame
    cname = f.__name__
    missing = {}

    @functools.wraps(f)
    def wrapped(self):
        cached = getattr(self, '_frameCache__', None)
        if cached is None:
            cached = self._frameCache__ = {}

        result = cached.get(cname, missing)
        if result is missing:
            cached[cname] = result = f(self)
        return result
    return wrapped
def __clearFrameCached(self):
    self._frameCache__ = {}
frameCachedProperty.clear = __clearFrameCached
