from __future__ import absolute_import, unicode_literals

import collections
import time
import itertools

from ferdinand.message_log.commit_log import RingBuffer

num_ops = 10**6


def append_many(seq):
    for i in range(0, num_ops):
        seq.append(i)
    return seq


def pop_many(seq):
    if isinstance(seq, list):
        func = lambda: seq.pop(0)
    else:
        func = lambda: seq.pop()

    for i in range(0, len(seq)):
        func()
    return seq


def take_from_x_to_end_many(seq):
    if isinstance(seq, list):
        func = lambda _seq, start: _seq[start: -1]
    elif isinstance(seq, collections.deque):
        func = _take_to_end
    for i in range(0, len(seq)):
        a = func(seq, i)
    return seq


def _take_to_end(deq, start):
    a = reversed(deq)
    return reversed(tuple(itertools.takewhile(lambda y: y > start, a)))

if __name__ == '__main__':
    for deq in (collections.deque(maxlen=num_ops//100), RingBuffer([], num_ops//100)):
        print("Start for: %s" % type(deq))
        start_time = time.time()
        deq = append_many(deq)
        print("append took <%f>" % (time.time() - start_time))
        start_rotate = time.time()
        deq = take_from_x_to_end_many(deq)
        print("slice took <%f>" % (time.time() - start_rotate))
        start_pop = time.time()
        deq = pop_many(deq)
        print("pop took <%f>" % (time.time() - start_pop))
        print("Operations took: <%f> seconds" % (time.time() - start_time))
        print()



