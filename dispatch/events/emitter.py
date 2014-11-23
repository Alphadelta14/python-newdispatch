
import functools


class Emitter(object):
    def on(self, event, callback=None):
        """Hook to an event

        Parameters
        ----------
        event : str
            Event to attach to
        callback : func
            Callback to call when event is fired. If not specified, this is
            used as a decorator

        Returns
        -------
        wrapper : func
            A decorator if callback is not set

        Examples
        --------
        >>> emitter = Emitter()
        >>> def my_func1():
                print('Event called me!')
        >>> emitter.on('some_event', my_func1)
        >>> @emitter.on('some_event')
            def my_func2():
                print('Event called me too!')
        >>> emitter.fire('some_event')
        Event called me!
        Event called me too!

        """
        try:
            self.event_handlers[event]
        except AttributeError:
            self.event_handlers = {event: []}
        except KeyError:
            self.event_handlers[event] = []

        if callback is None:
            def wrapper(func):
                self.event_handlers[event].append(callback)
                return func
            return wrapper
        else:
            self.event_handlers[event].append(callback)

    def off(self, event, callback):
        """Remove callback from an event

        Parameters
        ----------
        event : str
            Event to remove from
        callback : func
            Callback to be removed from this event. Only the first instance
            is removed

        Raises
        ------
        ValueError
            If the callback is not attached to this event
        """
        try:
            self.event_handlers[event].remove(callback)
        except (AttributeError, KeyError):
            raise ValueError('Callback not found')

    def once(self, event, callback=None):
        """Hook to an event once.

        Parameters
        ----------
        event : str
            Event to attach to
        callback : func
            Callback to call when event is fired. If not specified, this is
            used as a decorator

        Returns
        -------
        wrapper : func
            A decorator if callback is not set
        """

        if callback is None:
            def wrapper(func):
                @functools.wraps(func)
                def call_once(*args, **kwargs):
                    ret = func(*args, **kwargs)
                    self.off(event, call_once)
                    return ret
                self.on(event, call_once)
                return func
            return wrapper
        else:
            @functools.wraps(callback)
            def call_once(*args, **kwargs):
                ret = callback(*args, **kwargs)
                self.off(event, call_once)
                return ret
            self.on(event, call_once)

    def fire(self, event):
        """Fires an event

        Parameters
        ----------
        event : str
            Event to fire
        """
        try:
            callbacks = self.event_handlers[event]
        except (KeyError, AttributeError):
            pass
        else:
            for callback in callbacks:
                callback()
