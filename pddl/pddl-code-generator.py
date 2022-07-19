import os
import argparse
import re

durative = False
preGrounding = False

def validate_file(f):
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

def parseFile(file):
    f = open(file, "r")
    t = f.read().split("end")
    # for i, elem in enumerate(t):
    #     print(i, elem)

    x, y = t[0].split("grid")[1].split()[1].split(",")
    x = int("".join(filter(str.isdigit, x)))
    y = int("".join(filter(str.isdigit, y)))
    print("size:", x, "by", y)

    block = []

    blockages = list(filter(None, t[1].split("blockages")[1].split("\n")))
    for b in blockages:
        block.append(list(filter(None, re.split("[(), ]", b))))
    print("blockages:", block)

    start = []
    goal = []

    nets = list(filter(None, t[2].split("nets")[1].split("\n")))
    for net in nets:
        n, s, a, g = net.split()
        sx, sy = s.split(",")
        sx = sx.replace("(", "x")
        sy = sy.replace(")", "")
        sy = "y" + sy
        start.append(" ".join((sx, sy)))
 
        gx, gy = g.split(",")
        gx = gx.replace("(", "x")
        gy = gy.replace(")", "")
        gy = "y" + gy
        goal.append(" ".join((gx, gy)))
    print("start positions:", start)
    print("goal positions:", goal)

    return x, y, start, goal, block


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

def print_domain(x, y, blockages, duration=1):
    global durative
    global preGrounding

    if durative:
        actionType = ":durative-action"
        conditionType = ":condition"
        startType = "(at start "
        endType = "(at end "
        overallType = "(over all "
        bracket = ")"
    else:
        actionType = ":action"
        conditionType = ":precondition"
        startType = endType = overallType = bracket = ""

    domainfile = "domain_%ix%i.pddl" % (x, y)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, domainfile)
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, "x")
    f.write("(define (domain domain_%ix%i)\n" % (x, y))
    f.write("\n(:requirements :strips :typing :conditional-effects :negative-preconditions :disjunctive-preconditions")
    if durative:
        f.write(" :durative-actions")
    f.write(")\n\n")
    f.write("(:types\n    droplet coordinate - object\n    xcoord ycoord - coordinate\n    ")
    for i in range(1, x+1):
        f.write("x%i " % (i))
    f.write("- xcoord\n    ")
    for i in range(1, y+1):
        f.write("y%i " % (i))
    f.write("- ycoord\n)\n\n")
    f.write("(:predicates\n    (droplet-at ?d ?x ?y)\n    (occupied ?x ?y)\n)\n\n")

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
                        f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i+1, j))
                        f.write("    :parameters (?d - droplet)\n")
                        if durative:
                            f.write("    :duration (= ?duration %i)\n" % duration)
                        f.write("    " + conditionType + " (and\n")
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                        if i+1 < x:                 # then there exist fields that need to be checked 
                            for k in range(-1, 2):
                                if 0 < j+k < y+1:   # check only for existing fields
                                    f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+2, j+k, bracket))
                        f.write("    )\n")
                        f.write("    :effect (and\n")
                        f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i+1, j, bracket))
                        f.write("        %s(not (occupied x%i y%i))%s\n" % (endType,i, j, bracket))
                        f.write("        %s(occupied x%i y%i)%s\n" % (startType, i+1, j, bracket))
                        f.write("    )\n")
                        f.write(")\n")

                if (not("%i %i" % (i, j-1) in blocks)):
                    # move south
                    if j > 1:                       # then the move is possible
                        f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i, j-1))
                        f.write("    :parameters (?d - droplet)\n")
                        if durative:
                            f.write("    :duration (= ?duration %i)\n" % duration)
                        f.write("    " + conditionType + " (and\n")
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                        if j-2 > 0:                 # then there exist fields that need to be checked 
                            for k in range(-1, 2):
                                if 0 < i+k < x+1:   # check only for existing fields
                                    f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+k, j-2, bracket))
                        f.write("    )\n")
                        f.write("    :effect (and\n")
                        f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i, j-1, bracket))
                        f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                        f.write("        %s(occupied x%i y%i)%s\n" % (startType, i, j-1, bracket))
                        f.write("    )\n")
                        f.write(")\n")

                if (not("%i %i" % (i-1, j) in blocks)):
                    # move west
                    if i > 1:                       # then the move is possible
                        f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i-1, j))
                        f.write("    :parameters (?d - droplet)\n")
                        if durative:
                            f.write("    :duration (= ?duration %i)\n" % duration)
                        f.write("    " + conditionType + " (and\n")
                        f.write("            %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                        if i-2 > 0:                 # then there exist fields that need to be checked 
                            for k in range(-1, 2):
                                if 0 < j+k < y+1:   # check only for existing fields
                                    f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i-2, j+k, bracket))
                        f.write("    )\n")
                        f.write("    :effect (and\n")
                        f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i-1, j, bracket))
                        f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                        f.write("        %s(occupied x%i y%i)%s\n" % (startType, i-1, j, bracket))
                        f.write("    )\n")
                        f.write(")\n")

                if (not("%i %i" % (i, j+1) in blocks)):
                    # move north
                    if j < y:                       # then the move is possible
                        f.write("\n(" + actionType + " move_%i-%i_%i-%i\n" % (i, j, i, j+1))
                        f.write("    :parameters (?d - droplet)\n")
                        if durative:
                            f.write("    :duration (= ?duration %i)\n" % duration)
                        f.write("    " + conditionType + " (and\n")
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (startType, i, j, bracket))
                        if j+1 < x:                 # then there exist fields that need to be checked 
                            for k in range(-1, 2):
                                if 0 < i+k < x+1:   # check only for existing fields
                                    f.write("        %s(not (occupied x%i y%i))%s\n" % (overallType, i+k, j+2, bracket))
                        f.write("    )\n")
                        f.write("    :effect (and\n")
                        f.write("        %s(not (droplet-at ?d x%i y%i))%s\n" % (startType, i, j, bracket))
                        f.write("        %s(droplet-at ?d x%i y%i)%s\n" % (endType, i, j+1, bracket))
                        f.write("        %s(not (occupied x%i y%i))%s\n" % (endType, i, j, bracket))
                        f.write("        %s(occupied x%i y%i)%s\n" % (startType, i, j+1, bracket))
                        f.write("    )\n")
                        f.write(")\n")

    f.write("\n)")

    f.close()

