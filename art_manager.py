'''
This module defiens the ArtManager() class, which is designed so that
the software can be run as a script or as part of a gui without having
dependency issues and making sure file types are resolved. Also
encapsulates a few helper utilities for the cairo context.

Dependencies:
    cairo
'''

import cairo
import settings as s


class ArtManager():
    '''
    This is an intermediate class that wraps a small part of the cairo
    details, such as what kind of file type, etc... Most of the cairo
    API should be exposed to the DataManager object to do the actual rendering,
    but for one the housekeeping related to making sure a Cairo surface and
    context exist and are ready, and what file type. Also some functions are
    nice to encapsulate, like drawing labels here and there.
    '''
    w = s.img_width
    h = s.img_height

    surf = None
    draw_count = 0
    use_tree_copy = False
    node_labels_on = False
    leaf_labels_on = False
    write_image_to_path = False
    image_path = None
    show_root = False
    # background_color = (1., 1., 1.)
    background_color = None
    tree_line_color = (0., 0., 0.)
    matrix = None
    image_path_ext = ''
    valid_surface_types = ['png','wx','svg','pdf']
    cairo_surface_type = None

    def __init__(self, parent=None, image_path=None, type='png',*args, **kwargs):
        '''

        :param parent:
        :param image_path:
        :param args:
        :param kwargs:
        '''
        self.parent = parent

        if image_path is not None:
            self.image_path = image_path
        else:
            self.image_path = 'work\\temp_new.png'

        self.init_cairo_context(type=type)

    def set_image_path(self,path):
        '''
        Sets the path that the image should be saved as. Checks to see if there is a known extension
        on the path and separates that out.
        :param path:
        :return:
        '''
        if path[-4:] in ['.png','.jpg','.pdf','.svg']:
            if path[-4:]=='jpg':
                print("Cairo does not output as a jpg so we will use a png instead.")
                self.image_path_ext = 'png'
            else:
                self.image_path_ext = path[-3:]
            self.image_path = path[:-4]
        else:
            self.image_path = path

    def draw_label_on_screen(self, lab, point, size=16, color=(.35, .35, .35, 1.0), bold=False):
        '''
        You'll never guess what this method does.
        :param lab: String with the text to draw.
        :param point: (x,y) tuple or other size-2 iterable. Where to draw it.
        :param size: Font size (default: 16)
        :param color: Color (RGBA tuple). Default is a light grey.
        :param bold: Boolean.
        :return:
        '''
        oldm = self.ctx.get_matrix()
        oldfm = self.ctx.get_font_matrix()
        self.ctx.set_matrix(cairo.Matrix(1., 0., 0., 1., 0., 0.))
        self.ctx.set_font_matrix(cairo.Matrix(float(size), 0., 0., float(size), 0., 0.))
        oldf = self.ctx.get_font_face()
        if bold:
            self.ctx.set_font_face(cairo.ToyFontFace("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD))
        te = self.ctx.text_extents(lab)
        self.ctx.move_to(*point)
        self.ctx.rel_move_to(2, 2 + te[3])
        self.ctx.set_source_rgba(*color)
        self.ctx.show_text(lab)
        self.ctx.fill()
        self.ctx.set_matrix(oldm)
        self.ctx.set_font_matrix(oldfm)
        self.ctx.set_font_face(oldf)

    def draw_white_rectangle(self, L, R, T, B):
        '''
        Helper method to make sure the background isn't opaque in e.g. png files.
        :param L: Left Boundary
        :param R: Right Boundary
        :param T: Top Boundary
        :param B: Bottom Boundary
        :return: None
        '''
        self.ctx.set_matrix(cairo.Matrix(1., 0., 0., 1., 0., 0.))
        self.ctx.set_source_rgba(1., 1., 1., 1.)
        self.ctx.rectangle(L, T, abs(R - L), abs(B - T))
        self.ctx.fill()

    def init_cairo_context(self, type=None, svgsurf=None, newmatrix=True):
        '''
        This method creates the cairo surface and context used for drawing.
        :param svgsurf:
        :param newmatrix:
        :return:
        '''


        # Create the surface object.
        if self.surf is not None:
            del self.surf
        if svgsurf != None:
            self.surf = svgsurf
        else:
            if type is None:
                type = self.cairo_surface_type
            else:
                type = type.lower()
            if type in ('png','wx'):
                # This is the class to use if you want to render it to the screen.
                # Drawing to a png file is available from any image surface, so
                # if that option is specified just fall back on the type for rendering
                # to a gui window.
                self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.w, self.h)
                self.image_path_ext = 'png'
                self.cairo_surface_type = 'wx'
            elif type=='svg':
                self.image_path_ext = 'svg'
                self.cairo_surface_type = 'svg'
                self.surf = cairo.SVGSurface(self.image_path + '.svg', self.w, self.h)
            elif type=='pdf':
                self.image_path_ext = 'pdf'
                self.cairo_surface_type = 'pdf'
                self.surf = cairo.PDFSurface(self.image_path + '.pdf', self.w, self.h)
                # try:
                #     self.surf =cairo.PDFSurface(self.image_path + '.pdf', self.w, self.h)
                # except IOError:
                #     print (self.image_path)
                #     import sys
                #     sys.exit(0)

            else:
                print("surface type not recognized. Valid types are: \n%s" % str(self.valid_surface_types))
                self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32,self.w, self.h)
                self.cairo_surface_type = 'wx'

        self.ctx = cairo.Context(self.surf)

        if self.background_color is not None:
            self.ctx.set_source_rgb(*self.background_color)
            self.ctx.rectangle(0, 0, self.w, self.h)
            self.ctx.fill()
        else:
            self.ctx.set_source_rgba(1., 1., 1., 1.)
            self.ctx.rectangle(0, 0, self.w, self.h)
            self.ctx.fill()
            print ('\tw: %s, h: %s' % (self.w, self.h))

        if self.matrix is not None and newmatrix == True:
            self.ctx.set_matrix(self.matrix)

    def write_image_to_png(self,filepath=None):
        if filepath is not None:
            self.set_image_path(filepath)
        self.surf.write_to_png(self.image_path + '.png')

    def finish_cairo_content(self):
        '''
        When the image is done, write it to a file and re-initialize a new context.
        :return:
        '''
        if self.image_path_ext=='png':
            self.surf.write_to_png(self.image_path + '.png')
            self.init_cairo_context()
        self.surf.finish()



    def set_cairo_matrix(self, t11, t12, t13, t21, t22, t23):
        '''
        Sets the cairo coordinate transformation  based on the six points of the
        of the matrix
        :param t11:
        :param t12:
        :param t13:
        :param t21:
        :param t22:
        :param t23:
        :return:
        '''
        # self.ctx.set_matrix(cairo.Matrix(t11, -t21, t12, -t22, t13, -t23))
        # print 'matrix should be: [%.f, %.f, %.f, %.f, %.f, %.f]' % (t11, t12, t13, t21, t22, t23)
        self.ctx.set_matrix(cairo.Matrix(t11, t21, t12, t22, t13, t23))
        self.matrix = self.ctx.get_matrix()
