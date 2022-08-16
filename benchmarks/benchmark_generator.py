import argparse
import os
import random as rng

def generate(x=9, y=9, droplets=5, blockages=3, min_block_size=2):
    filename = "bm%ix%id%ib%i.bio" % (x, y, droplets, blockages)
    parentname = os.path.dirname(__file__)
    dirname = os.path.join(parentname, filename)

    # Remove existing files with the same name.
    if os.path.exists(dirname):
        os.remove(dirname)
    
    # Open the file and start writing.
    f = open(dirname, "x")
    f.write("grid\n")
    f.write("(1,1) (%i,%i)\n" % (x, y))
    f.write("end\n\n")

    # free is a list of positions that are not yet part of or adjacent to a blockage
    free = []
    # unocc_src is a list of positions that are not yet part of a blockage or occupied or adjacent to a droplet
    unocc_src = []
    # unocc_goal is a list of positions that are not yet part of a blockage or occupied or adjacent to a droplet
    unocc_goal = []
    no_more_blockages = False

    # populate free and unoccupied lists
    for i in range(1, x+1):
        for j in range(1, y+1):
            free.append("%i,%i" % (i, j))
            unocc_src.append("%i,%i" % (i, j))
            unocc_goal.append("%i,%i" % (i, j))

    f.write("blockages\n")
    # generate blockages
    for i in range(0,blockages):
        # generate a randomly sized blockage
        x_size = rng.randint(min_block_size, int(x/2))
        y_size = rng.randint(min_block_size, int(y/2))
        # origins is a list of positions that may be suitable as lower left part of the blockage
        origins = []
        int_x = 0
        int_y = 0
        # populate origins
        for ix in range(1, x-x_size+2):
            for iy in range(1, y-y_size+2):
                origins.append("%i,%i" % (ix, iy))
        # search for a suitable origin, until found or found impossible to place
        unplacable = True
        while unplacable:
            # if origins is empty, no position is suitable and the blockage can't be placed
            if not origins:
                no_more_blockages = True
                break
            unplacable = False
            # take a random origin position...
            sample_origin = rng.sample(origins, 1)[0]
            sample_x, sample_y = sample_origin.split(",")
            int_x = int(sample_x)
            int_y = int(sample_y)
            # ...and check if the blockage would fit
            for ix in range(int_x, int_x + x_size):
                for iy in range(int_y, int_y + y_size):
                    if not "%i,%i" % (ix, iy) in free:
                        unplacable = True
                        if sample_origin in origins:
                            origins.remove(sample_origin)
        if no_more_blockages:
            print("No more space for blockages!")
            break
        else:
            # if blockage is placable, remove all blocked and adjacent positions from free
            f.write("(%i,%i) (%i,%i)\n" % (int_x, int_y, int_x+x_size-1, int_y+y_size-1))
            for ix in range(int_x-1, int_x+x_size+1):
                for iy in range(int_y-1, int_y+y_size+1):
                    s = "%i,%i" % (ix, iy)
                    if s in free:
                        free.remove(s)
            # remove blocked positions from unoccupied
            for ix in range(int_x, int_x+x_size):
                for iy in range(int_y, int_y+y_size):
                    s = "%i,%i" % (ix, iy)
                    if s in unocc_src:
                        unocc_src.remove(s)
                    if s in unocc_goal:
                        unocc_goal.remove(s)

    f.write("end\n\n")

    f.write("nets\n")

    for i in range(0, droplets):
        if unocc_src:
            source = rng.sample(unocc_src, 1)[0]
            unocc_src.remove(source)
            source_x, source_y = source.split(",")
            sx = int(source_x)
            sy = int(source_y)
            for ix in range(sx-1, sx+2):
                for iy in range(sy-1, sy+2):
                    sc = "%i,%i" % (ix, iy)
                    if sc in unocc_src:
                        unocc_src.remove(sc)

            if not unocc_goal:
                break

            goal = rng.sample(unocc_goal, 1)[0]
            unocc_goal.remove(goal)
            goal_x, goal_y = goal.split(",")
            gx = int(goal_x)
            gy = int(goal_y)
            for ix in range(gx-1, gx+2):
                for iy in range(gy-1, gy+2):
                    gc = "%i,%i" % (ix, iy)
                    if gc in unocc_goal:
                        unocc_goal.remove(gc)

            f.write("(" + source + ") -> (" + goal + ")\n")

    f.write("end")

    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Define the parameters of the benchmarks to generate.")
    parser.add_argument("x", type=int, help='Define the horizontal size.')
    parser.add_argument("y", type=int, help='Define the vertical size.')
    parser.add_argument("droplets", type=int, help='Define the number of nets.')
    parser.add_argument("blockages", type=int, help='Define the number of blockages.')
    parser.add_argument("min_block_size", type=int, help='Define the minimal side length of a blockage.')
    args = parser.parse_args()

    generate(args.x, args.y, args.droplets, args.blockages, args.min_block_size)