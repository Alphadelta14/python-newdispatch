
from dispatch.events import Emitter


class Promise(Emitter):
    finished = False

    def done(self, data=None, success=True, err=None):
        """Indicate that this promise is complete

        This will now trigger its completion functions

        Parameters
        ----------
        data : object, optional
            Object passed into each callbacks EventData.data
        success : Bool, optional
            If successful (default), run the success callbacks. Else, the
            failure callbacks.
        err : Error
            If set, call the error callback. Generally failure callbacks
            get called with this
        """
        if success:
            self.fire('success', data=data, cancellable=False)
        else:
            self.fire('failure', data=data, cancellable=False)
        if err is not None:
            self.fire('error', data=err, cancellable=False)
        self.fire('complete', data=data, cancellable=False)
        self.all_off()
        self.finished = True

    def on(self, event, callback=None):
        """Hook a callback to an event

        See Also
        --------
        Emitter.on
        """
        # Do not allow hooking after completion
        if self.finished:
            raise RuntimeError('Promise has already completed')
        return super(Promise, self).on(event, callback)

    def throw(self, err):
        """Throw an exception and call off the success

        This will swallow the exception thrown.

        'error', 'failure', and 'complete' events are fired.

        Parameters
        ----------
        err : Exception
            The exception to provide to this promise
        """
        self.done(success=False, err=err)

    def fail(self, data=None):
        """Fail this progress and call done without success

        'failure' and 'complete' events are fired.
        """
        self.done(data, success=False)

    def success(self, callback=None):
        """Add a callback when this promise succeeds

        Parameters
        ----------
        callback : function(EventData)
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('success', callback)

    def failure(self, callback=None):
        """Add a callback when this promise fails. Generally this also
        gets called when the promise errs.

        Parameters
        ----------
        callback : function(EventData)
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('failure', callback)

    def error(self, callback=None):
        """Add a callback when this promise errs

        Parameters
        ----------
        callback : function(EventData)
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('error', callback)

    def complete(self, callback=None):
        """Add a callback when this promise completes regardless of its
        sucess

        Parameters
        ----------
        callback : function(EventData)
            Callback to call. If not set, this will be a decorator.
        """
        return self.on('complete', callback)

    @staticmethod
    def all(*promises, **kwargs):
        """Create a new promise that acts on the completion of all
        passed promises.

        'success' is fired if all promises are successful. 'fail' is fired
        as soon as any of them fail. 'error' is thrown if throw_error is True
        and any of them error.

        Parameters
        ----------
        promise_1 ... promise_n : Promise
            Promises to wait for
        throw_error : Bool, optional
            If False (default), this will continue until all promises are
            complete before throwing its failure. Else throw immediately.
        """
        new_promise = Promise()
        new_promise.waiting_for = list(promises)

        @new_promise.complete
        def cleanup(evt):
            new_promise.waiting_for = None

        def one_finished(evt):
            if new_promise.waiting_for:  # In case cleanup has been called
                new_promise.waiting_for.remove(evt.source)
            if not new_promise.waiting_for:
                new_promise.done()

        for promise in promises:
            promise.complete(one_finished)
            if kwargs.get('throw_error', False):
                promise.error(new_promise.throw)
            promise.failure(new_promise.fail)
        if not promises:
            new_promise.done()
        return new_promise

    @staticmethod
    def any(*promises, **kwargs):
        """Create a new promise that acts on the success of any of the
        passed promises.

        'success' is fired as soon as any promise succeeds. 'fail' is fired
        if all of them fail. 'error' is thrown if throw_error is True and
        and of them error.

        Parameters
        ----------
        promise_1 ... promise_n : Promise
            Promises to wait for
        throw_error : Bool, optional
            If False (default), this will continue until any promises are
            complete before throwing its failure. Else throw immediately.
        """
        new_promise = Promise()
        new_promise.waiting_for = list(promises)

        @new_promise.complete
        def cleanup(evt):
            new_promise.waiting_for = None

        def one_failed(evt):
            if new_promise.waiting_for:  # In case cleanup has been called
                new_promise.waiting_for.remove(evt.source)
            if not new_promise.waiting_for:
                new_promise.fail()

        for promise in promises:
            promise.success(new_promise.done)
            if kwargs.get('throw_error', False):
                promise.error(new_promise.throw)
            promise.failure(one_failed)
        if not promises:
            new_promise.done()
        return new_promise
