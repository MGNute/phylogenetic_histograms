import os.path
from art_manager import ArtManager
from data_controller import SeppJsonDataManager
from phylohist import *

base_folder = os.path.split(os.path.abspath(__file__))[0]
test_folder = os.path.join(base_folder,'test')

am = ArtManager()
dc = SeppJsonDataManager()
annot_file = os.path.join(test_folder,'ref_tree_annotation.txt')


def run_figure_1():
    sepp_results_folder = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\sepp_kernelplot\\sepp_results_w_archaea'
    img_output_folder = 'C:\\Users\\miken\\Dropbox\\GradSchool\\Phylogenetics\\work\\dark-matter\\sepp_kernelplot\\visuals\\temps'
    files = ['human_MID5_placement','human_BV2_MID3_placement']

    sepp_file = os.path.join(sepp_results_folder,files[0] + '.json')
    img_path = os.path.join(img_output_folder, files[0])

    # Even though the artman and dataman are module-variables here,
    # this is an example that is similar to the interface in run_scripts
    run_figure1_human_vaginal(am, dc, sepp_file, img_path,'pdf')

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

def run_figure1_human_vaginal(artman, dataman, seppfile, img_path, type):
    print('\topening sepp file')
    dataman.load_sepp_file(seppfile)
    dataman.load_read_multiplicities()
    dataman.load_reference_tree_annotation(annot_file)
    dataman.scale_multiplicities_to_total()
    # dataman.cap_multiplicities()

    # dataman.get_subtree_as_current_tree('order','clostridiales')
    # dataman.post_update_current_tree()

    print('\tdrawing tree')
    artman.set_image_path(img_path)
    artman.init_cairo_context(type='pdf')
    # pbw.init_cairo_pdf_context(svgfile_full)
    # pbw.init_cairo_svg_context(svgfile_full)


    fo, fi = os.path.split(img_path)

    dataman.draw_tree(artman)
    dataman.make_colored_histogram(artman)
    artman.draw_label_on_screen(fo, (0., 0.), bold=True)
    artman.draw_label_on_screen(fi, (0., 30.))

    draw_legend_at_loc(artman.ctx, 1000, 200)

    artman.finish_cairo_content()
    print('done drawing tree')

# def ibd_run_script_2_full_tree(artman, dataman, seppfile, multsfile, img_path, type):
#     # def run_script_2(pbw, dataman, seppfile, svgfile):
#     print ('\topening sepp file')
#     dataman.load_sepp_file(seppfile)
#     dataman.load_read_multiplicities(multsfile)
#     dataman.load_reference_tree_annotation(annot_file)
#     dataman.scale_multiplicities_to_total()
#     # dataman.cap_multiplicities()
#
#     # dataman.get_subtree_as_current_tree('order','clostridiales')
#     # dataman.post_update_current_tree()
#
#     print ('\tdrawing tree')
#     artman.init_cairo_context(type='png')
#     # pbw.init_cairo_pdf_context(svgfile_full)
#     # pbw.init_cairo_svg_context(svgfile_full)
#     artman.set_image_path(img_path)
#
#     fo, fi = os.path.split(img_path)
#
#     dataman.draw_tree(artman)
#     dataman.make_colored_histogram(artman)
#     artman.draw_label_on_screen(fo, (0., 0.), bold=True)
#     artman.draw_label_on_screen(fi, (0., 30.))
#
#     draw_legend_at_loc(artman.ctx, 1000, 200)
#
#     artman.finish_cairo_content()
#     print ('done drawing tree')

if __name__=='__main__':
    run_figure_1()
    # run_example_STAMPS()
    pass