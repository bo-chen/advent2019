import os
import sys

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

                wire.append([start, end])
                start = end
            wires.append(wire)
    return wires

def range_intersect(a1 : list, a2 : list):
    a1.sort()
    a2.sort()
    if (a1[1] < a2[0] or a1[0] > a2[1]):
        return False
    return True

def seg_intersect(seg1 : tuple, seg2 : tuple):
    if (seg1[0] == (0,0)):
        return None
    # If x intersect then the y is 
    if (range_intersect([seg1[0][0],seg1[1][0]], [seg2[0][0],seg2[1][0]]) 
    and range_intersect([seg1[0][1],seg1[1][1]], [seg2[0][1],seg2[1][1]])):
        x, y = 0, 0
        if seg1[0][0] == seg1[1][0]:
            x = seg1[0][0]
            if seg2[0][0] == seg2[1][0]:
                raise Exception("Unexpected intersection1", seg1, seg2)
        else:
            x = seg2[0][0]
            if seg2[0][0] != seg2[1][0]:
                raise Exception("Unexpected intersection2", seg1, seg2)
        
        if seg1[0][1] == seg1[1][1]:
            y = seg1[0][1]
            if seg2[0][1] == seg2[1][1]:
                raise Exception("Unexpected intersection3", seg1, seg2)
        else:
            y = seg2[0][1]
            if seg2[0][1] != seg2[1][1]:
                raise Exception("Unexpected intersection4", seg1, seg2)
        return (x, y)
    return None

def intersect_wires(wire1, wire2):
    intersects = []
    for s1 in wire1:
        for s2 in wire2:
            p = seg_intersect(s1, s2)
            if p:
                intersects.append(p)
    return intersects

def main(file):
    wires = parse_input(file)
    print(wires)
    intersects : list = intersect_wires(wires[0], wires[1])
    intersects.sort(key = lambda p : abs(p[0]) + abs(p[1]))

    print(intersects)
    print(intersects[0])

main("./input")