
from dispatch.events import Emitter


class Promise(Emitter):
    def done(self, success=True, err=None):
        """Indicate that this promise is complete

        This will now trigger its completion functions

        Parameters
        ----------
        success : Bool, optional
            If successful (default), run the success callbacks. Else, the
            failure callbacks.
        err : Error
            If set, call the error callback. Generally failure callbacks
            get called with this
        """
        if success:
            self.fire('success')
        else:
            self.fire('failure')
        if err is not None:
            self.fire('error')
        self.fire('complete')
        self.all_off()

    def success(self, callback=None):
        """Add a callback when this promise succeeds

        Parameters
        ----------
        callback : function
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('success', callback)

    def failure(self, callback=None):
        """Add a callback when this promise fails. Generally this also
        gets called when the promise errs.

        Parameters
        ----------
        callback : function
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('failure', callback)

    def error(self, callback=None):
        """Add a callback when this promise errs

        Parameters
        ----------
        callback : function
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('error', callback)

    def complete(self, callback=None):
        """Add a callback when this promise completes regardless of its
        sucess

        Parameters
        ----------
        callback : function
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('complete', callback)
