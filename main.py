import random
import numpy as np
from models import Model1, Model2, Model3
from plot import plot
import pandas as pd

random.seed(0)

def generateMatrix(size):
    matrix = np.array([[random.randint(1, 100) for i in range(size[0])]
              for j in range(size[1])]).transpose(1, 0)
    return matrix

size = [6, 6]
model = Model3()
matrix = generateMatrix(size)
solution = model.solve(matrix, size[0], size[1])
print(matrix)
print(solution)
plot(
    startTimeMatrix=solution["startTimeMatrix"],
    endTimeMatrix=solution["endTimeMatrix"]
)
breakpoint()



# sizes = [[3, 3], [3, 4], [4, 3], [4, 4], [4, 5], [5, 4], [5, 5], [5, 6], [6, 5], [6, 6]]
# sizes = [[3, 3], [3, 4], [4, 3], [4, 4], [4, 5], [5, 4], [5, 5], [5, 6]]
# nInstances = 2
# resultsListDict = []
# for modelId in range(1, 4):
#     for size in sizes:
#         if modelId in [1,2] and size in [[4, 5], [5, 4], [5, 5], [5, 6], [6, 5], [6, 6]]:
#             continue
#         for i in range(nInstances):
#             matrix = generateMatrix(size)
#             if modelId == 1:
#                 model = Model1()
#             elif modelId == 2:
#                 model = Model2()
#             elif modelId == 3:
#                 model = Model3()
#             solution = model.solve(matrix, size[0], size[1])
#             result = {
#                 "model": modelId,
#                 "size": size,
#                 "instance": i,
#                 "makespan": solution["makespan"][0],
#                 "timeRun": solution["timeRun"]
#             }
#             print(result)
#             resultsListDict.append(result)

# df = pd.DataFrame(resultsListDict)
# df.to_csv("table2.csv", index=False)
