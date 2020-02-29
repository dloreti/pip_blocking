
from __future__ import division # to get a float from int/int event in python 2
from matplotlib import pyplot as plt
from generator import gen_apps,load_apps
from background import buttazzo
#from loreti_faldella import p1,p2
import time
from scheduler import schedule
import pickle


#schedcat dependencies

import schedcat.model.tasks as tasks
import schedcat.sched.fp as fp
import schedcat.model.resources as resources
import schedcat.locking.bounds as bounds


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

# return a dictionary of (Bn,Bn_is_feasible) instead of (Bn,Bn_cs)
def yang(app ):
    t_list=[]
    for ti in range(len(app.tasks)) :
        response_time=app.tasks[ti].response_time()
        t_list.append(tasks.SporadicTask(response_time,response_time*1000))
    ts = tasks.TaskSystem(t_list)
    fp.bound_response_times(1, ts)

    resources.initialize_resource_model(ts)
    for ti in range(len(app.tasks)) :
        for cs in app.tasks[ti].cs :
            ts[ti].resmodel[cs.resource].add_request(cs.duration) 
    for t in ts: t.partition = 0
    bounds.assign_fp_preemption_levels(ts)
    
    r_but=buttazzo(a)

    res=bounds.apply_pip_bounds(ts,1)
    ret={}
    for n in range(len(app.tasks)-1) : # the blocking time of last task is always 0
        costH=0
        for h in range(n):
            costH+=ts[h].cost
        y_Bn = res.get_blocking_term(n) - costH #cost of all the processes with higher priority
        
        if y_Bn > r_but[n][0]:
            feasible=False
        else:
            _,feasible,_ = schedule(app,app.tasks[n],r_but[n][1])
        ret[n]=(y_Bn,feasible)
    return ret 

def avg_feas_sched(app,res):
    count_feasibles = 0
    for t in res:
        #_,feasible,_ = schedule(app,t,res[t][1])
        feasible=res[t][1]
        if feasible:
            print('Feasible!')
            count_feasibles += 1
    return count_feasibles/(len(app.tasks)-1) 

b_Bn={}
y_Bn={}
r_Bn={}
p1_Bn={}
p2_Bn={}

iL=0
for apps in apps_list:
    N=[]
    b_times=[]
    b_feas=[]
    b_Bn[iL] = []
    y_times=[]
    y_feas=[]
    y_Bn[iL] = []
    r_times=[]
    r_feas=[]
    r_Bn[iL] = []
    p1_times=[]
    p1_feas=[]
    p1_Bn[iL] = []
    p2_times=[]
    p2_feas=[]
    p2_Bn[iL] = []
    
    with open('apps2/'+apps_names[iL]+"_result", 'rb') as f:
        N_loaded = pickle.load(f)
        print("Nloaded="+str(N))
        b_times = pickle.load( f)
        r_times = pickle.load( f)
        p1_times = pickle.load( f)
        p2_times = pickle.load( f)
        b_feas = pickle.load( f)
        r_feas = pickle.load( f)
        p1_feas = pickle.load( f)
        p2_feas = pickle.load( f)
        b_Bn[iL] = pickle.load( f)
        print("b_Bn[iL]="+str(b_Bn[iL]))
        #r_Bn[iL] = pickle.load( f)
        #p1_Bn[iL] = pickle.load( f)
        #p2_Bn[iL] = pickle.load( f)


    for a in apps:
        N.append(len(a.tasks))
        print("appset = "+str(iL)+" N = "+str(len(a.tasks)))

        print('********** Yang ****************')
        start=time.time()
        r=yang(a)
        end=time.time()
        y_times.append(end-start)
        y_Bn[iL].append(r[0][0]) #blocking time of task 0 according to yang method
        V=avg_feas_sched(a,r)
        y_feas.append(V)
        print("Time="+str(end-start)+" Bn="+str(r[0][0])+" Avg_feas="+str(V))
        
    
    with open('apps2/'+apps_names[iL]+"_result_yan", 'wb') as f:
        #pickle.dump(N, f)
        pickle.dump(y_times, f)
        pickle.dump(y_feas, f)
        pickle.dump(y_Bn[iL], f)    
    iL+=1
