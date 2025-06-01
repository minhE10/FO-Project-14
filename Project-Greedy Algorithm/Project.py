from collections import defaultdict

T, N, M = map(int, input().split())

class_subjects = [[] for _ in range(N + 1)]
for c in range(1, N + 1):
    subjects = list(map(int, input().split()))
    class_subjects[c] = subjects[:-1]

subjects_teachers = [[] for _ in range(M + 1)]
for t in range(1, T + 1):
    subjects = list(map(int, input().split()))
    for s in subjects[:-1]:
        subjects_teachers[s].append(t)

durations = [0] + list(map(int, input().split()))

MAX_SLOT = 60
used_slots_class = defaultdict(set)
used_slots_teacher = defaultdict(set)

class_total_duration = []
for c in range(1, N + 1):
    total_dur = sum(durations[s] for s in class_subjects[c])
    class_total_duration.append((total_dur, c))
class_total_duration.sort()

assignments = []
assigned_classes = set()

for _, c in class_total_duration:
    for s in class_subjects[c]:
        d = durations[s]
        assigned = False
        teachers = sorted(subjects_teachers[s], key=lambda t: len(used_slots_teacher[t]))

        for t in teachers:
            for start in range(1, MAX_SLOT - d + 2):
                time_range = set(range(start, start + d))
                if time_range & used_slots_class[c]: continue
                if time_range & used_slots_teacher[t]: continue

                used_slots_class[c].update(time_range)
                used_slots_teacher[t].update(time_range)
                assignments.append((c, s, start, t))
                assigned = True
                break
            if assigned:
                break
            
print(len(assignments))
for c, s, start, t in assignments:
    print(c, s, start, t)
