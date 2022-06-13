import turtle as tt
import os

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
    
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def show_plan(filename):
    file = open(filename, "r")

    lis = []

    while (f := file.readline()):
        lis.append(f)

    moves = []
    i = 0

    for l in lis:
        time, move, droplet, cost = l.split()
        time = time[0:5]
        m, origin, target = move.split("_")
        dropletnumber = [int(s) for s in droplet if s.isdigit()][0]
        originx, originy = origin.split("-")
        targetx, targety = target.split("-")
        moves.append((int(originx), int(originy), int(targetx), int(targety), int(dropletnumber), float(time)))

    moves.sort(key=takeDroplet)
    # print(moves)

    x1 = max(moves, key=takeXOrigin)[0]
    x2 = max(moves, key=takeXTarget)[2]
    y1 = max(moves, key=takeYOrigin)[1]
    y2 = max(moves, key=takeYTarget)[3]
    x = max(x1, x2)
    y = max(y1, y2)

    scale = max(moves, key=takeDroplet)[4]*10+1
    # print("scale=", scale)
    colors = ['black', 'green', 'blue', 'red', 'violet', 'cyan', 'yellow']

    tt.TurtleScreen._RUNNING=True
    tt.bgcolor("lightgrey")
    tt.color(colors[0])
    tt.setworldcoordinates(-scale/10, -scale/10, (x*scale)+scale/10, (y*scale)+scale/10)
    tt.speed(0)
    tt.hideturtle()
    tt.turtlesize(scale/10)
    # print(tt.turtlesize())
    for i in range(x):
        for j in range(y):
            tt.setpos((i*scale, j*scale))
            tt.down()
            tt.setpos(((i+1)*scale, j*scale))
            tt.setpos(((i+1)*scale, (j+1)*scale))
            tt.setpos((i*scale, (j+1)*scale))
            tt.setpos((i*scale, j*scale))
            tt.up()

    current_droplet = 0
    step = 0
    for move in moves:
        droplet = move[4]
        if droplet != current_droplet and current_droplet != 0:
            tt.fd(scale/20)
            tt.stamp()
            step = 0
        tt.color(colors[droplet])
        tt.setpos(((move[0]*scale-move[4]*5), (move[1]*scale-move[4]*5)))
        tt.fd(scale/20)
        tt.setpos((tt.xcor(), tt.ycor()-step))
        tt.write(move[5])
        tt.setpos((tt.xcor(), tt.ycor()+step))
        tt.backward(scale/20)
        tt.down()
        if droplet != current_droplet:
            tt.dot(scale)
        current_droplet = droplet
        tt.setpos(((move[2])*scale-move[4]*5), (move[3]*scale-move[4]*5))
        tt.up()
        step += 1

    tt.stamp()
    tt.mainloop()

if __name__ == '__main__':
    path = "/home/altava/tfd/downward/sas_plan.1"
    
    show_plan(path)