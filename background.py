
from application import Application
from application import Task
from application import Cs
import logging



logger = logging.getLogger(__name__)
#u=0



#def build_table(app : Application):
def build_table(app):
    w, h = len(app.ceilings), len(app.tasks)
    table = [[None for x in range(w)] for y in range(h)] 
    for t in app.tasks:
        for c in t.longest:
            table[t.t_id][c.resource] = c 
    return table
        

#def buttazzo(app : Application):
def buttazzo(app):
    #print(app.hr_repr())
    table=build_table(app)
    ret = {}
    #for row in table:
    #    print(row)
    for n in range(len(app.tasks)-1) : # the blocking time of last task is always 0
        Bn,Bn_cs = buttazzo_t(app,table,n)
        ret[n]=(Bn,Bn_cs)
        #print("Task "+str(n)+": Bn = "+str(Bn)+" Bn_cs = "+str(Bn_cs))
    return ret

#def buttazzo_t(app : Application, table: list, t : int):
def buttazzo_t(app, table, t ):
    # create the table
    valid_res = [r for r in range(len(app.ceilings)) if app.ceilings[r]is not None and app.ceilings[r] <= t ]
    
    #iterate over the tasks that can block t
    Bl=0
    Bl_cs=[]  #  list of selected critical sections (the longest for each task)
    for ti in range(t+1,len(app.tasks)) :
        maxCs = Cs(0,0,ti,0)
        for r in valid_res :
            if table[ti][r] is not None and table[ti][r].duration > maxCs.duration :
                maxCs=table[ti][r]
        if maxCs.duration != 0:
            Bl += maxCs.duration
            Bl_cs.append(maxCs)
    #s="Bl="+str(Bl)+"  Bl_cs=["
    #for cs in Bl_cs:
    #    s+="T"+str(cs.t_id)+":"+str(cs)+", "
    #print(s[:-2]+"]")

    Bs=0
    Bs_cs=[]  #  list of selected critical sections (the longest for each resource)
    for r in valid_res :
        maxCs = Cs(0,0,ti,0)
        for ti in range(t+1,len(app.tasks)) :
            if table[ti][r] is not None and table[ti][r].duration > maxCs.duration :
                maxCs=table[ti][r]
        if maxCs.duration != 0:
            Bs += maxCs.duration
            Bs_cs.append(maxCs)
    #s="Bs="+str(Bs)+"  Bs_cs=["
    #for cs in Bs_cs:
    #    s+="T"+str(cs.t_id)+":"+str(cs)+", "
    #print(s[:-2]+"]")

    if (Bl < Bs):
        return Bl,Bl_cs
    else:
        return Bs,Bs_cs
### end of buttazzo



def build_path(path, current_idx, N , valid_res , table, maxB, maxpath):
    #print("*** build_path("+str(path)+","+str(current_idx)+","+str(N)+",valid_res,table,"+str(maxB)+","+str(maxpath)+")")
    if current_idx >= N:
        #global u
        #u = u + 1
        r_maxB, _ = compute_B(path)
        if r_maxB >= maxB:
            #print("Call to *** build_path("+str(path)+","+str(current_idx)+","+str(N)+",valid_res,table,"+str(maxB)+","+str(maxpath)+") returned: "+str(r_maxB)+","+str(path))
            return r_maxB, path #.copy()
        else:
            #print("Call to *** build_path("+str(path)+","+str(current_idx)+","+str(N)+",valid_res,table,"+str(maxB)+","+str(maxpath)+") returned: "+str(maxB)+","+str(maxpath))
            return maxB, maxpath #.copy()
    else:
        a_maxB = maxB
        a_maxpath = maxpath.copy()

        found=False
        while not found and current_idx < N:
            for i in valid_res:
                if table[current_idx][i] is not None:
                    found=True
                    break
            if not found:
                #print("skipping task "+str(current_idx))
                current_idx +=1

        if current_idx < N:
            for i in valid_res:
                if table[current_idx][i] is not None:
                    #print("i="+str(i)+" current_idx="+str(current_idx))
                    path.append(table[current_idx][i])
                    r_maxB, r_maxpath = build_path(path, current_idx+1, N , valid_res , table, a_maxB, a_maxpath)
                    if r_maxB >= a_maxB:
                        a_maxB = r_maxB
                        a_maxpath = r_maxpath.copy()
                    path.remove(table[current_idx][i])
        else:
            r_maxB, r_maxpath = build_path(path, current_idx, N , valid_res , table, a_maxB, a_maxpath)
            if r_maxB >= a_maxB:
                a_maxB = r_maxB
                a_maxpath = r_maxpath.copy()
        #print("Call to * build_path("+str(path)+","+str(current_idx)+","+str(N)+",valid_res,table,"+str(maxB)+","+str(maxpath)+") returned: "+str(a_maxB)+","+str(a_maxpath))
        return a_maxB, a_maxpath #.copy()

def compute_B(path):
    '''returns the B of the path and a list of the cs contributing to that B (repeated and None cs excluded) '''
    res = {}
    B=0
    #print(path)
    for cs in path:
        if cs is not None:
            if cs.resource not in res:
                B += cs.duration
                res[cs.resource]=cs
                #print("Added "+str(cs.duration))
            elif res[cs.resource].duration < cs.duration:
                B -= res[cs.resource].duration
                B += cs.duration
                #print("Removed "+str(res[cs.resource].duration)+" Added "+str(cs.duration))
                res[cs.resource]=cs
    return B, list(res.values())

#def rajkumar_t(app : Application , table: list, t : int):
def rajkumar_t(app , table, t ):
    valid_res = [r for r in range(len(app.ceilings)) if app.ceilings[r]is not None and app.ceilings[r] <= t ]
    maxB, maxpath = build_path([],t+1,len(app.tasks),valid_res,table, 0,[])
    #global u
    #print(u)
    _ , maxQn = compute_B(maxpath)
    #print("maxB="+str(maxB)+", maxpath="+str(maxpath)+ " , maxQn="+str(maxQn))
    return maxB, maxQn


#def rajkumar(app : Application):
def rajkumar(app ):
    table=build_table(app)
    ret = {}
    #for row in table:
    #    print(row)    
    for n in range(len(app.tasks)-1) : # the blocking time of last task is always 0
        Bn,Bn_cs = rajkumar_t(app,table,n)
        ret[n]=(Bn,Bn_cs)
        #print("Task "+str(n)+": Bn = "+str(Bn)+" Bn_cs = "+str(Bn_cs))
    return ret
