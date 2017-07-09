from __future__ import absolute_import, unicode_literals

import os
from collections import deque


_BYTEORDER = 'big'

_msg_size_data_type = 8
_index_data_type = 8


class _RingBuffer(list):

    def __init__(self, iterable, max_size=0):
        self.max_size = int(max_size)
        self._buffer = super(_RingBuffer, self).__init__(deque(iterable, max_size))

    def append(self, p_object):
        super(_RingBuffer, self).append(p_object)
        if len(self) > self.max_size:
            self.pop(0)


# noinspection PyPep8Naming
def RingBuffer(iterable, max_size=0):
    if max_size == 0:
        return list(iterable)
    else:
        return _RingBuffer(iterable, max_size)


class LogElement(object):
    __slots__ = ('index', 'content', '_size')

    def __init__(self, index, content, binary_size=None):
        self._size = binary_size
        self.index = index
        self.content = content
    
    @property
    def _binary_index(self):
        return self.index.to_bytes(_index_data_type, _BYTEORDER)
    
    @property
    def _binary_msg(self):
        return self.content.encode()
    
    @property
    def _binary_msg_size(self):
        if self._size is None:
            self._size = len(self._binary_index + self._binary_msg)
        return self._size

    def __bytes__(self):
        return self._binary_index + self._binary_msg + self._binary_msg_size.to_bytes(_msg_size_data_type, _BYTEORDER)
    
    @classmethod
    def from_bytes(cls, byte_buffer):    
        end_index_msg_idx = _index_data_type
        start_index_msg_size = -_msg_size_data_type

        index = int.from_bytes(byte_buffer[0:end_index_msg_idx], _BYTEORDER)
        msg_size = int.from_bytes(byte_buffer[start_index_msg_size:], _BYTEORDER)
        content = byte_buffer[end_index_msg_idx:start_index_msg_size].decode()
        return LogElement(index, content, msg_size)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return all(
                (getattr(self, _slot) == getattr(other, _slot)
                 for _slot in self.__slots__)
            )

    def __repr__(self):
        return "log-element: idx: <%d>, content[0:10] <%s> binary_size: <%d>" % (
            self.index, self.content[0:10], self._binary_msg_size)


def save_message(file_, message, index):
    binary_msg = message.encode()
    binary_index = index.to_byttes(_index_data_type, _BYTEORDER)
    indexed_message = binary_index + binary_msg
    msg_size = len(indexed_message).to_bytes(_msg_size_data_type, _BYTEORDER)

    file_.write(indexed_message+msg_size)


def get_latest_message_index(file_):
    bytes_to_read = file_.seek(-_msg_size_data_type, os.SEEK_END)
    message_size = int.from_bytes(file_.read(bytes_to_read), _BYTEORDER)
    file_.seek(-message_size)
    message_size = int.from_bytes(file_.read(_index_data_type), _BYTEORDER)




