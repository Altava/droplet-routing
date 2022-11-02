from curses.ascii import isdigit
import os
import argparse
import re

durative = False
preGrounding = False
coordinates = False
all = False
mixing = False

def validate_file(f):
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

# function to parse files using the BioGram grammar
def parseFile(file):
    f = open(file, "r")
    content = f.read()
    # t = f.read().split("end")
    # for i, elem in enumerate(t):
    #     print(i, elem)

    # search for "grid", parse into grid size
    x, y = re.search("(?s)grid(.*)end", content).group(1).split("end")[0].split()[1].split(",")
    x = int("".join(filter(str.isdigit, x)))
    y = int("".join(filter(str.isdigit, y)))
    print("size:", x, "by", y)

    # search for "blockages", parse into list of blocked fields
    block = []
    blocksearch = re.search("(?s)blockages(.*)end", content)
    if blocksearch:
        blockages = list(filter(None, blocksearch.group(1).split("end")[0].split("\n")))
        for b in blockages:
            block.append(list(filter(None, re.split("[(), ]", b))))
        print("blockages:", block)

    # search for "nets", parse into lists of start and goal positions for each droplet
    start = []
    goal = []
    netsearch = re.search("(?s)nets(.*)end", content)
    if netsearch:
        nets = list(filter(None, netsearch.group(1).split("end")[0].split("\n")))
        ni = 1
        for net in nets:
            n, s, a, g = net.split()
            sx, sy = s.split(",")
            sx = sx.replace("(", "x")
            sy = sy.replace(")", "")
            sy = "y" + sy
            start.append(" ".join((str(ni), sx, sy)))
    
            gx, gy = g.split(",")
            gx = gx.replace("(", "x")
            gy = gy.replace(")", "")
            gy = "y" + gy
            goal.append(" ".join((str(ni), gx, gy)))

            ni += 1
        print("start positions:", start)
        print("goal positions:", goal)
    
    # search for "mixings", parse into list of possible mixtures
    mix = []
    mixsearch = re.search("(?s)mixings(.*)end", content)
    if mixsearch:
        global mixing
        mixing = True
        mixings = list(filter(None, mixsearch.group(1).split("end")[0].split("\n")))
        for mx in mixings:
            elem = re.search("(\d+) \+ (\d+) = (\d+)", mx).group(1, 2, 3)
            mix.append(elem)

    # search for "dispensers", parse into list of dispenser locations
    dispenserssearch = re.search("(?s)dispensers(.*)end", content)
    if dispenserssearch:
        dispensers = list(filter(None, dispenserssearch.group(1).split("end")[0].split("\n")))
        for dsp in dispensers:
            elem = re.search("(\d+) \((\d+),(\d+)\)", dsp).group(1, 2, 3)
            start.append(elem[0] + " x" + elem[1] + " y" + elem[2])

    # search for "sinks", parse into list of sink locations
    sink = []
    sinkssearch = re.search("(?s)sinks(.*)end", content)
    if sinkssearch:
        sinks = list(filter(None, sinkssearch.group(1).split("end")[0].split("\n")))
        for snk in sinks:
            elem = re.search("\((\d+),(\d+)\)", snk).group(1, 2)
            if elem[0].isdigit():
                sink.append("x" + elem[0] + " y" + elem[1])
                
    # search for "detectors", parse into list of detector locations
    detectorssearch = re.search("(?s)detectors(.*)end", content)
    if detectorssearch:
        detectors = list(filter(None, detectorssearch.group(1).split("end")[0].split("\n")))
        for dtc in detectors:
            elem = re.search("\((\d+),(\d+)\) \d+ (\d+)", dtc).group(1, 2, 3)
            if elem[0].isdigit():
                goal.append(elem[2] + " x" + elem[0] + " y" + elem[1])


    return x, y, start, goal, block, mix, sink

# helper function for sequential coordinate calculation
def sc(x, y, xmax):
    return x + (y-1) * xmax

