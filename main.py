import random
import numpy as np
from models import Model1, Model2, Model3
from plot import plot


random.seed(1)

def generateMatrix(size):
    matrix = np.array([[random.randint(1, 100) for i in range(size[0])]
              for j in range(size[1])]).transpose(1, 0)
    return matrix

#generate Data
sizes = [[3, 3], [3, 4], [4, 3], [4, 4], [4, 5], [5, 4], [5, 5], [5, 6], [6, 5], [6, 6]]
nInstances = 1

# for size in sizes:
size = [4,3]
for i in range(nInstances):
    matrix = generateMatrix(size)
    # model 1
    model = Model1()
    # model 2
    # model = Model2()
    # model 3
    # model = Model3()
    
    solution = model.solve(matrix, size[0], size[1])
    plot(
        startTimeMatrix=solution["startTimeMatrix"],
        endTimeMatrix=solution["endTimeMatrix"]
    )
