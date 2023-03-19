from gurobipy import *


m = Model("Sudoku")
m.setParam('MIPGap', 0)

# Sets
N = set()
R = set()
C = set()

for i in range(1, 10):
    N.add(i)
    R.add(i)
    C.add(i)
    pass

# NONETS
NONETS = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
R_nonets = list()
C_nonets = list()
for nonet in NONETS:
    R_nonets.append(nonet)
    C_nonets.append(nonet)
    pass

# Pre-set values
V = set()
V.add((1, 1, 1))
V.add((1, 7, 3))
V.add((1, 8, 2))
V.add((2, 5, 2))
V.add((2, 7, 8))
V.add((3, 2, 7))
V.add((3, 4, 1))
V.add((4, 1, 3))
V.add((4, 4, 7))
V.add((4, 7, 5))
V.add((4, 9, 9))
V.add((5, 5, 6))
V.add((6, 1, 7))
V.add((6, 3, 5))
V.add((6, 6, 8))
V.add((6, 9, 6))
V.add((7, 6, 9))
V.add((7, 8, 1))
V.add((8, 3, 4))
V.add((8, 5, 8))
V.add((9, 2, 2))
V.add((9, 3, 7))
V.add((9, 9, 3))


# Variables

# X and Y
X = dict()
Y = dict()
for r in R:
    X[r] = dict()
    Y[r] = dict()
    for c in C:
        X[r][c] = m.addVar(lb=0, name='{}_r{}_c{}'.format('x', r, c))
        Y[r][c] = dict()
        for n in N:
            Y[r][c][n] = m.addVar(lb=0, vtype=GRB.BINARY, name='{}_r{}_c{}_n{}'.format('y', r, c, n))


# Constraints

# Only pick one value per 'cell'
for r in R:
    for c in C:
        m.addConstr(quicksum(Y[r][c][n] for n in N) == 1)

# Only pick a number once per row
for r in R:
    for n in N:
        m.addConstr(quicksum(Y[r][c][n] for c in C) == 1)

# Only pick a number once per column
for c in C:
    for n in N:
        m.addConstr(quicksum(Y[r][c][n] for r in R) == 1)

# Each number must appear once per NONET
for n in N:
    for r_nonet in R_nonets:
        for c_nonet in C_nonets:
            m.addConstr(quicksum(Y[r][c][n] for r in r_nonet for c in c_nonet) == 1)

# Sum of rows = 45
for r in R:
    m.addConstr(quicksum(n * Y[r][c][n] for c in C for n in N) == 45)

# Sum of columns = 45
for c in C:
    m.addConstr(quicksum(n * Y[r][c][n] for r in R for n in N) == 45)

# Sum of nonet = 45
for r_nonet in R_nonets:
    for c_nonet in C_nonets:
        m.addConstr(quicksum(n * Y[r][c][n] for r in r_nonet for c in c_nonet for n in N) == 45)


# X tie to Y
for r in R:
    for c in C:
        m.addConstr(quicksum(n * Y[r][c][n] for n in N) == X[r][c])


# Pre-filled value constraints
for v in V:
    m.addConstr(Y[v[0]][v[1]][v[2]] == 1)

m.optimize()

txt = '-----------------------\n'
for r in R:
    for c in C:
        txt += str(int(X[r][c].x)) + ' '
        if c % 3 == 0:
            txt += '| '
    txt = txt[:-1]
    if r % 3 == 0:
        txt += '\n-----------------------'
    txt += '\n'

print(txt)