from pprint import pprint
from copy import deepcopy
import math
import random


def generate_to_file(filename):
    default_radius = 15

    def l2_dist(x1,y1,x2,y2):
    #    print "Distance of ",x1,y1,x2,y2,
        res = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    #    print res
        return res

    def task(amplitude,diameter,w_ratio,density,cursor_type):
        radius = diameter/2
        ans = {'mouse':{'x':0,'y':0},
                'cursor_type':cursor_type}
        ans['args']=[amplitude,diameter,w_ratio,density,cursor_type]
        
        ans['target'] = [[amplitude,0,radius]]
        offsets =  [[int(diameter*w_ratio),0],
                    [-int(diameter*w_ratio),0],
                    [0,-int(diameter*w_ratio)],
                    [0,int(diameter*w_ratio)]
                    ]

        ans['distractors'] = [[o[0]+amplitude,o[1],radius] for o in offsets]
        
        if density==0:
            return ans
            
        def condition(i,j):
            if int(i+j)%2 == 0 and density==0.5:
                return False
            return True
        
        dist = amplitude - diameter*(w_ratio) 
        xes = [i*(diameter+1) for i in range(int(dist/(diameter+1)))]
        latice = []
        for i in range(-3,4):
            for j,x in enumerate(xes):
                if condition(i,j):
                    latice.append([x,i*(diameter+1)])
        new_distractors = [[o[0],o[1],radius] for o in latice]
        ans['distractors'].extend(new_distractors)        
        
        return ans

    def get_translate_circle(x,y):
        def translate_circle(c):
            return [c[0]+x,c[1]+y,c[2]] 
        return translate_circle
        
    def translate_task(tt,x,y):
        t = deepcopy(tt)
        translate_circle = get_translate_circle(x,y)
        t['distractors'] = [translate_circle(c) for c in  t['distractors']]
        t['target'] = map(translate_circle, t['target'])
        return t

    def get_rotate_circle(theta):
        def rotate_circle(c):
            x = c[0]
            y = c[1]
            cos = math.cos(theta)
            sin = math.sin(theta)
    #        print "SIN/COS:",sin,cos
            xx = int( x*cos - y*sin )
            yy = int( x*sin + y*cos )
            return [xx,yy,c[2]]
        return rotate_circle
        
    def rotate_task(tt,theta):
        t = deepcopy(tt)
        rotate_circle = get_rotate_circle(theta)
        t['distractors'] = [rotate_circle(c) for c in  t['distractors']]
        t['target'] = map(rotate_circle, t['target'])
        return t
             
    def rotate_translate_task(t,x,y,theta):
        t2 = rotate_task(t,theta)
        t2 = translate_task(t2,x,y)
        return t2    
        
    t = task(500,20,2,0.5,"Bubble")
    t = rotate_translate_task(t,500,0,math.pi/4)#,500,300)


    amplitudes = [256,512,768]
    diameters = [8,16,32]
    w_ratios = [1.33,2,3]
    densities = [0,0.5,1]
    cursors = ["Point","Bubble"]
    # 162

    param_list = [[]]
    params = [amplitudes,diameters,w_ratios,densities,cursors]
    for pp in params:
        fix = param_list
        param_list = []
        for pvalue in pp:
            fix2 = []
            for f in fix:
                ff = deepcopy(f)
                ff.append(pvalue)
                fix2.append(ff)
            param_list.extend(fix2)
            
           
    #print param_list #it is OK
    #TODO scramble them and arrange into groups
    all_tasks = []
    for pars in param_list:
        all_tasks.append(task(*pars))
        
    #all_tasks = map(lambda t: rotate_translate_task(t,100,100,math.pi/4),all_tasks)

    def task_amplitude(t):
        return t['target'][0][0]
        
    # assume param_list and all_tasks are equivalently ordered
    #maxx,maxy = 900,900
    maxx,maxy = 1024,768

    oldx, oldy = maxx/2,maxy/2
    xythetas = []
    for j in range(len(param_list)):
        print "Looking for theta ",j,
        if j+1<len(param_list):
                max_dist = task_amplitude(all_tasks[j+1])
        else:
            max_dist = 0
        print max_dist
        found = False
        for k in range(314):
            theta = random.random()*6.28
            amp = task_amplitude(all_tasks[j])
            newx = int(oldx + amp*math.cos(theta))
            newy = int(oldy + amp*math.sin(theta))
            if newx > 0 and newx < maxx-1 and newy > 0 and newy < maxy-1:
    #            print 'inside'
                if (l2_dist(newx,newy,0,0) > max_dist or
                    l2_dist(newx,newy,maxx-1,0) > max_dist or
                    l2_dist(newx,newy,0,maxy-1) > max_dist or
                    l2_dist(newx,newy,maxx-1,maxy-1) > max_dist):
                    xythetas.append(deepcopy([oldx,oldy,theta]))
                    oldx, oldy = newx, newy 
                    found = True
                    print "found", newx, newy
                    break
        if not found:
            raise "not found"

    print "XYT=",xythetas        

    print len(param_list)
    for i in range(len(param_list)):
        t = all_tasks[i]
    #    print i
        xyt = xythetas[i]
        t = rotate_translate_task(t,xyt[0],xyt[1],xyt[2])    
        all_tasks[i] = t    

    #add a start task in the beginning
    st = task(0,10,1.3,0,"Bubble")
    st = rotate_translate_task(st,maxx/2,maxy/2,0)
    start_task = [st]
    start_task.extend(all_tasks)
#    start_task.extend(all_tasks[10:20])
#    start_task.extend(all_tasks[-20:-10])
    en = deepcopy(st)
    en['target']=[]
    #en['distractors']=[]
    start_task.append(en)


    data = open(filename+".js","w")
    print >>data, "situations =",
    pprint(start_task,stream=data) #TODO still not nicely positioned.s
    #print >>data, [t]
    data.close()




#generate_to_file("data_"+"101")
#generate_to_file("data_"+"102")
#generate_to_file("data_"+"103")
#generate_to_file("data_"+"104")
#generate_to_file("data_"+"105")
#generate_to_file("data_"+"106")
#generate_to_file("data_"+"107")
#generate_to_file("data_"+"108")
#generate_to_file("data_"+"109")
#generate_to_file("data_"+"110")
#generate_to_file("data_"+"111")
#generate_to_file("data_"+"112")






