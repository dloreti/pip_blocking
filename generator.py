from application import Application,Task,Cs
import random



def generate(Nmin=5,Nmax=100,Nstep=5,**kwargs ):
    '''Generate a set of applications with increasing number of tasks.
        Nmin, Nmax, Nstep : define the number of tasks in each application. Only one app with a certain number of tasks will be generated
        M : number of resources for each application (M={K_max/2,K_max,K_max*2} to simulate different degrees of resource contention)
        K_min, K_max : define the number of critical sections in each task. Randomly chosen in [K_min, K_max]
        D_min, D_max : define the duration of each critical section. Randomly chosen in [D_min, D_max]
        Returns the list of the generated applications
    '''
    M = kwargs['M'] or 10
    K_min = kwargs['Kmin'] or 5
    K_max = kwargs['Kmax'] or 10
    D_min = kwargs['Dmin'] or 25
    D_max = kwargs['Dmax'] or 100
    
    n_app = 0 # id of the app
    apps = [] # list of all the apps

    for n_t in range(Nmin,Nmax+1,Nstep):            # n_t number of tasks to be generated for this app
        R = [ r for r in range(M) ]                 #resource list
        tasks=[]
        for t_id in range(n_t):                     # for each tasks
            K = random.randint(K_min,K_max)         # number of Cs in this task
            cs = [] 
            i = 0      
            for _ in range(K):
                cs.append(Cs(random.choice(R),random.randint(D_min,D_max),t_id,i))
                i += 1

            #generate task's critical sections
            tasks.append(Task(t_id,cs))

        app = Application(str(n_app),tasks)
        #print(app)
        apps.append(app)
        n_app += 1
    return apps

def save(apps,filename):
    with open(filename,'w',newline='') as appf:
        for a in apps:
            appf.write(a.__repr__()+'\n')


def load(filename):
    apps = []
    with open(filename,'r',newline='') as appf:
        for line in appf.readlines():
            apps.append(Application.load(line[:-1]))  # discard the final \n 
    return apps


def gen_apps():
    Nmin=5
    Nmax=100
    Nstep=5
    configurations = dict(  a=dict(Nmin=Nmin,Nmax=Nmax,Nstep=Nstep, Kmin=5,Kmax=10,M=20,Dmin=1,Dmax=25), #p_acc=0.32
                            b=dict(Nmin=Nmin,Nmax=Nmax,Nstep=Nstep, Kmin=5,Kmax=10,M=10,Dmin=25,Dmax=50), #p_acc=0.54
                            c=dict(Nmin=Nmin,Nmax=Nmax,Nstep=Nstep, Kmin=5,Kmax=20,M=10,Dmin=25,Dmax=50), #p_acc=0.70 
                            d=dict(Nmin=Nmin,Nmax=Nmax,Nstep=Nstep, Kmin=20,Kmax=30,M=5,Dmin=50,Dmax=100)  #p_acc=0.99
                            )
    apps_a = generate( **configurations['a'])
    apps_b = generate( **configurations['b'])
    apps_c = generate( **configurations['c'])
    apps_d = generate( **configurations['d'])

    save(apps_a,'apps/apps_a')
    save(apps_b,'apps/apps_b')
    save(apps_c,'apps/apps_c')
    save(apps_d,'apps/apps_d')
    return apps_a,apps_b,apps_c,apps_d

def load_apps():
    apps_a = load('apps/apps_a')
    apps_b = load('apps/apps_b')
    apps_c = load('apps/apps_c')
    apps_d = load('apps/apps_d')
    return apps_a,apps_b,apps_c,apps_d
