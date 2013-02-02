import scipy as sp
import scipy.optimize
import scipy.fftpack
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import matplotlib.patches as patch


# pylab.plot(xaxis, graph) to plot
# for example xasix = sp.linspace(0,1,100)

# Arnold's cat map
def Cat(init):
    # actually, there's no arg
    x0 = init[0]
    y0 = init[1]
    x  = sp.mod(2*x0 + y0, 1)
    y  = sp.mod(x0 + y0, 1)
    return (x,y)


# vCat: Arnold's cat map vectorized.
# element-wise application of Cat (for patch representation)
def vCat(shape):
    pts = shape[0]
    return (sp.array([Cat(p) for p in pts]), shape[1], shape[2])


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
    n = sp.sqrt(cover[0].shape[0]) # num of points per line
    pts = cover[0]
    r   = cover[1]
    colors = cover[2]
    for i in range(int(n**2)):
        # Plot the point
        p = pts[i]
        # Figure out the color of its patch
        cval = colors[i]
        plt.plot((p[0]),(p[1]),'o',color='black')
        subsq = patch.Rectangle(p - [r,r], 2*r, 2*r,color=cval)
        plt.gca().add_patch(subsq)
        plt.savefig('shape.png')


# sqcover = a representation of square by patches.
# Each patch is associated with a color.
# squares consisting of patches == cover
# a cover is a triple (U, r, c). 
# U: a collection of n^2 points evenly distributed over a square. 
# r: the "radius" of a subsquare
# c: the color of each patch
def sqcover(A,n):
    edge = sp.sqrt(A) # the length of an edge
    d = edge/n # the distance between two adjacent points
    r = d/2 # the "radius of "
    end = edge - r # end point
    base = sp.linspace(r, end, n)
    first_line = sp.transpose(sp.vstack((base, r*sp.ones(n))))
    increment = sp.transpose(sp.vstack((sp.zeros(n), d*sp.ones(n))))
    pts = first_line
    y_diff = increment
    for i in range(n-1):
        pts = sp.vstack((pts, first_line + y_diff))
        y_diff = y_diff + increment
    
    # Color matter
    colors = []
    for p in pts:
        cval = n*p[0] + p[1] # the x-coord has a higher weight
        cval = colormap.Spectral(cval/((n+1)*end)) # normalize by the max value that cval can take.
        colors.append(cval)

    colors = sp.array(colors)

    cover = (pts, r, colors)
    return cover


# IterateN: Iterate function g N-times with the initial condition init.
def IterateN(g, init, N):
    result = init
    for i in range(N):
        result = g(result)

    # Return a numpy array
    return result


# GenShape: the simulation code
# Create a square of area A, resolution mxm, iterate it N times.
# Print out the result in a png
def GenShape(g, A, m, N):
    sq = sqcover(A, m)
    new_shape = IterateN(vCat, sq, N)
    cvplot(new_shape)
    

############ PROBABLY USELESS STUFF #############

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

# element-wise application of Cat (works for point representation)
def vCat2(shape):
    return sp.array([Cat(p) for p in shape])

