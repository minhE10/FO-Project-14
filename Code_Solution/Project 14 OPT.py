import random
import copy
import math
# doc du lieu
# t la so giao vien, n la so lop, m la so mon
t,n,m=map(int,input().split())
classes=[]
teacher=[]
subject=[]
class_subject_not_added=set()
for _ in range(m+1):
    subject.append([])
#subject[i] la danh sach giao vien co the day mon i 
classes.append([])
teacher.append([])
#classes la mon ma lop do co the hoc
for _ in range(n):
    a=list(map(int,input().split()))
    a.pop()
    classes.append(a)
#teacher la mon ma giao vien do co the day
for _ in range(t):
    a=list(map(int,input().split()))
    a.pop()
    teacher.append(a)
# d[i] la so tiet cua mon thu i
d=list(map(int,input().split()))
d.insert(0,0)
# ham muc tieu: so lop-mon + so giao vien duoc phan kip
class_subject=[] # danh sach cac lop mon, moi lop mon gan voi (giao vien, thoi gian)
# khoi tao ban dau tat ca la (0,0)
index=0
for i in range(1,n+1):
    for x in classes[i]:
        
        class_subject.append((i,x))
        class_subject_not_added.add(index)
        index+=1
        

for i in range(1,t+1):
        for x in teacher[i]:
            subject[x].append(i)

check_teacher=[0]*(t+1)
check_class_subject=[0]*len(class_subject)
cnt_teacher=0
cnt_class_subject=0
intial_sol={}
time_teacher=[[0]*61 for _ in range(t+1)] 
time_class=[[0]*61 for _ in range(n+1)] 

def generate_intial_sol():
    
    # xay dung intial sol
    
    # random thu tu sap xep lop-mon
    perm=list(range(len(class_subject)))
    random.shuffle(perm)
    global cnt_class_subject
    global cnt_teacher
    for i in perm:
        status=False
        #lay ra class-subject[i]
        c=class_subject[i][0] # lop
        s=class_subject[i][1] # mon
        random.shuffle(subject[s])
        for teach in subject[s]: # duyet qua giao vien co the day mon s
            for j in range(1,61-d[s]): # duyet qua khoi thoi gian d[s]
                if sum(time_teacher[teach][j:j+d[s]])==0 and sum(time_class[c][j:j+d[s]])==0:
                    class_subject_not_added.remove(i)
                    for x in range(j,j+d[s]):
                        time_class[c][x]+=1
                        time_teacher[teach][x]+=1
                    if not check_teacher[teach]:
                        cnt_teacher+=1
                    check_teacher[teach]+=1
                    check_class_subject[i]+=1
                    cnt_class_subject+=1
                    intial_sol[i]=(teach, j)
                    status=True
                    break
            if status==True:
                break
    
    return intial_sol

#thiet lap cac toan tu

def destroy(a:dict): #bo di 1 lop-mon da duoc xep
    global cnt_teacher
    global cnt_class_subject
    index=random.choice(list(a.keys()))
    (c,s)=(class_subject[index][0],class_subject[index][1])
    (teach, time_start)=a[index]
    for i in range(time_start,time_start+d[s]):
        time_class[c][i]-=1
        time_teacher[teach][i]-=1
    class_subject_not_added.add(index)
    check_class_subject[index]-=1
    cnt_class_subject-=1
    check_teacher[teach]-=1
    cnt_teacher-=max(0,1-check_teacher[teach])
    a.pop(index)

def add(a:dict, b:set):   #them vao 1 lop mon chua duoc them
    global cnt_class_subject
    global cnt_teacher
    if len(b)==0:
        return
    index=random.choice(list(b))
    (c,s)=class_subject[index]
    random.shuffle(subject[s])
    for teach in subject[s]:
        for time in range(1,61-d[s]):
            if sum(time_class[c][time:time+d[s]])+sum(time_teacher[teach][time:time+d[s]])==0:
                for i in range(time, time+d[s]):
                    time_teacher[teach][i]+=1
                    time_class[c][i]+=1
                check_class_subject[index]+=1
                check_teacher[teach]+=1
                if check_teacher[teach]==1:
                    cnt_teacher+=1
                cnt_class_subject+=1
                class_subject_not_added.remove(index)
                a[index]=(teach,time)
                return

