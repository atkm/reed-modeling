import scipy as sp
import scipy.optimize
import scipy.fftpack
import matplotlib.pylab as plt
import matplotlib.cm as colormap

# pylab.plot(xaxis, graph) to plot
# for example xasix = sp.linspace(0,1,100)

def Henon(init, args):
    """
    args = (a,b)
    init = (x0, y0)
    Henon map 
    f(x,y) = y + 1 - ax^n
    g(x,y) = b*x
    """
    a = args[0]
    b = args[1]
    x0 = init[0]
    y0 = init[1]
    x = y0 + 1 - a*(x0**2)
    y = b * x0
    return (x,y)

def Cat(init):
    # actually, there's no arg
    x0 = init[0]
    y0 = init[1]
    x  = sp.mod(2*x0 + y0, 1)
    y  = sp.mod(x0 + y0, 1)
    return (x,y)

# element-wise application of Cat
def vCat(shape):
    return sp.array([Cat(p) for p in shape])

# a convenient plot function for shapes
# shape == an array of lists of length 2 (x,y).
def shplot(shape):
    # plot points
    plt.plot(shape[:,0], shape[:,1],'o', color='red')
    # plot line segments
    pt1 = shape[0]
    for i in range(len(shape)-1):
        pt2 = shape[i + 1]
        ptm = sp.vstack((pt1,pt2))
        plt.plot(ptm[:,0], ptm[:,1])
        pt1 = pt2

# cvplot: plot a cover
def cvplot(cover):
    pts = cover[0]
    r   = cover[1]
    for p in pts:
        # Plot the point
        cval = p[0]*10 + p[1]
        #cval = colormap.Spectral(cval)
        plt.plot((p[0]),(p[1]),'o',color='black')
        # Figure out where the four corners of the patch are
        c1 = [p[0]-r, p[1]-r]
        c2 = [p[0]+r, p[1]-r]
        c3 = [p[0]-r, p[1]+r]
        c4 = [p[0]+r, p[1]+r]
        rect = sp.transpose(sp.vstack((c1,c2,c3,c4)))
        print(rect)
        plt.fill(rect[0],rect[1], 'b', alpha = 0.2)

# sqshape == a representation of square by boundary points
# Create a square of area A with n points on one edge
# (0,0) is the bottom left corner
# Build points in this order:
# bottom left -> top left -> top right -> bottom right -> bottom left
# top, left, bottom, right are defined as:
#  t t t t r    
#  l       r     
#  l       r   
#  l       r   
#  l b b b b   
#
def sqshape(A,n):
    edge_len = sp.sqrt(A) # the length of each edge
    base = sp.linspace(0, edge_len, n+1) # n+1 points, equally spaced
    # create left edge
    left = sp.transpose(sp.vstack((sp.zeros(n), base[0:-1])) )
    # top edge
    top_y = base[-1] # the height of the square
    top = sp.transpose(sp.vstack((base[0:-1],top_y * sp.ones(n))))
    # bottom edge
    bottom = sp.transpose((base[1:], sp.vstack((sp.zeros(n)))))

    # right edge
    right_x = top_y # the x-coordinate of the right edge
    right = sp.transpose(sp.vstack((right_x * sp.ones(n), top_y - base[0:-1])))
    return sp.vstack((left, top, right, bottom[::-1])) # bottom is reversed for consistency


# sqcover = a representation of square by patches
# squares consisting of patches == cover
# a cover is a double (U, d). 
# U: a collection of n^2 points evenly distributed over a square. 
# d: the "radius" of a square. i.e. 2d = len(edge of a subsquare)
def sqcover(A,n):
    edge = sp.sqrt(A) # the length of an edge
    r = edge/(2*n)
    end = edge - r # end point
    base = sp.linspace(r, end, n)
    first_line = sp.transpose(sp.vstack((base, r*sp.ones(n))))
    increment = sp.transpose(sp.vstack((sp.zeros(n), r*sp.ones(n))))
    pts = first_line
    y_diff = increment
    for i in range(n):
        pts = sp.vstack((pts, first_line + y_diff))
        y_diff = y_diff + increment
    
    cover = (pts, r)
    return cover

def IterateN(g, init, N):
    result = init
    for i in range(N):
        result = g(result)

    # Return a numpy array
    return result


def IterateList2D(g, init, N):
    """
    Iterate the function g(x, mu) N-1 times, starting at x0, so that the
    full trajectory contains N points.
    Returns the entire list 
    (x, g(x), g(g(x)), ... g(g(...(g(x))...))). 

    use
        pylab.hist(attractorXs, bins=500, normed=1)
        pylab.show()
    to see the density of points.
    """
    x0 = init[0]
    y0 = init[1]

    result = [(x0, y0)]
    for i in range(N-1):
      result.append(g(result[-1]))

    # Return a numpy array
    return np.array(result)

#def PlotIterate2D(g, init, N, args=()):
#    """
#    Plots g, the diagonal y=x, and the boxes made of the segments
#    [[x0,x0], [x0, g(x0)], [g(x0), g(x0)], [g(x0), g(g(x0))], ...
#    """
#    points = IterateList2D(g, init, N, args)
#    matplotlib.pyplot.scatter(points[:,0], points[:,1], s=0.1, color='darkblue')
