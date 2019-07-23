from application import Application,Task,Cs
from background import build_table

import cplex
from cplex.exceptions import CplexError

def p1(app : Application):
    table=build_table(app)
    ret = {}
    #for row in table:
    #    print(row)
    for n in range(len(app.tasks)-1) : # the blocking time of last task is always 0
        Bn,Bn_cs = p1_t(app,table,n)
        ret[n]=(Bn,Bn_cs)
        ##print("Task "+str(n)+": Bn = "+str(Bn)+" Bn_cs = "+str(Bn_cs))
    return ret

def p1_t(app : Application ,table:list, t : int):
    valid_res = [r for r in range(len(app.ceilings)) if app.ceilings[r]is not None and app.ceilings[r] <= t ]
    obj1 = []
    for ti in range(t+1,len(app.tasks)):
        for r in valid_res :
            if table[ti][r] is None: 
                obj1.append(0.0)
            else: 
                obj1.append(float(table[ti][r].duration))
    #print("Objective : " + str(obj1))
    
    R = len(valid_res)
    T = len(app.tasks) - t - 1
    
    nvar = R * T
    ubs = [ 1.0 for i in range(nvar) ]
    ncon = R + T
    rhs1 = [ 1.0 for i in range(ncon)]
    sense = ""
    for i in range(ncon):
        sense += "L"
    
    rows = []
    cols = []
    vals = []
    for i in range(ncon):
        for j in range(nvar):
            rows.append(i)
            cols.append(j)
            if i < T :  #CONSTRAINT C1
                if i * R <= j < i * R + R:
                    vals.append(1.0)
                else:
                    vals.append(0.0)
            else:       #CONSTRAINT C2
                if j % R == i - T : # -T because the first T constraints are for C1
                    vals.append(1.0)
                else:
                    vals.append(0.0)
    #print("Coefficients : ")
    #for j in range(ncon):
    #    print(vals[j*nvar:j*nvar+nvar])

    try:
        prob = cplex.Cplex()
        ####### Do not Log the execution #######
        prob.set_log_stream(None)
        #prob.set_error_stream(None)
        #prob.set_warning_stream(None)
        prob.set_results_stream(None)
        
        prob.objective.set_sense(prob.objective.sense.maximize)
        prob.linear_constraints.add(rhs=rhs1, senses=sense)
        prob.variables.add(obj=obj1, ub=ubs)
        prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
        prob.solve()

        #print("Solution status = ", prob.solution.get_status(), ":", end=' ')
        #print(prob.solution.status[prob.solution.get_status()])
        Bt = prob.solution.get_objective_value()
        x = prob.solution.get_values()
        #print("Solution value = " + str(x))

        i=0
        Bt_cs=[]
        for ti in range(t+1,len(app.tasks)):
            for r in valid_res :
                if x[i] == 1.0:
                   Bt_cs.append(table[ti][r]) 
                i+=1
        return Bt, Bt_cs
    except CplexError as exc:
        print(exc)
        return None, None

def Theta(Phi_l : dict, l : int, m : int):
    The_l = []
    found = False
    for cs in Phi_l:
        if cs.resource == m:
            found = True
        if found:
            if cs.resource != m:
                The_l.append(cs)
    return The_l
    

