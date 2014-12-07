
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
