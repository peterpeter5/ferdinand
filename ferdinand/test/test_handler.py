from __future__ import absolute_import, unicode_literals
import unittest

from ferdinand.message_handler import is_new_message_available, get_indices_from_position


class TestMessageLogAnalysis(unittest.TestCase):

    def test_is_new_message_available(self):
        message_log = [0, 1]
        self.assertTrue(is_new_message_available(message_log, 0))
        self.assertFalse(is_new_message_available(message_log, 1))
        self.assertFalse(is_new_message_available(message_log, 5))

    def test_get_indices_from_position(self):
        message_log = [0, 1, "q", 3, "z"]
        self.assertEqual(get_indices_from_position(message_log, 2), (3, 4))
