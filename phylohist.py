"""
This module has several functions relevant specifically to drawing a Phylogenetic
Histogram. Several of them have been separated from their more natural places
in the code because the computation is part of the graphic design, and
may be changed to suit the user.

Requirements:
    Dendropy >=4.0
    Cairo
    Numpy

Attributes:
    s.roygbiv (List of 3-tuples of float): Specifies the list of color-stops
        in the continuous color scale for denoting pendant branch lengths.
        Colors are given as (R,G,B) where all entries are floats between 0.0
        and 255.0 (which is the default for cairo). By default, the colors
        are:
            1. Red, (255,0,0)
            2. Yellow, (255,255,0)
            3. Green, (0,255,0)
            4. Light-Blue, (0,255,255)
            5. Blue (0,0,255)
        NOTE: this has been moved to settings but is still documented here for right now.



"""

import os, math
import dendropy, cairo
import numpy as np
import cairo
# from . import settings as s
import settings as s
# import utilities
import colorsys
#from art_manager import ArtManager

steps = len(s.roygbiv)-1
steps_f = float(steps)


def get_annotation_dict(filepath = None):
    '''
    Ges an annotation for the reference phylogeny. This is expected to be
    a tab-delimited text file with the leaf name in the first column and field
    names on the first line. It stores a large dict keyed by the first column.
    The values are also a dict, keyed by the headers.
    :return:
    '''
    if filepath is not None:
        annotation_file = filepath
    elif s.annotation_file is not None:
        annotation_file = s.annotation_file
    else:
        print("No annotation file specified. Try again.")
        return None
    myf = open(annotation_file,'r')
    header = myf.readline()
    header_names = header.strip().split('\t')
    ann_dict = {}
    for line in myf:
        rec = line.strip().split('\t')
        rec_dict = {}
        for i in range(len(rec)):
            rec_dict[header_names[i]]=rec[i]
        ann_dict[rec[0]]=rec_dict.copy()
    myf.close()
    return ann_dict

def get_color_of_pendant_branch(length):
    '''
    Defines the mapping between the pendant branch length and the color.
    :param length:
    :return:
    '''
    if length > s.max_branch_length:
        length = s.max_branch_length
        return (s.roygbiv[steps][0] / 255.0, s.roygbiv[steps][1] / 255.0, s.roygbiv[steps][2] / 255.0, s.alpha_kernel)
    if length <= 0:
        return (s.roygbiv[0][0]/ 255.0, s.roygbiv[0][1]/ 255.0, s.roygbiv[0][2]/ 255.0, s.alpha_kernel )

    first = int(length / s.max_branch_length * steps_f)
    pct_inter = length / s.max_branch_length * steps_f - float(first)
    if first==steps:
        return map(lambda x: x/255.0,s.roygbiv[steps])
    col1 = s.roygbiv[first]
    col2 = s.roygbiv[first+1]

    # interpolating on the RGB scale:
    return ((pct_inter*col2[0]+(1-pct_inter)*col1[0])/255.,
            (pct_inter * col2[1] + (1 - pct_inter) * col1[1])/255.,
            (pct_inter * col2[2] + (1 - pct_inter) * col1[2])/255.,
            s.alpha_kernel)

def draw_legend_at_loc(ctx,x0,y0, w=200, h=200, lw=1, fontsize=14, verbose=False):
    '''
    Draws the legend for the branch lengths and read counts.
    :param ctx: cairo context
    :param x0: where to draw it
    :param y0:
    :param w: how big
    :param h:
    :param lw:
    :param fontsize:
    :param verbose: if True, prints some messages to stdout along the way
    :return:
    '''
    # store the old matrix so we can give it back at the end
    old_mat = ctx.get_matrix()
    ctx.set_matrix(cairo.Matrix(1., 0., 0., 1., 0., 0.))

    pat = cairo.LinearGradient(x0, y0, x0+w, y0 )
    for i in range(steps+1):
        pct = float(i)/steps_f
        pat.add_color_stop_rgba(pct, s.roygbiv[i][0], s.roygbiv[i][1], s.roygbiv[i][2], s.alpha_kernel)

    # make border
    ctx.set_line_width(lw)
    ctx.set_source_rgba(*s.border_font_color)
    ctx.move_to(x0, y0)
    ctx.rectangle(x0, y0, w, h)
    ctx.stroke()

    # make tick marks and labels
    ctx.set_font_size(fontsize)
    for i in range(steps + 1):
        pct = float(i) / steps_f
        blen = pct * s.max_branch_length
        # pat.add_color_stop_rgb(pct,*get_color_of_pendant_branch(blen))
        ctx.move_to(x0 + w * pct, y0 + h)
        ctx.line_to(x0 + w * pct, y0 + h + h*s.tick_height_rel_to_box)
        ctx.stroke()
        te = ctx.text_extents('%.1f' % blen)
        ctx.move_to(x0 + w * pct - te[2] / 2, y0 + h + h*s.tick_height_rel_to_box + 5 + te[3])
        ctx.show_text('%.1f' % blen)

    num_placements_to_full = int(1/s.alpha_kernel*.75)
    num_ticks = 5
    tick_gap = int(num_placements_to_full/num_ticks)
    if verbose:
        print ('numtofull %s, tick_gap: %s' % (num_placements_to_full, tick_gap))
    y_start = y0+h
    max_te=0
    for i in range(num_ticks+1):
        ctx.move_to(x0+w, y0+h*(num_placements_to_full-i*tick_gap)/num_placements_to_full)
        ctx.line_to(x0+w+h*s.tick_height_rel_to_box, y0+h*(num_placements_to_full-i*tick_gap)/num_placements_to_full)
        ctx.stroke()
        te = ctx.text_extents('%s' % int(i*tick_gap))
        if te[2]>max_te:
            max_te=te[2]
        ctx.move_to(x0+w+h*s.tick_height_rel_to_box + 3,y0+h*(num_placements_to_full-i*tick_gap)/num_placements_to_full+te[3]/2)
        ctx.show_text('%s' % int(i*tick_gap))

    lab_te = ctx.text_extents('Branch Length')
    ctx.move_to(x0 + w/2 - lab_te[2] / 2, y0 + h + h*s.tick_height_rel_to_box  + 5 + te[3] + 5 + lab_te[3])
    ctx.show_text('Branch Length')

    m = ctx.get_font_matrix()
    m.rotate(-math.pi/2)
    ctx.set_font_matrix(m)
    lab_vert = '# of Reads'
    te_vert = ctx.text_extents(lab_vert)
    ctx.move_to(x0+w+h*s.tick_height_rel_to_box + 5+max_te+10, y0+h/2+te_vert[3]/2)
    ctx.show_text(lab_vert)

    # fill in the gradient
    ctx.set_source(pat)
    ctx.move_to(x0, y0)
    for i in range(num_placements_to_full):
        hgt = float(num_placements_to_full-i)/float(num_placements_to_full)
        ctx.rectangle(x0, y0, w, h * hgt)
        ctx.fill()

    # give back the old matrix
    ctx.set_matrix(old_mat)

