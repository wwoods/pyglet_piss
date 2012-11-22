
from pyglet_piss.lib.reprconf import Config as _reprConfig

class Config(_reprConfig):
    """Extension of reprconf that allows saving back to the last file specified
    in an update() call.
    
    Also allows merging rather than the original update - that is, keep any
    unspecified keys from previous updates, rather than overwriting the entire
    section.
    
    Example:
    
    c = SavingConfig()
    c.merge({ defaults })
    c.merge('game.ini')
    c.merge('game_local.ini')
    """      
    
    def merge(self, *args, **kwargs):
        noExistOk = kwargs.pop('noExistOk', False)
        try:
            other = _reprConfig(*args, **kwargs)
        except IOError:
            if noExistOk:
                return
            raise
        for k, v in other.iteritems():
            mergeFrom = self.get(k, {})
            mergeFrom.update(v)
            self[k] = mergeFrom
            
            
    def save(self, fname):
        """Save this config out to fname.
        """
        # We keep the output in a buffer before it's all generated; that way,
        # if there's an error, we don't screw up the old file by only
        # writing part of the output
        bufferOut = []
        for s, v in self.iteritems():
            bufferOut.append('[{0}]\n'.format(s))
            for k, kv in v.iteritems():
                bufferOut.append('{0} = {1}\n'.format(k, repr(kv)))
            bufferOut.append('\n')
        bufferOut = ''.join(bufferOut)
        with open(fname, 'w') as f:
            f.write(bufferOut)
            
            