import wx
import seppostrator_wxfb, view_classes
import threading
import code, sys
import dendropy
from phylohist import *
import data_controller
import scripts as scr
import settings

class image_frame(seppostrator_wxfb.imgFrame):
    def __init__(self,parent):
        self.parent = parent
        seppostrator_wxfb.imgFrame.__init__(self,parent)
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        val = 255
        self.img_panel = view_classes.CairoBufferedWindow(self)
        self.img_panel.SetForegroundColour(wx.Colour(val, val, val))
        self.img_panel.SetBackgroundColour(wx.Colour(val, val, val))
        self.bSizer.Add(self.img_panel, 1, wx.EXPAND, 0)
        self.SetSizer(self.bSizer)
        self.Layout()

    def RemakeDrawing(self):
        self.img_panel.UpdateDrawing()


class cmd_manager(seppostrator_wxfb.ctrlFrame):
    def __init__(self,parent):
        self.parent=parent
        seppostrator_wxfb.ctrlFrame.__init__(self,parent)

        # print 'making image panel'
        self.image_panel = image_frame(self)
        self.image_panel.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.image_panel.Show()

        self.MoveXY(*settings.controls_xy)
        self.data_manager = data_controller.SeppJsonDataManager()
        # scr.startup(self.image_panel.img_panel, self.data_manager)


    def on_run_script( self, event = None ):
        reload(scr)
        scr.run_script_1(self.image_panel.img_panel, self.data_manager)
        self.image_panel.RemakeDrawing()

    def on_run_script_2(self, event = None):
        reload(scr)
        scr.run_script_2(self.image_panel.img_panel, self.data_manager)
        self.image_panel.RemakeDrawing()

    def redraw(self, calc_rotation=False):
        if calc_rotation:
            self.data_manager.rotate_perspective(self.image_panel.img_panel)
        t=threading.Thread(target=scr.redraw, args=(self.image_panel.img_panel, self.data_manager))
        t.start()

    def refresh_dashboard(self, event = None):
        print 'refreshing dashboard'
        m = self.image_panel.img_panel.matrix
        if m is not None:
            self.m_text_t11.SetLabel('%.1f' % m[0])
            self.m_text_t21.SetLabel('%.1f' % m[1])
            self.m_text_t12.SetLabel('%.1f' % m[2])
            self.m_text_t22.SetLabel('%.1f' % m[3])
            self.m_text_t13.SetLabel('%.1f' % m[4])
            self.m_text_t23.SetLabel('%.1f' % m[5])
            scal = math.sqrt(-m[0]*m[3]-m[1]*m[2])
            LR = lambda x: 1 if x>0 else -1
            rot = math.acos(m[2]/scal) * LR(m[0]/scal) /2 / math.pi * 360
            self.m_rotation.SetLabel('%.1f' % rot)
            self.m_scale.SetLabel('%.2f' % scal)



    def on_refresh_settings( self, event ):
        reload(settings)

class MyApp(wx.App):
    def OnInit(self):
        self.mainframe = cmd_manager(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.mainframe.Show()

        return True

if __name__ == '__main__':
    app = MyApp()
    # top = main.gui_manager.gui_manager(None)
    # top.Show(True)
    # print wx.GetTopLevelWindows()
    app.MainLoop()