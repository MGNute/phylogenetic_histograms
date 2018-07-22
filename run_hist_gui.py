import wx
import view_classes_wxfb, view_classes
import threading
import code, sys
import dendropy
from phylohist import *
from importlib import reload
import data_controller
import scripts as scr
import settings

class image_frame(view_classes_wxfb.imgFrame):
    def __init__(self,parent):
        self.parent = parent
        view_classes_wxfb.imgFrame.__init__(self, parent)
        self.bSizer = wx.BoxSizer(wx.VERTICAL)
        val = 255
        self.buff_window = view_classes.CairoBufferedWindow(self)
        self.buff_window.SetForegroundColour(wx.Colour(val, val, val))
        self.buff_window.SetBackgroundColour(wx.Colour(val, val, val))
        self.bSizer.Add(self.buff_window, 1, wx.EXPAND, 0)
        self.SetSizer(self.bSizer)
        self.Layout()

    def RemakeDrawing(self):
        self.buff_window.UpdateDrawing()

    def control_panel_tool_click(self, event=None):
        if self.parent.IsIconized() == True:
            self.parent.Iconize(False)
        self.parent.Raise()


class cmd_manager(view_classes_wxfb.ctrlFrame):
    def __init__(self,parent):
        self.parent=parent
        view_classes_wxfb.ctrlFrame.__init__(self, parent)

        # print 'making image panel'
        self.image_panel = image_frame(self)
        self.image_panel.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.image_panel.Show()

        self.Move(*settings.controls_xy)
        self.data_manager = data_controller.SeppJsonDataManager()
        # scr.startup(self.image_panel.img_panel, self.data_manager)


    def redraw(self, calc_rotation=False):
        if calc_rotation:
            self.data_manager.rotate_perspective(self.image_panel.buff_window)
        t=threading.Thread(target=view_classes.redraw, args=(self.image_panel.buff_window, self.data_manager))
        t.start()

    def refresh_dashboard(self, event = None):
        # print 'refreshing dashboard'
        m = self.image_panel.buff_window.matrix
        if m is not None:
            self.m_text_t11.SetLabel('%.3f' % m[0])
            self.m_text_t21.SetLabel('%.3f' % m[1])
            self.m_text_t12.SetLabel('%.3f' % m[2])
            self.m_text_t22.SetLabel('%.3f' % m[3])
            self.m_text_t13.SetLabel('%.3f' % m[4])
            self.m_text_t23.SetLabel('%.3f' % m[5])
            scal = math.sqrt(-m[0]*m[3]-m[1]*m[2])
            LR = lambda x: 1 if x>0 else -1
            rot = math.acos(m[2]/scal) * LR(m[0]/scal) /2 / math.pi * 360
            self.m_rotation.SetLabel('%.1f' % rot)
            self.m_scale.SetLabel('%.2f' % scal)

    def on_run_script_1( self, event ):
        scr.script_1(self.image_panel.buff_window.am,self.data_manager)

    def on_run_script_2( self, event ):
        scr.script_2(self.image_panel.buff_window.am,self.data_manager)

    def on_refresh_settings( self, event ):
        reload(settings)

    def load_json( self, event ):
        fp = self.m_filePckJSON.GetPath()
        fo, fi = os.path.split(fp)
        self.data_manager.load_sepp_file(fp)

        if self.m_outFileName.GetValue()=='':
            if fi[-5:].lower()=='.json':
                self.m_outFileName.SetValue(fi[:-5])
            else:
                self.m_outFileName.SetValue(fi)
        if self.m_dirPckWORKING_FOLDER.GetPath()=='':
            self.m_dirPckWORKING_FOLDER.SetPath(fo)

    def load_mults( self, event ):
        self.data_manager.load_read_multiplicities(self.m_filePckMULTS.GetPath())

    def load_ref_annotation( self, event ):
        self.data_manager.load_reference_tree_annotation(self.m_filePciANNOTATION.GetPath())


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