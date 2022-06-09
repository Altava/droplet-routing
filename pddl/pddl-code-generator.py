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

def print_domain(x, y):
    duration = 1
    print("(define (domain grid_%ix%i)" % (x, y))
    print("\n(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions :durative-actions)\n")
    print("(:types\n  droplet coordinate - object\n  xcoord ycoord - coordinate\n)\n")
    print("(:predicates\n  (droplet-at ?d ?x ?y)\n  (occupied ?x ?y)\n)\n")

    for i in range(1, x+1):
        for j in range(1, y+1):
            # move east
            if i < x:                       # then the move is possible
                print("\n(:durative-action move_%i%i_%i%i" % (i, j, i+1, j))
                print("  :parameters (?d - droplet)")
                print("  :duration (= ?duration %i)" % duration)
                print("  :condition (and")
                print("    (at start (droplet-at ?d x%i y%i))" % (i, j))
                if i+1 < x:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < j+k < y+1:   # check only for existing fields
                            print("    (over all (not (occupied x%i y%i)))" % (i+2, j+k))
                print("  )\n)")

            # move south
            if j > 1:                       # then the move is possible
                print("\n(:durative-action move_%i%i_%i%i" % (i, j, i, j-1))
                print("  :parameters (?d - droplet)")
                print("  :duration (= ?duration %i)" % duration)
                print("  :condition (and")
                print("    (at start (droplet-at ?d x%i y%i))" % (i, j))
                if j-2 > 0:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < i+k < x+1:   # check only for existing fields
                            print("    (over all (not (occupied x%i y%i)))" % (i+k, j-2))
                print("  )\n)")

            # move west
            if i > 1:                       # then the move is possible
                print("\n(:durative-action move_%i%i_%i%i" % (i, j, i-1, j))
                print("  :parameters (?d - droplet)")
                print("  :duration (= ?duration %i)" % duration)
                print("  :condition (and")
                print("    (at start (droplet-at ?d x%i y%i))" % (i, j))
                if i-2 > 0:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < j+k < y+1:   # check only for existing fields
                            print("    (over all (not (occupied x%i y%i)))" % (i-2, j+k))
                print("  )\n)")

            # move north
            if j < y:                       # then the move is possible
                print("\n(:durative-action move_%i%i_%i%i" % (i, j, i, j+1))
                print("  :parameters (?d - droplet)")
                print("  :duration (= ?duration %i)" % duration)
                print("  :condition (and")
                print("    (at start (droplet-at ?d x%i y%i))" % (i, j))
                if j+1 < x:                 # then there exist fields that need to be checked 
                    for k in range(-1, 2):
                        if 0 < i+k < x+1:   # check only for existing fields
                            print("    (over all (not (occupied x%i y%i)))" % (i+k, j+2))
                print("  )\n)")

    print("\n)\n)")

def print_problem(x, y, droplets, goals):
    print("(define (problem grid%iby%i) (:domain grid_%ix%i)\n" % (x, y, x, y))
    print("(:objects")
    for i in range(1, x+1):
        print("  x%i" % (i))
    for j in range(1, y+1):
        print("  y%i" % (j))
    for d in range(1, len(droplets)+1):
        print("  droplet%i" % (d))
    print(")\n")
    
    print("(:init")
    i = 1
    for d in droplets:
        print("  (droplet-at droplet%i " % (i) + d + ")")
        print("  (occupied " + d + ")")
        i+=1
    print(")")

    print("(:goal (and")
    i = 1
    for g in goals:
        print("  (droplet-at droplet%i " % (i) + g + ")")
        i+=1
    print("))\n)")

if __name__ == '__main__':
    print_domain(3, 3)
    # print_problem(3, 3, ("x1 y1", "x3 y3"), ("x3 y3", "x1 y1"))