def p2_t(app : Application , t : int):
    Phi = [] # set of ALL cs that COULD contribute to the blocking of t
    Phi_l = {} # set of cs if task l (l>t) that COULD contribute to the blocking of t
    Phi_m = {} # set of cs involving resource m that COULD contribute to the blocking of t
    
    obj = []
    nvar = 0
    for ti in range(t+1,len(app.tasks)):
        css = app.tasks[ti].cs
        Phi_l[ti] = []
        for cs in css:
            if app.ceilings[cs.resource] is not None and app.ceilings[cs.resource] <= t :
                Phi.append(cs)
                Phi_l[ti].append(cs)
                if cs.resource not in Phi_m:
                    Phi_m[cs.resource] = []
                Phi_m[cs.resource].append(cs)
                obj.append(float(cs.duration))
                nvar += 1
    #print("Objective : "+str(obj))

    ubs = [ 1.0 for i in range(nvar) ]

    R = len(Phi_m)
    T = len(app.tasks) - t - 1
    ncon = T + R #+ T *...
    for l in range(t+1,len(app.tasks)):
        for m in app.tasks[l].longest: #get the list of the resources used by l
            if app.ceilings[m.resource] is not None and app.ceilings[m.resource] <= t :
                ncon+=1
            
    rhs = [ 1.0 for i in range(ncon)]
    sense = ""
    for i in range(ncon):
        sense += "L"

    ctype = ""
    for i in range(nvar):
        ctype += "I"

    #vals = [0.0 for x in range(nvar)]
    #valsM = []
    #for y in range(ncon):
    #    valsM.append(vals.copy)
    valsM = [[0.0 for x in range(nvar)] for y in range(ncon)] 
    
    #vals = [0.0 for i in range(ncon*nvar)]
    #CONSTRAINT C1
    c1i=0
    for ti in range(t+1,len(app.tasks)):
        for cs in Phi_l[ti]:
            valsM[c1i][Phi.index(cs)] = 1.0
        c1i+=1
    
    #CONSTRAINT C2
    c2i=c1i
    for m in Phi_m:
        for cs in Phi_m[m]:
            valsM[c2i][Phi.index(cs)] = 1.0
        c2i+=1
    
    #CONSTRAINT C3
    c3i=c2i
    for l in range(t+1,len(app.tasks)-1):
        for m in app.tasks[l].longest: #just to get the list of the resources used by l
            if app.ceilings[m.resource] is not None and app.ceilings[m.resource] <= t :
                valsM[c3i] = [0.0 for x in range(nvar)]
                The_l = Theta(Phi_l[l],l,m.resource)
                #print("l="+str(l)+" m.resource="+str(m.resource)+" The_l="+str(The_l))
                for cs in The_l:
                    valsM[c3i][Phi.index(cs)]=1.0
                for v in range(l+1,len(app.tasks)):
                    for cs in Phi_l[v]:
                        if cs.resource == m.resource:
                            valsM[c3i][Phi.index(cs)]=1.0
                c3i += 1
                #print(vals)
                #valsM[c3i] = vals.copy() #[vals[i] for i in range(len(vals))]
        
    #print("Coefficients : ")
    #for row in range(len(valsM)):
    #    print(valsM[row])

    vals = [ valsM[i][j] for i in range(len(valsM)) for j in range(len(valsM[0]))]
    rows = []
    cols = []
    for i in range(ncon):
        for j in range(nvar):
            rows.append(i)
            cols.append(j)

    try:
        prob = cplex.Cplex()
        ####### Do not Log the execution #######
        prob.set_log_stream(None)
        #prob.set_error_stream(None)
        #prob.set_warning_stream(None)
        prob.set_results_stream(None)

        prob.objective.set_sense(prob.objective.sense.maximize)
        prob.linear_constraints.add(rhs=rhs, senses=sense)
        prob.variables.add(obj=obj, ub=ubs, types=ctype)
        prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
        prob.solve()

        #print("Solution status = ", prob.solution.get_status(), ":", end=' ')
        #print(prob.solution.status[prob.solution.get_status()])
        Bt = prob.solution.get_objective_value()
        x = prob.solution.get_values()
        #print("Solution value = " + str(x))

        i=0
        Bt_cs=[]
        for cs in Phi:
            if x[i] == 1.0:
                Bt_cs.append(cs) 
            i+=1
        return Bt, Bt_cs

    except CplexError as exc:
        print(exc)
        return None, None

def p2(app : Application ):
    ret = {}
    for n in range(len(app.tasks)-1) : # the blocking time of last task is always 0
        Bn,Bn_cs = p2_t(app,n)
        ret[n]=(Bn,Bn_cs)
        #print("Task "+str(n)+": Bn = "+str(Bn)+" Bn_cs = "+str(Bn_cs))
    return ret