'''
This module contains several utilities that were developed in the course
of developing this module. They are not all used currently, but some are.

Attributes:
    colors (List of int 3-tuples):  A list of 64 colors that are maximally different
        from each other. The idea is that for any subset of the colors from 0 to K<64,
        the subset also contains a list that is maximally different and thus suitable
        as a discrete color scale in a data graphic. The source of this color scale is
        at:
            http://godsnotwheregodsnot.blogspot.ru/2012/09/color-distribution-methodology.html

    phylum_orders (dict):   A dict keyed by bacterial phyla that returns a number. The
        number corresponds roughly to how many of these phyla are in RDP as of 2017. The
        idea is that we can use this to define the order of scales so that regardless
        of which phyla are being rendered, the most important ones are near the top.

'''
import math
import numpy as np
import random
import colorsys
import platform


''' citation for this color set: http://godsnotwheregodsnot.blogspot.ru/2012/09/color-distribution-methodology.html
'''
colors = [(0,255,0),(0,0,255),(255,0,0),(1,255,254),(255,166,254),(255,219,102),(0,100,1),(1,0,103),(149,0,58),
          (0,125,181),(255,0,246),(255,238,232),(119,77,0),(144,251,146),(0,118,255),(213,255,0),(255,147,126),
          (106,130,108),(255,2,157),(254,137,0),(122,71,130),(126,45,210),(133,169,0),(255,0,86),(164,36,0),(0,174,126),
          (104,61,59),(189,198,255),(38,52,0),(189,211,147),(0,185,23),(158,0,142),(0,21,68),(194,140,159),
          (255,116,163),(1,208,255),(0,71,84),(229,111,254),(120,130,49),(14,76,161),(145,208,203),(190,153,112),
          (150,138,232),(187,136,0),(67,0,44),(222,255,116),(0,255,198),(255,229,2),(98,14,0),(0,143,156),(152,255,82),
          (117,68,177),(181,0,255),(0,255,120),(255,110,65),(0,95,57),(107,104,130),(95,173,78),(167,87,64),(165,255,210),
          (255,177,103),(0,155,255),(232,94,190),(0,0,0)]
phylum_orders={'Proteobacteria':1,'Actinobacteria':2,'Firmicutes':3,'Bacteroidetes':4,'Tenericutes':5,
'Spirochaetes':6,'Deinococcus-Thermus':7,'Streptophyta':8,'Verrucomicrobia':9,'Thermotogae':10,
'Fusobacteria':11,'Aquificae':12,'Acidobacteria':13,'Chloroflexi':14,'Synergistetes':15,'Planctomycetes':16,
'Chlamydiae':17,'Deferribacteres':18,'Chlorobi':19,'#N/A':20,'Chlorophyta':21,'Nitrospirae':22,'Thermodesulfobacteria':23,
'Cyanobacteria':24,'Chrysiogenetes':25,'Fibrobacteres':26,'Armatimonadetes':27,'Lentisphaerae':28,'Bacillariophyta':29,
'Dictyoglomi':30,'Euglenida':31,'Elusimicrobia':32,'Gemmatimonadetes':33,'Caldiserica':34,'Ignavibacteriae':35,
'proteobacteria':1,'actinobacteria':2,'firmicutes':3,'bacteroidetes':4,'tenericutes':5,'spirochaetes':6,
'deinococcus-thermus':7,'verrucomicrobia':9,'thermotogae':10,'fusobacteria':11,'aquificae':12,'acidobacteria':13,
'chloroflexi':14,'synergistetes':15,'planctomycetes':16,'chlamydiae':17,'deferribacteres':18,'chlorobi':19,
'nitrospira':22,'thermodesulfobacteria':23,'cyanobacteria_chloroplast':24,'chrysiogenetes':25,
'fibrobacteres':26,'armatimonadetes':27,'lentisphaerae':28,'dictyoglomi':30,'elusimicrobia':32,
'gemmatimonadetes':33,'caldiserica':34}


