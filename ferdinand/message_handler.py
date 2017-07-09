from __future__ import absolute_import, unicode_literals


def is_new_message_available(message_log, my_index):
    return my_index < len(message_log) - 1


def get_indices_from_position(message_log, my_index):
    return tuple(range(my_index + 1, len(message_log)))


def on_new_message(message_log, handle_save, message):
    insertion_index = handle_save(message)
