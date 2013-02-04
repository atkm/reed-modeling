from ga_shapes import *


# initial population:
# 1/3 squares; 1/3 circles; 1/6 mutation of squares; 1/6 mutation of circles
# circle not implemented yet: do 1/2 squares; 1/2 mutation of squares
def init_poplulation(A, n, N):
    shapesphere = []
    for i in range(int(N/2)):
        shapesphere.append(Shape('square', A, n))
    for i in range(N - int(N/2)):
        shapesphere.append(Shape('square', A, n).mutate())

    return shapesphere


# eval_fit: evalutate fitness of each individual
# vectorized version of fit_func
# w is the weight on the importance of 
def eval_fit(population, w):
    return [fit_func(p) for p in population]

def fit_func():
    pass


# eff_area: Compute the effective area.
def eff_area(shape):
    # compute the center of mass
    xctr = 0
    yctr = 0
    for p in shape.pts:
        xctr += p[0]
        yctr += p[1]
    # the center of mass
    ctr = (xctr/shape.resolution, xctr/shape.resolution)
    # the four vertices. initially just the center
    v1 = v2 = v3 = v4 = ctr
    # the distance of the four vertices from the center
    dv1 = dv2 = dv3 = dv4 = 0
    # the four quadrants
    for p in shape.pts:
        d = sp.linalg.norm((p[0] - ctr[0], p[1] - ctr[1])) # the distance of p from the center
        if p[1] >= ctr[1]:
            # 1st quad
            if p[0] >= ctr[0]:
                # if the point is farther than the current one, replace the old one
                if d > dv1:
                    v1 = p.copy(); dv1 = d
            # 2nd quad
            else:
                if d > dv2:
                    v2 = p.copy(); dv2 = d
        else:
            # 3rd quad
            if p[0] <= ctr[0]:
                # if the point is farther than the current one, replace the old one
                if d > dv3:
                    v3 = p.copy(); dv3 = d
            # 4th quad
            else:
                if d > dv4:
                    v4 = p.copy(); dv4 = d

    vs = (v1,v2,v3,v4)
    # then compute the area
    diag1 = sp.linalg.norm((v1,v3))
    diag2 = sp.linalg.norm((v2,v4))
    edge1 = sp.linalg.norm((v1,v2))
    edge2 = sp.linalg.norm((v2,v3))
    edge3 = sp.linalg.norm((v3,v4))
    edge4 = sp.linalg.norm((v4,v1))
    return bretschneider(diag1, diag2, edge1, edge2, edge3, edge4) 

def bretschneider(p,q,a,b,c,d):  
    return sp.sqrt(4 * p**2 * q**2 - (b**2 + d**2 - a**2 - c**2)**2) / 4

# demo version of eff are algorithm
def eff_area_demo(shape):
    # compute the center of mass
    xctr = 0
    yctr = 0
    for p in shape.pts:
        xctr += p[0]
        yctr += p[1]
    # the center of mass
    ctr = (xctr/shape.resolution, xctr/shape.resolution)
    # the four vertices. initially just the center
    v1 = v2 = v3 = v4 = ctr
    # the distance of the four vertices from the center
    dv1 = dv2 = dv3 = dv4 = 0
    # the four quadrants
    for p in shape.pts:
        d = sp.linalg.norm((p[0] - ctr[0], p[1] - ctr[1])) # the distance of p from the center
        if p[1] >= ctr[1]:
            # 1st quad
            if p[0] >= ctr[0]:
                # if the point is farther than the current one, replace the old one
                if d > dv1:
                    v1 = p.copy(); dv1 = d
            # 2nd quad
            else:
                if d > dv2:
                    v2 = p.copy(); dv2 = d
        else:
            # 3rd quad
            if p[0] <= ctr[0]:
                # if the point is farther than the current one, replace the old one
                if d > dv3:
                    v3 = p.copy(); dv3 = d
            # 4th quad
            else:
                if d > dv4:
                    v4 = p.copy(); dv4 = d

    vs = (v1,v2,v3,v4)
    trans_vs = sp.transpose(vs)
    plt.plot(trans_vs[0], trans_vs[1], 'o')
    plt.plot(trans_vs[0], trans_vs[1], color='green')
    plt.plot((trans_vs[0][3], trans_vs[0][0]), (trans_vs[1][3], trans_vs[1][0]), color='green')
    # then compute the area
    diag1 = sp.linalg.norm((v1,v3))
    diag2 = sp.linalg.norm((v2,v4))
    edge1 = sp.linalg.norm((v1,v2))
    edge2 = sp.linalg.norm((v2,v3))
    edge3 = sp.linalg.norm((v3,v4))
    edge4 = sp.linalg.norm((v4,v1))
    print("The effective area is")
    print(bretschneider(diag1, diag2, edge1, edge2, edge3, edge4))
