import textwrap
import types
from typing import Tuple

import simpy
from simpy.events import NORMAL

from linsimpy.simpy import ReadableFilterStore


class TupleFilter(object):

    def __init__(self, pattern: Tuple):
        self.pattern = pattern

    def __call__(self, tup: Tuple):

        # check length
        if not len(tup) == len(self.pattern):
            return False

        # check each element of tuples
        for tup_val, pattern_val in zip(tup, self.pattern):

            # check tup value against formal type placeholders in pattern
            if isinstance(pattern_val, type):
                if not isinstance(tup_val, pattern_val):
                    return False
            # otherwise check for equality
            else:
                if not tup_val == pattern_val:
                    return False

        return True


class TupleSpace(object):
    """A tuple-space implementation based on the Linda coordination language.

    Supports duplicate tuples.
    """

    def __init__(self, env: simpy.Environment = None):
        self._env = env if env else simpy.Environment()
        self._store = ReadableFilterStore(self._env)

    # Linda

    def out(self, tup: Tuple):
        """Returns a simpy event which writes a tuple"""
        return self._store.put(tuple(tup))

    def in_(self, pattern: Tuple):
        """Returns a simpy event which atomically reads and and removes a tuple,
        waiting if necessary.
        """
        return self._store.get(TupleFilter(pattern))

    def rd(self, pattern: Tuple):
        """Returns a simpy event which non-destructively reads a tuple,
        waiting if necessary.
        """
        filter_store_get_event = self._store.read(TupleFilter(pattern))
        return filter_store_get_event

    def eval(self, tup: Tuple):
        """Returns a simpy process which evaluates tuples with simpy style
        generator describing the process as elements. Adds the tuple
        to the tuple-space when complete"""

        # To avoid confusion
        if isinstance(tup, types.GeneratorType):
            raise ValueError("Iterable such as tuple or list expected, not"
                             "generator. Try (generator,)!")
        try:
            iter(tup)
        except TypeError:
            raise ValueError(f"Input must be a tuple (or list) not {type(tup)}")

        generator_list = []
        for i, element in enumerate(tup):
            if isinstance(element, types.GeneratorType):
                generator_list.append((i, element))
        if not generator_list:
            raise TypeError('at least one generator expected in input tuple')

        def eval_process():
            tup_as_list = list(tup)
            proc_list = []
            idx_list = []
            for idx, gen in generator_list:
                proc = self._env.process(gen)
                proc_list.append(proc)
                idx_list.append(idx)

            # ret = yield self._env.all_of(proc_list)
            ret_list = (yield self._env.all_of(proc_list)).values()
            ret_list = list(ret_list)

            for idx, value in zip(idx_list, ret_list):
                tup_as_list[idx] = value

            yield self.out(tuple(tup_as_list))
            return tuple(tup_as_list)

        return self._env.process(eval_process())

    def inp(self, pattern: Tuple):
        """Atomically reads and removes—consumes—a tuple, raising KeyError if
        not found. """
        item = self._do_find(pattern)
        self._store.items.remove(item)
        return item

    def rdp(self, pattern: Tuple):
        """Non-destructively reads a tuple, raising KeyError if not found."""
        return self._do_find(pattern)
        # may have to inp and out without yielding control

    def _do_find(self, pattern):
        filter = TupleFilter(pattern)
        for item in self._store.items:
            if filter(item):
                return item
        raise KeyError(f"Tuple matching '{pattern}' not found")

    # store

    @property
    def items(self):
        """Return all tuples in store"""
        # TODO: limit access to store to ensure only tuples are added
        return self._store.items

    def __str__(self):
        wrapper = textwrap.TextWrapper(
            initial_indent='  ', subsequent_indent='  ', drop_whitespace=False,
            replace_whitespace=False)
        lines = []
        for tup in self.items:
            lines.append('(')
            for field in tup:
                # field_lines = wrapper.wrap(str(field))
                field_lines = str(field).splitlines()
                field_lines[-1] = field_lines[-1] + ','
                lines.extend(['  ' + l for l in field_lines])
            lines.append('),')
        return '\n'.join(lines)

"""
(
   field
   field
)
"""



class TupleSpaceEnvironment(TupleSpace):

    @property
    def now(self):
        """The current simulation time."""
        return self._env.now

    @property
    def active_process(self):
        """The currently active process of the environment."""
        return self._env.active_process

    def process(self, generator):
        raise Exception("Use eval() not process().")

    def timeout(self, delay, value=None):
        
        return self._env.timeout(delay, value)

    def event(self):
        
        return self._env.event()

    def all_of(self, events):
        
        return self._env.all_of(events)

    def any_of(self, events):
       
        return self._env.any_of(events)

    def schedule(self, event, priority=NORMAL, delay=0):
        """Schedule an *event* with a given *priority* and a *delay*."""
        return self._env.schedule(event, priority, delay)

    def peek(self):
        
        return self._env.peek()

    def step(self):
        """Process the next event.

        Raise an :exc:`EmptySchedule` if no further events are available.

        """
        return self._env.step()

    def run(self, until=None):
       
        return self._env.run(until)

    def exit(self, value=None):
     
        return self._env.exit(value)

