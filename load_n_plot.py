
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

#apps_list = [apps_a]
#apps_descr = [  'K=[5,10],M=20,d=[1,25] => p_acc=0.31' ]


bu_style = dict(color='k',ls='dotted',label='But', marker="s", fillstyle='none',markersize=6)
ya_style = dict(color='k',ls='dotted',label='Yan', marker="+", fillstyle='none',markersize=7)
ra_style = dict(color='k',ls='dashed',label='Raj', marker="x", fillstyle='none',markersize=7)
p1_style = dict(color='k',ls='dashdot',label='(M1)', marker="o", fillstyle='none',markersize=5,linewidth=0.8)
p2_style = dict(color='k',ls='solid',label='(M2)', marker="o", fillstyle='full',markersize=5,linewidth=0.8)

params = {'text.latex.preamble': [r'\usepackage{siunitx}', 
    r'\usepackage{sfmath}', r'\sisetup{detect-family = true}',
    r'\usepackage{amsmath}']}   
plt.rcParams.update(params)   


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
    

    with open('apps/'+apps_names[iL]+"_result", 'rb') as f:
        N = pickle.load(f)
        print("N="+str(N))
        b_times = pickle.load( f)
        print("b_times="+str(b_times))
        r_times = pickle.load( f)
        p1_times = pickle.load( f)
        p2_times = pickle.load( f)
        b_feas = pickle.load( f)
        r_feas = pickle.load( f)
        p1_feas = pickle.load( f)
        p2_feas = pickle.load( f)
        b_Bn[iL] = pickle.load( f)
        print("b_Bn[iL]="+str(b_Bn[iL]))
        r_Bn[iL] = pickle.load( f)
        p1_Bn[iL] = pickle.load( f)
        p2_Bn[iL] = pickle.load( f)

    with open('apps2/'+apps_names[iL]+"_result_yan", 'rb') as f: #store with protocol=2 because schedcat is in pyhton 2
        y_times=pickle.load(f)
        y_feas=pickle.load(f)
        y_Bn[iL]=pickle.load(f)    

    #plt.subplot(3, 1, 1)
    axes = plt.gca()
    axes.set_ylim([0,180])
    plt.plot(N,b_times, **bu_style)
    plt.plot(N,r_times, **ra_style)
    plt.plot(N,p1_times, **p1_style)
    plt.plot(N,p2_times, **p2_style)
    #plt.title('Performance '+apps_descr[iL])
    
    plt.tick_params(axis='both',labelsize='xx-large')
    plt.xlabel('Tasks', fontsize='xx-large')
    plt.ylabel('Time ($\mu$s)', fontsize='xx-large')
    #plt.legend(loc='upper right', fontsize='large')
    plt.legend(loc='upper right', bbox_to_anchor=( 0.9, 1), fontsize='xx-large')
    plt.tight_layout(pad=0.1)
    plt.savefig('/Users/daniela/Desktop/time_'+apps_names[iL][-1:]+'.png', dpi=300)
    plt.figure()


    #plt.subplot(3, 1, 3)
    #print("****** N="+str(len(N))+" b_avg_f="+str(len(b_avg_f))+" r_avg_f="+str(len(r_avg_f))+" p1_avg_f="+str(len(p1_avg_f))+" p2_avg_f="+str(len(p2_avg_f)))
    plt.plot(N,b_feas, **bu_style)
    #plt.plot(N,r_feas, **ra_style)
    plt.plot(N,p1_feas, **ra_style)
    plt.plot(N,p1_feas, **p1_style)
    plt.plot(N,p2_feas, **p2_style)
    #plt.title('Feasible block chainings '+apps_descr[iL])
    plt.tick_params(axis='both',labelsize='xx-large')
    plt.xlabel('Tasks', fontsize='xx-large')
    plt.legend(loc='right', fontsize='xx-large')
    plt.ylabel('Ratio of feasible block chainings', fontsize='xx-large')
    plt.tight_layout(pad=0.1)
    plt.savefig('/Users/daniela/Desktop/feas_'+apps_names[iL][-1:]+'.png', dpi=300)
    plt.figure()

    iL+=1

avg_b_Bn = []
avg_y_Bn = []
avg_r_Bn = []
avg_p1_Bn = []
avg_p2_Bn = []
for i in range(len(b_Bn[0])):
    s_b=0
    s_y=0
    s_r=0
    s_p1=0
    s_p2=0
    for j in range(len(apps_list)):
        s_b+=b_Bn[j][i] or 0
        s_y+=y_Bn[j][i] or 0
        s_r+=r_Bn[j][i] or 0
        s_p1+=p1_Bn[j][i] or 0
        s_p2+=p2_Bn[j][i] or 0
    avg_b_Bn.append(s_b/len(apps_list))
    avg_y_Bn.append(s_y/len(apps_list))
    avg_r_Bn.append(s_p1/len(apps_list))
    avg_p1_Bn.append(s_p1/len(apps_list))
    avg_p2_Bn.append(s_p2/len(apps_list))
    
print('\n')
print('N = '+str(N))
print('avg_b_Bn = '+str(avg_b_Bn))
print('avg_y_Bn = '+str(avg_y_Bn))
print('avg_r_Bn = '+str(avg_r_Bn))
print('avg_p1_Bn = '+str(avg_p1_Bn))
print('avg_p2_Bn = '+str(avg_p2_Bn))

#plt.subplot(3, 1, 2)
plt.plot(N,avg_b_Bn, **bu_style)
plt.plot(N,avg_r_Bn, **ra_style)
plt.plot(N,avg_p1_Bn, **p1_style)
plt.plot(N,avg_p2_Bn, **p2_style)
#plt.title('Average blocking time')
plt.tick_params(axis='both',labelsize='xx-large')
plt.legend(loc='lower right', fontsize='xx-large')
plt.xlabel('Tasks', fontsize='xx-large')
plt.ylabel('Blocking time (ms)', fontsize='xx-large')
plt.tight_layout(pad=0.1)
plt.savefig('/Users/daniela/Desktop/Bvalue.png', dpi=300)
   
plt.show()
