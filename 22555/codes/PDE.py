## finite difference for 2d grid.
## set up
import scipy as sp
sp.set_printoptions(precision = 2, suppress = True, linewidth=200)
## suggested... Tb = 176, Ti = 26, c1 = 3, c2 = .17, w = 1

## step forward
def u_next(S,i,j,c, delta_t, delta_s,m,n):
   return  S[i,j] + c*delta_t/delta_s**2*(S[min(i+1,m-1),j] + S[max(i-1,0),j] - 4*S[i,j] + S[i, min(j+1,n-1)] + S[i,max(j-1,0)])

#bindM will maintain boundary conditions
def bindM(S, Tb):
    M = S.copy()
    m = M.shape[0]
    n = M.shape[1]
    for i in range(m):
        for j in range(n):
            M[i,0] = M[0,j] = M[m-1,j] = M[i,n-1] = Tb
    return M 
# sets up initial conditions
def init_con(In, Ti,w):
    m= In.shape[0]
    n = In.shape[1]
    for i in range(m):
        for j in range(n):
            if (i >= w and j >= w) and (i < m-1 and j < n-1):
                In[i,j] = Ti

def heating_up(m,n, tf, c1, c2,w, Ti, Tb,delta_t,outputfile):
    # define spatial mesh
    S = sp.zeros(m*n).reshape(m,n)
    Cons = S.copy()
    In = S.copy()
    # define conduction constants
    for i in range(m):
        for j in range(n):
            Cons[i,0] = Cons[0,j] = Cons[m-1,j] = Cons[i,n-1] = 0.024
            if (0 < i <= w and 0 < j < n-1) or (0 < j <= w and 0<i<m-2) or (m-w-1 < i <= m-2 and 0<j<n-2): 
                Cons[i,j] = c1
                Cons[m-i-1,j] = c1

    for i in range(m):
        for j in range(n):
            if Cons[i,j] == 0:
                Cons[i,j] = c2
    # temoral mesh
    Time = sp.arange(1, tf+2)
    delta_s = 1./n
    if not delta_t <= delta_s**2/(2*c1) and delta_t<= delta_s**2/(2*c2):
        print('LOWER DELTA_T!!!\n\n\n\n\n\n\n\n\n')
        sleep(5)
    # set initial and boundary conditions:
    S = bindM(S, Tb)
    init_con(In, Ti,w)
    S1 = S + In 
    S2 = S1.copy()
    for t in Time[:-1]:
        for i in range(m):
            for j in range(n):
                S2[i,j] = u_next(S1, i,j,Cons[i,j],delta_t, delta_s,m,n)
                S2 = bindM(S2, Tb)
                S1 = S2.copy()
        print(S2)
        print('\n')
    output = open(outputfile, mode = 'w')
    output.write(str(S2)+ '\n' + str((m,n, tf, c1, c2,w, Ti, Tb,delta_t))+ '\n')
    output.close()
    return S2

def u_next3(S,i,j,k,c, delta_t, delta_s,m,n,l):
       return  S[i,j,k] + c*delta_t/delta_s**2*(S[min(i+1,m-1),j,k] + S[i, min(j+1,n-1),k] + S[i,j,min(k+1,l-1)] + S[max(i-1,0),j,k] + S[i, max(j-1,0), k] + S[i,j,max(k-1,0)]  - 6*S[i,j,k])

def bindM3(S, Tb):
    M = S.copy()
    m = M.shape[0]
    n = M.shape[1]
    l = M.shape[2]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                if 0 in [i,j,k] or 1 in [m-i,n-j,l-k]:
                    M[i,j,k] = Tb
    return M
    
def bindMgen(S, Tb, pan_points):
    M = S.copy()
    m = M.shape[0]
    n = M.shape[1]
    l = M.shape[2]
    for i in range(n):
        for j in range(m):
            for k in range(l):
                if not sp.array([i,j,k]) in pan_points:
                    return pan_points
                    M[i,j,k] = Tb
    return M
    
def init_congen(In, Ti, pan_points):
    for p in pan_points:
        tup = tuple([int(i) for i in p])
        In[tup] = Ti
                
def init_con3(In, Ti):
    m = In.shape[0]
    n = In.shape[1]
    l = In.shape[2]
    for i in range(m):
        for j in range(n):
            for k in range(l):
                if not (0 in [i,j,k] or 1 in [m-i,n-j,l-k]):
                    In[i,j,k] = Ti
                else:
                    In[i,j,k] = 0
    return In                


def bound_list(shape):
    height = int(100*shape.wall[0,2])
    boundary_points  = []
    for i in range(height):
        wa = shape.wall_func(i/100.)
        boundary_points.append([(wa[i,0], wa[i,1], wa[i,2]) for i in range(shape.resolution)])
    return    

def uniques(A):
    uniqs = []
    for i in range(len(A)):
        if not i in uniqs:
            uniqs.append(i)
    return uniqs

def myround(x):
    return round(x,1)

def array_round(A):
    vecround = sp.vectorize(myround)
    return vecround(A)

