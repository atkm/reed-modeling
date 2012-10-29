import sys
import scipy as sp
import numpy as np

class Traffic:
    """
    a vector representing the state of traffic circle
    """
    def __init__(self, distribution):
        """
        distribution ~ a tuple of the amount of traffics from e1, e2, and e3
        """
        self.size = len(distribution)
        self.wait_line = list(distribution)
        self.state = np.zeros(3 * self.size)   
    
    def enter(self):
        """
        If an entrance is empty, throw in a new car.
        """
        for i in range(self.size):
            if (self.state[3*i] == 0) and (self.wait_line[i-1] > 0):
                self.wait_line[i-1] -= 1
                self.state[3*i] += 1


class Car:
    def __init__(self):
        self.speed = 1
        self.size  = 1

class Circle:
    def __init__(self):
        self.lanes = 1
        # number of nodes = (eingang, ausgang, lane)*3 = 9
        # order: E1, R1, A1, E2, R2, A2, E3, R3, A3
        e1 = np.array([1,1,0,1,0,0,0,0,0])
        r1 = np.array([0,1,1,1,0,0,0,0,0])
        a1 = np.zeros(9)
        e2 = np.array([0,0,0,1,1,0,1,0,0])
        r2 = np.array([0,0,0,0,1,1,1,0,0])
        a2 = np.zeros(9)
        e3 = np.array([1,0,0,0,0,0,1,1,0])
        r3 = np.array([1,0,0,0,0,0,0,1,1])
        a3 = np.zeros(9)
        # name these
        nodes = [e1, r1, a1, e2, r2, a2, e3, r3, a3]
        # create Markov matrix
        self.layout = np.vstack((v for v in nodes))/3

def probablistic():
    simple_circle = Circle()
    simple_traffic = Traffic((1,1,1))
    print("Run Traffic.enter()")
    simple_traffic.enter()
    print("State:")
    print(simple_traffic.state)
    print("Wait line:")
    print(simple_traffic.wait_line)
    print("layout:")
    print(simple_circle.layout)
    
    for i in range(100):
        print("Proceed one time step:")
        simple_traffic.state = np.dot(simple_circle.layout, simple_traffic.state)
        print(simple_traffic.state)
        if converged(simple_traffic.state):
            print("Result: " + repr(i) + " iterations.")
            break

def converged(arr):
    if all(arr < 10**(-5)):
        return True
    else:
        return False


if __name__ == "__main__":
    sys.exit(probablistic())
