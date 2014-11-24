

class Event(object):
    """Object passed into emitted events

    Attributes
    ----------
    name : str
        Name of event
    source : Emitter
        Source of event
    data : object
        Data passed in
    cancelled : bool
        Whether this event should continue to propagate.
        Use Event.cancel() to cancel an event

    Methods
    -------
    cancel
        Cancel this event if cancellable
    """
    def __init__(self, name, source, data=None, cancellable=True):
        self.name = name
        self.source = source
        self.data = data
        self.cancelled = False
        self.cancellable = cancellable

    def cancel(self):
        """Cancel this event if possible"""
        if self.cancellable:
            self.cancelled = True
