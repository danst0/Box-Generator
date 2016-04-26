#!/usr/bin/env python3

"""box_generator
Generator for Boxes with in either castled or uncastled style. Output as DXF.

Usage:
  box_generator.py
  box_generator.py <width> <height> <depth> <thickness> (--castled|--uncastled)
  box_generator.py (-h | --help)
  box_generator.py --version

Options:
  -c --castled      Castled box
  -u --uncastled    Uncastled box
  -h --help         Show this screen.
  --version         Show version.
  
"""

from docopt import docopt

def new_drawing(name):
    fheader = open("template.dxf", "r")
    fout = open(name, "w")

    fout.write(fheader.read())
    return fout

def save(fout):
    fout.write("ENDSEC\n  0\nEOF")
    fout.close()

def begin_polyline(fout):
    fout.write("POLYLINE\n  8\n0\n  66\n1\n  10\n0.0\n  20\n0.0\n  30\n0" + \
        "\n  70\n1\n  0\n")

def add_vertex(fout, x, y):
    fout.write("VERTEX\n  8\n0\n  10\n" + str(x) + "\n  20\n" + str(y)\
               + "\n  0\n")

def end_polyline(fout):
    fout.write("SEQEND\n  0\n")

def castled_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout):
    ny = 9
    dy = (p2y - p1y)/ny
    nx = 9
    dx = (p2x - p1x)/nx
    begin_polyline(fout)
    add_vertex(fout, p1x, p1y)
    t = lr%2
    for ind in range(0, ny):
        x = p1x - t*th
        add_vertex(fout, x, p1y + ind*dy)
        add_vertex(fout, x, p1y + (ind+1)*dy)
        t = (t+1)%2
    add_vertex(fout, p1x, p2y)
    t = tb%2
    for ind in range(0, nx):
        y = p2y + t*th
        add_vertex(fout, p1x + ind*dx, y)
        add_vertex(fout, p1x + (ind+1)*dx, y)
        t = (t+1)%2
    add_vertex(fout, p2x, p2y)
    t = lr%2
    for ind in range(0, ny):
        x = p2x + t*th
        add_vertex(fout, x, p2y - ind*dy)
        add_vertex(fout, x, p2y - (ind+1)*dy)
        t = (t+1)%2
    add_vertex(fout, p2x, p1y)
    t = tb%2
    for ind in range(0, nx):
        y = p1y - t*th
        add_vertex(fout, p2x - ind*dx, y)
        add_vertex(fout, p2x - (ind+1)*dx, y)
        t = (t+1)%2
    add_vertex(fout, p1x, p1y)
    end_polyline(fout)

