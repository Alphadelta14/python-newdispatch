

class EventData(object):
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
    errors : list
        List of exceptions this event has encountered
    success : Bool
        Whether this event has successfully executed

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
        self.errors = []

    def cancel(self):
        """Cancel this event if possible"""
        if self.cancellable:
            self.cancelled = True

    def add_error(self, err):
        """Adds an error to the list of errors this event came across

        Parameters
        ----------
        err : Exception
        """
        self.errors.append(err)

    @property
    def success(self):
        """Whether or not this event has successfully executed"""
        return not self.cancelled and not self.errors
