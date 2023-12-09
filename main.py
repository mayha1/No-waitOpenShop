import random
import gurobipy as gb
from gurobipy import GRB
import numpy as np
random.seed(1)

def generateMatrix(size):
    matrix = np.array([[random.randint(1, 100) for i in range(size[0])]
              for j in range(size[1])]).transpose(1, 0)
    return matrix

class Model1:
    def __init__(self):
        self.model = gb.Model()

    def solve(self, matrix, nJobs, nMachines):

        self.timeMatrix = matrix

        # Add variables
        self.nMachines = nMachines
        self.nJobs = nJobs
        self.addX()
        self.addY()
        self.addC()
        self.addS()
        self.addMakespan()

        # Add constraints
        self.addNotPreceedItselfConstraint()
        self.addScheduleOnceConstraint()
        self.addSucceedAtMostOneConstraint()
        self.addSucceedDummyConstraint()
        self.addNotAllSucceedPreceedConstraint()
        self.addNoWaitConstraint()
        self.addStartingConstraint()
        self.addMakespanConstraint()

        # Add objective
        # self.model.setObjective(0, GRB.MINIMIZE)
        # self.model.optimize()

        # change objective
        self.model.setObjective(self.makespan, GRB.MINIMIZE)
        self.model.optimize()
        print("timeMatrix", self.timeMatrix)
        print("x", self.x)
        print("y", self.y)
        print("c: ", self.c.X)
        print("s", self.s.X)
        print(self.c.X[3,1], "------", self.s.X[3],"---------", self.timeMatrix[3,1])
        print("makespan: ", self.makespan.X)

        print(f"-----------Model runtime: {self.model.runtime}")

    def addX(self):
        self.x = self.model.addMVar((self.nJobs, self.nMachines, self.nMachines+1), vtype=gb.GRB.BINARY, name="x")
    
    def addY(self):
        self.y = self.model.addMVar((self.nJobs, self.nMachines, self.nJobs+1), vtype=gb.GRB.BINARY, name="y")
    
    def addC(self):
        self.c = self.model.addMVar((self.nJobs, self.nMachines), vtype=gb.GRB.INTEGER, name="c")
    
    def addS(self):
        self.s = self.model.addMVar(self.nJobs, vtype=gb.GRB.INTEGER, name="s")

    def addMakespan(self):
        self.makespan = self.model.addMVar(1, vtype=gb.GRB.INTEGER, name="makespan")
    
    # 3*
    def addNotPreceedItselfConstraint(self):
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                self.model.addConstr(self.x[j, i, i] == 0)
                self.model.addConstr(self.y[j, i, j] == 0)
    # 3
    def addScheduleOnceConstraint(self):
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                self.model.addConstr(self.x[j, i, :].sum() == 1)
                self.model.addConstr(self.y[j, i, :].sum() == 1)
    
    # 4 & 5
    def addSucceedAtMostOneConstraint(self):
        for j in range(self.nJobs):
            for l in range(self.nMachines):
                self.model.addConstr(self.x[j, :, l].sum() <= 1)

        for i in range(self.nMachines):
            for k in range(self.nJobs):
                self.model.addConstr(self.y[:, i, k].sum() <= 1)
    # 6 & 7
    def addSucceedDummyConstraint(self):
        for j in range(self.nJobs):
            self.model.addConstr(self.x[j, :, self.nMachines].sum() == 1)
        for i in range(self.nMachines):
            self.model.addConstr(self.y[:, i, self.nJobs].sum() == 1)

    # 8 & 9
    def addNotAllSucceedPreceedConstraint(self):
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                for k in range(j, self.nJobs):
                    self.model.addConstr(self.y[j, i, k] + self.y[k, i, j] <= 1)
                for l in range(i, self.nMachines):
                    self.model.addConstr(self.x[j, i, l] + self.x[j, l, i] <= 1)
    
    # 10 & 11
    def addNoWaitConstraint(self):
        for i in range(self.nMachines):
            for j in range(self.nJobs):
                self.model.addConstr(
                    self.c[j,i] <= self.s[j] + self.timeMatrix[j, :].sum()
                )
                self.model.addConstr(
                    self.c[j,i] >= self.s[j] + self.timeMatrix[j, i]
                )
    # 12 & 13
    def addStartingConstraint(self):
        M = 100*100
        for i in range(self.nMachines):
            for j in range(self.nJobs):
                for l in range(self.nMachines):
                    self.model.addConstr(self.c[j, i] >= self.c[j, l] + self.timeMatrix[j, i] - (1 - self.x[j, i, l])*M)
                for k in range(self.nJobs):
                    self.model.addConstr(self.c[j, i] >= self.c[k, i] + self.timeMatrix[j, i] - (1 - self.y[j, i, k])*M)

    def addMakespanConstraint(self):
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                self.model.addConstr(self.makespan >= self.c[j, i])
# Add variables
class Model2:
    def __init__(self):
        self.model = gb.Model()

    def solve(self, matrix, nJobs, nMachines):

        self.timeMatrix = matrix

        # Add variables
        self.nMachines = nMachines
        self.nJobs = nJobs
        self.addX()
        self.addY()
        self.addC()
        self.addS()
        self.addMakespan()

        self.addScheduleOnceConstraint()
        self.addOneOrderPerOperationConstraint()
        self.addNoWaitConstraint()
        self.addOrderConstraint()
        self.addMakespan()

        # Add objective
        # self.model.setObjective(0, GRB.MINIMIZE)
        # self.model.optimize()

        # change objective
        self.model.setObjective(self.makespan, GRB.MINIMIZE)
        self.model.optimize()
        print("timeMatrix", self.timeMatrix)
        print("x", self.x)
        print("y", self.y)
        # print("c: ", self.c.X)
        # print("s", self.s.X)
        # print("makespan: ", self.makespan.X)

        print(f"-----------Model runtime: {self.model.runtime}")

    def addX(self):
        self.x = self.model.addMVar((self.nJobs, self.nMachines, self.nJobs), vtype=gb.GRB.BINARY, name="x")

    def addY(self):
        self.y = self.model.addMVar((self.nJobs, self.nMachines, self.nMachines), vtype=gb.GRB.BINARY, name="y")
    
    def addC(self):
        self.c = self.model.addMVar((self.nJobs, self.nMachines), vtype=gb.GRB.INTEGER, name="c")
    
    def addS(self):
        self.s = self.model.addMVar(self.nJobs, vtype=gb.GRB.INTEGER, name="s")

    def addMakespan(self):
        self.makespan = self.model.addMVar(1, vtype=gb.GRB.INTEGER, name="makespan")

    # 17
    def addScheduleOnceConstraint(self):
        for j in range (self.nJobs):
            for i in range (self.nMachines):
                self.model.addConstr(
                    self.x[j, i, :].sum() == 1
                )
                self.model.addConstr(
                    self.y[j, i, :].sum() == 1
                )
    
    # 18 & 19 
    def addOneOrderPerOperationConstraint(self):
        for j in range(self.nJobs):
            for k in range(self.nJobs):
                self.model.addConstr(
                    self.x[j, :, k].sum() == 1
                )
        for i in range(self.nMachines):
            for l in range(self.nMachines):
                self.model.addConstr(
                    self.y[:, i, l].sum() == 1
                )

    # 20 & 21
    def addNoWaitConstraint(self):
        for i in range(self.nMachines):
            for j in range(self.nJobs):
                self.model.addConstr(
                    self.c[j,i] <= self.s[j] + self.timeMatrix[j, :].sum()
                )
                self.model.addConstr(
                    self.c[j,i] >= self.s[j] + self.timeMatrix[j, i]
                )

    # 22 & 23
    def addOrderConstraint(self):
        M = 100*100
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                for r in range(self.nMachines):
                    for k in range(1, self.nJobs):
                        self.model.addConstr(
                            self.c[j, i] >= self.c[j, r] + self.timeMatrix[j, i] - (1 - self.x[j, i, k]) * M
                            - (1 - self.x[[j], :, :][:, [r], :][:, :, [t for t in range(k-1)]] )
                        )
                for e in range(self.nJobs):
                    for l in range(1, self.nMachines):
                        self.model.addConstr(
                            self.c[j, i] >= self.c[e, i] + self.timeMatrix[j, i] - (1 - self.y[j, i, l]) * M
                            - (1 - self.y[[e], :, :][:, [i], :][:, :, [t for t in range(l-1)]] )
                        )
    
    def addMakespanConstraint(self):
        for j in range(self.nJobs):
            for i in range(self.nMachines):
                self.model.addConstr(self.makespan >= self.c[j, i])

            



#generate Data
sizes = [[3, 3], [3, 4], [4, 3], [4, 4], [4, 5], [5, 4], [5, 5], [5, 6], [6, 5], [6, 6]]
nInstances = 2
# for size in sizes:
size = [4,3]
for i in range(nInstances):
    matrix = generateMatrix(size)
    # model 1
    # model1 = Model1()
    # model1.solve(matrix, size[0], size[1])
    # breakpoint()
    # model 2
    model2 = Model2()
    model2.solve(matrix, size[0], size[1])
