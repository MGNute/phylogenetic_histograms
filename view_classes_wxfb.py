# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jul 20 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class imgFrame
###########################################################################

class imgFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Phylogenetic Histograms GUI - Viewer", pos = wx.Point( 1,1 ), size = wx.Size( 1900,1000 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar2 = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Phylogenetic Histograms GUI - Controls", pos = wx.Point( 1,1 ), size = wx.Size( 842,556 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.BORDER_RAISED )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_notebook1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer66 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer73 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText12 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Graphic Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		
		self.m_staticText12.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.m_staticText12.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		bSizer73.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		bSizer76 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText47 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Matrix:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		
		self.m_staticText47.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_staticText47.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer76.Add( self.m_staticText47, 0, wx.ALL, 5 )
		
		self.m_panel13 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL|wx.BORDER_SIMPLE )
		gSizer1 = wx.GridSizer( 2, 3, 0, 0 )
		
		self.m_text_t11 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t11.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t11, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t12 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t12.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t12, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t13 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t13.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t21 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t21.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t21, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t22 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t22.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t22, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_text_t23 = wx.StaticText( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_t23.Wrap( -1 )
		
		gSizer1.Add( self.m_text_t23, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel13.SetSizer( gSizer1 )
		self.m_panel13.Layout()
		gSizer1.Fit( self.m_panel13 )
		bSizer76.Add( self.m_panel13, 1, wx.ALL, 1 )
		
		
		bSizer73.Add( bSizer76, 0, wx.EXPAND, 5 )
		
		bSizer78 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText54 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Rotation: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )
		
		self.m_staticText54.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_staticText54.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_staticText54, 0, wx.ALL, 5 )
		
		self.m_rotation = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_rotation.Wrap( -1 )
		
		self.m_rotation.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_rotation, 0, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Scale: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		
		self.m_staticText56.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_staticText56.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.m_scale = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_scale.Wrap( -1 )
		
		self.m_scale.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer78.Add( self.m_scale, 0, wx.ALL, 5 )
		
		
		bSizer73.Add( bSizer78, 0, wx.EXPAND, 5 )
		
		bSizer781 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText541 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText541.Wrap( -1 )
		
		self.m_staticText541.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_staticText541.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer781.Add( self.m_staticText541, 0, wx.ALL, 5 )
		
		self.m_width = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_width.Wrap( -1 )
		
		self.m_width.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer781.Add( self.m_width, 0, wx.ALL, 5 )
		
		self.m_staticText561 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText561.Wrap( -1 )
		
		self.m_staticText561.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		self.m_staticText561.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer781.Add( self.m_staticText561, 0, wx.ALL, 5 )
		
		self.m_height = wx.StaticText( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 60,-1 ), 0 )
		self.m_height.Wrap( -1 )
		
		self.m_height.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer781.Add( self.m_height, 0, wx.ALL, 5 )
		
		
		bSizer73.Add( bSizer781, 0, 0, 5 )
		
		bSizer721 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button481 = wx.Button( self.m_panel2, wx.ID_ANY, u"refresh settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer721.Add( self.m_button481, 0, wx.ALL, 5 )
		
		
		bSizer73.Add( bSizer721, 0, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer73.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText33 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Scripting:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		
		self.m_staticText33.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.m_staticText33.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		bSizer73.Add( self.m_staticText33, 0, wx.ALL, 5 )
		
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button44 = wx.Button( self.m_panel2, wx.ID_ANY, u"run_script_1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.m_button44, 0, wx.ALL, 5 )
		
		self.m_button441 = wx.Button( self.m_panel2, wx.ID_ANY, u"run_script_2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.m_button441, 0, wx.ALL, 5 )
		
		
		bSizer73.Add( bSizer71, 0, wx.EXPAND, 5 )
		
		
		bSizer73.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer66.Add( bSizer73, 1, wx.EXPAND, 5 )
		
		self.m_staticline24 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer66.Add( self.m_staticline24, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer74 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText121 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Input:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )
		
		self.m_staticText121.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.m_staticText121.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		bSizer74.Add( self.m_staticText121, 0, wx.ALL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText26 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"SEPP Json:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText26.Wrap( -1 )
		
		self.m_staticText26.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_staticText26.SetToolTip( u"Main results file from SEPP output. " )
		
		bSizer20.Add( self.m_staticText26, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_filePckJSON = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_SMALL )
		self.m_filePckJSON.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer20.Add( self.m_filePckJSON, 1, wx.ALL, 2 )
		
		
		bSizer20.Add( ( 5, 0), 0, 0, 0 )
		
		self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, u"load", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer20.Add( self.m_button6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		
		bSizer74.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		bSizer201 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText261 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Mults:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText261.Wrap( -1 )
		
		self.m_staticText261.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_staticText261.SetToolTip( u"Multiplicities for reads in the SEPP results file." )
		
		bSizer201.Add( self.m_staticText261, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_filePckMULTS = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_SMALL )
		self.m_filePckMULTS.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer201.Add( self.m_filePckMULTS, 1, wx.ALL, 2 )
		
		
		bSizer201.Add( ( 5, 0), 0, 0, 5 )
		
		self.m_button61 = wx.Button( self.m_panel2, wx.ID_ANY, u"load", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer201.Add( self.m_button61, 0, wx.ALL, 2 )
		
		
		bSizer74.Add( bSizer201, 0, wx.EXPAND, 5 )
		
		bSizer202 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText262 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Ref. Annot.", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText262.Wrap( -1 )
		
		self.m_staticText262.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_staticText262.SetToolTip( u"Tab-delimited annotation of the reference tree. (Optional)" )
		
		bSizer202.Add( self.m_staticText262, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_filePciANNOTATION = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_SMALL )
		self.m_filePciANNOTATION.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer202.Add( self.m_filePciANNOTATION, 1, wx.ALL, 2 )
		
		
		bSizer202.Add( ( 5, 0), 0, 0, 0 )
		
		self.m_button62 = wx.Button( self.m_panel2, wx.ID_ANY, u"load", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer202.Add( self.m_button62, 0, wx.ALL, 2 )
		
		
		bSizer74.Add( bSizer202, 0, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer74.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Output:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		
		self.m_staticText32.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
		self.m_staticText32.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		
		bSizer74.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText35 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Working Folder", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.m_staticText35.Wrap( -1 )
		
		self.m_staticText35.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_staticText35.SetToolTip( u"Folder into which any output images will be saved. By default is set as the folder containing the SEPP output.\n" )
		
		bSizer27.Add( self.m_staticText35, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_dirPckWORKING_FOLDER = wx.DirPickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
		self.m_dirPckWORKING_FOLDER.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer27.Add( self.m_dirPckWORKING_FOLDER, 1, wx.ALL, 2 )
		
		
		bSizer74.Add( bSizer27, 0, wx.EXPAND, 5 )
		
		bSizer271 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText351 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"File Name:", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.m_staticText351.Wrap( -1 )
		
		self.m_staticText351.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
		self.m_staticText351.SetToolTip( u"Folder into which any output images will be saved. By default is set as the folder containing the SEPP output.\n" )
		
		bSizer271.Add( self.m_staticText351, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_outFileName = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_outFileName.SetToolTip( u"Name of the file to create. (A .png extension will be added automatically.)" )
		
		bSizer271.Add( self.m_outFileName, 1, wx.ALL, 2 )
		
		
		bSizer74.Add( bSizer271, 0, wx.EXPAND, 5 )
		
		self.m_button12 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save to PNG", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button12.SetToolTip( u"Saves the currently generated image to a png file." )
		
		bSizer74.Add( self.m_button12, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		bSizer66.Add( bSizer74, 2, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer66 )
		self.m_panel2.Layout()
		bSizer66.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Dashboard", False )
		
		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_frame_close )
		self.Bind( wx.EVT_ICONIZE, self.on_frame_iconize )
		self.m_panel2.Bind( wx.EVT_PAINT, self.refresh_dashboard )
		self.m_button481.Bind( wx.EVT_BUTTON, self.on_refresh_settings )
		self.m_button44.Bind( wx.EVT_BUTTON, self.on_run_script_1 )
		self.m_button441.Bind( wx.EVT_BUTTON, self.on_run_script_2 )
		self.m_button6.Bind( wx.EVT_BUTTON, self.load_json )
		self.m_button61.Bind( wx.EVT_BUTTON, self.load_mults )
		self.m_button62.Bind( wx.EVT_BUTTON, self.load_ref_annotation )
		self.m_button12.Bind( wx.EVT_BUTTON, self.on_save_to_png )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_frame_close( self, event ):
		event.Skip()
	
	def on_frame_iconize( self, event ):
		event.Skip()
	
	def refresh_dashboard( self, event ):
		event.Skip()
	
	def on_refresh_settings( self, event ):
		event.Skip()
	
	def on_run_script_1( self, event ):
		event.Skip()
	
	def on_run_script_2( self, event ):
		event.Skip()
	
	def load_json( self, event ):
		event.Skip()
	
	def load_mults( self, event ):
		event.Skip()
	
	def load_ref_annotation( self, event ):
		event.Skip()
	
	def on_save_to_png( self, event ):
		event.Skip()
	

