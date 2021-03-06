
from matplotlib import pyplot as plt
from generator import gen_apps,load_apps
from background import buttazzo, rajkumar
from loreti_faldella import p1,p2
import time
from scheduler import schedule


#apps_a,apps_b,apps_c,apps_d = gen_apps()
apps_a,apps_b,apps_c,apps_d = load_apps()

apps_list = [apps_a,apps_b,apps_c,apps_d]
apps_descr = [  'K=[5,10],M=20,d=[1,25] => p_acc=0.31' ,
                'K=[5,10],M=10,d=[25,50] => p_acc=0.53',
                'K=[5,20],M=10,d=[25,50] => p_acc=0.70',
                'K=[20,30],M=5,d=[50,100] => p_acc=0.99'
            ]

#apps_list = [apps_a]
#apps_descr = [  'K=[5,10],M=20,d=[1,25] => p_acc=0.31' ]

def avg_feas_sched(app,res):
    count_feasibles = 0
    for t in res:
        _,feasible,_ = schedule(app,t,res[t][1])
        if feasible:
            count_feasibles += 1
    return count_feasibles/(len(app.tasks)-1)


bu_style = dict(color='k',ls='dotted',label='But', marker="s", fillstyle='full',markersize=5)
ra_style = dict(color='k',ls='dashed',label='Raj', marker="v", fillstyle='full',markersize=5)
p1_style = dict(color='k',ls='dashdot',label='(1)', marker="o", fillstyle='full',markersize=5)
p2_style = dict(color='k',ls='solid',label='(2)', marker="o", fillstyle='none',markersize=5)


b_Bn={}
r_Bn={}
p1_Bn={}
p2_Bn={}

iL=0
for apps in apps_list:
    N=[]
    b_times=[]
    b_avg_f=[]
    b_Bn[iL] = []
    r_times=[]
    r_avg_f=[]
    r_Bn[iL] = []
    p1_times=[]
    p1_avg_f=[]
    p1_Bn[iL] = []
    p2_times=[]
    p2_avg_f=[]
    p2_Bn[iL] = []
    
    for a in apps:
        
        N.append(len(a.tasks))
        print("appset = "+str(iL)+" N = "+str(len(a.tasks)))
        
        print('********** Buttazzo ****************')
        start=time.time()
        r=buttazzo(a)
        end=time.time()
        b_times.append(end-start)
        b_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        b_avg_f.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))

        print('********** P1 ****************')
        start=time.time()
        r=p1(a)
        end=time.time()
        p1_times.append(end-start)
        p1_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        p1_avg_f.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))

        print('********** Rajkumar ****************')
        start=time.time()
        r=rajkumar(a)
        end=time.time()
        r_times.append(end-start)
        r_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        r_avg_f.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Bn_cs="+str(r[0][1])+" Avg_feas="+str(V))

        print('********** P2 ****************')
        start=time.time()
        r=p2(a)
        end=time.time()
        p2_times.append(end-start)
        p2_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        p2_avg_f.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))

    #plt.subplot(3, 1, 1)
    axes = plt.gca()
    axes.set_ylim([0,180])
    plt.plot(N,b_times, **bu_style)
    plt.plot(N,r_times, **ra_style)
    plt.plot(N,p1_times, **p1_style)
    plt.plot(N,p2_times, **p2_style)
    plt.title('Performance '+apps_descr[iL])
    plt.xlabel('Tasks')
    plt.ylabel('time (s)')
    plt.legend(loc='upper left')
    plt.figure()


    #plt.subplot(3, 1, 3)
    #print("****** N="+str(len(N))+" b_avg_f="+str(len(b_avg_f))+" r_avg_f="+str(len(r_avg_f))+" p1_avg_f="+str(len(p1_avg_f))+" p2_avg_f="+str(len(p2_avg_f)))
    plt.plot(N,b_avg_f, **bu_style)
    plt.plot(N,r_avg_f, **ra_style)
    plt.plot(N,p1_avg_f, **p1_style)
    plt.plot(N,p2_avg_f, **p2_style)
    plt.title('Percentage of feasible blockings '+apps_descr[iL])
    plt.xlabel('Tasks')
    plt.legend(loc='upper right')
    plt.ylabel('Feasible blockings')
    plt.figure()

    iL+=1

avg_b_Bn = []
avg_r_Bn = []
avg_p1_Bn = []
avg_p2_Bn = []
for i in range(len(b_Bn[0])):
    s_b=0
    s_r=0
    s_p1=0
    s_p2=0
    for j in range(len(apps_list)):
        s_b+=b_Bn[j][i] or 0
        s_r+=r_Bn[j][i] or 0
        s_p1+=p1_Bn[j][i] or 0
        s_p2+=p2_Bn[j][i] or 0
    avg_b_Bn.append(s_b/len(apps_list))
    avg_r_Bn.append(s_p1/len(apps_list))
    avg_p1_Bn.append(s_p1/len(apps_list))
    avg_p2_Bn.append(s_p2/len(apps_list))
    

#plt.subplot(3, 1, 2)
plt.plot(N,avg_b_Bn, **bu_style)
plt.plot(N,avg_r_Bn, **ra_style)
plt.plot(N,avg_p1_Bn, **p1_style)
plt.plot(N,avg_p2_Bn, **p2_style)
plt.title('Average value of computed blocking time')
plt.legend(loc='lower right')
plt.xlabel('Tasks')
plt.ylabel('Blocking time')

plt.show()