def assign_new_teacher(a:dict): #thay 1 giao vien moi cho 1 lop mon neu giao vien do con trong
    global cnt_class_subject
    global cnt_teacher
    index=random.choice(list(a.keys()))
    (c,s)=class_subject[index]
    current_teacher=a[index][0]
    time=a[index][1]
    random.shuffle(subject[s])
    for teach in subject[s]: 
        if sum(time_teacher[teach][time:time+d[s]])==0 and teach !=current_teacher:
            for i in range(time, time+d[s]):
                time_teacher[teach][i]+=1
                time_teacher[current_teacher][i]-=1
            check_teacher[teach]+=1
            if check_teacher[teach]==1:
                cnt_teacher+=1
            check_teacher[current_teacher]-=1
            if check_teacher[current_teacher]==0:
                cnt_teacher-=1
            a[index]=(teach,time)
            break


def swap_teacher(a:dict): # hoan doi giao vien của 2 lop mon neu thoa man
    global cnt_class_subject
    global cnt_teacher
    
    random_sample=random.sample(list(a.keys()),2)
    index1=random_sample[0]
    index2=random_sample[1]
    (c1,s1)=class_subject[index1]
    (c2,s2)=class_subject[index2]
    (teach1, time1)=a[index1]
    (teach2, time2)=a[index2]
    if teach1 not in subject[s2] or teach2 not in subject[s1]: # kiem tra xem giao vien co the day mon do sau khi doi hay khong
        return
    if time1>=time2:   #kiem tra xem thoi gian giao vien co thoa man khi doi khong
        if time1+d[s1]<=time2+d[s2]:
            if sum(time_teacher[teach1][time2:time1])>0 or sum(time_teacher[teach1][time1+d[s1]:time2+d[s2]])>0:
                return
        else :
            if sum(time_teacher[teach1][time2:time1])>0 or sum(time_teacher[teach2][time2+d[s2]:time1+d[s1]])>0:
                return
    else:
        if time1+d[s1]>=time2+d[s2]:
            if sum(time_teacher[teach2][time1:time2])>0 or sum(time_teacher[teach2][time2+d[s2]:time1+d[s1]])>0:
                return
        else :
            if sum(time_teacher[teach2][time1:time2])>0 or sum(time_teacher[teach1][time1+d[s1]:time2+d[s2]])>0:
                return
    for i in range(time1,time1+d[s1]):
        time_teacher[teach1][i]-=1
        time_teacher[teach2][i]+=1
    for i in range(time2,time2+d[s2]):
        time_teacher[teach2][i]-=1
        time_teacher[teach1][i]+=1
    a[index1]=(teach2,time1) #doi 2 giao vien
    a[index2]=(teach1,time2)


def move_time_slot(a:dict): # chuyen time cua 1 lop mon sang 1 thoi gian khac
    global cnt_class_subject
    global cnt_teacher
    index=random.choice(list(a.keys()))
    (c,s)=class_subject[index]
    (teach,time)=a[index]
    
    available=[]
    for i in range(1,61-d[s]):
        if sum(time_teacher[teach][i:i+d[s]])==0 and sum(time_class[c][i:i+d[s]])==0 and i!=time:
            available.append(i)
    if not available:
        return
    new_time=random.choice(available)
    for i in range(time, time+d[s]):
        time_teacher[teach][i]-=1
        time_class[c][i]-=1
    for i in range(new_time,new_time+d[s]):
        time_teacher[teach][i]+=1
        time_class[c][i]+=1
    a[index]=(teach,new_time)
