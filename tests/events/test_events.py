
import unittest

from dispatch import Emitter, EventData


class State(object):
    pass


class TestEvents(unittest.TestCase):
    def test_init(self):
        emitter = Emitter()

    def test_order(self):
        order = []

        emitter = Emitter()

        @emitter.on('event:order')
        def callback(evt):
            order.append(1)

        @emitter.on('event:order')
        def callback(evt):
            order.append(2)

        emitter.fire('event:order')
        self.assertEqual(order, [1, 2])

    def test_defer(self):
        order = []

        emitter = Emitter()

        @emitter.on('event:order')
        def callback(evt):
            evt.defer()
            order.append(1)

        @emitter.on('event:order')
        def callback(evt):
            order.append(2)

        emitter.fire('event:order')
        self.assertEqual(order, [2, 1])

    def test_cancel(self):
        order = []

        emitter = Emitter()

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(1)
            evt.cancel()
            order.append(2)

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(3)

        emitter.fire('event:cancel')
        self.assertEqual(order, [1])

    def test_cancel_nested(self):
        order = []

        emitter = Emitter()

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(1)

            @emitter.on('event:cancel_nested')
            def callback_nested(subevt):
                order.append(2)
                evt.cancel()
                order.append(3)

            @emitter.on('event:cancel_nested')
            def callback_nested(subevt):
                order.append(4)
            emitter.fire('event:cancel_nested')
            order.append(5)

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(6)

        emitter.fire('event:cancel')
        self.assertEqual(order, [1, 2])

    def test_cancel_nested2(self):
        order = []

        emitter = Emitter()

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(1)

            @emitter.on('event:cancel_nested')
            def callback_nested(subevt):
                order.append(2)
                subevt.cancel()
                order.append(3)

            @emitter.on('event:cancel_nested')
            def callback_nested(subevt):
                order.append(4)
            emitter.fire('event:cancel_nested')
            order.append(5)

        @emitter.on('event:cancel')
        def callback(evt):
            order.append(6)

        emitter.fire('event:cancel')
        self.assertEqual(order, [1, 2, 5, 6])
