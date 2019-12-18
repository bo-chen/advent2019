import os
import sys
import math

global xmin
global xmax
global ymin
global ymax

# Reads initial state of the program
def parse_input(file):
    wires = []
    with open(file) as fp:
        for line in fp:
            wire = []
            start = (0,0)
            for ins in line.split(","):
                d = ins[0]
                mag = int(ins[1:])
                end = (0,0)
                if (d == "R"):
                    end = (start[0] + mag, start[1])
                elif (d == "L"):
                    end = (start[0] - mag, start[1])
                elif (d == "U"):
                    end = (start[0], start[1] + mag)
                elif (d == "D"):
                    end = (start[0], start[1] - mag)
                else:
                    raise Exception("Unrecognized direction: " + d)

                wire.append(end)
                start = end
            wires.append(wire)
    return wires

def initmap(xmin, xmax, ymin, ymax):
    m = []
    for _ in range(abs(ymin) + abs(ymax) + 1):
        m.append([0] * (abs(xmin) + abs(xmax) + 1))
    return m

def minmax(wire1, wire2):
    xs = []
    ys = []
    for s in wire1 + wire2:
        xs.append(s[0])
        ys.append(s[1])

    return [min(xs),max(xs), min(ys), max(ys)]

def setmap(m, x, y, v):
    global xmin
    global ymin
    if y-ymin < 0 or x-xmin < 0:
        raise Exception("negative index")
    m[y-ymin][x-xmin] = v

def getmap(m, x, y):
    global xmin
    global ymin
    if y-ymin < 0 or x-xmin < 0:
        raise Exception("negative index")
    return m[y-ymin][x-xmin]

def printmap(m):
    for a in reversed(m):
        print("\t".join(map(lambda x: str(x), a)))

def plotmap(m, w):
    s = (0,0)
    i = 1
    for p in w:
        if p[0] >= s[0]:
            sign = 1
            xr = p[0] + 1
            xl = s[0]
        else:
            sign = -1
            xr = p[0] - 1
            xl = s[0]
        
        for x in range(xl,xr,sign):
            if p[1] >= s[1]:
                sign = 1
                yr = p[1] + 1
                yl = s[1]
            else:
                sign = -1
                yr = p[1] - 1
                yl = s[1]
            for y in range(yl,yr,sign):
                if (x,y) != s:
                    cur = getmap(m,x,y)
                    if cur == 0:
                        setmap(m,x,y,i)
                    i += 1
        s = p

def intersect_maps(m1, m2, xmin, xmax, ymin, ymax):
    inters = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            if getmap(m1, x, y) != 0 and getmap(m2, x, y) != 0:
                inters.append(getmap(m1, x, y) + getmap(m2, x, y))
    return inters

def main(file):
    [wire1, wire2] = parse_input(file)
    global xmin
    global xmax
    global ymin
    global ymax
    [xmin, xmax, ymin, ymax] = minmax(wire1, wire2)

    wire1map = initmap(xmin, xmax, ymin, ymax)
    print("init1")
    plotmap(wire1map, wire1)
    print("plot1")
    wire2map = initmap(xmin, xmax, ymin, ymax)
    print("init2")
    plotmap(wire2map, wire2)
    print("plot2")

    inters = intersect_maps(wire1map, wire2map, xmin, xmax, ymin, ymax)
    #printmap(wire1map)
    print("")
    #printmap(wire2map)
    print("intersect:", min(inters))

main("./input")