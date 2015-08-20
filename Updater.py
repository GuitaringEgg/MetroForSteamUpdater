import urllib2

import win32api
import os
import os.path as path
import zipfile
import distutils.core
import shutil
import urllib

import json
from bs4 import BeautifulSoup

class Updater:

    def __init__(self):
        self.link = ''
        self.current_version = 'Not Installed'
        self.latest_version = ''
        self.skin_folder = ''
        self.dev = False
        self.debug = False

        os.chdir("data/")

        if not self.LoadConfig():
            self.GetSteamFolder()
        self.CheckForUpdate()

        self.GetInstalledVersion()


    def UpdateSkin(self):
        if self.dev:
            self.DownloadUpdateDev()
        else:
            self.DownloadUpdate()

        self.InstallSkin()
        self.CleanUp()

        self.GetInstalledVersion()

        print self.current_version

        return True


    def LoadConfig(self):
        try:
            with open('config.json', 'r') as config:
                data = json.load(config)
                self.skin_folder = data['skin_folder']
                self.dev = data['dev']
                self.debug = data['debug']
                return True
        except EnvironmentError:
            print "File not file."

        return False


    def SaveConfig(self):
        with open('config.json', 'w') as outfile:
            data = dict()
            data["skin_folder"] = self.skin_folder
            data["dev"] = self.dev
            data["debug"] = self.debug
            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
            return True

        return False


    def CheckForUpdate(self):
        data = urllib2.urlopen('http://www.metroforsteam.com/')

        soup = BeautifulSoup(data.read())

        self.link = soup.find_all(attrs={'class':'button'})[0].get('href')
        self.latest_version = soup.find_all(attrs={'id':'date'})[0].get_text()
        print self.link
        print self.latest_version


    def GetInstalledVersion(self):
        if path.exists(path.join(self.skin_folder, 'Metro for Steam\\resource\\menus\\steam.menu')):
            with open(path.join(self.skin_folder, 'Metro for Steam\\resource\\menus\\steam.menu')) as f:
                for line in f:
                    if line.find('text="Metro For Steam - ') != -1:
                        start = line.find('text="Metro For Steam - ') + len('text="Metro For Steam - ')
                        end = line[start:].find('"') + start
                        self.current_version = line[start : end]
                        print line
                        print path.join(self.skin_folder, 'Metro for Steam\\resource\\menus\\steam.menu')
                        print "Current Version: {}".format(self.current_version)


    def DownloadUpdate(self):
        data = urllib.urlretrieve(self.link, 'data.zip')

        return zipfile.is_zipfile('data.zip')


    def GetSteamFolder(self):
        # Check default location
        if path.exists(path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')):
            self.skin_folder = path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')

        # True to find the folder elsewhere
        else:
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            for drive in drives:
                if path.exists(path.join(drive, 'Program Files\\Steam\\skins')):
                    self.skin_folder = path.join(drive, 'Program Files\\Steam\\skins')

                elif path.exists(path.join(drive, 'Program Files (x86)\\Steam\\skins')):
                    self.skin_folder = path.join(drive, 'Program Files (x86)\\Steam\\skins')
                elif path.exists(path.join(drive, 'Steam\\skins')):
                    self.skin_folder = path.join(drive, 'Steam\\skins')
                print path.exists(path.join(drive, 'Steam\\skins'))

    def SetSteamFolder(self, loc):
        if path.exists(loc) and loc.endswith('skins'):
            print loc
            self.skin_folder = loc
            return True
        elif path.exists(path.join(loc, 'skins')):
            self.skin_folder = path.join(loc, 'skins')
            return True
        else:
            return False


    def InstallSkin(self):
        zf = zipfile.ZipFile('data.zip')

        for f in zf.namelist():
            if f.startswith('Metro for Steam'):
                if f.endswith('/'):
                    if not os.path.exists(f):
                        os.makedirs(f)
                else:
                    zf.extract(f)


        distutils.dir_util.copy_tree('Metro for Steam', path.join(self.skin_folder, 'Metro for Steam'), update=1)


    def CleanUp(self):
        shutil.rmtree('Metro for Steam')
        if self.dev:
            os.remove([f.endswith('.zip') for f in os.listdir(('.'))][0])
        else:
            os.remove("data.zip")
