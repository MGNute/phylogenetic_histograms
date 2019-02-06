'''
This module is a script that contains all the functions required to reproduce the graphics created in the manuscript.

The functions given here rely on the data for the paper that is publicly available at
    https://doi.org/10.13012/B2IDB-1678505_V1. Specifically you will need to download:

        ...to run the IBD examples:
        - IBD_sepp_output.zip
        - IBD_sequence_mults.zip

        ...to run the primate examples:
        - primate_vaginal_sepp_output.zip

    After extracting each of those (which are within a subfolder in the zip file), you will need to point
        variables at the top of this module to each of those subfolders.

    In a sense, you will also need to download the reference data that is at that DOI also. Technically though,
        to run the examples you will only need the annotation file, and a copy of that is included in this repo
        in the 'test' folder. The variable "annot_file" below points to this annotation file. The tree is technically
        contained in each of the SEPP outputs, and the alignment is not used.

The key parts of this script are all contained in the individual functions. To run any of them, put a call to them
    in the loop at the very bottom of this script.
'''
import os.path
from art_manager import ArtManager
from data_controller import SeppJsonDataManager
from phylohist import *

base_folder = os.path.split(os.path.abspath(__file__))[0]
test_folder = os.path.join(base_folder,'test')

am = ArtManager()
dc = SeppJsonDataManager()
annot_file = os.path.join(test_folder,'ref_tree_annotation.txt')

primate_sepp = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\sepp_kernelplot\\sepp_results_w_archaea'
ibd_sepp = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\ibd\\sepp_jsons'
ibd_mults = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\ibd\\data_mults_by_seqname'
default_image_output_folder = ''


def run_figure_1():
    '''
    This function recreates the two graphics that are used in Figure 1 of the manuscript. The main call at the
    bottom of this function is another function that actually draws the graphic. All of the graphics for the
    primate vaginal study can be re-created using that call, by changing the arguments.
    '''
    sepp_results_folder = primate_sepp
    img_output_folder = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\sepp_kernelplot\\visuals\\temps'
    files = ['human_MID5_placement','human_BV2_MID3_placement']

    sepp_file = os.path.join(sepp_results_folder,files[0] + '.json')
    img_path = os.path.join(img_output_folder, files[0])

    # Even though the artman and dataman are module-variables here,
    # this is an example that is similar to the interface in run_scripts
    run_figure1_human_vaginal(am, dc, sepp_file, img_path,'pdf')

def run_primate_vaginal_graphics():
    '''
    This script creates new versions of the full set of graphics for the primate vaginal study, a.k.a. the
    graphics included in the supplement (not including the reference tree). In order to create these with the
    accessibility-enhanced hue scale, go to 'settings.py' and uncomment the proper value of the variable 'roygbiv'
    '''
    sepp_file_names = list(map(lambda x: x[:-5],os.listdir(primate_sepp)))  #get list of the files
    img_output_folder = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\results\\2018-08-phylogenetic-histograms\\ISMB_supplement_accessible\\primate_vaginal'

    for fi_nm in sepp_file_names:
        sepp_file = os.path.join(primate_sepp, fi_nm + '.json')
        img_path = os.path.join(img_output_folder, fi_nm)
        run_figure1_human_vaginal(am, dc, sepp_file, img_path, 'pdf')


def run_figure1_human_vaginal(artman, dataman, seppfile, img_path, type):
    '''
    This is a poorly named function because it's really the workhorse behind making all the graphics
    for the primate vaginal study.
    '''
    print('\topening sepp file')
    dataman.load_sepp_file(seppfile)
    dataman.load_read_multiplicities()
    dataman.load_reference_tree_annotation(annot_file)
    dataman.scale_multiplicities_to_total()


    print('\tdrawing tree')
    artman.set_image_path(img_path)
    artman.init_cairo_context(type='pdf')

    fo, fi = os.path.split(img_path)

    dataman.draw_tree(artman)
    dataman.make_colored_histogram(artman)
    artman.draw_label_on_screen(fo, (0., 0.), bold=True)
    artman.draw_label_on_screen(fi, (0., 30.))

    draw_legend_at_loc(artman.ctx, 1000, 200)

    artman.finish_cairo_content()
    print('done drawing tree')

def run_ibd_full_tree_all():
    '''
    This script creates all graphs for all IBD samples, including both on the full tree and on the clostridia-only
    subtree. Currently it is set up to create them as png files because the animations script below uses images.
    '''
    img_output_folder = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\results\\2018-08-phylogenetic-histograms\\ISMB_supplement_accessible\\ibd'
    sepp_file_names = list(map(lambda x: x.replace('_placement.json',''), os.listdir(ibd_sepp))) #get list of file names

    label_tups_dict = get_ibd_mapping()

    for fi_nm in sepp_file_names:
        sepp_file = os.path.join(ibd_sepp, fi_nm + '_placement.json')
        mults_file = os.path.join(ibd_mults, fi_nm + '.txt')
        img_path = os.path.join(img_output_folder, 'full_tree', fi_nm)
        ibd_full_tree_single_graphic(am, dc, sepp_file, mults_file, img_path, label_tups_dict[fi_nm])
        img_path = os.path.join(img_output_folder, 'clostridia', fi_nm)
        ibd_full_tree_single_graphic(am, dc, sepp_file, mults_file, img_path, label_tups_dict[fi_nm], clostridia_only=True)

