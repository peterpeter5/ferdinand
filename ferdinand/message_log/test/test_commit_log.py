from __future__ import absolute_import, unicode_literals
import unittest

from ferdinand.message_log.commit_log import RingBuffer, LogElement


class TestRingBuffer(unittest.TestCase):

    def test_unbounded_ringbuffer(self):
        unbounded = RingBuffer((1, 2, 3, 4, 5))
        self.assertEqual(unbounded, [1, 2, 3, 4, 5])
        unbounded.append(6)
        self.assertEqual(unbounded, [1, 2, 3, 4, 5, 6])

    def test_bounded_ringbuffer_init(self):
        bounded = RingBuffer((1, 2, 3, 4, 5), 3)
        self.assertEqual(bounded, [3, 4, 5])

    def test_bounded_append(self):
        bounded = RingBuffer([], 3)
        bounded.append(3)
        bounded.append(2)
        bounded.append(1)
        self.assertEqual([3, 2, 1], bounded)
        bounded.append(4)
        self.assertEqual([2, 1, 4], bounded)


class TestLogElement(unittest.TestCase):

    def test_serialization_and_deserialization(self):
        log_elem = LogElement(12, "asdfasdf")
        self.assertEqual(log_elem, LogElement.from_bytes(bytes(log_elem)))