def modify_pan_points(pan_points):
    alist = []
    for array in pan_points:
      alist.append(array)
    pan_points = sp.vstack(alist)
    return pan_points  
 
def heating_up_gen(pan_points,tf, c1, c2,w, Ti, Tb, delta_t, outputfile):
    m=n=l = int(max([i for i in sp.transpose(pan_points[2])[0]])+1)
    pan_points = modify_pan_points(pan_points)
    S = sp.zeros(m*n*l).reshape(m,n,l)
    Cons = S.copy()
    In = S.copy()
    # indentify interior points from pan_points:
    zmax = int(max([p[2] for p in pan_points]))
    xys = pan_points[:,:2]
    xyz = unique(xys) 
    pre_interior_points = pan_points
    M = 0
    for h in range(1, zmax):
      for dub in xyz:
        slice = sp.array([[dub[0], dub[1], h]])
        pre_interior_points[M,:] = slice
        M+=1
    interior_points = []
    N = 0
    for slice1 in pre_interior_points:
        Q = 0
        for slice2 in pan_points:
          if slice1[0] == slice2[0] and slice1[1] == slice2[1]:
              Q = 1
        if Q == 0:
           interior_points[N,:] = slice1
           N+=1        
    # define conduction constants
    for p in pan_points:
      tup = tuple([int(i) for i in p])
      Cons[tup] = c1
    for p in interior_points:
      tup = tuple([int(i) for i in p])
      Cons[p] = c2
    Time = sp.arange(1,tf+2)
    delta_s = 1./n
    if not delta_t <= delta_s**2/(2*c1) and delta_t<= delta_s**2/(2*c2) and delta_t <= delta_s**2/(2*.024):
        print('LOWER DELTA_T!!!\n\n\n\n\n\n\n\n\n')
        sleep(5)
    S = bindMgen(S, Tb, pan_points) 
    init_congen(In, Ti, pan_points) 
    S1 = S+In
    S2 = S1.copy()
    for t in Time[:-1]:
        for i in range(m):
          for j in range(n):
            for k in range(l):
                 S2[i,j,k] = u_next3(S1, i,j,k,Cons[i,j,k],delta_t, delta_s,m,n,l)
                 S2 = bindMgen(S2, Tb, pan_points)
                 S1 = S2.copy()
        for i in range(l):
            print(S2[:,:,l-i])
            print('\n')
        print('\n\n')
    output = open(outputfile, mode = 'w')
    output.write(str(S2))
    output.close()
    return S2


 


def heating_up3(m,n,l, tf, c1, c2,w, Ti, Tb,delta_t, outputfile):
    # define spatial mesh
    S = sp.zeros(m*n*l).reshape(m,n,l)
    Cons = S.copy()
    In = S.copy()
    # define conduction constants
    for i in range(m):
       for j in range(n):
           for k in range(l):
               if 0 in [i,j,k] or 1 in [m-i,n-j,l-k]:
                   Cons[i,j,k] = .024 
               if 0<i<=w and 0<j<n-1 and 0<k<l-1:
                   Cons[i,j,k] = c1
               if 0<j<=w and 0<i<m-1 and 0 <k<l-1:
                   Cons[i,j,k] = c1
               if 0 <k<= w and 0<i<m-1 and 0<j<n-1:
                   Cons[i,j,k] = c1
               if m-1-w <= i <m-1 and 0<j<n-1 and 0<k<l-1:
                   Cons[i,j,k] = c1
               if n-1-w <= j < n-1 and 0<i< m-1 and 0<k<l-1:
                   Cons[i,j,k] = c1
               if Cons[i,j,k] == 0:
                   Cons[i,j,k] = c2
    # temoral mesh
    Time = sp.arange(1, tf+2)
    delta_s = 1./n
    if not delta_t <= delta_s**2/(2*c1) and delta_t<= delta_s**2/(2*c2) and delta_t <= delta_s**2/(2*.024):
        print('LOWER DELTA_T!!!\n\n\n\n\n\n\n\n\n')
        sleep(5)
    # set initial and boundary conditions:
    S = bindM3(S, Tb)
    init_con3(In, Ti)
    S1 = S + In 
    S2 = S1.copy()
    for t in Time[:-1]:
        for i in range(m):
            for j in range(n):
                for k in range(l):
                    S2[i,j,k] = u_next3(S1, i,j,k,Cons[i,j,k],delta_t, delta_s,m,n,l)
                    S2 = bindM3(S2, Tb)
                    S1 = S2.copy()
        for i in range(l):
            print(S2[:,:,l-i])
            print('\n')
        print('\n\n')
    output = open(outputfile, mode = 'w')
    output.write(str(S2))
    output.close()
    return S2

def unique(a):
    order = sp.lexsort(a.T)
    a = a[order]
    diff = sp.diff(a, axis=0)
    ui = sp.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1) 
    return a[ui]

def multidim_setdiff(arr1, arr2):
    arr1_vquew = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    set_difference = numpy.setdiff1d(arr1_view, arr2_view)
    return set_difference.view(arr1.dtype).reshape(-1, arr1.shape[1])