def make_ibd_animations_clostridia_and_full_tree():
    '''
    This script creates the animations from the image files in the previous function. Calls one main workhorse 2x.
    '''

    # Full Tree:
    video_out_fold = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\results\\' \
                       '2018-08-phylogenetic-histograms\\ISMB_supplement_accessible\\ibd\\IBD_animations_full_tree'
    img_src_fold = os.path.join(video_out_fold, '..', 'full_tree')
    make_ibd_animations(video_out_fold, img_src_fold)

    # Clostridiales Only:
    video_out_fold = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\results\\' \
                     '2018-08-phylogenetic-histograms\\ISMB_supplement_accessible\\ibd\\IBD_animations_clostridia_only'
    img_src_fold = os.path.join(video_out_fold, '..', 'clostridia')
    make_ibd_animations(video_out_fold, img_src_fold)


def make_ibd_animations(video_out_folder, img_src_folder):
    '''
    This function creates the IBD animations for each of the 7 conditions. It relies on the mapping.txt file to know
    which ones are which, so that has to be correct. This function also imports OpenCV so that dependency coms in here.

    Basically it uses the mapping to make a dict of lists, one list for each condition. The list is then sorted and
    converted to a list of files in order, and the OpenCV VideoWriter just writes these into the video one at a time.
    '''
    mp = get_ibd_mapping()

    # get list of conditions
    conds=[]
    for k in mp.keys():
        conds.append(mp[k][1])
    conds = list(set(conds))

    # dict of lists of figures for each condition, in order
    condfigs = {c: [] for c in conds}
    for k in mp.keys():
        condfigs[mp[k][1]].append(mp[k][0])
    for k in condfigs.keys():
        condfigs[k].sort()

    mp_rev = {} # reverse lookup of mp: label --> figure
    for k in mp.keys():
        mp_rev[mp[k][0]] = k

    # make the videos
    import cv2
    fcc = cv2.VideoWriter_fourcc('F','M','P','4')   # this is a dependency but I'm not sure what's involved.

    for condition in condfigs.keys():
        figlist = list(map(lambda x: mp_rev[x], condfigs[condition]))
        vid_path = os.path.join(video_out_folder, condition + '.avi')
        vw = cv2.VideoWriter(vid_path, fcc, 3, (1500,900))  # 3 here is 3 frames-per-second. Could do faster also.
        for i in range(len(figlist)):
            img_path = os.path.join(img_src_folder, figlist[i] + '.png')
            img = cv2.imread(img_path)
            vw.write(img)
        vw.release()


def get_ibd_mapping():
    '''
    Gets the labels (e.g. 'CCD_193_1') based on the sample accession ID, which is what the file is named from
    '''
    mapping_file = os.path.join(os.path.abspath(os.path.join(ibd_mults,'..')),'mappings.txt')
    f=open(mapping_file,'r')
    ibd_labs = {}
    for ln in f:
        a=ln.strip().split('\t')
        ibd_labs[a[0]] = tuple(a[1:])
    f.close()
    return ibd_labs

def ibd_full_tree_single_graphic(artman, dataman, seppfile, multsfile, img_path, label_tuple=None, clostridia_only=False):
    '''
    This script creates a single graphic in the format used in the IBD graphics. It is set up to do both the
    full-tree graphics and the clostridia-only graphics, based on the final argument (self-explanatory).

    :param artman: (module level)
    :param dataman: (ditto)
    :param seppfile: sepp outputs JSON file
    :param multsfile: multiplicities file
    :param img_path: path to write the output image to
    :param label_tuple: (tuple) the label contents coming out of the mapping.txt file.
                        Example: ('UC_19_6', 'UC', '19', '6')
    :param clostridia_only: Boolean, self-explanatory
    :return:
    '''
    # def run_script_2(pbw, dataman, seppfile, svgfile):
    print ('\topening sepp file')
    dataman.load_sepp_file(seppfile)
    dataman.load_read_multiplicities(multsfile)
    dataman.load_reference_tree_annotation(annot_file)
    dataman.scale_multiplicities_to_total()
    # dataman.cap_multiplicities()

    if clostridia_only:
        dataman.get_subtree_as_current_tree('order','Clostridiales')
        dataman.post_update_current_tree()

    print ('\tdrawing tree')
    artman.init_cairo_context(type='png')
    # pbw.init_cairo_pdf_context(svgfile_full)
    # pbw.init_cairo_svg_context(svgfile_full)
    artman.set_image_path(img_path)

    fo, fi = os.path.split(img_path)

    dataman.draw_tree(artman)
    dataman.make_colored_histogram(artman)
    # artman.draw_label_on_screen(fo, (0., 0.), bold=True)
    if label_tuple is None:
        artman.draw_label_on_screen(fi, (0., 30.))
    else:
        artman.draw_label_on_screen(fi, (0., 0.))
        artman.draw_label_on_screen(label_tuple[0], (0., 30.), bold=True)

    draw_legend_at_loc(artman.ctx, 1000, 200)

    artman.finish_cairo_content()
    print ('done drawing tree')

if __name__=='__main__':
    ###
    ### Primate Vaginal Microbiome Study:
    ###
    # run_figure_1()
    # run_primate_vaginal_graphics()

    ###
    ### IBD Microbiome Study:
    ###
    # run_ibd_full_tree_all()
    # make_ibd_animations_clostridia_and_full_tree()


    pass