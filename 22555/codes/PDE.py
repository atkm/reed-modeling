## finite difference for 2d grid.
## set up
import scipy as sp
sp.set_printoptions(precision = 3, suppress = True, linewidth=200)
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
            if (i > w-1 and j > w-1) and (i < m-1 and j < n-1):
                In[i,j] = Ti

def heating_up(m,n, tf, c1, c2,w, Ti, Tb,delta_t):
    # define spatial mesh
    S = sp.zeros(m*n).reshape(m,n)
    Cons = S.copy()
    In = S.copy()
    # define conduction constants
    for i in range(m):
        for j in range(n):
            if i <= w-1 or j <= w-1 or i > m-w-1:
                Cons[i,j] = c1
            else:
                Cons[i,j] = c2
    # temoral mesh
    Time = sp.arange(1, tf+2)
    delta_s = 1./n
    if not delta_t <= delta_s**2/(2*c1) and delta_t<= delta_s**2/(2*c2):
        print 'LOWER DELTA_T!!!\n\n\n\n\n\n\n\n\n'
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
        print (100*S2)
        print '\n'
    print S2
