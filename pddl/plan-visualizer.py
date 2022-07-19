import turtle as tt
import os
import argparse
from functools import partial
import re

from more_itertools import last

step = 0
time = 0
last_pos = []
# define colors for up to 11 droplets
colors = ['black', 'green', 'blue', 'red', 'violet', 'yellow', 'aquamarine', 'brown', 'darkgreen', 'DarkOrchid1', 'CornflowerBlue', 'cyan']


def validate_file(f):
    if not os.path.exists(f):
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f

def takeXOrigin(elem):
    return elem[0]

def takeYOrigin(elem):
    return elem[1]

def takeXTarget(elem):
    return elem[2]

def takeYTarget(elem):
    return elem[3]

def takeDroplet(elem):
    return elem[4]

def takeTime(elem):
    return elem[5]
    
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def fun(x, y):
    print(x, y)

def show_plan(filename, blockfilename=None):
    global last_pos
    file = open(filename, "r")

    lis = []

    # read all parts of the plan into lis
    while (f := file.readline()):
        lis.append(f)
    file.close()

    moves = []
    i = 0
    time = 0

    # parse plan into time, coordinates and droplet numbers
    for l in lis:
        elem = l.split()
        if elem[0] == ";":
            break
        if len(elem) == 4:
            time = elem[0]
            move = elem[1]
            droplet = elem[2]
            time = time[0:5]
        else:
            move = elem[0]
            droplet = elem[1]
        
        m, origin, target = move.split("_")
        dropletnumber = [int(s) for s in droplet if s.isdigit()][0]
        originx, originy = origin.split("-")
        targetx, targety = target.split("-")
        moves.append((int(originx), int(originy), int(targetx), int(targety), int(dropletnumber), float(time)))
        if len(elem) != 4:
            time += 1

    moves.sort(key=takeTime)
    # print(moves)

    # find max coordinates
    x1 = max(moves, key=takeXOrigin)[0]
    x2 = max(moves, key=takeXTarget)[2]
    y1 = max(moves, key=takeYOrigin)[1]
    y2 = max(moves, key=takeYTarget)[3]
    x = max(x1, x2)
    y = max(y1, y2)
    max_d = max(moves, key=takeDroplet)[4]
    max_t = max(moves, key=takeTime)[5]
    # print("max droplet", max_d)

    # calculate scale of the window
    scale = max(moves, key=takeDroplet)[4]*10+1
    # print("scale=", scale)

    blocks = []

    if blockfilename != None:
        blockfile = open(blockfilename, "r")
        blockages = blockfile.read()
        b1 = blockages.split("blockages")[1]
        b2 = list(filter(None, b1.split("end")[0].split("\n")))
        blocklist = []
        for bi in b2:
            blocklist.append(list(filter(None, re.split("[(), ]", bi))))

        for b in blocklist:
            x = max(x, int(b[0]), int(b[2]))
            y = max(y, int(b[1]), int(b[3]))
            for i in range(int(b[0]), int(b[2])+1):
                for j in range(int(b[1]), int(b[3])+1):
                    blocks.append("%i %i" % (i, j))
        
        print(blocks)

    # define some basic properties of the window and turtle
    tt.TurtleScreen._RUNNING=True
    tt.bgcolor("lightgrey")
    tt.color(colors[0])
    tt.setworldcoordinates(-scale/10, -scale/10, (x*scale)+scale/10, (y*scale)+scale/10)
    tt.speed(0)
    tt.hideturtle()
    tt.turtlesize(max(1, 100/scale))
    # print(tt.turtlesize())
    screen = tt.Screen()
    screen.tracer(0, 10)

    # draw the raster
    for i in range(x):
        for j in range(y):
            if "%i %i" % (i+1, j+1) in blocks:
                tt.begin_fill()
            tt.setpos((i*scale, j*scale))
            tt.down()
            tt.setpos(((i+1)*scale, j*scale))
            tt.setpos(((i+1)*scale, (j+1)*scale))
            tt.setpos((i*scale, (j+1)*scale))
            tt.setpos((i*scale, j*scale))
            tt.up()
            tt.end_fill()

    # draw the droplet paths
    last_pos = [[0, 0]] * max_d
    screen.tracer(0, 1)

    def timestep(moves, tt, scale, x, y):
        global step
        global max_t
        global time
        global last_pos
        global colors

        if step < len(moves):
            move = moves[step]
            tt.clearstamps()
            while int(move[5]) == time:
                print("printing timestep", move)
                droplet = move[4]
                tt.color(colors[droplet])
                tt.setpos(((move[0]*scale-move[4]*5), (move[1]*scale-move[4]*5)))
                tt.fd(scale/20)
                tt.setpos((tt.xcor(), tt.ycor()-step))
                tt.write(move[5])
                tt.setpos((tt.xcor(), tt.ycor()+step))
                tt.backward(scale/20)
                tt.down()
                tt.setpos(((move[2])*scale-move[4]*5), (move[3]*scale-move[4]*5))
                last_pos[droplet-1] = [((move[2])*scale-move[4]*5), (move[3]*scale-move[4]*5)]
                tt.stamp()
                tt.up()
                step += 1
                move = moves[step]
            for i, pos in enumerate(last_pos):
                tt.color(colors[i+1])
                tt.setpos(pos)
                tt.stamp()
            time += 1
        else:
            tt.color('black')
            tt.setpos(3, 3)
            tt.write("done")

    screen.onscreenclick(partial(timestep, moves, tt, scale))
    screen.mainloop()

    # tt.stamp()
    tt.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Provide sas_plan file path.")
    parser.add_argument(dest='path', type=validate_file, nargs=1, help='Provide the path to the sas_plan file to be visualized.', metavar="FILE")
    parser.add_argument('-b', '-block', '-blocks', dest='blocks', type=validate_file, nargs=1, help='Provide the path to a file containing the blockage infos.', metavar='FILE')
    args = parser.parse_args()
    
    if args.blocks:
        show_plan(args.path[0], args.blocks[0])
    else:
        show_plan(args.path[0])