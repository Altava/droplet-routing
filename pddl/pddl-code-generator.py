import os

def print_neighbours(x, y):
    for ix in range(1, x + 1):
        for iy in range(1, y + 1):
            if iy < y:
                print("(NEIGHBOUR x%i y%i x%i y%i)" % (ix, iy, ix, iy + 1))
            if iy > 1:
                print("(NEIGHBOUR x%i y%i x%i y%i)" % (ix, iy, ix, iy - 1))
            if ix < x:
                print("(NEIGHBOUR x%i y%i x%i y%i)" % (ix, iy, ix + 1, iy))
            if ix > 1:
                print("(NEIGHBOUR x%i y%i x%i y%i)" % (ix, iy, ix - 1, iy))

def print_vicinity(x, y):
    for ix in range(1, x + 1):
        for iy in range(1, y + 1):
            if iy < y:
                print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix, iy + 1))
                if ix < x:
                    print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix + 1, iy + 1))
            if iy > 1:
                print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix, iy - 1))
                if ix > 1:
                    print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix - 1, iy - 1))
            if ix < x:
                print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix + 1, iy))
                if iy > 1:
                    print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix + 1, iy - 1))
            if ix > 1:
                print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix - 1, iy))
                if iy < y:
                    print("(VICINITY x%i y%i x%i y%i)" % (ix, iy, ix - 1, iy + 1))

def print_domain(x, y, duration=1):
    domainfile = "domain_%ix%i.pddl" % (x, y)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, domainfile)
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, "x")
    f.write("(define (domain domain_%ix%i)\n" % (x, y))
    f.write("\n(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :durative-actions)\n\n")
    f.write("(:types\n    droplet coordinate - object\n    xcoord ycoord - coordinate\n    ")
    for i in range(1, x+1):
        f.write("x%i " % (i))
    f.write("- xcoord\n    ")
    for i in range(1, y+1):
        f.write("y%i " % (i))
    f.write("- ycoord\n)\n\n")
    f.write("(:predicates\n    (droplet-at ?d ?x ?y)\n    (occupied ?x ?y)\n)\n\n")

    for i in range(1, x+1):
        for j in range(1, y+1):
            # move east
            if i < x:                       # then the move is possible
                f.write("\n(:durative-action move_%i-%i_%i-%i\n" % (i, j, i+1, j))
                f.write("    :parameters (?d - droplet)\n")
                f.write("    :duration (= ?duration %i)\n" % duration)
                f.write("    :condition (and\n")
                f.write("        (at start (droplet-at ?d x%i y%i))\n" % (i, j))
                if i+1 < x:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < j+k < y+1:   # check only for existing fields
                            f.write("        (over all (not (occupied x%i y%i)))\n" % (i+2, j+k))
                f.write("    )\n")
                f.write("    :effect (and\n")
                f.write("        (at start (not (droplet-at ?d x%i y%i)))\n" % (i, j))
                f.write("        (at end (droplet-at ?d x%i y%i))\n" % (i+1, j))
                f.write("        (at end (not (occupied x%i y%i)))\n" % (i, j))
                f.write("        (at start (occupied x%i y%i))\n" % (i+1, j))
                f.write("    )\n")
                f.write(")\n")

            # move south
            if j > 1:                       # then the move is possible
                f.write("\n(:durative-action move_%i-%i_%i-%i\n" % (i, j, i, j-1))
                f.write("  :parameters (?d - droplet)\n")
                f.write("  :duration (= ?duration %i)\n" % duration)
                f.write("  :condition (and\n")
                f.write("    (at start (droplet-at ?d x%i y%i))\n" % (i, j))
                if j-2 > 0:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < i+k < x+1:   # check only for existing fields
                            f.write("    (over all (not (occupied x%i y%i)))\n" % (i+k, j-2))
                f.write("    )\n")
                f.write("    :effect (and\n")
                f.write("        (at start (not (droplet-at ?d x%i y%i)))\n" % (i, j))
                f.write("        (at end (droplet-at ?d x%i y%i))\n" % (i, j-1))
                f.write("        (at end (not (occupied x%i y%i)))\n" % (i, j))
                f.write("        (at start (occupied x%i y%i))\n" % (i, j-1))
                f.write("    )\n")
                f.write(")\n")

            # move west
            if i > 1:                       # then the move is possible
                f.write("\n(:durative-action move_%i-%i_%i-%i\n" % (i, j, i-1, j))
                f.write("  :parameters (?d - droplet)\n")
                f.write("  :duration (= ?duration %i)\n" % duration)
                f.write("  :condition (and\n")
                f.write("    (at start (droplet-at ?d x%i y%i))\n" % (i, j))
                if i-2 > 0:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < j+k < y+1:   # check only for existing fields
                            f.write("    (over all (not (occupied x%i y%i)))\n" % (i-2, j+k))
                f.write("    )\n")
                f.write("    :effect (and\n")
                f.write("        (at start (not (droplet-at ?d x%i y%i)))\n" % (i, j))
                f.write("        (at end (droplet-at ?d x%i y%i))\n" % (i-1, j))
                f.write("        (at end (not (occupied x%i y%i)))\n" % (i, j))
                f.write("        (at start (occupied x%i y%i))\n" % (i-1, j))
                f.write("    )\n")
                f.write(")\n")

            # move north
            if j < y:                       # then the move is possible
                f.write("\n(:durative-action move_%i-%i_%i-%i\n" % (i, j, i, j+1))
                f.write("  :parameters (?d - droplet)\n")
                f.write("  :duration (= ?duration %i)\n" % duration)
                f.write("  :condition (and\n")
                f.write("    (at start (droplet-at ?d x%i y%i))\n" % (i, j))
                if j+1 < x:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < i+k < x+1:   # check only for existing fields
                            f.write("    (over all (not (occupied x%i y%i)))\n" % (i+k, j+2))
                f.write("    )\n")
                f.write("    :effect (and\n")
                f.write("        (at start (not (droplet-at ?d x%i y%i)))\n" % (i, j))
                f.write("        (at end (droplet-at ?d x%i y%i))\n" % (i, j+1))
                f.write("        (at end (not (occupied x%i y%i)))\n" % (i, j))
                f.write("        (at start (occupied x%i y%i))\n" % (i, j+1))
                f.write("    )\n")
                f.write(")\n")

    f.write("\n)")

    f.close()

