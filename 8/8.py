
# outputs list of layers, each of which is a 2d list itself
def parse_input(file, width, height):
    image = []
    with open(file) as fp:
        r = list(fp.read(width))
        while len(r) == width:
            layer = []
            for _ in range(height):
                layer.append(list(map(lambda d: int(d), r)))
                r = list(fp.read(width))
            image.append(layer)
    return image
        
def print_layer(l):
    for r in l:
        for c in r:
            if c == 0:
                print("  ", end = "")
            elif c == 1:
                print("XX", end = "")
            elif c == 2:
                print("!!" ,end = "")
            else:
                raise Exception("Unexpected pixel")
        print("")


def count_digits(layer, d):
    t = 0
    for r in layer:
        t += len(list(filter(lambda x: x == d, r)))
    return t

def checksum():
    image = parse_input("./input",25,6)
    m = 999999999
    m_layer = 0
    i = 0
    for l in image:
        c = count_digits(l, 0)
        if c < m:
            m = c
            m_layer = i
        i += 1

    print(count_digits(image[m_layer], 1) * count_digits(image[m_layer], 2))

def merge_layers(image, w, h):
    d = len(image)
    o = []
    for y in range(h):
        r = []
        for x in range(w):
            for l in range(d):
                p = image[l][y][x]
                if p == 1 or p == 0:
                    r.append(p)
                    break
                elif l == (d - 1):
                    r.append(p)
                if p != 2:
                    raise("Unexpected transparency")
        o.append(r)
    return o

image = parse_input("./input",25,6)
l = merge_layers(image, 25, 6)
print_layer(l)

