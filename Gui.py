import wx
from Updater import Updater
from Frame1 import Window


class UpdaterGUI(Window):
    def __init__( self, parent):
        self.updater = Updater()
        super(UpdaterGUI, self).__init__(parent)
        self.m_dirPicker1.SetPath(self.updater.skin_folder)

    def UpdateButton( self, event ):
        result = False

        if self.updater.skin_folder == "":
            dlg = wx.MessageDialog( self, "The Steam folder has not been specified. Please input the Steam folder location first.", "Input Steam Folder Location", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            event.Skip()

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


    def UpdateSteamFolder( self, event ):
        print "cool"
        print self.m_dirPicker1.GetPath()
        if not self.updater.SetSteamFolder(self.m_dirPicker1.GetPath()):
            dlg = wx.MessageDialog( self, "Couldn't find the folder \"{}\". Please double check this is the where steam is installed.".format(self.m_dirPicker1.GetPath()), "Cannot find Steam Folder", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.m_dirPicker1.SetPath(self.updater.skin_folder)
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

if __name__ == "__main__":
    app = wx.App(False)
    frame = UpdaterGUI(None)
    frame.Show()
    app.MainLoop()
