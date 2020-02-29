class Application:
    
    def __init__(self,app_id,tasks):
        self.app_id=app_id
        self.tasks=tasks
        self.ceilings = self.compute_ceilings()

    
    @classmethod
    def load(cls,s):
        v=s.split('.')
        ts=[]
        for t in v[1].split(';'):
            ts.append(Task.load(t))
        return cls(int(v[0][1:]),ts)

    def __repr__(self):
        ts=''
        for t in self.tasks:
            ts += t.__repr__()+';'
        return "A{}.{}".format(self.app_id,ts[:-1])
    
    def hr_repr(self):
        ts=''
        for t in self.tasks:
            ts += t.__repr__()+'\n'
        return "A{}\n{}".format(self.app_id,ts[:-1])
    
    def compute_ceilings(self):
        ''' Computes the ceiling for each used resource'''
        ceiling={}  # { resource : ceiling , ... : ...}
        for t in self.tasks:
            for c in t.cs:
                if c.resource not in ceiling:
                    # since you iterate over the tasks by decreasing priority, 
                    # the first time you see a resource is in the highest priority task using it. So you get the ceiling
                    ceiling[c.resource]=t.t_id
        used_resources=sorted(ceiling)
        #print("used_resources"+str(used_resources))
        #fill the gaps in the ceiling dictionary
        for x in range(used_resources[-1]):
            if x not in ceiling:
                ceiling[x] = None # or len(tasks) ?
        return ceiling


class Task:
    def __init__(self,t_id,cs):
        self.t_id = t_id
        self.cs = cs
        self.longest = self.compute_longest()
    
    @classmethod
    def load(cls,s):
        v=s.split(':')
        crit=[]
        i=0
        for c in v[1].split(','):
            crit.append(Cs.load(c,int(v[0][1:]),i))
            i += 1
        return cls(int(v[0][1:]),crit)


    def __repr__(self):
        csc=''
        for c in self.cs:
            csc += c.__repr__()+','
        return "T{}:{}".format(self.t_id,csc[:-1])
    
    def compute_longest(self):
        longest=[] #list of longest cs
        for c in self.cs:
            found=False
            for l in longest:
                if l.resource == c.resource:
                    found = True
                    if l.duration < c.duration :
                        longest.remove(l)
                        longest.append(c)
            if not found :
                longest.append(c)
        #print("t="+str(self.t_id)+" longest="+str(longest))
        return longest

    def response_time(self):
        sum=0
        for c in self.cs:
            sum+=c.duration
        return sum

    def startingtime(self,crit):
        cs_sofar = []
        if crit.t_id != self.t_id:
            return None,None
        time=0
        for c in self.cs:
            if crit.resource == c.resource and crit.duration == c.duration and crit.idx == c.idx:
                return time, cs_sofar
            time += c.duration
            cs_sofar.append(c)
        return None,None  # if the critical section is not found in the task return None
        

class Cs:
    def __init__(self,resource,duration,t_id,idx):
        self.t_id=t_id
        self.resource=resource
        self.duration=duration
        self.idx=idx
    
    @classmethod
    def load(cls,s,t_id,idx):
        v=s.split('-')
        return cls(int(v[0][1:]),int(v[1]),t_id,idx)

    def __repr__(self):
        return "R{}-{}".format(self.resource,self.duration)


'''
critical_section = Cs(3,4)
print(critical_section)

task0 = Task(0,[Cs(3,4),Cs(4,1),Cs(1,3),Cs(3,4)])
print(task0)
task1 = Task(1,[Cs(1,4),Cs(2,4),Cs(3,4),Cs(4,1),Cs(1,3),Cs(3,4)])

app = Application("A0",[task0,task1])
print(app)
'''
