'''
This module contains two classes that extend the wx panel and make
rendering a cairo image to the screen pretty simple.
'''

import wx, os.path
import settings as s
import dendropy
import cairo
global colors
from utilities import *
import phylohist
import settings
import threading
from art_manager import ArtManger


USE_BUFFERED_DC = False

# class BufferedWindow(wx.Window):
class BufferedWindow(wx.Panel):
    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self, file_name, file_type) method.

    """
    def __init__(self, *args, **kwargs):
        # make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Window.__init__(self, *args, **kwargs)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_RIGHT_DCLICK(self,self.OnRightDclick)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)
        self.paint_count = 0
        self.x_off = 0
        self.y_off = 0

    def Draw(self,dc):
        ## just here as a place holder.
        ## This method should be over-ridden when subclassed
        pass

    def OnRightDclick(self, event):
        print event.GetPosition()

    def OnPaint(self, event):
        self.paint_count += 1
        # print "OnPaint called: ", self.paint_count
        # All that is needed here is to draw the buffer to screen

        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            memdc = wx.MemoryDC()
            memdc.SelectObject(self._Buffer)
            dc.Blit(self.x_off, self.y_off, self._Buffer.Width, self._Buffer.Height, memdc, 0, 0)
            # dc.DrawBitmap(self._Buffer, 0, 0)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()


        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(*Size)
        self.UpdateDrawing()

    def SaveToFile(self,FileName,FileType=wx.BITMAP_TYPE_JPEG):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName,FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. If that data changes, the drawing needs to
        be updated.

        This code re-draws the buffer, then calls Update, which forces a paint event.
        """
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        self.Refresh()
        self.Update()

class CairoBufferedWindow(BufferedWindow):
    '''
    This class is a version of the BufferedWindow above that does relevant drawing on a cairo context
    and can render it to the screen. Several of the methods in this module relate to user interactions
    via the mouse, but are disabled (since the lines in __init__ that bind the methods are commented).
    '''
    w = s.img_width
    h = s.img_height

    surf=None
    draw_count = 0
    use_tree_copy = False
    node_labels_on = False
    leaf_labels_on = False
    write_image_to_path = False
    image_path = None
    show_root = False
    # background_color = (1., 1., 1.)
    background_color = None
    tree_line_color = (0.,0.,0.)
    matrix = None
    moving = False; rotating = False;


    def __init__(self,parent,*args,**kwargs):
        BufferedWindow.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.am = ArtManger()
        self.image_path = 'work\\temp_new.png'
        # self.Bind(wx.EVT_RIGHT_DCLICK, self.DrawCairoFigure)

        # self.Bind(wx.EVT_LEFT_DOWN,self.on_left_mouse_down)
        # self.Bind(wx.EVT_LEFT_UP, self.on_left_mouse_up)
        # self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        # self.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave_window)
        self.Bind(wx.EVT_LEFT_DOWN,self.on_click)

    def on_click(self,event):
        pos = event.GetPosition()
        self.print_position_translation(pos)

    def print_position_translation(self,pos):
        m = self.am.ctx.get_matrix()
        m.invert()
        treepos = m.transform_point(*pos)
        self.parent.m_statusBar2.SetStatusText('user space: (%s, %s), tree space: (%.4f, %.4f)' % (pos[0],pos[1],treepos[0], treepos[1]),0)

    def set_cairo_matrix(self, t11, t12, t13, t21, t22, t23):
        self.am.set_cairo_matrix(t11, t12, t13, t21, t22, t23)

        self.matrix = self.ctx.get_matrix()
        # print self.matrix

    def on_left_mouse_down(self,event=None):
        self.anchor = event.GetPosition()
        if event.AltDown():
            self.rotating=True
            self.startxy=(float(self.anchor[0]),float(self.anchor[1]))
        else:
            self.moving = True

    def on_mouse_motion(self, event=None):
        if self.moving==True:
            ps = event.GetPosition()
            self.x_off += ps[0] - self.anchor[0]
            self.y_off += ps[1] - self.anchor[1]
            self.anchor=ps
            self.Refresh()
            # print '%s, %s' % (self.x_off, self.y_off)

    def on_left_mouse_up(self,event):
        '''
        currently, clicking on the image will rotate it. This may not be working
        properly.
        :param event:
        :return:
        '''
        if self.moving and self.matrix is not None:
            det = 1.0/(self.matrix[0]*self.matrix[3]-self.matrix[1]*self.matrix[2])
            x_off_t = det*(self.matrix[3]*self.x_off - self.matrix[2]*self.y_off)
            y_off_t = det*(-self.matrix[2]*self.x_off + self.matrix[0]*self.y_off)
            self.matrix.translate(x_off_t, y_off_t)
            self.x_off=0; self.y_off=0;
            self.ctx.set_matrix(self.matrix)
            self.parent.parent.redraw()
        if self.rotating:
            ps = event.GetPosition()
            self.stopxy = (float(ps[0]),float(ps[1]))
            self.parent.parent.redraw(calc_rotation=True)

        self.moving = False
        self.rotating = False

    def on_mouse_leave_window(self,event=None):
        self.on_left_mouse_up(event)

    def Draw(self,dc):
        self.draw_count +=1

        if self.am.surf is not None:
            h = self.am.surf.get_height()
            w = self.am.surf.get_width()
            # self._Buffer = wx.BitmapFromBufferRGBA(w,h,self.surf.get_data())
            self._Buffer = wx.EmptyBitmapRGBA(w,h)
            self._Buffer.CopyFromBuffer(self.surf.get_data(),format=wx.BitmapBufferFormat_ARGB32)
            dc.SelectObject(self._Buffer)
            # print 'done drawing'