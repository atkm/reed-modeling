## finite difference for 2d grid.
m = 20
n = 20
tf = 30
c1 = 205 #205 ~ aluminum
c2 = .17 #.17 ~ olive oil
Tb = 176.67
Ti = 26.67
# pan width (in fraction of n)
w = 1
delta_s = 1/n
delta_t = 1
# define spatial mesh
S = matrix(RR,m,n)
Cons = copy(S)
In = copy(S)
# define conduction constants
for i in range(m):
    for j in range(n):
        if i <= w-1 or j <= w-1 or i > m-w-1:
            Cons[i,j] = c1
        else:
            Cons[i,j] = c2


# define temporal mesh
Time  = [0..tf+1]

def u_next(S,i,j,c):
   return  S[i,j] + c*delta_t/delta_s^2*(S[min(i+1,m-1),j] + S[max(i-1,0),j] - 4*S[i,j] + S[i, min(j+1,n-1)] + S[i,max(j-1,0)])

#maintain boundary conditions
def bindM(S, Tb):
    M = copy(S)
    m = M.dimensions()[0]
    n = M.dimensions()[1]
    for i in range(m):
        for j in range(n):
            M[i,0] = M[0,j] = M[m-1,j] = M[i,n-1] = Tb
    return M 
# set boundary conditions and initial conditions:
for i in range(m):
    for j in range(n):
        S[i,0] = S[0,j] = S[m-1,j] = S[i,n-1] = Tb
        if (i > w-1 and j >w-1) and (i < m-1 and j <n-1):
            In[i,j] = Ti

# 
def heating_up(S, In, Cons, Time):
    m = S.dimensions()[0]
    n = S.dimensions()[1]
    S1 = S2 = S + In
    for t in Time[:-1]:
        for i in range(m):
            for j in range(n):
                S2[i,j] = u_next(S1, i,j,Cons[i,j])
                S1 = copy(S2)
                S2 = bindM(S1, Tb)
    return S1            