def print_problem(x, y, droplets, goals, blockages):
    problemfile = "p_%ix%i_%id.pddl" % (x, y, len(droplets))
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, problemfile)
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, "x")
    f.write("(define (problem p_%ix%i_%id) (:domain domain_%ix%i)\n\n" % (x, y, len(droplets), x, y))
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

    # for b in blockages:
    #     for i in range(int(b[0]), int(b[2])+1):
    #         for j in range(int(b[1]), int(b[3])+1):
    #             f.write("    (occupied x%i y%i)\n" % (i, j))
    
    f.write(")\n\n")

    f.write("(:goal (and\n")
    i = 1
    for g in goals:
        f.write("    (droplet-at droplet%i " % (i) + g + ")\n")
        i+=1
    f.write("))\n)\n")

    f.close()

def add_droplet(i, j, coords):
    print(i, j)
    coords.append("%i%i" % (i, j))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Provide .bio file path.")
    parser.add_argument("-b", "-bio", dest='path', type=validate_file, nargs=1, help='Provide the path to the .bio file to be loaded as configuration.', metavar="FILE")
    parser.add_argument("-d", "-durative", dest='durative', action='store_true', default=False, help='Add if you want the domain to be durative.')
    parser.add_argument("-g", "-grounding", dest='grounding', action='store_true', default=False, help='Add if you want the domain to be pre-grounded. This will eliminate forall statements.')
    args = parser.parse_args()

    if args.durative:
        durative = True

    if args.grounding:
        preGrounding = True
    
    if args.path:
        x, y, start, goal, block = parseFile(args.path[0])
        currentSet = (x, y, start, goal, block)
    else:
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
        set3 = (x, y, (d1_start, d2_start, d3_start, d4_start), (d1_goal, d2_goal, d3_goal, d4_goal), ())

        currentSet = set3

    print_domain(currentSet[0], currentSet[1], currentSet[4])
    print_problem(currentSet[0], currentSet[1], currentSet[2], currentSet[3], currentSet[4])
    print("Domain and problem files generated.")

    # coords = []

    # master=tkinter.Tk()
    # master.title("grid() method")
    # geometry = "%ix%i" % (x*100, y*100)
    # master.geometry(geometry)

    # buttongrid=[]

    # for i in range(x):
    #     for j in range(y):
    #         buttongrid.append(tkinter.Button(master, text="%i%i" % (i+1, j+1), height=5, width=9))
    #         buttongrid[i*y+j].config(command=lambda x=i+1, y=j+1: add_droplet(x, y, coords))
    #         buttongrid[i*y+j].grid(row=y-j, column=i)

    # master.mainloop()

    # print(coords)
