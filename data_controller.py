'''
This module does the heavy-lifting. The class "SeppJsonDataManager()" is the one
that should be created when getting started. It imports the data, adds the tree,
and does all the rendering. It needs to be given an "ArtManager()" object as the
target for the rendering.

Dependencies:
    numpy
    scipy.spatial
    dendropy
    cairo
'''

import json, dendropy
import numpy as np
import copy
from phylohist import *
import settings as s
import scipy.spatial
from functools import reduce

class DataManager():
    def __init__(self):

        pass

class SeppJsonDataManager(DataManager):
    new_perspective = False
    clade_hull_locations = {}
    mrca_list = {}
    multiplicities = None
    total_read_count = None
    annotation_loaded = False
    multiplicities_loaded = False

    def __init__(self, seppfile=None):
        DataManager.__init__(self)
        if seppfile!=None:
            self.load_sepp_file(seppfile)

    def load_sepp_file(self,seppfile):
        '''
        This is a workhorse method to import results from SEPP. The input here
        has to be a path to a SEPP JSON results file. There are a lot of places
        in this process where some sanity checks on the input data would be
        helpful, but right now there are very few.

        TODO:
            * Since the reference tree is contained in the SEPP file, right now
                we are just using the one in the SEPP file. That means storing things
                like special layouts and such are not an option. They should be though.

        :param seppfile:
        :return:
        '''
        myf = open(seppfile,'r')
        self.myjson = json.load(myf)
        myf.close()
        self.tree = dendropy.Tree.get(data=self.myjson['tree'],schema='newick')
        # self.annotation = get_annotation_dict()
        self.annotation_loaded = False
        self.multiplicities_loaded = False

        print ('\tAdding new properties')
        for i in self.tree.preorder_node_iter():
            i.collapsed = False
            i.drawn = True
            ei = i.edge
            ei.comments = copy.deepcopy(i.comments)
            ei.distal_node = i
            ei.proximal_node = i.parent_node


        for i in self.tree.preorder_node_iter():
            i.comments = i.edge.comments

        self.node_ct = add_radial_phylogram_to_tree(self.tree)

        print ('\tcopying tree')
        self.current_tree = self.tree.extract_tree('orig')
        self.update_current_tree()

        print ('\tgetting max dimensions of tree:')
        self.max_dims = get_max_dims(self.current_tree)
        self.midpt = (self.max_dims[0] + 0.5 * (self.max_dims[1] - self.max_dims[0]),
                      self.max_dims[2] + 0.5 * (self.max_dims[3] - self.max_dims[2]))
        print ('\t\t(%s, %s, %s, %s)' % self.max_dims)
        self.set_coordinate_transform(topleft=True)

        self.get_comment_edge_lookup()
        self.append_placements()
        # self.update_current_tree_edges()
        # self.make_colored_histogram()

    def load_read_multiplicities(self,filename):
        '''
        For computation sake, it is helpful to remove duplicate reads from the
        read file before giving it to SEPP. Then when rendering we import the
        multiplicities for each read. Currently this is mandatory, although in
        the future it would be good to detect whether this is necessary first.
        :param filename:
        :return:
        '''
        mults = []
        mf = open(filename,'r')
        total = 0
        for i in mf:
            rd = i.strip().split('\t')
            rct = int(rd[1])
            total += rct
            mults.append((rd[0],rct))
        mf.close()
        self.multiplicities = dict(mults)
        self.multiplicities_orig = dict(mults)
        self.total_read_count = total
        print ("\ttotal reads: %s, multiplicities: %s, multiplicities_orig: %s" %
               (self.total_read_count, len(self.multiplicities), len(self.multiplicities_orig)))
        self.multiplicities_loaded = True

    def scale_multiplicities_to_total(self,new_total=None):
        '''
        Since abundance is represented by saturation, as long as we are using
        alpha-blending for saturation, it is important to scale the multiplicites
        to a certain total. This is a real headache though and I recommend
        just capping them if that doesn't make the graph too busy looking.
        :param new_total:
        :return:
        '''
        if self.multiplicities_loaded==False:
            print("No read multiplicity file loaded.")
            return
        s.reads_scale_method = 'Scale to Scalar'
        import random
        if new_total is None:
            new_total = s.reads_scalar
        newmults2 = list(map(lambda x: (x[0],float(x[1])/self.total_read_count * new_total,random.random()), self.multiplicities_orig.items()))
        newmults = list(map(lambda x: (x[0], int(x[1])+(1 if x[2]<(x[1]-float(int(x[1]))) else 0)),newmults2))
        print("newmults2 length: %s\tnewmults length: %s" % (len(newmults2), len(newmults)))

        self.multiplicities = dict(newmults)
        print ('%s keys in self.multiplicities, %s in original' % (len(self.multiplicities.keys()), len(self.multiplicities_orig.keys())))
        # tot = reduce(lambda x, y: (y[0],x[1]+y[1]), newmults)
        tot = sum(map(lambda x: x[1], newmults))
        if tot > new_total:
            '''
            One issue that can arise is that by scaling the totals, you end up with 
            fractional counts that have to be rounded. If the counts are small enough
            though, that rounding can screw up the totals so you have to select randomly
            which ones to round up or down.
            '''
            import collections
            # randomly select to bring the total down
            population = [val for val, cnt in self.multiplicities.items() for i in range(cnt)]

            self.multiplicities = dict(collections.Counter(random.sample(population,new_total)))
            a=len(self.multiplicities.keys())
            self.multiplicities.update(dict(map(lambda x: (x,0),list(set(self.multiplicities_orig.keys()).difference(set(self.multiplicities.keys()))))))
            b=len(self.multiplicities.keys())
            print ('%s keys before, %s keys after' % (a,b))
            # tot = reduce(lambda x, y: (y[0], x[1] + y[1]), self.multiplicities)
            tot = sum(map(lambda x: x[1],self.multiplicities.items()))
        print ("\tnew total = %s" % min(tot,1000000000))

    def cap_multiplicities(self,cap = None):
        '''
        Since the abundance is represented by saturation, it is sometimes useful
        to adjust that by setting a certain read-count to be fully saturated. This
        is done by going through the multiplicites and just putting a cap on each one.
        :param cap:
        :return:
        '''
        if self.multiplicities_loaded==False:
            print("No read multiplicity file loaded.")
            return
        s.reads_scale_method = 'Cap at Cap'
        if cap is None:
            cap = s.reads_cap
        newmults = map(lambda x: (x[0], x[1] if x[1] <= cap else cap), self.multiplicities_orig.items())
        self.multiplicities = dict(newmults)
        tot = reduce(lambda x, y: (y[0],x[1]+y[1]), newmults)
        print ("\tnew total = %s" % tot[1])

    def load_reference_tree_annotation(self,filepath=None):
        '''
        Loads the annotation file for the reference tree.
        :param filepath:
        :return:
        '''
        if filepath is None:
            print("No annotation file has been specified, so the previous annotation will"
                  "be enabled for further use. If there has not been one loaded, you will"
                  "likely encounter an error.")
        else:
            get_annotation_dict(filepath)
        self.annotation_loaded=True

    def get_mrca(self, rank, name):
        '''
        Returns the MRCA of all nodes with a particular taxonomic ID at a given
        rank. This requies the use of an annotation file with taxonomic IDs.
        :param rank:
        :param name:
        :return:
        '''
        if self.annotation_loaded==False:
            print("Function get_mrca requires an annotation for the reference tree but one has"
                  "not been loaded.")
            return
        if not isinstance(name, list):
            name = [name,]
        mytaxalabels = []
        outtaxalabels = []
        for i in self.current_tree.leaf_node_iter():
            if self.annotation[i.taxon.label][rank] in name:
                mytaxalabels.append(i.taxon.label)
            else:
                outtaxalabels.append(i.taxon.label)
        # mytaxalabels = [i.taxon.label for i in self.current_tree.leaf_node_iter() if
        #                 self.annotation[i.taxon.label][rank] == name]
        my_mrca = self.current_tree.mrca(taxon_labels=mytaxalabels)
        if my_mrca.root_clade_id != 0:
            self.mrca_list[rank + "|" + "".join(name)]=my_mrca
            return my_mrca
        else:
            my_mrca_2 = self.current_tree.mrca(taxon_labels=outtaxalabels)
            self.mrca_list[rank + "|" + "".join(name)] = my_mrca_2
            return my_mrca_2

    def collapse_at_mrca(self,rank,name):
        '''
        (Not Implemented Yet.) This goes through and collapses all nodes of a
        particular rank.
        :param rank:
        :param name:
        :return:
        '''
        my_mrca = self.get_mrca(rank,name)
        self.collapse_nodes(my_mrca)

    def get_comment_edge_lookup(self):
        '''
        Dendropy sometimes stores information about the tree in an attribute
        called "comments". This method is some housekeeping related to that but
        at the moment I can't remember exactly why it was necessary.
        :return:
        '''
        self.comment_edge_lookup = {}
        for i in self.tree.preorder_node_iter():
            ei = i.edge
            if len(ei.comments)>0 and ei.comments[0] is not None:
                ei.label = ei.comments[0]
                self.comment_edge_lookup[ei.comments[0]]=ei
            ei.distal_placements = []
            ei.pendant_lengths = []
            ei.names = []
            # these will eventually be needed for true kernel density plots
            ei.node_leftover_distal_placement = 0
            ei.node_leftover_pendant_length = 0

    def set_bounding_box(self,L,R,T,B):
        '''
        This sets the boundaries so that the image will be contained in the viewing window.
        This is particularly helpful if you want to draw multiple graphs on the same image,
        and you want to set a specific window for the sub-image.
        :param L:
        :param R:
        :param T:
        :param B:
        :return:
        '''
        w = abs(R-L)
        h = abs(B-T)
        aspect = abs((self.max_dims[1]-self.max_dims[0])/(self.max_dims[3]-self.max_dims[2]))
        if aspect > float(w) / float(h):
            B = T + (R - L) / aspect
        else:
            R = L + (B - T) * aspect
        p1new = (L,T)
        p2new = (L,B)
        p3new = (R,T)
        p1 = (self.max_dims[0],self.max_dims[3])
        p2 = (self.max_dims[0],self.max_dims[2])
        p3 = (self.max_dims[1],self.max_dims[3])
        self.set_coordinate_transform_3pts(p1,p2,p3,p1new, p2new, p3new)

    def collapse_nodes(self,node_list):
        '''
        (Not yet implemented.) There may be cases where we choose not to render
        certain clades in order to show everything else better. This marks a set
        of nodes in the tree as "collapsed" so they will not render.
        :param node_list:
        :return:
        '''
        if not isinstance(node_list,list):
            node_list = [node_list,]
        for i in node_list:
            i.collapsed = True
            for j in i.preorder_iter():
                j.drawn = False

    def append_placements(self):
        '''
        It is important for computation to store a reference to the set of reads
        that will be drawn on a given branch with the branch itself. This is mostly
        for the future where we don't want to rely on alpha-blending to get the
        saturation. But if you're trying to figure out how to render colors on
        a given branch, it helps not to have to scan through the reads first to
        find the ones that are relevant.
        :return:
        '''
        self.append_placements_general()

    # def append_placements_annotated(self):
    #     '''
    #     I'm not sure this has been fully implemented, but the idea here is to
    #     control some aspects of the drawing using an annotation file, for example if
    #     a set of reads should be omitted or something like that.
    #     :return:
    #     '''
    #     ann = get_sepp_annotation()
    #     for i in self.myjson['placements']:
    #         br = i['p'][0][0]
    #         nd = self.comment_edge_lookup[str(br)]
    #         for j in i['nm']:
    #
    #             if ann[j[0]]=='1':
    #                 nd.distal_placements.append(i['p'][0][3])
    #                 nd.pendant_lengths.append(i['p'][0][4])
    #     return ann

    def append_placements_general(self):
        '''

        :return:
        '''
        for i in self.myjson['placements']:
            br = i['p'][0][0]
            nd = self.comment_edge_lookup[str(br)]
            for j in i['nm']:
                nd.distal_placements.append(i['p'][0][3])
                nd.pendant_lengths.append(i['p'][0][4])
                nd.names.append(j[0])



    def make_colored_histogram(self, pbw, dump_file_name = None):
        '''
        This is the workhorse method that draws the histogram over the background
        phylogeny.
        :param pbw: an ArtManger object
        :return:
        '''
        m = pbw.ctx.get_matrix()
        m.invert()
        newdist = m.transform_distance(s.circle_width_pixels,0.)
        s.raw_circle_width = newdist[0]
        # s.raw_circle_width = (self.max_dims[1]-self.max_dims[0])*s.circle_width_factor
        # s.raw_circle_width = .1
        # print 'circle width is %s' % s.raw_circle_width
        drawn_ct = 0
        drawn_locs = []

        # check if we should make a dump file for the sequence names
        if dump_file_name is not None:
            dfile = open(dump_file_name,'w')

        for j in self.current_tree.preorder_node_iter():
            i = j.orig.edge
            if len(i.comments) > 0 and i.comments[0] is not None:
                np = len(i.distal_placements)
                try:
                    h_loc = i.distal_node.location
                    t_loc = i.proximal_node.location
                except AttributeError:
                    print (i.proximal_node.__dict__)
                    print (i.__dict__)
                for k in range(len(i.distal_placements)):
                    if i.length<=0.:
                        # print i.distal_placements[j]
                        pct_dist = 1
                    else:
                        pct_dist = 1-(i.distal_placements[k] / i.length)

                    if dump_file_name is not None:
                        dfile.write(i.names[k] + '\n')

                    my_x = pct_dist*h_loc[0]+(1-pct_dist)*t_loc[0]
                    my_y = pct_dist * h_loc[1] + (1 - pct_dist) * t_loc[1]
                    clr = get_color_of_pendant_branch(i.pendant_lengths[k])
                    pbw.ctx.set_source_rgba(*clr)

                    nm = i.names[k]
                    m = 1
                    if self.multiplicities is not None:
                        m = self.multiplicities[nm]
                    for ct in range(m):
                        pbw.ctx.arc(my_x, my_y, s.raw_circle_width, 0, 2 * math.pi)
                        pbw.ctx.fill()
                    drawn_locs.append((my_x,my_y))

                    drawn_ct+=1

        # tf.close()
        if dump_file_name is not None:
            dfile.close()
        return drawn_ct, drawn_locs

    def update_current_tree(self):
        '''
        This is a helper method. When we import a tree, we store a copy of the original
        tree and then create a working copy. This goes through and copies all the
        attributes of the original tree to the working copy. Sepcifically the attributes
        related to the drawing as a phylogram.
        :return:
        '''
        for i in self.current_tree.preorder_node_iter():
            i.index = i.orig.index
            i.location = i.orig.location
            i.deflect_angle = i.orig.deflect_angle
            i.wedge_angle = i.orig.wedge_angle
            i.edge_segment_angle = i.orig.edge_segment_angle
            i.right_wedge_border = i.orig.right_wedge_border
            i.left_wedge_border = i.orig.left_wedge_border
            i.nu = i.orig.nu
            i.collapsed = i.orig.collapsed
            i.drawn = i.orig.drawn
            i.root_clade_id = i.orig.root_clade_id

    def update_current_tree_edges(self):
        '''
        Anothe helper method for changing around the working copy of the tree.
        :return:
        '''
        for i in self.current_tree.preorder_node_iter():
            i.edge.comments = i.orig.edge.comments
            i.edge.distal_node = i.orig.edge.distal_node
            i.edge.proximal_node = i.orig.edge.proximal_node
            i.edge.distal_placements = i.orig.edge.distal_placements
            i.edge.pendant_lengths = i.orig.edge.pendant_lengths

    def post_update_current_tree(self):
        '''
        When we modify the working copy of the tree, there might be some housekeeping
        to do. This method is a dumping ground for housekeeping as we develop.
        :return:
        '''
        self.get_comment_edge_lookup()
        self.append_placements()


    def setup_numpy_arrays(self):
        '''
        This method creates a set of numpy arrays that store the attributes of the
        tree related to rendering. A lot of the computation related to rendering can
        get heavy, so it's best to do this in Numpy or C
        :return:
        '''
        self.np_topology = np.ones((self.node_ct, 3),dtype = np.int32)
        self.np_deflect_angles = np.zeros(self.node_ct, dtype = np.float64)
        self.np_edge_segment_angles = np.zeros(self.node_ct, dtype=np.float64)
        self.np_pts = np.zeros((self.node_ct,2), dtype=np.float64)
        self.right_wedge_borders = np.zeros(self.node_ct, dtype=np.float64)
        self.left_wedge_borders = np.zeros(self.node_ct, dtype=np.float64)
        self.wedge_angle = np.zeros(self.node_ct, dtype=np.float64)
        self.edge_lengths = np.zeros(self.node_ct, dtype=np.float64)

        # todo: fill the rest of this part in

    def get_rotation_for_optimal_aspect(self):
        '''
        It would be nice to be able to rotate the tree so as to fill the rectangular
        viewing window optimally. Sadly this is for the future.
        :return:
        '''
        print("This method has not been implemented yet. Doing nothing.")
        # todo: use numpy for this

        pass

    def draw_circle_around_clade(self,rank,name,pbw,draw_label=False):
        '''
        Occasionally it's helpful for annotation to circle some group. This does that.
        It is pretty slow though.
        :param rank:
        :param name:
        :param pbw:
        :param draw_label:
        :return:
        '''
        if self.annotation_loaded==False:
            print("Function draw_circle_around_clade requires an annotation for the reference tree but one has"
                  "not been loaded.")
            return
        if self.new_perspective:
            self.load_perspective(pbw)
            self.new_perspective=False
        key = rank + '|' + name
        if key in self.clade_hull_locations.keys():
            area = self.clade_hull_locations[key]
            nvert = area.shape[0]
        else:
            # tr = copy.deepcopy(self.current_tree)
            # fn = lambda nd: nd.taxon is not None and self.annotation[nd.taxon.label][rank]==name
            # subtree = self.tree.extract_tree('orig',fn,suppress_unifurcations=True)
            # nodesout = tr.filter_leaf_nodes(fn)
            # mytaxalabels = [i.taxon.label for i in self.current_tree.leaf_node_iter() if self.annotation[i.taxon.label][rank]==name]
            my_leaf_nodes = [i for i in self.current_tree.leaf_node_iter() if
                            self.annotation[i.taxon.label][rank] == name]
            my_mrca = self.get_mrca(rank,name)
            # print 'len mytaxa: %s\tlen nodesout: %s' % ( len(mytaxa), len(nodesout))
            # my_mrca = self.current_tree.mrca(taxon_labels=mytaxalabels)


            pts = np.zeros((len(self.current_tree.leaf_nodes())+1,3),dtype=np.float64)
            pts = np.zeros((len(my_leaf_nodes) + 1, 3), dtype=np.float64)
            # pr = self.current_tree.leaf_node_iter()

            pts[0,0] = my_mrca.location[0]
            pts[0,1] = my_mrca.location[1]
            ct = 1
            for i in my_leaf_nodes:
                pts[ct, 0] = i.location[0]
                pts[ct, 1] = i.location[1]
                pts[ct, 2] = i.edge_segment_angle
                ct+=1

            hull = scipy.spatial.ConvexHull(pts[:,0:2])
            nvert = hull.vertices.shape[0]
            cent = np.sum(pts[hull.vertices,0:2],0)/nvert
            chull = pts[hull.vertices,0:2]-cent
            hyps = np.hypot(chull[:,0],chull[:,1])

            s.clade_circle_margin = np.mean(hyps) * .05
            area = pts[hull.vertices,0:2]
            for i in range(area.shape[0]):
                area[i,:]+=(s.clade_circle_margin * math.cos(pts[hull.vertices[i], 2]) * ((hull.vertices[i] != 0) * 1),
                            s.clade_circle_margin * math.sin(pts[hull.vertices[i], 2]) * ((hull.vertices[i] != 0) * 1))

            self.clade_hull_locations[key] = area

        pbw.ctx.set_source_rgba(*s.clade_circle_color_tuple)
        pbw.ctx.move_to(*area[0,:])

        for i in range(1,nvert):
            pbw.ctx.line_to(*area[i, :])

        pbw.ctx.line_to(*area[0, :])

        dash_len = s.clade_circle_margin*.25
        pbw.ctx.set_line_width(abs(self.max_dims[0]-self.max_dims[1])/500)
        pbw.ctx.set_dash([dash_len, dash_len])
        pbw.ctx.stroke()
        pbw.ctx.set_dash([])

        if draw_label:
            lab_area = area - (self.midpt)
            lab_vert = np.argmax(np.hypot(lab_area[:,0],lab_area[:,1]))
            m = pbw.ctx.get_matrix()
            scal = math.sqrt(abs(1./(m[0]*m[3]-m[1]*m[2])))
            border_to_label = 5 * scal
            if lab_vert==area.shape[0]-1:
                lab_next_vert = 0
            else:
                lab_next_vert = lab_vert + 1
            initial_m = pbw.ctx.get_font_matrix()
            angle = math.atan2(area[lab_vert,1]-area[lab_next_vert,1],area[lab_vert,0]-area[lab_next_vert,0])
            pbw.ctx.set_font_size(16)
            oldm = pbw.ctx.get_font_matrix()
            # print "m:"; print m
            m.invert()

            if abs(angle)>math.pi/2:   # on the top half
                oldm.rotate(-(angle - math.pi))
                oldm = oldm.multiply(cairo.Matrix(m[0], m[1], m[2], m[3], 0, 0))
                x_height = pbw.ctx.text_extents('X')[3]*scal

                pbw.ctx.set_font_matrix(oldm)
                pbw.ctx.move_to(area[lab_vert, 0] + math.cos(angle + math.pi/2) * (border_to_label+x_height),
                                area[lab_vert, 1] + math.sin(angle + math.pi/2) * (border_to_label+x_height))

                pbw.ctx.show_text(name)
            else:
                # points_out = ...
                x_height = pbw.ctx.text_extents('X')[3]
                oldm.rotate(-angle)
                oldm = oldm.multiply(cairo.Matrix(m[0], m[1], m[2], m[3], 0, 0))
                # print oldm
                pbw.ctx.set_font_matrix(oldm)
                pbw.ctx.move_to(area[lab_next_vert, 0] + math.cos(angle + math.pi / 2) * (border_to_label),
                                area[lab_next_vert, 1] + math.sin(angle + math.pi / 2) * (border_to_label))
                # pbw.ctx.move_to(area[lab_next_vert, 0] + math.cos(angle + math.pi / 2) * 0,
                #                 area[lab_next_vert, 1] - math.sin(angle + math.pi / 2) *0)

                pbw.ctx.show_text(name)
                # print name
            pbw.ctx.stroke()
            pbw.ctx.set_font_matrix(initial_m)

    def get_subtree_as_current_tree(self,rank,included):
        '''
        Replaces the current working tree with a specified subtree
        :param rank:
        :param included:
        :return:
        '''
        if self.annotation_loaded==False:
            print("Function get_subtree_as_current_tree requires an annotation for the "
                  "reference tree but one has not been loaded.")
            return
        if not isinstance(included,list):
            included = [included]
        fn = lambda nd: self.annotation[nd.taxon.label][rank] in included
        del self.current_tree
        self.current_tree = self.tree.extract_tree('orig',fn,suppress_unifurcations=False)
        self.update_current_tree()
        self.update_current_tree_edges()

        add_radial_phylogram_to_tree(self.current_tree)
        self.max_dims = get_max_dims(self.current_tree)
        print ('new max_dims are (%s, %s, %s, %s)' % self.max_dims)
        self.midpt = (self.max_dims[0] + 0.5*(self.max_dims[1]-self.max_dims[0]),self.max_dims[2] + 0.5*(self.max_dims[3]-self.max_dims[2]))
        self.set_coordinate_transform(topleft=True)
        # self.post_update_current_tree()

    def set_coordinate_transform_3pts(self,x1, x2, x3, x1new, x2new, x3new):
        '''
        This method resets the transformation between the phylogeny space and the
        viewing window. Specifically though, this method does it by taking three
        points in the phylogeny space and three corresponding poitns in the viewing
        spacce, and sets the transform to match them up.
        :param x1: tuple or 1 x 2 array (x,y) in the phylogeny space
        :param x2: tuple or 1 x 2 array (x,y) in the phylogeny space
        :param x3: tuple or 1 x 2 array (x,y) in the phylogeny space
        :param x1new: tuple or 1 x 2 array (x,y) in the viewing space
        :param x2new: tuple or 1 x 2 array (x,y) in the viewing space
        :param x3new: tuple or 1 x 2 array (x,y) in the viewing space
        :return: None
        '''
        a=np.transpose(np.array([[x1[0], x1[1], 1],
                                 [x2[0], x2[1], 1],
                                 [x3[0], x3[1], 1]],dtype=np.float64))
        b = np.transpose(np.array([[x1new[0], x1new[1], 1],
                                   [x2new[0], x2new[1], 1],
                                   [x3new[0], x3new[1], 1]], dtype=np.float64))
        newm = np.dot(b,np.linalg.inv(a))
        self.t11 = newm[0, 0];
        self.t12 = newm[0, 1];
        self.t13 = newm[0, 2];
        self.t21 = newm[1, 0];
        self.t22 = newm[1, 1];
        self.t23 = newm[1, 2];
        # mark the transformation as having been changed so other methods can
        # adjust accordingly.
        self.new_perspective = True

    def set_coordinate_transform(self, topleft=False):
        '''
        There are several ways to set the transformation between the phylogeny space
        and the viewer space. In this particular case it take the height and width
        of the viewer space, squeezes the rendering points in phylogeny space into
        that window and centers the thing (unless topleft=True, then it puts it in the
        top left of the viewing window). The bounds in phylogeny space are kep in the
        self.max_dims variable.

        :param topleft: if topleft is True, just sets the top left corner to be whatever the max_dims dictates
        :return:
        '''
        max_dims = self.max_dims
        aspect = abs((max_dims[1] - max_dims[0]) / (max_dims[3] - max_dims[2]))
        w = s.img_width
        h = s.img_height

        if topleft==False:
            # print aspect
            if aspect > (float(w) / float(h)):
                # print 'cd is horiz'
                # constraining dimension is horizontal
                vgap = (h - w / aspect) / 2
                hgap = 0
            else:
                # print 'cd is vert'
                # constraining dimension is horizontal
                vgap = 0
                hgap = (w - h * aspect) / 2

            x1 = max_dims[0]; x2 = max_dims[1]; y1 = max_dims[3];
            a= np.array([[x1, 1 ,0],[x2,1,0], [-y1,0,1]], dtype=np.float64)
            b=np.array([hgap, w - hgap, vgap],dtype=np.float64)
            abc = np.dot(np.linalg.inv(a),b)
            # print a
            # print b

            self.t11 = np.asscalar(abc[0])
            self.t13 = np.asscalar(abc[1])
            self.t23 = np.asscalar(abc[2])
            self.t12 = 0; self.t21 = 0; self.t22 = -self.t11;
            self.new_perspective = True
        else:
            if aspect > float(w)/ float(h):
                hfact = float(w)/aspect
                wfact = float(w)
            else:
                hfact = float(h)
                wfact = float(h)*aspect
            x1new = (0,0); x1 = (self.max_dims[0],self.max_dims[3])
            x2new = (wfact,0); x2 = (self.max_dims[1],self.max_dims[3])
            x3new = [0,hfact]; x3 =(self.max_dims[0],self.max_dims[2])
            self.set_coordinate_transform_3pts(x1, x2, x3, x1new, x2new, x3new)

    def load_perspective(self,pbw):
        '''
        When we change the coordinate tranform, this is a helper to make sure
        the Cairo class has been adjusted properly.
        :param pbw: an ArtManager object
        :return:
        '''
        if self.new_perspective == True:
            pbw.set_cairo_matrix(self.t11, self.t12, self.t13, self.t21, self.t22, self.t23)
            self.new_perspective=False

    def rotate_perspective(self,pbw):
        '''
        Adjust the coordinate transformation so as to rotate the image relative to
        the viewer. A better way to rotate the image would probably be to change points
        in the phylogeny space so the changes would stick, but that is a headache.
        :param pbw: an ArtManager object
        :return:
        '''

        # get the midpoint of current image. This is the point about which to rotate.
        self.midpt = (self.max_dims[0] + 0.5 * (self.max_dims[1] - self.max_dims[0]),
                      self.max_dims[2] + 0.5 * (self.max_dims[3] - self.max_dims[2]))
        m = np.array([[pbw.matrix[0],pbw.matrix[2],pbw.matrix[4]],
                     [pbw.matrix[1],pbw.matrix[3], pbw.matrix[5]],
                     [0., 0., 1.]], dtype=np.float64)
        mi = np.linalg.inv(m)

        # if we rotate, we might push things out of the viewing window, so we
        # keep track of that to adjust scaling later.
        startxy = pbw.startxy;
        stopxy = pbw.stopxy;
        # print 'initial startxy: (%.1f, %.1f), stopxy: (%.1f, %.1f)' % (startxy[0], startxy[1], stopxy[0], stopxy[1])
        midxy_screen = pbw.matrix.transform_point(*self.midpt)
        h1 = math.hypot(startxy[0]-midxy_screen[0],startxy[1]-midxy_screen[1])
        h2 = math.hypot(stopxy[0]-midxy_screen[0], stopxy[1]-midxy_screen[1])
        stopxy = (midxy_screen[0] + (stopxy[0]-midxy_screen[0])* h1 / h2, midxy_screen[1] + (stopxy[1]-midxy_screen[1])* h1 / h2)


        moving_pt = (startxy[0]*mi[0,0]+startxy[1]*mi[0,1]+mi[0,2],startxy[0]*mi[1,0]+startxy[1]*mi[1,1]+mi[1,2])
        x1 = startxy[0]-midxy_screen[0]; y1 = startxy[1]-midxy_screen[1]; x2 = stopxy[0]-midxy_screen[0]; y2 = stopxy[1]-midxy_screen[1];
        rightturn = (x1*y2-x2*y1)/abs(x1*y2-x2*y1)
        theta = rightturn * math.acos((x1*x2+y1*y2)/(math.hypot(x1,y1)*math.hypot(x2,y2)))
        p3 = (moving_pt[0]+1,moving_pt[1])
        delt = pbw.matrix.transform_distance(1,0)
        delt_new = (delt[0]*math.cos(theta)-delt[1]*math.sin(theta),delt[0]*math.sin(theta)+delt[1]*math.cos(theta))

        pts1=np.transpose(np.array([[moving_pt[0], moving_pt[1], 1],
                                    [self.midpt[0], self.midpt[1], 1],
                                    [moving_pt[0]+1, moving_pt[1], 1]],dtype=np.float64))
        pts1new = np.transpose(np.array([[stopxy[0], stopxy[1], 1],
                                         [midxy_screen[0], midxy_screen[1], 1],
                                         [stopxy[0]+delt_new[0], stopxy[1]+delt_new[1],1]],dtype=np.float64))
        newm = np.dot(pts1new,np.linalg.inv(pts1))

        self.t11 = newm[0, 0]; self.t12 = newm[0, 1]; self.t13 = newm[0, 2];
        self.t21 = newm[1, 0]; self.t22 = newm[1, 1]; self.t23 = newm[1, 2];
        self.new_perspective = True
        pbw.startxy = None; pbw.stopxy = None;

    def draw_tree(self, pbw):
        '''
        This is the workhorse method that renders the background tree for drawing
        the historgram
        :param pbw: an ArtManger object
        :return:
        '''
        self.load_perspective(pbw)
        pbw.ctx.set_line_width(abs(self.max_dims[0]-self.max_dims[1])*s.tree_line_pct_of_width)

        pbw.ctx.set_source_rgba(*s.tree_color_tup)
        fn = lambda x: x.orig.drawn
        pr = self.current_tree.preorder_node_iter(fn)
        rt = next(pr)
        for i in pr:
            i.orig.location=i.location
            # i.orig.location[1]=i.location[1]
            pbw.ctx.move_to(*i.parent_node.location)
            pbw.ctx.line_to(*i.location)
            if i.orig.collapsed:
                pbw.ctx.stroke()
                p1x = i.location[0]+math.cos(i.left_wedge_border)*.5
                p1y = i.location[1]+math.sin(i.left_wedge_border)*.5
                p2x = i.location[0] + math.cos(i.right_wedge_border) * .5
                p2y = i.location[1] + math.sin(i.right_wedge_border) * .5
                pbw.ctx.move_to(*i.location)
                pbw.ctx.line_to(p1x,p1y)
                pbw.ctx.line_to(p2x,p2y)
                pbw.ctx.line_to(*i.location)
                pbw.ctx.set_source_rgb(*s.collapsed_clade_color)
                pbw.ctx.fill()
                pbw.ctx.set_source_rgba(*s.tree_color_tup)

        pbw.ctx.stroke()