def swap_time_slot(a:dict): #hoan doi thoi gian cua 2 lop mon
    global cnt_class_subject
    global cnt_teacher
    status=True
    random_sample=random.sample(list(a.keys()),2)
    index1=random_sample[0]
    index2=random_sample[1]
    (c1,s1)=class_subject[index1]
    (c2,s2)=class_subject[index2]
    (teach1, time1)=a[index1]
    (teach2, time2)=a[index2]
    for i in range(time1,time1+d[s1]):
        time_teacher[teach1][i]-=1
        time_class[c1][i]-=1
    for i in range(time2,time2+d[s2]):
        time_teacher[teach2][i]-=1
        time_class[c2][i]-=1
    if sum(time_teacher[teach1][time2:time2+d[s1]])>0 or sum(time_teacher[teach2][time1:time1+d[s2]])>0:
        status=False
    if sum(time_class[c1][time2:time2+d[s1]])>0 or sum(time_class[c2][time1:time1+d[s2]])>0:
        status=False
    if status==False:
        for i in range(time1,time1+d[s1]):
            time_teacher[teach1][i]+=1
            time_class[c1][i]+=1
        for i in range(time2,time2+d[s2]):
            time_teacher[teach2][i]+=1
            time_class[c2][i]+=1
    else:
        for i in range(time1,time1+d[s2]):
            time_teacher[teach2][i]+=1
            time_class[c2][i]+=1
        for i in range(time2,time2+d[s1]):
            time_teacher[teach1][i]+=1
            time_class[c1][i]+=1
        a[index1]=(teach1, time2) # doi 2 khung thoi gian
        a[index2]=(teach2, time1)


def LNS(a:dict): #large neighbourhood search de thoat khoi cuc bo
    num=min(10, cnt_class_subject//2)
    for _ in range(num):
        if len(a)>0:
            destroy(a)

def operate(index):
    if index==1 and len(class_subject_not_added) >0:
        add(sol,class_subject_not_added)
        
    elif index==2 and len(sol)>0:
        destroy(sol)
        
    elif index==3 and len(sol)>0:
        assign_new_teacher(sol)
        
    elif index==4 and len(sol)>=2:
        swap_teacher(sol)
        
    elif index==6 and len(sol)>=2:
        swap_time_slot(sol)
        
    elif index==5 and len(sol)>0:
        move_time_slot(sol)
        




def accept(new_val, current_val, T):  # xet xem co chap nhan loi giai moi ke ca khi no te hon 
    delta = new_val - current_val
    if delta > 0:
        return True
    prob = math.exp(delta / T)
    return random.random() < prob


#thuc hien LS
sol=generate_intial_sol()

res=cnt_teacher+cnt_class_subject
best_res=res
limit=15
no_improve=0
final_solution=copy.deepcopy(sol)

temperature = 100.0  
cooling_rate = 0.95

for _ in range(200):
    cur_solution=copy.deepcopy(sol)
    cur_check_teacher=copy.deepcopy(check_teacher) #luwu lai loi giai hien tai
    cur_check_class_subject=copy.deepcopy(check_class_subject)
    cur_time_teacher=copy.deepcopy(time_teacher)
    cur_time_class=copy.deepcopy(time_class)
    cur_cnt_teacher=cnt_teacher
    cur_cnt_class_subject=cnt_class_subject
    idx=random.randint(1,6)
    operate(idx)
    
    new_val = cnt_class_subject + cnt_teacher
    if accept(new_val, res, temperature):  #neu accept thi di den loi giai moi
        if new_val>best_res:
            final_solution=copy.deepcopy(sol)
            best_res=new_val
        res = new_val
        no_improve = 0
    else: #neu khong thi quay tro lai 
        sol=copy.deepcopy(cur_solution)
        check_teacher=copy.deepcopy(cur_check_teacher)
        check_class_subject=copy.deepcopy(cur_check_class_subject)
        time_teacher=copy.deepcopy(cur_time_teacher)
        time_class=copy.deepcopy(cur_time_class)
        cnt_teacher=cur_cnt_teacher
        cnt_class_subject=cur_cnt_class_subject
        no_improve += 1
    temperature *= cooling_rate

    if no_improve>=limit:
        LNS(sol)


# in ra ket qua
print(len(final_solution))
a=sorted(list(final_solution.keys()))

for x in a:
    c,s=class_subject[x][0],class_subject[x][1]
    print(c,s, end=' ')
    print(final_solution[x][1], final_solution[x][0])
