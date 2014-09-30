import wx
from Updater import Updater


class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 539,311 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"D:\\dev\\MetroForSteamUpdater\\data\\images\\logo.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_bitmap1, 0, wx.ALL, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button1, 0, wx.ALL, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Latest Version: ?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Installed Version: ?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.m_button1.Bind( wx.EVT_BUTTON, self.UpdateButton )
        self.m_staticText1.Bind( wx.EVT_PAINT, self.UpdateCurrentVersion )
        self.m_staticText2.Bind( wx.EVT_PAINT, self.UpdateLatestVersion )
        self.m_statusBar1.Bind( wx.EVT_PAINT, self.UpdateStatusBar )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnClose( self, event ):
        event.Skip()

    def UpdateButton( self, event ):
        event.Skip()

    def UpdateCurrentVersion( self, event ):
        event.Skip()

    def UpdateLatestVersion( self, event ):
        event.Skip()

    def UpdateStatusBar( self, event ):
        event.Skip()




class UpdaterGUI(MyFrame1):
    def __init__( self, parent):
        self.updater = Updater()
        super(UpdaterGUI, self).__init__(parent)

    def UpdateButton( self, event ):
        result = False

        if self.updater.current_version == self.updater.latest_version:
            dlg = wx.MessageDialog( self, "You seem to have the latest version installed already. Do you want to update anyway?", "Latest Version Already Installed", wx.OK | wx.CANCEL)
            answer = dlg.ShowModal() # Show it
            dlg.Destroy() # finally destroy it when finished.
            if answer == wx.ID_OK:
                result = self.updater.UpdateSkin()
        else:
            result = self.updater.UpdateSkin()

        if result:
            dlg = wx.MessageDialog( self, "Updated to {}. Please restart Steam.".format(self.updater.latest_version), "Finished", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            self.m_staticText2.SetLabel('Installed Version: {}'.format(self.updater.current_version))


    def OnClose( self, event ):
        self.updater.SaveConfig()
        event.Skip()


    def UpdateCurrentVersion( self, event ):
        self.m_staticText1.SetLabel('Latest Version: {}'.format(self.updater.latest_version))
        event.Skip()


    def UpdateLatestVersion( self, event ):
        self.m_staticText2.SetLabel('Installed Version: {}'.format(self.updater.current_version))
        print self.updater.current_version
        event.Skip()


    def UpdateStatusBar( self, event ):
        self.SetStatusText("Status")
        event.Skip()

app = wx.App(False)
frame = UpdaterGUI(None)
frame.Show()
app.MainLoop()
