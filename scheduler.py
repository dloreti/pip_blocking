from application import Application, Task
#from background import buttazzo_t,rajkumar_t,build_table
#from loreti_faldella import p1_t,p2_t
import copy


#def schedule(app: Application, n: int, Qn : list, epsilon=0.01):
def schedule(app, n, Qn , epsilon=0.01):
    T = copy.deepcopy(app.tasks)
    S = {} #starting times of each task
    #S_Qn = {} ##starting times of each critical section in Qn
    R = {} # resources acquired so far { resource : task }
    Qn1=copy.deepcopy(Qn)
    time=0.0
    while len(T)!=0 :
        tx = T.pop()
        if tx.t_id > n:
            for cs in Qn1:
                if cs.t_id == tx.t_id:
                    #print('popping cs '+str(cs))
                    S[tx.t_id] = time
                    s, cs_sofar = tx.startingtime(cs)
                    #print("s="+str(s))
                    if s == None: # cs is not a critical section of tx
                        err_string = 'The critical section T'+str(cs.t_id)+":"+str(cs)+" is not an actual critical section of "+str(tx)
                        print('Error : '+err_string)
                        return S, False, err_string
                    for previous_cs in cs_sofar:
                        if previous_cs.resource in R:
                            #time += previous_cs.duration
                            return S, False, 'The resource R'+str(previous_cs.resource)+' held by T'+str(R[previous_cs.resource])+' is requested by T'+str(tx.t_id)+'('+str(previous_cs)+') before T'+str(n)+' is started'
                    time += s + epsilon
                    R[cs.resource]=tx.t_id
                    Qn1.remove(cs)
                    break
        else : # if tx has priority higher or equal to tn
            S[tx.t_id] = time
            time += epsilon
    if len(Qn1) != 0:
        return S, False, 'Not able to start all cs in Qn. Not started are: '+str(Qn1)
    '''
    else :
        #check if the start of tn is between the start and the end of each critical section of Qn
        for cs in Qn:
            start = S[cs.t_id] + app.tasks[cs.t_id].startingtime(cs)[0] + epsilon
            end = start + cs.duration
            if start > S[n] or end < S[n]:
                return Qn, S, False, str(start)+"<"+str(S[n])+"<"+str(end)+" is not True. ==> s(cs) < s(n) < e(cs) not satified for cs T"+str(cs.t_id)+":"+str(cs)
    '''
    return S, True, 'OK'

def hr_blocking_set(Bn,Bn_cs):
    s = "Bn="+str(Bn)+" Bn_cs=["
    for cs in Bn_cs:
        s += "T"+str(cs.t_id)+":"+str(cs)+","
    return s[:-1]+"]"

'''
def test_with_predef_app():
    app = Application.load("A0.T0:R4-34,R0-56,R5-77,R9-32,R6-61,R9-81,R7-32;T1:R2-97,R2-63,R6-51,R7-43,R5-42,R1-40,R5-55,R4-96,R5-60,R9-100;T2:R7-38,R3-87,R9-32,R7-53,R2-80;T3:R6-64,R9-97,R2-76,R2-78,R7-81,R3-37,R6-77,R5-72,R0-82;T4:R2-98,R2-36,R4-96,R8-49,R6-70,R8-39,R1-61,R0-67")
    print(app.hr_repr())
    table=build_table(app)

    print("\n********* Buttazzo ************")
    Bn,Bn_cs=buttazzo_t(app,table,0)
    print(hr_blocking_set(Bn,Bn_cs))
    print(schedule(app,0,Bn_cs))

    print("\n********* Rajkumar ************")
    Bn,Bn_cs=rajkumar_t(app,table,0)
    print(hr_blocking_set(Bn,Bn_cs))
    print(schedule(app,0,Bn_cs))

    print("\n************ P1 ***************")
    Bn,Bn_cs=p1_t(app,table,0)
    print(hr_blocking_set(Bn,Bn_cs))
    print(schedule(app,0,Bn_cs))

    print("\n************ P2 ***************")
    Bn,Bn_cs=p2_t(app,0)
    print(hr_blocking_set(Bn,Bn_cs))
    print(schedule(app,0,Bn_cs))
'''
