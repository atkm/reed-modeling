from shape_trans import *

def main():
    A = 0.25
    m = 5
    N = 1
    name = 'shape_' + str(A) + '_' + str(m) + '_' + str(N) + '.png'
    GenShape(vCat, A, m, N, name)

if __name__ == "__main__":
    main()
