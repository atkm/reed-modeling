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
def eval_fit(population):
    return [fit_func(p) for p in population]

def fit_func():
    pass
