from ga_shapes import *

def floodfill(pts):
    n = len(pts) # num of points
    mx = max([p for p in sp.transpose(pts)[0]])
    my = max([p for p in sp.transpose(pts)[1]])
    lim = max(mx,my)