def dump_settings_to_file(fp):
    import settings as s
    f = open(fp,'w')
    f.write('# initial panel settings\n')
    f.write('controls_xy =  %s\n' % str(s.controls_xy))
    f.write('\n')
    f.write('# cairo settings\n')
    f.write('img_width =  %s\n' % s.img_width)
    f.write('img_height =  %s\n' % s.img_height)
    f.write('tree_color =  %s\n' % s.tree_color)
    f.write('tree_alpha =  %s\n' % s.tree_alpha)
    f.write('tree_color_tup =  %s\n' % str(s.tree_color_tup))
    f.write('tree_line_pct_of_width =  %s\n' % s.tree_line_pct_of_width)
    f.write('\n')
    f.write('# histogram settings\n')
    f.write('alpha_kernel =  %s\n' % s.alpha_kernel)
    f.write('length_for_red =  %s\n' % s.length_for_red)
    f.write('length_for_blue =  %s\n' % s.length_for_blue)
    f.write('circle_width_factor =  %s\n' % s.circle_width_factor)
    f.write('circle_width_pixels =  %s\n' % s.circle_width_pixels)
    f.write('raw_circle_width =  %s\n' % s.raw_circle_width)
    f.write('\n')
    f.write('reads_scalar =  %s\n' % s.reads_scalar)
    f.write('reads_cap =  %s\n' % s.reads_cap)
    f.write('reads_scale_method =  %s\n' % s.reads_scale_method)
    f.write('\n')
    f.write('\n')
    f.write('# annotation settings\n')
    f.write('clade_circle_margin =  %s\n' % s.clade_circle_margin)
    f.write('clade_circle_color =  %s\n' % s.clade_circle_color)
    f.write('clade_circle_alpha =  %s\n' % s.clade_circle_alpha)
    f.write('clade_circle_color_tuple =  %s\n' % str(s.clade_circle_color_tuple))
    f.write('collapsed_clade_color =  %s\n' % str(s.collapsed_clade_color))
    f.write('collapsed_clade_wedge =  %s\n' % s.collapsed_clade_wedge)
    f.write('\n')
    f.write('# color legend settings:\n')
    f.write('border_font_color =  %s\n' % str(s.border_font_color))
    f.write('tick_height_rel_to_box =  %s\n' % s.tick_height_rel_to_box)
    f.close()


def get_random_color(incr=None):
    if incr is None:
        H=random.random()
    else:
        H=incr+.03+random.random()*.08
    while True:
        S=random.random()*.5 + .5
        V=random.random()*.5 + .5
        if S+V>1.5:
            break
    rgb=colorsys.hsv_to_rgb(H,S,V)
    return rgb

def write_list_to_file(mylist,filepath):
    myf=open(filepath,'w')

    for i in mylist:
        myf.write(i + '\n')

    myf.close()

def color_scale_set(total, as_ints=True):
    lower_lim = .40

    side = int(float(total) ** .333 + 1)
    # print 'side length: %s' % side
    gap = 1.0 / float(side)

    #get the number of ineligible points (in the dark part of the cube
    ineliglbe_pts = int((lower_lim - gap * 5 / 6) / gap + 1) ** 3
    ineliglbe_pts += 1 #white is not allowed

    while side ** 3 - ineliglbe_pts < total:
        side += 1
        gap = 1.0 / float(side)
        ineliglbe_pts = int((lower_lim - gap * 5 / 6) / gap + 1) ** 3
    # print 'adjusted # pts: %s' % (side ** 3 - ineliglbe_pts )

    coords = []
    for i in range(side):
        c = gap * 5 / 6 + gap * float(i)
        coords.append(c)

    locus = []
    backrange = range(side)
    backrange.sort(reverse=True)
    for i in backrange:
        for j in backrange:
            for k in backrange:
                newc = (coords[i], coords[j], coords[k])
                if max(newc) > lower_lim and min(i,j,k)<max(backrange):
                    locus.append(newc)

    sss = side * side * side - ineliglbe_pts
    # print 'sss: %s' % sss
    # print 'length of locus (locus): %s' % len(locus)
    perm = get_ideal_permutation(len(locus))
    finals = []
    for i in perm:
        finals.append(locus[len(perm) - i - 1])
    if as_ints==True:
        finals2 = []
        for i in finals:
            finals2.append((int(i[0]*255), int(i[1]*255), int(i[2]*255)))
        return finals2
    else:
        return finals

def get_ideal_permutation(els):
    random.seed(100)
    m1 = int(els / 2)
    m2 = m1 + 1
    Ai = range(1, m1)
    Bi = range(m2 + 1, els + 1)
    A = random.sample(Ai, len(Ai))
    B = random.sample(Bi, len(Bi))
    out = []
    out.append(m1 - 1)
    if len(B) <> len(A):
        out.append(B.pop() - 1)
    for i in range(len(A)):
        out.append(A.pop() - 1)
        out.append(B.pop() - 1)
    out.append(m2 - 1)
    return out

