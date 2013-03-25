## FINITE DIFFERENCE SCHEME FOR 2D GRID

## heating_up()  simulates heat dispersion through a "randomly shaped"  2-dimensional brownie pan 
## into batter using  finite differences, then creates a heatmap of the pan after a specified 
## number of timesteps and can record the final pan and parameter choices in an output file. This 
## function was intended to accept pan boundaries generated by chaotic distortions of the unit
## square, but this version uses a cruder method to randomize the pans (see make_random_pan.)

## PARAMETERS:   
##              - Tb:   bake temperature (C)
##              - Ti:  initial temperature of the oven
##              - tf:  number of timesteps to evaluate
##              - c1: conduction constant of the pan
##              - c2:  conduction constant of the batter
##              - outputfile (optional): string


## SUGGESTED FUNCTION CALL:

## from PDE2 import *
## heating_up()                                      # see default parameters if interested

##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

## set up
import scipy as sp
import numpy as np
sp.set_printoptions(precision = 2, suppress = True, linewidth=200)
from random import choice
from matplotlib import pyplot as PLT
from matplotlib import cm as CM

## creates a heatmap of an array
def create_heatmap(S, oven_points, Tb):
    M = S.copy()
    for point in oven_points:
        S[point] = Tb
    fig = PLT.figure()
    ax1 = fig.add_subplot(111)
    cmap = CM.get_cmap('gist_heat', 15)
    ax1.imshow(M, interpolation = "nearest", cmap = cmap)
    PLT.show()

## creates a "random" set of pan boundary points
def make_random_pan(m,n): ## m and n are dimensions of oven; space is automatically left for air
    bm = m-3
    bn = n-3
    paired_coordinate_list = []
    C = 0
    while (C <= m):
        yco = choice(range(2, bm))
        xco1 = choice(range(2, bn))
        xco2 = choice(range(2, bn))
        paired_coordinate_list.append([(yco, xco1), (yco, xco2)])
        C +=1
    return paired_coordinate_list    

## advances FD one timestep
def u_next(S,i,j,c, delta_t, delta_s,m,n):
   return  S[i,j] + c*delta_t/delta_s**2*(S[min(i+1,m-1),j] + S[max(i-1,0),j] - 4*S[i,j] + S[i, min(j+1,n-1)] + S[i,max(j-1,0)])

## defines a list of batter points by filling in the pan boundaries.  Takes a 
## paired_coordinate_list like that created by make_random_pan()

def define_batter_points(paired_coordinate_list):
    batter_points = []
    for pair in paired_coordinate_list:
        for k in range(pair[0][1], pair[1][1]+1):
            batter_points.append((pair[0][0], k))
    return batter_points

## defines non-batter points adjacent to batter points as pan points
def define_pan_points(batter_points):
    pan_points = []
    for point in batter_points:
        for i in [-1,1]:
            if (point[0]+i, point[1]) in batter_points: continue
            else: pan_points.append((point[0]+i, point[1])) 
            if (point[0], point[1]+i) in batter_points: continue 
            else: pan_points.append((point[0], point[1] + i))
    return pan_points 

## defines every point that is not a batter point or a pan point as an oven point
def define_oven_points(m,n, pan_points, batter_points):
    oven_points =[]
    for i in range(m):
        for j in range(n):
            if not (i,j) in (pan_points + batter_points):
                oven_points.append((i,j))
    return oven_points

## holds oven points at bake temperature
def maintain_boundary(S, Tb, m,n):
    M = S.copy()
    for i in range(m):
        M[0,i] = Tb
        M[n-1,i] = Tb
    for i in range(n):
        M[i,0] = Tb
        M[i, m-1] =Tb
    return M

# sets up initial conditions -- batter points and pan points at initial temperatures
def initial_conditions(In, batter_points, pan_points, Ti, oven_points, Tb):
    for point in batter_points + pan_points:
        In[point] = Ti
    for point in oven_points:
        In[point] = Tb
    return In

## creates a matrix to hold conduction constants
def conduction_constant_matrix(m,n, c1,c2,c3, pan_points, batter_points, oven_points):
    C = sp.zeros(m*n).reshape(m,n)
    for point in pan_points:
        C[point] = c1
    for point in batter_points:
        C[point] = c2
    for point in oven_points:
        C[point] = c3 
    return C

def heating_up(m = 20,n = 20, tf = 2000, c1 = 1.05, c2 =.58 ,c3 = .024, Ti= 24, Tb = 176,delta_t = 1/500000., outputfile = ''):
    # define spatial mesh
    S = sp.zeros(m*n).reshape(m,n)
    
    # create a random pan boundary:
    paired_coordinate_list = make_random_pan(m,n)

    # define batter points from paired coordinate list 
    batter_points = define_batter_points(paired_coordinate_list)
    
    # define pan points
    pan_points = define_pan_points(batter_points)
 
    # define oven points
    oven_points = define_oven_points(m,n,pan_points, batter_points)
   
    # store conduction constants in a matrix
    Cons = conduction_constant_matrix(m,n,c1,c2,c3,pan_points,batter_points,oven_points)
   
    # set batter and pan points to initial temperature
    In = initial_conditions(S.copy(), batter_points, pan_points, Ti, oven_points, Tb)

    # temoral mesh
    Time = sp.arange(1, tf+2)
    delta_s = 1./n
    if not delta_t <= delta_s**2/(2*c1) and delta_t<= delta_s**2/(2*c2):
        print('LOWER DELTA_T!!!\n\n\n\n\n\n\n\n\n')
        sleep(5)
    
    # set initial and boundary conditions:
    S1 = In 
    S2 = S1.copy()
    for t in Time[:-1]:
        for i in range(m):
            for j in range(n):
                S2[i,j] = u_next(S1, i,j,Cons[i,j],delta_t, delta_s,m,n)
                S2 = maintain_boundary(S2, Tb, m,n)
                S1 = S2.copy()
        print(S2)
        print('\n')
    if not outputfile == '':
        output = open(outputfile, mode = 'w')
        output.write(str(S2)+ '\n' + str((m,n, tf, c1, c2, Ti, Tb,delta_t))+ '\n')
        output.close()
    create_heatmap(S2, oven_points+pan_points, Tb)
    return S2
