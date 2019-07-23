
from matplotlib import pyplot as plt
from generator import gen_apps,load_apps
from background import buttazzo, rajkumar
from loreti_faldella import p1,p2
import time
from scheduler import schedule
import pickle

#apps_a,apps_b,apps_c,apps_d = gen_apps()
apps_a,apps_b,apps_c,apps_d = load_apps()

apps_list = [apps_a,apps_b,apps_c,apps_d]
apps_names = [  'apps_a' ,
                'apps_b',
                'apps_c',
                'apps_d'
            ]
apps_descr = [  'K=[5,10],M=20,d=[1,25] => p_acc=0.32' ,
                'K=[5,10],M=10,d=[25,50] => p_acc=0.54',
                'K=[5,20],M=10,d=[25,50] => p_acc=0.70',
                'K=[20,30],M=5,d=[50,100] => p_acc=0.99'
            ]

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
    b_feas=[]
    b_Bn[iL] = []
    r_times=[]
    r_feas=[]
    r_Bn[iL] = []
    p1_times=[]
    p1_feas=[]
    p1_Bn[iL] = []
    p2_times=[]
    p2_feas=[]
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
        b_feas.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))


        print('********** P1 ****************')
        start=time.time()
        r=p1(a)
        end=time.time()
        p1_times.append(end-start)
        p1_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        p1_feas.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))

        print('********** Rajkumar ****************')
        start=time.time()
        r=rajkumar(a)
        end=time.time()
        r_times.append(end-start)
        r_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        r_feas.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Bn_cs="+str(r[0][1])+" Avg_feas="+str(V))
        
        print('********** P2 ****************')
        start=time.time()
        r=p2(a)
        end=time.time()
        p2_times.append(end-start)
        p2_Bn[iL].append(r[0][0])
        V=avg_feas_sched(a,r)
        p2_feas.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))

    with open('apps/'+apps_names[iL]+"_result", 'wb') as f:
        pickle.dump(N, f)
        pickle.dump(b_times, f)
        pickle.dump(r_times, f)
        pickle.dump(p1_times, f)
        pickle.dump(p2_times, f)
        pickle.dump(b_feas, f)
        pickle.dump(r_feas, f)
        pickle.dump(p1_feas, f)
        pickle.dump(p2_feas, f)
        pickle.dump(b_Bn[iL], f)
        pickle.dump(r_Bn[iL], f)
        pickle.dump(p1_Bn[iL], f)
        pickle.dump(p2_Bn[iL], f)

    iL+=1
