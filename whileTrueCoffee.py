########################################
Li Xi
lxi@bu.edu
CS 330 Algorithms
########################################


import sys
import numpy as np
import os


def parseInput(filename=None):
    if filename == None:
        try:
            weights = readIntList(sys.stdin)
        except:
            False, "Error parsing standard input as sequence of integers."
    else:
        try:
            with open(filename, 'r') as f:
                weights = readIntList(f)
        except:
            False, "Error parsing input file as sequence of integers."
    return True, weights


def readIntList(f):
    ints_list = []
    for line in f.readlines():
        if line != '\n':
            ints_list.append(int(line))
    return ints_list


def writeOutput(optset, filename=None):
    assert type(optset) == list
    if filename == None:
        writeIntList(optset, sys.stdout)
    else:
        with open(filename, 'w') as f:
            writeIntList(optset, f)


def writeIntList(optset, f):
    for x in optset:
        f.write(str(int(x)) + "\n")
    return


##################################################
# Coffee shop solution
##################################################
test_WTC_input = [5, 5, 9, 5, 5]
test_WTC_output = [0, 1, 3, 4]


def computeMaxValues(values):
    # values is a nonempty list of nonengative integers
    # values[i] is the serving capacity of location i
    assert len(values) >= 3
    n = len(values)
    # Fill the table:
    # opt[i] is the value of the heaviest ok set
    # among vertices 0,1,...,i.
    opt = [0] * n
    ########################################
    # Your code here.
    j = 0
    for j in range(n):
        if (j == 0):
            opt[j] = values[j]
        elif (j == 1):
            opt[j] = values[j] + values[j-1]
        elif (j == 2):
            opt[j] = max(values[j] + values[j-1],
                         values[j] + opt[j-2],
                         opt[j-1])
        else:
            opt[j] = max(values[j] + values[j-1] + opt[j-3],
                         values[j] + opt[j-2],
                         opt[j-1])
    print(opt)
    ########################################
    return opt


def computeOptSet(values, opt):
    assert len(values) >= 3
    n = len(values)
    # Now compute the optimal set
    optset = []
    ########################################
    # Your code here.
    j = len(values) - 1
    while j >= 3:
        if (opt[j] == values[j] + opt[j-2]):
            optset.append(j)
            j = j-2
        elif (opt[j] == values[j] + values[j-1] + opt[j-3]):
            optset.append(j)
            optset.append(j-1)
            j = j-3
        elif (opt[j]) == opt[j-1]:
            j = j-1
        if (j == 2):
            if (opt[j] == values[j] + opt[j-2]):
                optset.append(j)
                j = j-2
            elif (opt[j] == values[j] + values[j-1]):
                optset.append(j)
                optset.append(j-1)
                j = -1
            elif (opt[j]) == opt[j-1]:
                j = j-1
        if (j == 1):
            if (opt[j] == values[j] + values[j-1]):
                optset.append(j)
                j = 0
            elif (opt[j]) == opt[j-1]:
                j = j-1
        if (j == 0):
            optset.append(j)

    optset.reverse()
    print(optset)
    ########################################
    return optset


def main(args=[]):
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 2.".format(len(args)))
        return
    success, result = parseInput(filename=args[0])
    if success:
        values = result
        opt = computeMaxValues(values)
        optset = computeOptSet(values, opt)
        writeOutput(optset, filename=args[1])
    else:
        print(result)
    return


if __name__ == "__main__":
    main(sys.argv[1:])
