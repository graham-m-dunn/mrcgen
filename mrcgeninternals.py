import collections
import re

class Interval(collections.namedtuple("Interval", ["duration", "power"])):
    def __str__(self):
        return "[%g, %g]" % (self.duration, self.power)

class Set(object):
    def __init__(self, repeat, intervals):
        self.repeat = repeat
        self.intervals = intervals

    def __iter__(self):
        if isinstance(self.intervals, Interval):
            # this Set is just a repeat of one interval
            # output it n times
            for _ in xrange(self.repeat):
                yield self.intervals
        else:
            # this Set is a list of Intervals or sub-Sets
            for _ in xrange(self.repeat):
                for i in self.intervals:
                    if isinstance(i, Interval):
                        # this list item is an interval, output it
                        yield i
                    elif isinstance(i, Set):
                        # this is a sub-Set, iterate over it and yield
                        # it's intervals (this is the recursive bit)
                        for j in i:
                            yield j
                    else:
                        raise Exception("Unknown type in set: %s" % type(i))

    def reduce(self, parent=None, idx=None):
        """
        This will collapse intervals where repeat == 1 into their parent.
        """
        if parent is not None and self.repeat == 1:
            # self will be orphaned by this action, but we copy self.intervals into the parent
            parent.intervals[idx:idx+1] = self.intervals
            return True
        else:
            while True:
                for n, i in enumerate(self.intervals):
                    if isinstance(i, Set):
                        if i.reduce(self, n):
                            break
                else:
                    break # only if we didn't break out of the for-loop
        return False

    def __str__(self):
        return "%d x (%s)" % (self.repeat, ", ".join([str(i) for i in self.intervals]))

def parse_input(input_str):
    res = None
    bt = []
    while input_str:
        m = re.match("""(?x)
                        \s*(?P<repeat>[0-9]+)\s*x\s*\(\s*                              | # Set start
                        \s*\[\s*(?P<duration>[0-9.]+)\s*,\s*(?P<power>[0-9.]+)\s*\]\s* | # Interval
                        \s*(?P<operator>,|\))\s*                                       | # comma or Set end
                     """, input_str)
        if m is None:
            raise Exception("Parse error (at '%s')" % input_str)
        if m.group("repeat") is not None:
            if res is None:
                res = Set(int(m.group("repeat")), [])
                bt.append(res.intervals)
            else:
                if len(bt) == 0:
                    raise Exception("Not expecting a new repeat here (at '%s')" % input_str)
                bt[-1].append(Set(int(m.group("repeat")), []))
                bt.append(bt[-1][-1].intervals)
        elif m.group("operator") is not None:
            if m.group("operator") == ",":
                if len(bt) == 0:
                    # , only allowed in a set
                    raise Exception("Not expecting a comma here (at '%s')" % input_str)
            elif m.group("operator") == ")":
                if len(bt) == 0:
                    # , only allowed in a set
                    raise Exception("Unmatched ')' (at '%s')" % input_str)
                bt.pop()
            else:
                raise Exception("Unknown operator match (at '%s')" % input_str)
        elif m.group("duration") is not None:
            if len(bt) == 0:
                raise Exception("Not expecting an interval here (at '%s')" % input_str)
            bt[-1].append(Interval(float(m.group("duration")), float(m.group("power"))))
        else:
            raise Exception("Unknown parser error (at '%s')" % input_str)
        input_str = input_str[m.end():]
    if len(bt) != 0:
        raise Exception("Unmatched '(' (at end of input)")
    if res is not None:
        res.reduce()
    return res

