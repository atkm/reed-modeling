import scipy as sp
import scipy.optimize
import scipy.fftpack
import matplotlib.pylab as plt
import matplotlib.cm as colormap
import matplotlib.patches as patch
import random


# pylab.plot(xaxis, graph) to plot
# for example xasix = sp.linspace(0,1,100)

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

# circle
def circle(A, n):
    r = sp.sqrt(A) # the radius

# Chirikov standard map
# K > 1 is pretty chaotic. 
# use K = 0.5 as a default
def Kick(init,param):
    k = param
    x0 = init[0] * 2*sp.pi
    y0 = init[1] * 2*sp.pi
    # tweaked from the default: y = sp.mod(y0 + k * sp.sin(x0), 2*sp.pi)
    y = sp.mod(1.05 * sp.pi + y0 + k * sp.sin(x0), 2*sp.pi)
    x = sp.mod(x0 + y, 2*sp.pi)
    return (x/(2*sp.pi),y/(2*sp.pi))

def vKick(shape, param):
    pts = shape[0]
    return (sp.array([Kick(p,param) for p in pts]), shape[1], shape[2])

# Arnold's cat map
# default param = 2
def Cat(init,param=2):
    a  = param
    b  = a - 1
    x0 = init[0]
    y0 = init[1]
    x  = sp.mod(a*x0 + b*y0, 1)
    y  = sp.mod(x0 + y0, 1)
    return (x,y)

# vCat: Arnold's cat map vectorized.
# element-wise application of Cat (for patch representation)
# Increasing param would increase the x-orientation of the distortion
def vCat(shape,param=2):
    pts = shape[0]
    return (sp.array([Cat(p,param) for p in pts]), shape[1], shape[2])


# cvplot: plot a cover
def cvplot(cover, name):
    n = sp.sqrt(cover[0].shape[0]) # num of points per line
    pts = cover[0]
    r   = cover[1]
    colors = cover[2]
    for i in range(int(n**2)):
        # Plot the point
        p = pts[i]
        # Figure out the color of its patch
        cval = colors[i]
        plt.plot((p[0]),(p[1]),'o', markersize = 40/n, color='black')
        subsq = patch.Rectangle(p - [r,r], 2*r, 2*r,color=cval)
        plt.gca().add_patch(subsq)
        plt.savefig(name)

# interactive version
def cvplot_nosave(cover):
    n = sp.sqrt(cover[0].shape[0]) # num of points per line
    pts = cover[0]
    r   = cover[1]
    colors = cover[2]
    for i in range(int(n**2)):
        # Plot the point
        p = pts[i]
        # Figure out the color of its patch
        cval = colors[i]
        plt.plot((p[0]),(p[1]),'o', markersize = 40/n, color='black')
        subsq = patch.Rectangle(p - [r,r], 2*r, 2*r,color=cval)
        plt.gca().add_patch(subsq)

# animation in interactive version
# NOT WORKING
def cvanimate(cover,N):
    cvplot_nosave(cover)
    for i in range(N):
        cover = vCat(cover,param)
        plt.cla()
        cvplot_nosave(cover)

# IterateN: Iterate function g N-times with the initial condition init.
def IterateN(g, init, N, param):
    result = init
    for i in range(N):
        result = g(result,param)

    # Return a numpy array
    return result

# IterRand: Do one iteration of Cat or Kick map
def IterRand(init):
    rnum = random.randint(0,2) # generate 0 or 1
    if rnum==1:
        g = vCat
        param = 5*random.random() # generate a parameter between 0 and 5
    else:
        g = vKick
        param = random.random() # generate a parameter between 0 and 1

    return g(result,param)


# IterRandN: Randomly iterate N times
def IterRandN(init, N):
    result = init
    for i in range(N):
        result = IterRand(result)
    return result


# GenShape: the simulation code
# Create a square of area A, resolution mxm, iterate it N times.
# Print out the result in a png
def GenShape(g, A, m, N, name):
    sq = sqcover(A, m)
    if (N!=0):
        new_shape = IterateN(vCat, sq, N)
    else:
        new_shape = sq

    cvplot(new_shape, name)
    

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

