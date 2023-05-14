from gurobipy import *
m = Model("Sudoku")
m.setParam('MIPGap', 0)
########################################################################################################################
# Sets
P = set()

for p in ['Person 1','Person 2','Person 3', 'Person 4']:
    P.add(p)
########################################################################################################################
# Data
n = len(P)  # Number of people
b = dict()  # Required balances
b['Person 1'] = 11.25
b['Person 2'] = -36.75
b['Person 3'] = 62.25
b['Person 4'] = -36.75

maxval = max(b.values())
maxval *= 2
########################################################################################################################
# Variables

# T[p1][p2] and DT[p1][p2]
T = dict()  # Transfer amounts (from p1 to p2)
DT = dict()  # Decision Variables for Transferring something or not (from p1 to p2)
for p1 in P:
    T[p1] = dict()
    DT[p1] = dict()
    for p2 in P:
        T[p1][p2] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name='{}_{}_t'.format(p1, p2))
        DT[p1][p2] = m.addVar(vtype=GRB.BINARY, name='{}_{}_dt'.format(p1, p2))
        pass
    pass
########################################################################################################################
# Constraints

# C1 - Can't transfer to yourself
for p in P:
    m.addConstr(T[p][p] == 0)
    m.addConstr(DT[p][p] == 0)
    pass

# C2 - Lock T to DT (Upperbound only)
# Lower bound lock is not required since the objective function is minimizing Sum of DTs
# Big M Constraint
for p1 in P:
    for p2 in P:
        # If T > 0 --> DT = 1
        m.addConstr(T[p1][p2] <= maxval * DT[p1][p2])
        pass

# C3 - ALL balances must align
for p1 in P:
    m.addConstr(quicksum(T[p2][p1] - T[p1][p2] for p2 in P) == b[p1])
    pass
########################################################################################################################
# Objective Function
m.setObjective(quicksum(DT[p1][p2] for p1 in P for p2 in P), GRB.MINIMIZE)
########################################################################################################################
# Solve!
m.optimize()
########################################################################################################################
# Print result
for p1 in P:
    for p2 in P:
        # print(T[p1][p2])
        x = T[p1][p2].X
        if x > 0:
            print('{} owes {} ${}'.format(p1, p2, x))