def ss(drop, xmax):
    d, x, y = drop.split()
    x = int("".join(filter(str.isdigit, x)))
    y = int("".join(filter(str.isdigit, y)))
    return d + " c%i" % (sc(x, y, xmax))

def sss(drop, xmax):
    d, x, y = drop.split()
    x = int("".join(filter(str.isdigit, x)))
    y = int("".join(filter(str.isdigit, y)))
    return "c%i" % (sc(x, y, xmax))

def cs(drop):
    d, x, y = drop.split()
    return x + " " + y

def print_neighbours(x, y, f):
    global coordinates
    for ix in range(1, x + 1):
        for iy in range(1, y + 1):
            # northside neighbour
            if iy < y:
                if coordinates:
                    f.write("    (NEIGHBOUR x%i y%i x%i y%i)\n" % (ix, iy, ix, iy + 1))
                else:
                    f.write("    (NEIGHBOUR c%i c%i)\n" % (ix + (iy - 1) * x, ix + iy * x))
            # southside neighbour
            if iy > 1:
                if coordinates:
                    f.write("    (NEIGHBOUR x%i y%i x%i y%i)\n" % (ix, iy, ix, iy - 1))
                else:
                    f.write("    (NEIGHBOUR c%i c%i)\n" % (ix + (iy - 1) * x, ix + (iy - 2) * x))
            # eastside neighbour
            if ix < x:
                if coordinates:
                    f.write("    (NEIGHBOUR x%i y%i x%i y%i)\n" % (ix, iy, ix + 1, iy))
                else:
                    f.write("    (NEIGHBOUR c%i c%i)\n" % (ix + (iy - 1) * x, ix + 1 + (iy - 1) * x))
            # westside neighbour
            if ix > 1:
                if coordinates:
                    f.write("    (NEIGHBOUR x%i y%i x%i y%i)\n" % (ix, iy, ix - 1, iy))
                else:
                    f.write("    (NEIGHBOUR c%i c%i)\n" % (ix + (iy - 1) * x, ix - 1 + (iy - 1) * x))

def print_vicinity(x, y, f):
    global coordinates
    for ix in range(1, x + 1):
        for iy in range(1, y + 1):
            if coordinates:
                if iy < y:
                    f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix, iy + 1))
                    if ix < x:
                        f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix + 1, iy + 1))
                if iy > 1:
                    f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix, iy - 1))
                    if ix > 1:
                        f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix - 1, iy - 1))
                if ix < x:
                    f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix + 1, iy))
                    if iy > 1:
                        f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix + 1, iy - 1))
                if ix > 1:
                    f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix - 1, iy))
                    if iy < y:
                        f.write("    (VICINITY x%i y%i x%i y%i)\n" % (ix, iy, ix - 1, iy + 1))
            else:
                if iy < y:
                    f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix + iy * x))
                    if ix < x:
                        f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix + 1 + iy * x))
                if iy > 1:
                    f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix + (iy - 2) * x))
                    if ix > 1:
                        f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix - 1 + (iy - 2) * x))
                if ix < x:
                    f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix + 1 + (iy - 1) * x))
                    if iy > 1:
                        f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix + 1 + (iy - 2) * x))
                if ix > 1:
                    f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix - 1 + (iy - 1) * x))
                    if iy < y:
                        f.write("    (VICINITY c%i c%i)\n" % (ix + (iy - 1) * x, ix - 1 + iy * x))