# colors=[(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)]

def np_do_two_segments_intersect(a,b):
    '''
    Returns true if segments a and b intersect. Also returns the parametric indices [t1,t2] of the intersection point, if it exists.
    Segments are defined like: a=[x1,y1,x2,y2]

    NOTE: the segments touching is not good enough. They need to intersect in the open set between the endpoints.
    :param a:
    :param b:
    :return:
    '''

    #not a line, we'll call that false and move on...
    if ((a[0]==a[2]) and (a[1]==a[3])) or ((a[0]==a[2]) and (a[1]==a[3])):
        return False, a,b
    if ((a[0]==b[0] and a[1]==b[1]) or (a[0]==b[2] and a[1]==b[3]) or (a[2]==b[0] and a[3]==b[1])or (a[2]==b[2] and a[3]==b[3])):
        return False, a,b
    m1=np.dot(np.vstack((a[2:4]-a[0:2],b[2:4]-b[0:2])).transpose(),np.array([[1,0],[0,-1]],dtype=np.float64))

    m2 = b[0:2]-a[0:2]
    try:
        # matrix is full rank, solve away...
        t = np.dot(np.linalg.inv(m1),m2)
        return np.all((t>0.)*(t<1.)), t[0], t[1]
    except np.linalg.linalg.LinAlgError:
        # ugh, edge cases
        if a[2]==a[0]:
            t2 = (b[1] - a[1]) / (a[3] - a[1])
            t4 = (b[3] - a[1]) / (a[3] - a[1])
            return (b[0]==a[0] and ((t2>0 and t2<1) or (t4>0 and t4 <1))), a, b
        if a[1]==a[3]:
            t1 = (b[0] - a[0]) / (a[2] - a[0])
            t3 = (b[2] - a[0]) / (a[2] - a[0])
            return (b[1]==a[1] and ((t1>0 and t1<1) or (t3>0 and t3 <1))), a, b
        t1=(b[0]-a[0])/(a[2]-a[0])
        t2 = (b[1]-a[1]) / (a[3] - a[1])
        t3 = (b[2] - a[0])/ (a[2] - a[0])
        t4 = (b[3]-a[1]) / (a[3] - a[1])
        return (t1>0 and t1==t2 and t1<1) or (t3>0 and t3==t4 and t3<1), (t1,t2,t3,t4)

def get_list_from_file(filepath):
    myf=open(filepath,'r')
    ol=[]
    for i in myf:
        if i.strip()<>'':
            ol.append(i.strip())

    myf.close()
    return ol

def distance_btw_points(pt1,pt2):
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def dot_product(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]

def get_dict_from_tab_delimited_file(filename, keysfirst = True):
    myf = open(filename,'r')
    args = {}
    if keysfirst==True:
        for i in myf:
            if len(i.strip())>0:
                a=i.strip().split('\t')
                args[a[0]]=a[1]
    else:
        for i in myf:
            if len(i.strip())>0:
                a=i.strip().split('\t')
                args[a[1]]=a[0]
    myf.close()
    return args


