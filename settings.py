'''
contains user-settings that may not need to be changed regularly.
'''
# initial panel settings
# controls_xy = (2300,300)  #cincy monitor
controls_xy = (100,100)  #cincy monitor

# cairo settings
img_width = 1500
img_height = 900
img_aspect = float(img_width)/float(img_height)
tree_color = .70
tree_alpha = 1.0
tree_color_tup = (tree_color, tree_color, tree_color, tree_alpha)
tree_line_pct_of_width = .0005

# histogram settings
alpha_kernel = .10
min_branch_length = 0.
max_branch_length = .30
circle_width_factor = .006
circle_width_pixels = 5
raw_circle_width = .01

reads_scalar = 1000
reads_cap = 500
reads_scale_method = None

# annotation settings
clade_circle_margin = .1
clade_circle_color = .60
clade_circle_alpha = .75
clade_circle_color_tuple = (clade_circle_color, clade_circle_color, clade_circle_color, clade_circle_alpha)
collapsed_clade_color = (119./255., 55./255., 11./255.)
collapsed_clade_wedge = .10472 # pi/30

# color legend settings:
border_font_color = (0., 0., 0.,1.)
tick_height_rel_to_box = 0.025

# reference data settings
annotation_file = None