def print_problem(x, y, droplets, goals):
    problemfile = "p_%ix%i.pddl" % (x, y)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, problemfile)
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, "x")
    f.write("(define (problem p_%ix%i) (:domain domain_%ix%i)\n\n" % (x, y, x, y))
    f.write("(:objects\n    ")
    for d in range(1, len(droplets)+1):
        f.write("droplet%i " % (d))
    f.write("- droplet\n")
    f.write(")\n\n")
    
    f.write("(:init\n")
    i = 1
    for d in droplets:
        f.write("    (droplet-at droplet%i " % (i) + d + ")\n")
        f.write("    (occupied " + d + ")\n")
        i+=1
    f.write(")\n")

    f.write("(:goal (and\n")
    i = 1
    for g in goals:
        f.write("    (droplet-at droplet%i " % (i) + g + ")\n")
        i+=1
    f.write("))\n)\n")

    f.close()

if __name__ == '__main__':
    set1 = (3, 3, ("x1 y1", "x3 y3"), ("x3 y3", "x1 y1"))
    set2 = (4, 4, ("x1 y1", "x4 y4", "x1 y4"), ("x4 y4", "x1 y1", "x4 y1"))
    
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
    set3 = (x, y, (d1_start, d2_start, d3_start, d4_start), (d1_goal, d2_goal, d3_goal, d4_goal))

    currentSet = set1
    print_domain(currentSet[0], currentSet[1])
    print_problem(currentSet[0], currentSet[1], currentSet[2], currentSet[3])