def print_domain(x, y, droplets, blockages, n="", duration=1):
    global durative
    global preGrounding
    global coordinates
    global mixing

    if durative:
        f1 = "durative_"
        actionType = ":durative-action"
        conditionType = ":condition"
        startType = "(at start "
        endType = "(at end "
        overallType = "(over all "
        bracket = ")"
    else:
        f1 = "classical_"
        actionType = ":action"
        conditionType = ":precondition"
        startType = endType = overallType = bracket = ""

    if preGrounding:
        f2 = "grounded_"
    else:
        f2 = "lifted_"
    
    if coordinates:
        f3 = "coords"
        coordType = "?x ?y"
        coordTypeWithType = "?x - xcoord ?y - ycoord"
        originType = "?xo ?yo"
        originTypeWithType = "?xo - xcoord ?yo - ycoord"
        targetType = "?xt ?yt"
        targetTypeWithType = "?xt - xcoord ?yt - ycoord"
        equalityType = "(and (= ?x ?xo) (= ?y ?yo))"
    else:
        f3 = "sequential"
        coordType = "?c"
        coordTypeWithType = "?c - coordinate"
        originType = "?co"
        originTypeWithType = "?co"
        targetType = "?ct"
        targetTypeWithType = "?ct - coordinate"
        equalityType = "(= ?c ?co)"

    print("n:")
    print(n)
    domainfile = "p%ix%id%ib%in" % (x, y, len(droplets), len(blockages)) + n + "-domain.pddl"
    parentname = os.path.dirname(__file__)
    dirname = os.path.join(parentname, "benchmarks", f1 + f2 + f3)

    # If folder does not yet exist, create it.
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    filename = os.path.join(dirname, domainfile)

    # Remove existing files with the same name.
    if os.path.exists(filename):
        os.remove(filename)
    
    # Open the file and start writing.
    f = open(filename, "x")
    f.write("(define (domain p%ix%id%in" % (x, y, len(droplets)) + n + "-domain)\n")
    f.write("\n(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions")

    # required for durative version
    if durative:
        f.write(" :durative-actions")

    # required for forall statements
    if not preGrounding:
        f.write(" :universal-preconditions")
    f.write(")\n\n")

    # Define types.
    f.write("(:types\n    droplet coordinate - object\n    ")

    if coordinates:
        f.write("xcoord ycoord - coordinate\n    ")
        for i in range(1, x+1):
            f.write("x%i " % (i))
        f.write("- xcoord\n    ")
        for i in range(1, y+1):
            f.write("y%i " % (i))
        f.write("- ycoord\n)\n\n")
    else:
        for i in range(0, x*y):
            f.write("c%i " % (i+1))
        f.write("- coordinate\n)\n\n")

    # Define predicates.
    f.write("(:predicates\n    (droplet-at ?d - droplet " + coordTypeWithType + ")\n    (occupied " + coordTypeWithType + ")")
    if not preGrounding:
        f.write("    (VICINITY " + originTypeWithType + " " + targetTypeWithType + ")\n")
        f.write("    (NEIGHBOUR " + originTypeWithType + " " + targetTypeWithType + ")\n")
        f.write("    (blocked " + coordTypeWithType + ")\n")
    if mixing:
        f.write("    (MIX ?d1 ?d2 ?dt - droplet)\n")
    f.write(")\n\n")

    if not preGrounding:
        f.write("(" + actionType + " move\n    :parameters (?d - droplet ")
        if coordinates:
            f.write("?xo ?xt - xcoord ?yo ?yt - ycoord")
        else:
            f.write("?co ?ct - coordinate")
        f.write(")\n")
        if durative:
            f.write("    :duration (= ?duration %i)\n" % duration)
        f.write("    " + conditionType + " (and\n        " + startType + "(droplet-at ?d " + originType + ")" + bracket + "\n")
        f.write("        " + startType + "(NEIGHBOUR " + originType + " " + targetType + ")" + bracket + "\n")
        f.write("        " + startType + "(not (blocked " + targetType + "))" + bracket + "\n")
        if coordinates:
            f.write("        " + overallType + "(forall (?x - xcoord)\n          (forall (?y - ycoord)\n")
        else:
            f.write("        " + overallType + "(forall (?c - coordinate)\n")
        f.write("            (imply (and\n                (not " + equalityType + ")\n")
        f.write("                (VICINITY " + coordType + " " + targetType + ")\n")
        f.write("            )\n                (not (occupied " + coordType + "))\n            )\n")
        if coordinates:
            f.write("          )\n")
        f.write("        )" + bracket + "\n    )\n")

        f.write("    :effect (and\n        " + startType + "(not (droplet-at ?d " + originType + "))" + bracket + "\n")
        f.write("        " + endType + "(droplet-at ?d " + targetType + ")" + bracket + "\n")
        f.write("        " + endType + "(not (occupied " + originType + "))" + bracket + "\n")
        f.write("        " + startType + "(occupied " + targetType + ")" + bracket + "\n    )\n)\n")

    else:

        blocks = []

        for b in blockages:
            for i in range(int(b[0]), int(b[2])+1):
                for j in range(int(b[1]), int(b[3])+1):
                    blocks.append("%i %i" % (i, j))

        for i in range(1, x+1):
            for j in range(1, y+1):
                if (not("%i %i" % (i, j) in blocks)):
                    if (not("%i %i" % (i+1, j) in blocks)):
                        # move east
                        if i < x:                       # then the move is possible
                            if coordinates:
                                f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i+1, j))
                            else:
                                f.write("\n(" + actionType + " move_%i_%i\n" % (sc(i, j, x), sc(i+1, j, x)))
                            f.write("    :parameters (?d - droplet)\n")
                            if durative:
                                f.write("    :duration (= ?duration %i)\n" % duration)
                            f.write("    " + conditionType + " (and\n")
                            if coordinates:
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                            else:
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (startType, sc(i, j, x), bracket))
                            if i+1 < x:                 # then there exist fields that need to be checked 
                                for k in range(-1, 2):
                                    if 0 < j+k < y+1:   # check only for existing fields
                                        if coordinates:
                                            f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+2, j+k, bracket))
                                        else:
                                            f.write("        %s(not (occupied c%i))%s\n" % (overallType, sc(i+2, j+k, x), bracket))
                            f.write("    )\n")
                            f.write("    :effect (and\n")
                            if coordinates:
                                f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i+1, j, bracket))
                                f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                                f.write("        %s(occupied x%i y%i)%s\n" % (startType, i+1, j, bracket))
                            else:
                                f.write("        %s(not (droplet-at ?d c%i))%s\n" % (startType, sc(i, j, x), bracket))
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (endType, sc(i+1, j, x), bracket))
                                f.write("        %s(not (occupied c%i))%s\n" % (endType, sc(i, j, x), bracket))
                                f.write("        %s(occupied c%i)%s\n" % (startType, sc(i+1, j, x), bracket))
                            f.write("    )\n")
                            f.write(")\n")

                    if (not("%i %i" % (i, j-1) in blocks)):
                        # move south
                        if j > 1:                       # then the move is possible
                            if coordinates:
                                f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i, j-1))
                            else:
                                f.write("\n(" + actionType + " move_%i_%i\n" % (sc(i, j, x), sc(i, j-1, x)))
                            f.write("    :parameters (?d - droplet)\n")
                            if durative:
                                f.write("    :duration (= ?duration %i)\n" % duration)
                            f.write("    " + conditionType + " (and\n")
                            if coordinates:
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                            else:
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (startType, sc(i, j, x), bracket))
                            if j-2 > 0:                 # then there exist fields that need to be checked 
                                for k in range(-1, 2):
                                    if 0 < i+k < x+1:   # check only for existing fields
                                        if coordinates:
                                            f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+k, j-2, bracket))
                                        else:
                                            f.write("        %s(not (occupied c%i))%s\n" % (overallType, sc(i+k, j-2, x), bracket))
                            f.write("    )\n")
                            f.write("    :effect (and\n")
                            if coordinates:
                                f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i, j-1, bracket))
                                f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                                f.write("        %s(occupied x%i y%i)%s\n" % (startType, i, j-1, bracket))
                            else:
                                f.write("        %s(not (droplet-at ?d c%i))%s\n" % (startType, sc(i, j, x), bracket))
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (endType, sc(i, j-1, x), bracket))
                                f.write("        %s(not (occupied c%i))%s\n" % (endType, sc(i, j, x), bracket))
                                f.write("        %s(occupied c%i)%s\n" % (startType, sc(i, j-1, x), bracket))
                            f.write("    )\n")
                            f.write(")\n")

                    if (not("%i %i" % (i-1, j) in blocks)):
                        # move west
                        if i > 1:                       # then the move is possible
                            if coordinates:
                                f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i-1, j))
                            else:
                                f.write("\n(" + actionType + " move_%i_%i\n" % (sc(i, j, x), sc(i-1, j, x)))
                            f.write("    :parameters (?d - droplet)\n")
                            if durative:
                                f.write("    :duration (= ?duration %i)\n" % duration)
                            f.write("    " + conditionType + " (and\n")
                            if coordinates:
                                f.write("            %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                            else:
                                f.write("            %s(droplet-at ?d c%i)%s\n" % (startType, sc(i, j, x), bracket))
                            if i-2 > 0:                 # then there exist fields that need to be checked 
                                for k in range(-1, 2):
                                    if 0 < j+k < y+1:   # check only for existing fields
                                        if coordinates:
                                            f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i-2, j+k, bracket))
                                        else:
                                            f.write("        %s(not (occupied c%i))%s\n" % (overallType, sc(i-2, j+k, x), bracket))
                            f.write("    )\n")
                            f.write("    :effect (and\n")
                            if coordinates:
                                f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i-1, j, bracket))
                                f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                                f.write("        %s(occupied x%i y%i)%s\n" % (startType, i-1, j, bracket))
                            else:
                                f.write("        %s(not (droplet-at ?d c%i))%s\n" % (startType, sc(i, j, x), bracket))
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (endType, sc(i-1, j, x), bracket))
                                f.write("        %s(not (occupied c%i))%s\n" % (endType, sc(i, j, x), bracket))
                                f.write("        %s(occupied c%i)%s\n" % (startType, sc(i-1, j, x), bracket))
                            f.write("    )\n")
                            f.write(")\n")

                    if (not("%i %i" % (i, j+1) in blocks)):
                        # move north
                        if j < y:                       # then the move is possible
                            if coordinates:
                                f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i, j+1))
                            else:
                                f.write("\n(" + actionType + " move_%i_%i\n" % (sc(i, j, x), sc(i, j+1, x)))
                            f.write("    :parameters (?d - droplet)\n")
                            if durative:
                                f.write("    :duration (= ?duration %i)\n" % duration)
                            f.write("    " + conditionType + " (and\n")
                            if coordinates:
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                            else:
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (startType, sc(i, j, x), bracket))
                            if j+1 < x:                 # then there exist fields that need to be checked 
                                for k in range(-1, 2):
                                    if 0 < i+k < x+1:   # check only for existing fields
                                        if coordinates:
                                            f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+k, j+2, bracket))
                                        else:
                                            f.write("        %s(not (occupied c%i))%s\n" % (overallType, sc(i+k, j+2, x), bracket))
                            f.write("    )\n")
                            f.write("    :effect (and\n")
                            if coordinates:
                                f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                                f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i, j+1, bracket))
                                f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                                f.write("        %s(occupied x%i y%i)%s\n" % (startType, i, j+1, bracket))
                            else:
                                f.write("        %s(not (droplet-at ?d c%i))%s\n" % (startType, sc(i, j, x), bracket))
                                f.write("        %s(droplet-at ?d c%i)%s\n" % (endType, sc(i, j+1, x), bracket))
                                f.write("        %s(not (occupied c%i))%s\n" % (endType, sc(i, j, x), bracket))
                                f.write("        %s(occupied c%i)%s\n" % (startType, sc(i, j+1, x), bracket))
                            f.write("    )\n")
                            f.write(")\n")

    if mixing:
        if not(durative) and not(preGrounding) and coordinates:
            f.write("(:action merge\n")
            f.write("    :parameters (?d1 ?d2 ?d3 - droplet ?x1 ?x2 ?xt - xcoord ?y1 ?y2 ?yt - ycoord)\n")

            f.write("    :precondition (and\n")
            f.write("        (droplet-at ?d1 ?x1 ?y1)\n")
            f.write("        (droplet-at ?d2 ?x2 ?y2)\n")
            f.write("        (NEIGHBOUR ?x1 ?y1 ?xt ?yt)\n")
            f.write("        (NEIGHBOUR ?x2 ?y2 ?xt ?yt)\n")
            f.write("        (not (blocked ?xt ?yt))\n")
            f.write("        (MIX ?d1 ?d2 ?d3)\n")
            f.write("    )\n")

            f.write("    :effect (and\n")
            f.write("        (not (droplet-at ?d1 ?x1 ?y1))\n")
            f.write("        (not (droplet-at ?d2 ?x2 ?y2))\n")
            f.write("        (droplet-at ?d3 ?xt ?yt)\n")
            f.write("        (not (occupied ?x1 ?y1))\n")
            f.write("        (not (occupied ?x2 ?y2))\n")
            f.write("        (occupied ?xt ?yt)\n")
            f.write("    )\n")
            f.write(")\n")

    f.write("\n)")

    f.close()

