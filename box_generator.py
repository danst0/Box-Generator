#!/usr/bin/env python3

"""box_generator
Generator for Boxes with in either castled or uncastled style. Output as DXF.

Usage:
  box_generator.py
  box_generator.py <width> <height> <depth> <thickness> [--castled|--uncastled] [--spacing=<mm>] [--lid=<type>] [--lid-side=<1|2|3>]
  box_generator.py (-h | --help)
  box_generator.py --version

Options:
  -c --castled              Castled box 
  -u --uncastled            Uncastled box [default]
  -s --spacing=<mm>         Select spacing between parts [default: thickness]
  -l --lid=<type>           Establish one side as a lid (_i_nside or _o_utside) [default: None]
  -i --lid-side=<1|2|3>     Select side for lid [default: 1]
  -h --help                 Show this screen.
  --version                 Show version.
  
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
    else:
        shape = 'n'
    # else:
#         shape = input("\nCastled? (y/n): ")
#     
    print('Processing input...')
        
    if (shape[0] == 'y'):
        rectangle = lambda p1x, p1y, p2x, p2y, th, lr, tb, fout: \
                    castled_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout)
    else:
        rectangle = lambda p1x, p1y, p2x, p2y, th, lr, tb, fout: \
                    pretty_rectangle(p1x, p1y, p2x, p2y, th, lr, tb, fout)
    
    dim = [w, d, h]
    dim.sort()
    dim.reverse()
    
    print(arguments)
    if arguments['--spacing'] != 'thickness':
        spacing = tk + int(arguments['--spacing'])
    else:
        spacing = tk + tk 
    
            

    print('Generating output...')
    

    drawing = new_drawing('box.dxf')
    # arranged from left to right and top to bottom

    rectangle(tk, spacing + dim[0]+2*tk, dim[1]+tk, spacing + dim[0]+dim[2]+2*tk, tk, 0, 0, drawing)
    
    rectangle(2*spacing + dim[1]+dim[2]+3*tk, spacing + dim[0]+2*tk, 2* spacing + 2*dim[1]+dim[2]+3*tk, spacing + dim[0]+dim[2]+2*tk, tk, 0, 0, drawing)

    rectangle(tk, tk, dim[1]+tk, dim[0]+tk, tk, 1, 1, drawing)

    rectangle(spacing + dim[1]+2*tk, tk, spacing + dim[1]+dim[2]+2*tk, dim[0]+tk, tk, 0, 1, drawing)

    rectangle(2* spacing + dim[1]+dim[2]+3*tk, tk, 2*spacing + 2*dim[1]+dim[2]+3*tk, dim[0]+tk, tk, 1, 1, drawing)

    rectangle(3* spacing + 2*dim[1]+dim[2]+4*tk, tk, 3* spacing+ 2*dim[1]+2*dim[2]+4*tk, dim[0]+tk, tk, 0, 1, drawing)
 



    save(drawing)


    
    print('Done.')
    