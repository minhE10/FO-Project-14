#PYTHON 
from ortools.linear_solver import pywraplp

T, N, M = map(int, input().split())
classes = []
teachers = []

for i in range(N):
    a = list(map(int, input().split()))
    a.pop()  
    classes.append([x - 1 for x in a])  

for i in range(T):
    a = list(map(int, input().split()))
    a.pop()
    teachers.append([x - 1 for x in a]) 

time = list(map(int, input().split()))

class_subjects = [(i, j) for i in range(N) for j in classes[i]]
solver = pywraplp.Solver.CreateSolver('SCIP')
x = {}

for u in range(len(class_subjects)):
    i, j = class_subjects[u]
    d = time[j]
    for s in range(60 - d + 1):
        for t in range(T):
            if j in teachers[t]:
                x[u, s, t] = solver.IntVar(0, 1, f'x[{u},{s},{t}]')

for u in range(len(class_subjects)):
    solver.Add(solver.Sum(
        x[u, s, t] for s in range(60) for t in range(T)
        if (u, s, t) in x) <= 1)

for t in range(T):
    for p in range(60):
        sum1 = []
        for u in range(len(class_subjects)):
            i, j = class_subjects[u]
            d = time[j]
            for s in range(max(0, p - d + 1), min(60 - d + 1, p + 1)):
                if (u, s, t) in x and s <= p < s + d:
                    sum1.append(x[u, s, t])
        solver.Add(solver.Sum(sum1) <= 1)

for i in range(N):
    for p in range(60):
        sum2 = []
        for u in range(len(class_subjects)):
            l, j = class_subjects[u]
            if l == i:
                d = time[j]
                for s in range(max(0, p - d + 1), min(60 - d + 1, p + 1)):
                    for t in range(T):
                        if (u, s, t) in x and s <= p < s + d:
                            sum2.append(x[u, s, t])
        solver.Add(solver.Sum(sum2) <= 1)


solver.Maximize(solver.Sum(x[u, s, t] for (u, s, t) in x))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    result = []
    for (u, s, t) in x:
        if x[u, s, t].solution_value() > 0:
            i, j = class_subjects[u]
            result.append((i + 1, j + 1, s + 1, t + 1))

    print(len(result))
    for r in result:
        for thing in r:
            print(thing, end=' ')
else:
    print(0)