def print_problem(x, y, droplets, goals, blockages, mix, n=""):
    global durative
    global preGrounding
    global coordinates

    if durative:
        f1 = "durative_"
    else:
        f1 = "classical_"

    if preGrounding:
        f2 = "grounded_"
    else:
        f2 = "lifted_"
    
    if coordinates:
        f3 = "coords"
    else:
        f3 = "sequential"

    # Name the problem file.
    problemfile = "p%ix%id%ib%in" % (x, y, len(droplets), len(blockages)) + n + ".pddl"
    parentname = os.path.dirname(__file__)
    dirname = os.path.join(parentname, "benchmarks", f1 + f2 + f3)

    # If folder does not yet exist, create it.
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    filename = os.path.join(dirname, problemfile)

    # Remove existing files with the same name.
    if os.path.exists(filename):
        os.remove(filename)
    
    # Open the file and start writing.
    f = open(filename, "x")
    f.write("(define (problem p%ix%id%in" % (x, y, len(droplets)) + n + ") (:domain p%ix%id%in" % (x, y, len(droplets)) + n + "-domain)\n\n")

    dropletlist = []
    for dr in droplets:
        d, _, _ = dr.split()
        dropletlist.append(d)
    for gl in goals:
        d, _, _ = gl.split()
        dropletlist.append(d)
    for mx in mix:
        dropletlist.append(mx[0])
        dropletlist.append(mx[1])
        dropletlist.append(mx[2])
    
    dropletlist = list(dict.fromkeys(dropletlist))

    # List all objects - in the problem file we only need the droplets.
    f.write("(:objects\n    ")
    for d in dropletlist:
        f.write("droplet" + d + " ")
    f.write("- droplet\n    ")

    if coordinates:
        f.write("xcoord ycoord - coordinate\n    ")
        for i in range(1, x+1):
            f.write("x%i " % (i))
        f.write("- xcoord\n    ")
        for i in range(1, y+1):
            f.write("y%i " % (i))
        f.write("- ycoord\n)\n\n")
    else:
        for i in range(0, x*y):
            f.write("c%i " % (i+1))
        f.write("- coordinate\n)\n\n")

    # Define the initial state, which is just the position of all droplets.    
    f.write("(:init\n")
    i = 1
    for d in droplets:
        if coordinates:
            f.write("    (droplet-at droplet" + d + ")\n")
            f.write("    (occupied " + cs(d) + ")\n")
        else:
            f.write("    (droplet-at droplet" + ss(d, x) + ")\n")
            f.write("    (occupied " + sss(d, x) + ")\n")
        i+=1

    for m in mix:
        f.write("    (MIX droplet" + m[0] + " droplet" + m[1] + " droplet" + m[2] + ")\n")

    if not preGrounding:
        print_neighbours(x, y, f)
        print_vicinity(x, y, f)

        for b in blockages:
            for i in range(int(b[0]), int(b[2])+1):
                for j in range(int(b[1]), int(b[3])+1):
                    if coordinates:
                        f.write("    (blocked x%i y%i)\n" % (i, j))
                    else:
                        f.write("    (blocked c%i)\n" % (sc(i, j, x)))
    
    f.write(")\n\n")

    f.write("(:goal (and\n")
    i = 1
    for g in goals:
        if coordinates:
            f.write("    (droplet-at droplet" + g + ")\n")
        else:
            f.write("    (droplet-at droplet" + ss(g, x) + ")\n")
        i+=1
    f.write("))\n)\n")

    f.close()

