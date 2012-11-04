import sys
import scipy as sp

"""
Actual simulation. i.e. no fractional cars.
"""
    
class Circle:
    def __init__(self, lanes, entrances, radius, avg_speed):
        self.lanes     = lanes
        self.ents      = entrances
        self.radius    = radius
        self.avg_speed = avg_speed
        #self.buff_size = buff_size

class Car:
    def __init__(self, size, speed, goal):
        self.size  = size
        self.speed = speed
        self.goal  = goal

if __name__ == "__main__":
    circ = Circle(2, 4, 10, 1)
    car1 = Car(1,1,3)
    sys.exit(print("Success."))
