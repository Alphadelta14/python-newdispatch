

class EventException(BaseException):
    pass


class EventCancelled(EventException):
    def __init__(self, evt):
        EventException.__init__(self)
        self.evt = evt


class EventDeferred(EventException):
    pass


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
    deferred : Bool
        If True, this is the second time this function is called

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
        self.deferred = False

    def cancel(self):
        """Cancel this event if possible

        This halts the active callback
        """
        if self.cancellable:
            self.cancelled = True
        raise EventCancelled(self)

    def defer(self):
        """Call the current callback again later.

        This will cause all lines before the defer to run again, so please
        use at the start of the file.

        Examples
        --------
        >>> emitter = Emitter()
        >>> @emitter.on('some_event')
            def my_func1(evt):
                evt.defer()
                print('Callback #1 called!')
        >>> @emitter.on('some_event')
            def my_func2(evt):
                print('Callback #2 called!')
        >>> emitter.fire('some_event')
        Callback #2 called!
        Callback #1 called!
        """
        if not self.deferred:
            raise EventDeferred

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