def add_droplet(i, j, coords):
    print(i, j)
    coords.append("%i%i" % (i, j))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Usage:\nAdd -b to provide a .bio file to generate domain and problem from. If none is provided, a simple 3 by 3 problem will be generated.\nUse -d, -g, -c, -a to refine which version you want to generate.")
    parser.add_argument("-b", "-bio", dest='path', type=validate_file, nargs=1, help='Provide the path to the .bio file to be loaded as configuration.', metavar="FILE")
    parser.add_argument("-dir", "-directory", dest='dir', type=validate_file, nargs=1, help='Provide the path to the directory containing the .bio files to be loaded as configuration. Will automatically generate all versions (similar to -all).')
    parser.add_argument("-d", "-durative", dest='durative', action='store_true', default=False, help='Add if you want the domain to be durative.')
    parser.add_argument("-g", "-grounding", dest='grounding', action='store_true', default=False, help='Add if you want the domain to be pre-grounded. This will eliminate forall statements.')
    parser.add_argument("-c", "-coordinates", dest='coordinates', action='store_true', default=False, help='Add if you want to use x- and y-coordinates. Else fields will be simply enumerated.')
    parser.add_argument("-a", "-all", dest='all', action='store_true', default=False, help='Add if you want to generate all versions: (durative / classical) (grounded / lifted) (coords / sequential).')
    args = parser.parse_args()

    if args.durative:
        durative = True

    if args.grounding:
        preGrounding = True

    if args.coordinates:
        coordinates = True

    if args.all:
        all = True
    
    if args.path:
        x, y, start, goal, block, mix = parseFile(args.path[0])
        currentSet = (x, y, start, goal, block, mix)

    elif args.dir:
        dir = args.dir[0]
        print("dir: ")
        print(os.listdir(dir))
        for fl in os.listdir(dir):
            print("Current file: " + fl)
            x, y, start, goal, block, mix = parseFile(os.path.join(dir, fl))
            n, ext = os.path.splitext(fl)
            currentSet = (x, y, start, goal, block, mix)
            for durative in [True, False]:
                for preGrounding in [True, False]:
                    for coordinates in [True, False]:
                        print_domain(currentSet[0], currentSet[1], currentSet[2], currentSet[4], n)
                        print_problem(currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5], n)

    else:
        set1 = (3, 3, ("x1 y1", "x3 y3"), ("x3 y3", "x1 y1"), ())
        set2 = (4, 4, ("x1 y1", "x4 y4", "x1 y4"), ("x4 y4", "x1 y1", "x4 y1"), ())
        
        x = 5
        y = 4
        d1_start = "x1 y1"
        d2_start = "x4 y4"
        d3_start = "x1 y4"
        d4_start = "x3 y2"
        d1_goal = "x3 y3"
        d2_goal = "x1 y1"
        d3_goal = "x4 y1"
        d4_goal = "x1 y4"
        set3 = (x, y, (d1_start, d2_start, d3_start, d4_start), (d1_goal, d2_goal, d3_goal, d4_goal), ())

        currentSet = set1

    if all:
        for durative in [True, False]:
            for preGrounding in [True, False]:
                for coordinates in [True, False]:
                    print_domain(currentSet[0], currentSet[1], currentSet[2], currentSet[4])
                    print_problem(currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5])
        print("Domain and problem files generated.")
        
    else:
        if not args.dir:
            print_domain(currentSet[0], currentSet[1], currentSet[2], currentSet[4])
            print_problem(currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4], currentSet[5])
            print("Domain and problem files generated.")
