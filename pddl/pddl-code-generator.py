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

if __name__ == '__main__':
    print_vicinity(3, 3)

