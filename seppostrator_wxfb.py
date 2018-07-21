# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class imgFrame
###########################################################################

class imgFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SEPPostrator", pos = wx.Point( 1,1 ), size = wx.Size( 1900,1000 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar2 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.icnControlPanel = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/icnControls30.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Control Panel", u"Show/Hide the Control Panel", None ) 
		
		self.m_toolBar1.AddSeparator()
		
		self.m_tool2 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/rot_clock.bmp", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.control_panel_tool_click, id = self.icnControlPanel.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def control_panel_tool_click( self, event ):
		event.Skip()
	

###########################################################################
## Class ctrlFrame
###########################################################################

class ctrlFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Sepp-o-strator - Controls", pos = wx.Point( 1,1 ), size = wx.Size( 842,556 ), style = wx.DEFAULT_FRAME_STYLE|wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_notebook1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer66 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer73 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer76 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText47 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Matrix:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		self.m_staticText47.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.m_staticText47.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer76.Add( self.m_staticText47, 0, wx.ALL, 5 )
		
		self.m_panel13 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
		gSizer1 = wx.GridSizer( 2, 3, 0, 0 )
		
		self.m_text_t11 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t11.Wrap( -1 )
		gSizer1.Add( self.m_text_t11, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t12 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t12.Wrap( -1 )
		gSizer1.Add( self.m_text_t12, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t13 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t13.Wrap( -1 )
		gSizer1.Add( self.m_text_t13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t21 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t21.Wrap( -1 )
		gSizer1.Add( self.m_text_t21, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t22 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t22.Wrap( -1 )
		gSizer1.Add( self.m_text_t22, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t23 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t23.Wrap( -1 )
		gSizer1.Add( self.m_text_t23, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel13.SetSizer( gSizer1 )
		self.m_panel13.Layout()
		gSizer1.Fit( self.m_panel13 )
		bSizer76.Add( self.m_panel13, 0, wx.ALL, 1 )
		
		
		bSizer73.Add( bSizer76, 0, wx.EXPAND, 5 )
		
		bSizer78 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText54 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Rotation: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )
		self.m_staticText54.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.m_staticText54.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_staticText54, 0, wx.ALL, 5 )
		
		self.m_rotation = wx.StaticText( self.m_panel2, wx.ID_ANY, u"rotation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_rotation.Wrap( -1 )
		self.m_rotation.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_rotation, 0, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Scale: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		self.m_staticText56.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.m_staticText56.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.m_scale = wx.StaticText( self.m_panel2, wx.ID_ANY, u"(scale)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_scale.Wrap( -1 )
		self.m_scale.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_scale, 0, wx.ALL, 5 )
		
		
		bSizer73.Add( bSizer78, 0, wx.EXPAND, 5 )
		
		
		bSizer73.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer66.Add( bSizer73, 1, wx.EXPAND, 5 )
		
		self.m_staticline24 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer66.Add( self.m_staticline24, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer74 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer74.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer66.Add( bSizer74, 1, wx.EXPAND, 5 )
		
		self.m_staticline25 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer66.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer75 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer75.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer66.Add( bSizer75, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer66 )
		self.m_panel2.Layout()
		bSizer66.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Dashboard", True )
		self.m_panel12 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel12.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		bSizer67 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer68 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button44 = wx.Button( self.m_panel12, wx.ID_ANY, u"run_script", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.m_button44, 0, wx.ALL, 5 )
		
		self.m_button441 = wx.Button( self.m_panel12, wx.ID_ANY, u"run_script_2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.m_button441, 0, wx.ALL, 5 )
		
		
		bSizer68.Add( bSizer71, 0, wx.EXPAND, 5 )
		
		
		bSizer68.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer67.Add( bSizer68, 1, wx.EXPAND, 5 )
		
		self.m_staticline22 = wx.StaticLine( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer67.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer69 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer72 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button48 = wx.Button( self.m_panel12, wx.ID_ANY, u"refresh settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer72.Add( self.m_button48, 0, wx.ALL, 5 )
		
		
		bSizer69.Add( bSizer72, 0, wx.EXPAND, 5 )
		
		
		bSizer69.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer67.Add( bSizer69, 1, wx.EXPAND, 5 )
		
		self.m_staticline23 = wx.StaticLine( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer67.Add( self.m_staticline23, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer70 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer70.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer67.Add( bSizer70, 1, wx.EXPAND, 5 )
		
		
		self.m_panel12.SetSizer( bSizer67 )
		self.m_panel12.Layout()
		bSizer67.Fit( self.m_panel12 )
		self.m_notebook1.AddPage( self.m_panel12, u"Buttons", False )
		
		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_frame_close )
		self.Bind( wx.EVT_ICONIZE, self.on_frame_iconize )
		self.m_panel2.Bind( wx.EVT_PAINT, self.refresh_dashboard )
		self.m_button44.Bind( wx.EVT_BUTTON, self.on_run_script )
		self.m_button441.Bind( wx.EVT_BUTTON, self.on_run_script_2 )
		self.m_button48.Bind( wx.EVT_BUTTON, self.on_refresh_settings )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_frame_close( self, event ):
		event.Skip()
	
	def on_frame_iconize( self, event ):
		event.Skip()
	
	def refresh_dashboard( self, event ):
		event.Skip()
	
	def on_run_script( self, event ):
		event.Skip()
	
	def on_run_script_2( self, event ):
		event.Skip()
	
	def on_refresh_settings( self, event ):
		event.Skip()
	

