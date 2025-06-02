# input processing
slots = 60
T, N, M = map(int, input().split()) #teacher, class, subj
subj = [0]
teacher = [0]
for _ in range(N):
    a = list(map(int, input().split())) #list of subj that class i learn
    a.pop()
    subj.append(a)
for _ in range(T):
    b = list(map(int, input().split())) #list of subj teacher t can teach
    b.pop()
    teacher.append(b)
period = (list(map(int, input().split()))) #num of period of subj m
period.insert(0, 0)
lopmon = [] #pairs of lớp-môn
for i in range(1, N + 1):
    for j in subj[i]:
        lopmon.append((i, j))
num = len(lopmon)

#import model
from ortools.sat.python import cp_model
model = cp_model.CpModel()

#decision variables
done = [model.NewIntVar(0, 1, f'done{i}') for i in range(num)] #lớp-môn[i] assigned or not
start = [] #lớp-môn[i] starts when
for i in range(num):
    classid, subjectid = lopmon[i]
    duration = period[subjectid]
    #check the latest possible start time
    latest_possible_start = slots - duration
    if latest_possible_start < 0:
        model.Add(done[i] == 0)
        start.append(model.NewIntVar(0, 0, f'starting{i}'))
    else:
        start.append(model.NewIntVar(0, latest_possible_start, f'start{i}')) #variable to store lopmon's start time
teachindex = [model.NewIntVar(1, T, f'teachindex{i}') for i in range(num)]
class_intervals = []
#create variable to check for overlap with same class
for i in range(num):
    classid, subjectid = lopmon[i]
    dur = period[subjectid]
    class_intervals.append(
        model.NewOptionalIntervalVar(start[i], dur, start[i] + dur, done[i], f'class_interval{i}')
    )

#constraints
#constraint 1: if teacher can teach the subj
for i in range(num):
    classid, subjectid = lopmon[i]
    allowed_teachers = [tx for tx in range(1,T+1) if subjectid in teacher[tx]]
    if not allowed_teachers:
        model.Add(done[i] == 0)
    else: #assigned teacher must be allowed teacher
        model.AddAllowedAssignments([teachindex[i]], [[tteach] for tteach in allowed_teachers]).OnlyEnforceIf(done[i])

#constraint 2: no overlap for same class
for i in range(num):
    for j in range(i+1, num):
        c1, _ = lopmon[i]
        c2, _ = lopmon[j]
        if c1 == c2: #intervals for the same class must not overlap
            model.AddNoOverlap([class_intervals[i], class_intervals[j]])

#constraint 3: no teacher overlap
for tx in range(1, T + 1):
    teacher_specific_intervals = []
    for i in range(num):
        #an interval is on a teacher's timeline if lopmon is assigned and is assigned to this teacher
        #assigned2teacher will be true if lopmon[i] is assigned to teacher tx, else false
        assigned2teacher = model.NewBoolVar(f'assigned{i}to_t{tx}')
        model.Add(teachindex[i] == tx).OnlyEnforceIf(assigned2teacher)
        model.Add(teachindex[i] != tx).OnlyEnforceIf(assigned2teacher.Not())

        # active4teacher will be true if lopmon[i] is done and is assigned to teacher
        active4teacher = model.NewBoolVar(f'active4_t{tx}_{i}')
        model.AddBoolAnd([done[i], assigned2teacher]).OnlyEnforceIf(active4teacher)
        model.AddBoolOr([done[i].Not(), assigned2teacher.Not()]).OnlyEnforceIf(active4teacher.Not())

        #create optional interval
        task_class_id, task_subject_id = lopmon[i]
        dur = period[task_subject_id]
        teacher_specific_intervals.append(
            model.NewOptionalIntervalVar(start[i], dur, start[i] + dur, active4teacher, f'teacher_interval_{tx}_{i}')
        )
    # all intervals in 1 teacher's timeline cannot overlap
    model.AddNoOverlap(teacher_specific_intervals)

#objective
model.Maximize(sum(done))

#solve
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    print(int(solver.ObjectiveValue()))
    for k in range(num):
        if solver.Value(done[k]):
            c, s = lopmon[k]
            t = solver.Value(teachindex[k])
            st = solver.Value(start[k])
            print(c, s, st + 1, t)
else:
    print("No feasible solution")