def add_radial_phylogram_to_tree(tr):
    '''
    Takes a dendropy object and computes the layout of a radial phylogram
    on it, and adds the relevant data as attributes on the nodes. The scale
    coordinate space for the layout locations are defined by the legnths
    of the branches in the tree. The tree needs to have an edge length for
    every node.
    :param tr:
    :return:
    '''
    pr = tr.preorder_node_iter()

    # start with the root node
    ct = 0
    # r=pr.next()
    r=next(pr)
    # label every node
    if not hasattr(tr.leaf_nodes()[0], 'root_clade_id'):
        ct=1
        r.root_clade_id = 0
        for i in r.child_nodes():
            for j in i.preorder_iter():
                j.root_clade_id=ct
            ct+=1

    leafct = len([i for i in tr.leaf_node_iter() if i.drawn == True])
    collapsed_wedge_ct = len([i for i in tr.preorder_node_iter() if i.collapsed == True])

    tr.calc_node_ages(is_force_min_age=True)
    tr.calc_node_root_distances(return_leaf_distances_only=False)
    r.index = ct
    r.location = (0.0, 0.0)
    r.deflect_angle = 0.
    r.wedge_angle = 2 * math.pi
    r.edge_segment_angle = 0.
    r.right_wedge_border = 0.
    r.left_wedge_border = r.right_wedge_border
    r.nu = 0.

    ct +=1

    for i in pr:
        # This doesn't seem to work...
        if not i.collapsed:
            ww = float(len(i.leaf_nodes())) / leafct * (2 * math.pi-collapsed_wedge_ct*s.collapsed_clade_wedge)
        else:
            ww = s.collapsed_clade_wedge
        i.index = ct
        ct+=1
        i.wedge_angle = ww
        i.right_wedge_border = i.parent_node.nu
        i.left_wedge_border = i.right_wedge_border + i.wedge_angle
        i.nu =i.right_wedge_border
        thetav = i.parent_node.nu + ww/2
        i.edge_segment_angle = thetav
        i.parent_node.nu += ww
        if i.edge_length is None:
            i.edge_length = 0.
        delta = i.edge_length
        x1 = i.parent_node.location[0] + delta*math.cos(thetav)
        x2 = i.parent_node.location[1] + delta*math.sin(thetav)
        i.location = (x1, x2)
        i.deflect_angle = thetav - i.parent_node.edge_segment_angle
    return ct

def relocate_subtree_by_deflection_angle(nd):
    '''
    Given a node of a dendropy tree, it will recompute the locations
    of all the nodes below it. Crucially, this is only relevant if the
    'deflect_angle' attribute of the node has changed since the last
    rendering.
    :param nd:
    :return:
    '''
    pr = nd.preorder_node_iter()
    r = pr.next()
    if r.parent_node is not None:
        r.location[0] = r.parent_node.location[0]+r.edge_length*(
                        math.cos(r.parent_node.edge_segment_angle + r.deflect_angle))
        r.location[1] = r.parent_node.location[0] + r.edge_length * (
                        math.sin(r.parent_node.edge_segment_angle + r.deflect_angle))

def get_max_dims(tr, margin_pct=0.05):
    '''
    Finds the bounding box containing every point in the tree, plus a margin
    specified (as a fraction of the total screen size) by margin_pct
    :param tr: dendropy tree ojbect
    :param margin_pct: percentage of the screen given to the margin.
    :return:
    '''
    xmax = None
    xmin = None
    ymax = None
    ymin = None
    for i in tr.preorder_node_iter():
        if xmax is None or i.location[0]>xmax:
            xmax = i.location[0]
        if xmin is None or i.location[0]<xmin:
            xmin = i.location[0]
        if ymax is None or i.location[1]>ymax:
            ymax = i.location[1]
        if ymin is None or i.location[1]<ymin:
            ymin = i.location[1]
    xmarg = abs(xmax-xmin)*margin_pct
    ymarg = abs(ymax-ymin)*margin_pct
    return (xmin-xmarg, xmax+xmarg, ymin-ymarg, ymax+ymarg)

def draw_graphic_gui(artman, dataman):
    '''
    When using the GUI, a lot of actions require that the image be re-drawn,
    like rotating it or adding certain labels or such. This is the function
    that encapsulates the process of drawing the graphic. It can be
    changed by the user which is why it's in this module.
    :param artman:
    :param dataman:
    :return:
    '''
    dataman.draw_tree(artman)
    dataman.make_colored_histogram(artman)