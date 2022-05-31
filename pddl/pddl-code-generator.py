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



if __name__ == '__main__':
    print_neighbours(3, 3)