def np_find_intersect_segments_allpy(segs):
    '''
    implements the sweep-line algorithm to find out if any of a list of line segments intersect.
    We don't count lines as intersecting if they share an endpoint.
    :param segs: (n x 4) numpy array where each row is given as (x_1, y_1, x_2, y_2) for the
                line going from (x_1,y_1) to (x_2,y_2)
    :return: do_intersect
    '''

    numpts = segs.shape[0]
    '''These arrays are laid out as (x,y,left?,index) where left is 1 if the point is a left point
    '''

    left_pts = np.zeros((numpts,2),dtype=np.float64)
    left_inds = np.vstack((np.zeros(numpts,dtype=np.int8),np.arange(numpts, dtype=np.int32))).transpose()
    right_pts = np.zeros((numpts, 2), dtype=np.float64)
    right_inds = np.vstack((np.ones(numpts,dtype=np.int8),np.arange(numpts, dtype=np.int32))).transpose()

    left_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 2], segs[:, 0])
    left_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 3], segs[:, 1])
    right_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 0], segs[:, 2])
    right_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 1], segs[:, 3])

    ordered_segs = np.hstack((left_pts,right_pts)).copy()

    all_pts = np.vstack((left_pts,right_pts))
    all_inds = np.vstack((left_inds,right_inds))

    all_view = np.array(np.zeros(2*numpts),dtype=[('x','f8'),('y','f8'),('left','i1'),('ind','i4')])
    all_view['x']=all_pts[:,0]
    all_view['y'] = all_pts[:, 1]
    all_view['left'] = all_inds[:,0]
    all_view['ind'] = all_inds[:,1]
    sort_inds = np.argsort(all_view,order=['x','left'])

    all_pts = all_pts[sort_inds]
    all_inds = all_inds[sort_inds]
    active_segs=None

    start_pt = 0
    wait=True
    while(wait):
        if all_inds[start_pt,1] != all_inds[start_pt+1,1]:
            wait=False
            if np_do_two_segments_intersect(ordered_segs[all_inds[start_pt,1],:],ordered_segs[all_inds[start_pt+1,1],:])==True:
                return False,ordered_segs[all_inds[start_pt,1],:],ordered_segs[all_inds[start_pt+1,1],:]
            active_segs = np.hstack((ordered_segs[all_inds[start_pt, 1], :], all_inds[start_pt, 1])).reshape((1, 5))
        else:
            start_pt +=2
            if start_pt >= all_inds.shape[0]:
                # print 'condition: start'
                return True, None, None

    for i in range(start_pt+1,2*numpts):
        nact = int(active_segs.shape[0])
        if all_inds[i,0]==0:
            k=sum(active_segs[:,1]<all_pts[i,1])

            pt = ordered_segs[all_inds[i,1],:]
            active_segs=np.insert(active_segs,k,np.hstack((ordered_segs[all_inds[i,1],:],all_inds[i,1])),0)
            if k>0:
                pred = active_segs[k-1,0:4]
                time_to_quit=np_do_two_segments_intersect(pt,pred)
                if time_to_quit[0]==True:

                    return False, pt ,pred
            if k<(nact-1):

                succ = active_segs[k+1,0:4]

                time_to_quit=np_do_two_segments_intersect(pt,succ)
                if time_to_quit[0]==True:
                    return False, pt, succ


        else:
            # try:
            # k=active_inds.pop(all_inds[i,1])
            try:
                k=np.asscalar(np.where(active_segs[:,4]==all_inds[i,1])[0])
            except:
                print ('error at that ascalar command')

                import sys
                sys.exit(0)
            if k < (nact-1) and k > 0:
                time_to_quit=np_do_two_segments_intersect(active_segs[k-1,0:4],active_segs[k+1,0:4])
                if time_to_quit[0]==True:
                    return False, active_segs[k-1,0:4],active_segs[k+1,0:4]
            active_segs=np.delete(active_segs,k,0)
    return True, None, None

def distance_to_line_segment(segx1, segx2, pt):
    '''
    Computes the ditstance from a point to a line segment. All three args are given as
    2-tupes or other length-2 iterable of floats.
    :param segx1: first endpoitn of segment
    :param segx2: second endpoitn of segment
    :param pt: point in question
    :return:
    '''
    diff = (segx2[0]-segx1[0],segx2[1]-segx1[1])
    v1 = (pt[0]-segx1[0],pt[1]-segx1[1])
    v2 = (pt[0] - segx2[0], pt[1] - segx2[1])

    if dot_product(v1,diff)*dot_product(v2,diff) < 0:
        return abs((segx2[1]-segx1[1])*pt[0] - (segx2[0]-segx1[0])*pt[1] + segx2[0]*segx1[1]-segx2[1]*segx1[0])/distance_btw_points(segx1,segx2)
    else:
        return min(distance_btw_points(segx1,pt),distance_btw_points(segx2,pt))

def read_from_fasta(file_path):
    '''
    Reads a fasta file into a dictionary where the keys are sequence names and values are strings representing the
    sequence.

    :param file_path:
    :return:
    '''
    output={}
    fasta=open(file_path,'r')
    first=True
    for l in fasta:
        if l[0]=='>':
            if first<>True:
                output[name]=seq
            else:
                first=False
            name=l[1:].strip()
            seq=''
        else:
            seq=seq + l.strip()
    output[name]=seq
    fasta.close()
    return output

def rotate(x,theta):
    '''
    rotates the point x around the origin by angle theta.
    :param x: (x,y) ordered pair representing coordinates
    :param theta: rotation angle (in radians)
    :return:
    '''

    return (x[0]*math.cos(theta)-x[1]*math.sin(theta),x[0]*math.sin(theta)+x[1]*math.cos(theta))
