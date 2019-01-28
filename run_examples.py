'''
This module is a script that runs the three examples provided in the 'test'
subfolder. It can also be used as a guide for how to design and generate
varied graphics for a given study.
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

def run_example_1():
    print("Running first example:")
    sepp_file = os.path.join(test_folder,'ERR1746344_placement.json')
    mults_file = os.path.join(test_folder,'ERR1746344_mults.txt')
    img_path = os.path.join(test_folder, 'ERR1746344_image')

    # Even though the artman and dataman are module-variables here,
    # this is an example that is similar to the interface in run_scripts
    ibd_run_script_2_full_tree(am, dc, sepp_file, mults_file, img_path,'png')

def run_example_STAMPS():
    sepp_file = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\code\\stamps-tutorial\\tipp\\out\\TIPP-RDP-CLOSTRIDIA-95-SRR1219742_placement.json'
    img_path = 'C:\\Users\\miken\\GradSchoolStuff\\Research\\Phylogenetics\\code\\stamps-tutorial\\images\\TIPP-RDP-CLOSTRIDIA-95-SRR1219742_phylo_heat_map.pdf'
    dc.load_sepp_file(sepp_file)
    dc.load_read_multiplicities()
    dc.load_reference_tree_annotation(annot_file)
    # dc.scale_multiplicities_to_total()

    print('\tdrawing tree')
    am.set_image_path(img_path)
    am.init_cairo_context(type='pdf')

    fo, fi = os.path.split(img_path)

    dc.draw_tree(am)
    dc.make_colored_histogram(am)
    am.draw_label_on_screen(fi, (0., 0.), bold=True)
    # am.draw_label_on_screen(fi, (0., 30.))

    draw_legend_at_loc(am.ctx, 1000, 200)

    am.finish_cairo_content()
    print('done drawing tree')


def ibd_run_script_2_full_tree(artman, dataman, seppfile, multsfile, img_path, type):
    # def run_script_2(pbw, dataman, seppfile, svgfile):
    print ('\topening sepp file')
    dataman.load_sepp_file(seppfile)
    dataman.load_read_multiplicities(multsfile)
    dataman.load_reference_tree_annotation(annot_file)
    dataman.scale_multiplicities_to_total()
    # dataman.cap_multiplicities()

    # dataman.get_subtree_as_current_tree('order','clostridiales')
    # dataman.post_update_current_tree()

    print ('\tdrawing tree')
    artman.set_image_path(img_path)
    artman.init_cairo_context(type='png')
    # pbw.init_cairo_pdf_context(svgfile_full)
    # pbw.init_cairo_svg_context(svgfile_full)


    fo, fi = os.path.split(img_path)

    dataman.draw_tree(artman)
    dataman.make_colored_histogram(artman)
    artman.draw_label_on_screen(fo, (0., 0.), bold=True)
    artman.draw_label_on_screen(fi, (0., 30.))

    draw_legend_at_loc(artman.ctx, 1000, 200)

    artman.finish_cairo_content()
    print ('done drawing tree')

if __name__=='__main__':
    # run_example_1()
    run_example_STAMPS()