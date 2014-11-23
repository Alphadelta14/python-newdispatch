
import unittest

from dispatch import Promise


class State(object):
    pass


class TestPromise(unittest.TestCase):
    def test_init(self):
        promise = Promise()
        self.assertEqual(promise.finished, False)

    def test_success(self):
        promise = Promise()
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)

    def test_failure(self):
        promise = Promise()
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 1)

    def test_complete(self):
        promise = Promise()
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1

        @promise.complete
        def failure():
            state.complete += 1
        state.success = 0
        state.failure = 0
        state.complete = 0
        promise.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)
        self.assertEqual(state.complete, 1)

    def test_complete2(self):
        promise = Promise()
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1

        @promise.complete
        def failure():
            state.complete += 1
        state.success = 0
        state.failure = 0
        state.complete = 0
        promise.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 1)
        self.assertEqual(state.complete, 1)

    def test_complete_once(self):
        promise = Promise()
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1

        @promise.complete
        def failure():
            state.complete += 1
        state.success = 0
        state.failure = 0
        state.complete = 0
        promise.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)
        self.assertEqual(state.complete, 1)
        promise.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)
        self.assertEqual(state.complete, 1)
        promise.done(False)
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)
        self.assertEqual(state.complete, 1)

    def test_no_bind_after_done(self):
        promise = Promise()
        promise.done()

        def success():
            pass

        with self.assertRaises(RuntimeError):
            promise.success(success)

    def test_all(self):
        promise1 = Promise()
        promise2 = Promise()
        promise = Promise.all(promise1, promise2)
        self.assertEqual(promise.remaining, 2)
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise1.done()
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 0)
        promise2.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)

    def test_all2(self):
        promise1 = Promise()
        promise2 = Promise()
        promise = Promise.all(promise1, promise2)
        self.assertEqual(promise.remaining, 2)
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise1.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 1)
        promise2.done()
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 1)

    def test_any(self):
        promise1 = Promise()
        promise2 = Promise()
        promise = Promise.any(promise1, promise2)
        self.assertEqual(promise.remaining, 2)
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise1.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)
        promise2.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)

    def test_any2(self):
        promise1 = Promise()
        promise2 = Promise()
        promise = Promise.any(promise1, promise2)
        self.assertEqual(promise.remaining, 2)
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise1.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 0)
        promise2.done()
        self.assertEqual(state.success, 1)
        self.assertEqual(state.failure, 0)

    def test_any3(self):
        promise1 = Promise()
        promise2 = Promise()
        promise = Promise.any(promise1, promise2)
        self.assertEqual(promise.remaining, 2)
        state = State()

        @promise.success
        def success():
            state.success += 1

        @promise.failure
        def failure():
            state.failure += 1
        state.success = 0
        state.failure = 0
        promise1.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 0)
        promise2.done(False)
        self.assertEqual(state.success, 0)
        self.assertEqual(state.failure, 1)
