"""
Generate MRC files for a computrainer
workout is a list of lists
Each list is an interval
Each interval is of the form [n, m], where n is the repeats for that
interval, and m is a list. m can be another interval, or a two-item list
that specifies duration and power of the interval.

processing:
1) break up the workout into discrete intervals (for interval in workout...)
2) Send each interval to be expanded sequentially by expand_interval()
3) Has the interval been fully expanded? (the first item is 1) yes: return
the two-item list contained in interval[1]
no: set the interval counter and extend the list by adding a multiple of
itself it in place
4) The slightly hacky part is to flatten the workout into a list of two-item
lists. Each time expand_workout gets called, it wraps its return in a list,
so that's where the additional lists come from. 
"""

import argparse

def course_header(version, units, description, filename):
    """
    Print the standard MRC file header
    """
    print "[COURSE HEADER]"
    print "VERSION = %s" % version 
    print "UNITS = %s" % units
    print "DESCRIPTION = %s" % description
    print "FILE NAME = %s" % filename
    print "MINUTES PERCENTAGE"
    print "[END COURSE HEADER]"

def flatten(item):
    """
    Hacky way to deal with intervals being wrapped
    in lists
    """
    # print "DEBUG: list is %s:" % item
    result = []
    for element in item:
        if isinstance(element[0], list):
            result.extend(flatten(element))
        else:
            result.append(element)
    #print "DEBUG: flattened list is %s:" % result
    return result
            
def course_data(final_workout):
    """
    Print the actual time/power data for the MRC
    file
    """
    print "[COURSE DATA]"
    start_time = 0
    end_time = 0
    for interval in final_workout:
        print "%f %f" % (start_time, interval[1])
        end_time += interval[0]
        print "%f %f" % (end_time, interval[1])
        start_time = end_time
    print "[END COURSE DATA]"


def expand_interval(interval):
    """
    Expands intervals to their simplest form (a list of
    lists of time/power tuples
    """
    #print "DEBUG: expand_interval got %s:" % interval
    if interval[0] == 1:
        expanded = interval[1]
        if len(expanded) > 2: # still a list of intervals
            return expand_workout(expanded)
        else:
            # print "DEBUG: returning %s" % expanded
            return expanded
    else:
        repeats = interval[0] - 1 # 4 repeats means add 3 more copies
        interval[0] = 1 # set the repeats so it'll get handled above
        new_interval = interval[1]
        new_interval.extend(repeats * new_interval[:]) # by reference
        # print "DEBUG: Sending to expand_workout with %s" % new_interval
        return expand_workout(new_interval)


def expand_workout(workout):
    """
    Takes a list of intervals and sends the parts to be
    expanded
    """
    # print "DEBUG: expand_workout got %s:" % workout
    return([expand_interval(interval) for interval in workout])


workout = []
course_header("2", "METRIC", "Golden Cheetah", "/Users/gdunn/Dropbox/test.mrc")
workout = expand_workout([[1, [10, 75]],
                          [5, [[1, [0.5, 100]],
                               [1, [0.5, 65]]]],
                          [1, [5, 75]],
                          [3, [[1, [10, 100]],
                               [1, [3, 65]]]],
                          [1, [5, 60]]])
course_data(flatten(workout))


