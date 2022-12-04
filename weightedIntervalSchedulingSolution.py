import numpy as np
import bisect


########################################
# Each interval is represented as a 4-tuple (id, s, f, v)
# where id is the "name" of the interval (string)
# s:: float. Start time of interval
# f:: float. Finish time
# v:: float. Value of the best interval
#
# So, for example, intervals[i][1] is the start of the i-th input interval.
# and intervals[i][2] is its finish time.
########################################

def predecessors(ints_by_f):
    # Assumes list of intervals is sorted by finish time.
    # And assumes a dummy interval has been added at the start. 
    p = [None] * len(ints_by_f)
    finish_times = [x[2] for x in ints_by_f]
    for i in range(1, len(ints_by_f)):
        j = bisect.bisect(finish_times, ints_by_f[i][1], hi = i) 
        # bisect uses binary search to find the first index j for which ints_by_f[j][2] > ints_by_f[i][1]
        # That is, j is the first interval in the sorted list that conflicts with i
        p[i] = j -1 
    return p


def computeMaxValues(intervals, verbose = False):
    assert len(intervals) >= 3
    ints_by_f = intervals.copy() # Make a copy so we don't mess up the input.

    # Sort by finish time
    ints_by_f.sort(key = (lambda x: x[2]))
    # Add a dummy interval at the start so that something can have a predecessor of 0
    ints_by_f = [("dummy", -np.inf, -np.inf, 0)] + ints_by_f

    # Compute the predecessor for each item
    p = predecessors(ints_by_f)
    
    values = [x[3] for x in ints_by_f] # this extracts just the values, for easy reference.

    # Fill the table:
    # opt[i] is the value of the heaviest ok set 
    # among vertices 0,1,...,i.
    opt = [None] * (len(ints_by_f))
    opt[0] = 0
    for i in range(1, len(ints_by_f)):
        opt[i] = max(opt[i-1],
                         opt[ p[i] ] + values[i])
        if verbose:
            print("We're done with i = ", i)
            print("Opt = ", opt)
            input("proceed?")
    return opt, ints_by_f, values, p

def computeOptSet(intervals, opt, ints_by_f, values, p, verbose = False):
    assert len(values) >= 3
    #Now compute the optimal set
    optset = []
    i = len(ints_by_f) - 1
    while i > 0:
        # At this point, we know we should use the best subset among {1,...,i}
        if verbose:
            print("Now looking at best subset among 1 to i=", i)
        if opt[i] == opt[i-1]:  # We know NOT to use interval i
            # So proceed to add best subset among {1,...,i-1}
            i = i-1
        else: # We know that we SHOULD use interval i
            optset.append(i)
            if verbose:
                print("Adding i=",i)
            # So proceed to add best subset among {1,...,p[i]}
            i = p[i]
    optset.reverse() # Sort by increasing finish time.
    # Convert this to a list of interval IDs
    opt_IDs = []
    for x in optset:
        opt_IDs.append(ints_by_f[x][0]) # Add ID of interval x.
    return opt_IDs