def pretty_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout):
    begin_polyline(fout)
    add_vertex(fout, p1x, p1y)
    t = lr%2
    x = p1x - t*th
    add_vertex(fout, x, p1y)
    add_vertex(fout, x, p1y+th)
    t = (t+1)%2
    x = p1x - t*th
    add_vertex(fout, x, p1y+th)
    add_vertex(fout, x, p2y-th)
    t = (t+1)%2
    x = p1x - t*th
    add_vertex(fout, x, p2y-th)
    add_vertex(fout, x, p2y)
    add_vertex(fout, p1x, p2y)
    t = tb%2
    y = p2y + t*th
    add_vertex(fout, p1x, y)
    add_vertex(fout, p1x+th, y)
    t = (t+1)%2
    y = p2y + t*th
    add_vertex(fout, p1x+th, y)
    add_vertex(fout, p2x-th, y)
    t = (t+1)%2
    y = p2y + t*th
    add_vertex(fout, p2x-th, y)
    add_vertex(fout, p2x, y)
    add_vertex(fout, p2x, p2y)
    t = lr%2
    x = p2x + t*th
    add_vertex(fout, x, p2y)
    add_vertex(fout, x, p2y-th)
    t = (t+1)%2
    x = p2x + t*th
    add_vertex(fout, x, p2y-th)
    add_vertex(fout, x, p1y+th)
    t = (t+1)%2
    x = p2x + t*th
    add_vertex(fout, x, p1y+th)
    add_vertex(fout, x, p1y)
    add_vertex(fout, p2x, p1y)
    t = tb%2
    y = p1y - t*th
    add_vertex(fout, p2x, y)
    add_vertex(fout, p2x-th, y)
    t = (t+1)%2
    y = p1y - t*th
    add_vertex(fout, p2x-th, y)
    add_vertex(fout, p1x+th, y)
    t = (t+1)%2
    y = p1y - t*th
    add_vertex(fout, p1x+th, y)
    add_vertex(fout, p1x, y)
    add_vertex(fout, p1x, p1y)
    end_polyline(fout)


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Box Generator 0.1')
    #print(arguments)
    
    print("The dimensions are the desired inner dimensions of the box in mm.")
    if arguments['<width>']:
        w = float(arguments['<width>'])
    else:
        w = float(input("\nWidth: "))
    if arguments['<depth>']:
        d = float(arguments['<depth>'])
    else:
        d = float(input("\nDepth: "))
    if arguments['<height>']:
        h = float(arguments['<height>'])
    else:
        h = float(input("\nHeight: "))
    if arguments['<thickness>']:
        tk = float(arguments['<thickness>'])
    else:
        tk = float(input("\nThickness of Material: "))
    
    if arguments['--castled']:
         shape = 'y'
    elif arguments['--uncastled']:
        shape = 'n'
    else:
        shape = input("\nCastled? (y/n): ")
    
    
    if (shape[0] == 'y'):
        rectangle = lambda p1x, p1y, p2x, p2y, th, lr, tb, fout: \
                    castled_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout)
    else:
        rectangle = lambda p1x, p1y, p2x, p2y, th, lr, tb, fout: \
                    pretty_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout)
    
    dim = [w, d, h]
    dim.sort()
    dim.reverse()
    
    if ((dim[0] + 2*tk)>18):
        if ((dim[1] + 3*tk + dim[2])<=18):
            drawing = new_drawing('box1.dxf')
            rectangle(tk, tk, dim[0] + tk, dim[1]+ tk, tk, 1, 1, drawing)
            rectangle(tk, dim[1] + 2*tk, dim[0] + tk, dim[1] + dim[2] \
                      + 2*tk, tk, 1, 0, drawing)
            drawing2 = new_drawing('box2.dxf')
            rectangle(tk, tk, dim[0] + tk, dim[1]+ tk, tk, 1, 1, drawing2)
            rectangle(tk, dim[1] + 2*tk, dim[0] + tk, dim[1] + dim[2] \
                      + 2*tk, tk, 1, 0, drawing2)
            if ((dim[0]+3*tk + dim[2])>32):
                save(drawing)
                save(drawing2)
                drawing3 = new_drawing('box3.dxf')
                rectangle(tk, tk, dim[1]+tk, dim[2]+tk, tk, 0, 0, drawing3)
                rectangle(tk, dim[2]+3*tk, dim[1]+tk, 2*dim[2]+3*tk,\
                          tk, 0, 0, drawing3)
                save(drawing3)
            else:
                rectangle(dim[0]+2*tk, tk, dim[0]+dim[2]+2*tk, dim[1]+\
                          tk, tk, 0, 0, drawing)
                rectangle(dim[0]+2*tk, tk, dim[0]+dim[2]+2*tk, dim[1]+\
                          tk, tk, 0, 0, drawing2)
                save(drawing)
                save(drawing2)
        elif ((dim[1] + 2*tk)<=18):
            drawing = new_drawing('box1.dxf')
            rectangle(tk, tk, dim[0]+tk, dim[1]+tk, tk, 1, 1, drawing)
            if ((dim[2] + 2*tk)>9):
                save(drawing)
                drawing2 = new_drawing('box2.dxf')
                rectangle(tk, tk, dim[0]+tk, dim[2]+tk, tk, 1, 0, drawing2)
                save(drawing2)
                drawing3 = new_drawing('box3.dxf')
                rectangle(tk, tk, dim[1]+tk, dim[2]+tk, tk, 0, 0, drawing3)
                save(drawing3)
            else:
                drawing2 = new_drawing('box2.dxf')
                rectangle(tk, tk, dim[0]+tk, dim[2]+tk, tk, 1, 0, drawing2)
                rectangle(tk, dim[2]+3*tk, dim[0]+tk, 2*dim[2]+2*tk, \
                          tk, 1, 0, drawing2)
                save(drawing2)
                if ((dim[0] + 3*tk + dim[1])>32):
                    save(drawing)
                    drawing3 = new_drawing('box3.dxf')
                    rectangle(tk, tk, dim[1]+tk, dim[2]+tk, tk, 0, 0, drawing3)
                    rectangle(tk, dim[2]+3*tk, dim[1]+tk, 2*dim[2]+\
                              3*tk, tk, 0, 0, drawing3)
                    save(drawing3)
        else:
            print("More than 2 dimensions are greater than 18 inches. This piece"+\
                  " cannot fit on the laser cutter bed.")
            input()
    
    else:
        drawing = new_drawing('box1.dxf')
        rectangle(tk, tk, dim[1]+tk, dim[0]+tk, tk, 1, 1, drawing)
        rectangle(dim[1]+2*tk, tk, dim[1]+dim[2]+2*tk, dim[0]+tk, tk, 0, 1, drawing)
        if ((dim[1]+dim[2]+ 2*tk) < 18):
            rectangle(dim[1]+dim[2]+3*tk, tk, 2*dim[1]+dim[2]+3*tk, dim[0]+tk, tk,\
                      1, 1, drawing)
            rectangle(2*dim[1]+dim[2]+4*tk, tk, 2*dim[1]+2*dim[2]+\
                      4*tk, dim[0]+tk, tk, 0, 1, drawing)
            if ((dim[0]+dim[2]+3*tk) < 18):
                rectangle(tk, dim[0]+2*tk, dim[1]+tk, dim[0]+\
                          dim[2]+2*tk, tk, 0, 0, drawing)
                rectangle(dim[1]+dim[2]+3*tk, dim[0]+2*tk, 2*dim[1]+\
                          dim[2]+3*tk, dim[0]+dim[2]+2*tk, tk, 0, 0, drawing)
                save(drawing)
            else:
                save(drawing)
                drawing2 = new_drawing('box2.dxf')
                rectangle(tk, tk, dim[1]+tk, dim[2]+tk, tk, 0, 0, drawing2)
                rectangle(dim[1]+2*tk, tk, 2*(dim[1]+tk), dim[2]+tk, \
                          tk, 0, 0, drawing2)
                save(drawing2)
        else:
            if ((dim[1]+2*dim[2]+4*tk) < 36):
                rectangle(dim[1]+dim[2]+4*tk, tk, dim[1]+2*dim[2]+4*tk, \
                          dim[1]+tk, tk, 0, 0, drawing)
                save(drawing)
            else:
                save(drawing)
                drawing2 = new_drawing('box2.dxf')
                rectangle(tk, tk, dim[1]+tk, dim[2]+tk, tk, 0, 0, drawing2)
                rectangle(dim[1]+2*tk, tk, 2*(dim[1]+tk), dim[2]+tk, \
                                       tk, 0, 0, drawing2)
                save(drawing2)


    
