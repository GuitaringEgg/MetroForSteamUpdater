import urllib
import urllib2
from bs4 import BeautifulSoup

import win32api
import os
import zipfile
import distutils.core
import shutil


class Updater:

    def __init__(self):
        self.link = ''
        self.version = ''
        self.current_version = '0.0'
        self.skin_folder = ''
        pass


    def Run(self):
        self.CheckForUpdate()
        self.DownloadUpdate()
        self.skin_folder = self.CheckForSteamFolder()
        self.GetCurrentVersion()
        self.InstallSkin()
        self.CleanUp()


    def CheckForUpdate(self):
        data = urllib2.urlopen('http://www.metroforsteam.com/')

        soup = BeautifulSoup(data.read())
        div = soup.find_all(attrs={'class':'left info'})
        text = div[0].get_text()
        self.version = text[text.find('Latest Version: ') + len('Latest Version: '):text.find('Download') - 1]
        print "Latest Version: {}".format(self.version)

        download = div[0].find_all('a')
        self.link = download[0].get('href')

    def GetCurrentVersion(self):
        if os.path.exists(os.path.join(self.skin_folder, 'Metro for Steam\\resource\\menus\\steam.menu')):
            with open(os.path.join(self.skin_folder, 'Metro for Steam\\resource\\menus\\steam.menu')) as f:
                for line in f:
                    if line.find('text="Metro For Steam - ') != -1:
                        start = line.find('text="Metro For Steam - ') + len('text="Metro For Steam - ')
                        end = line[start:].find('"') + start
                        self.current_version = line[start : end]
                        print "Current Version: {}".format(self.current_version)



    def DownloadUpdate(self):
        #http://stackoverflow.com/questions/13436418/simulating-clicking-on-a-javascript-link-in-python
        data = urllib2.urlopen(self.link)
        soup = BeautifulSoup(data.read())

        download = soup.find_all(attrs={'class':'dev-page-button dev-page-button-with-text dev-page-download'})
        link = download[0].get('href')
        print link
        link = 'http://fc09.deviantart.net/fs71/f/2014/267/4/e/metro_for_steam___3_8_by_boneyardbrew-d4u3kjv.zip'

        data = urllib.urlretrieve(link, 'data.zip')

        print zipfile.is_zipfile('data.zip')


    # Check that the passed steamapps is valid
    def CheckForSteamFolder(self):

        # Check default location
        if os.path.exists(os.path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')):
            return os.path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')

        # True to find the folder elsewhere
        else:
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            for drive in drives:
                if os.path.exists(os.path.join(drive, 'Program Files\\steam\\skins')):
                    return os.path.join(drive, 'Program Files\\steam\\skins')

                elif os.path.exists(os.path.join(drive, 'Program Files (x86)\\steam\\skins')):
                    return os.path.join(drive, 'Program Files (x86)\\steam\\skins')
                elif os.path.exists(os.path.join(drive, 'steam\\skins')):
                    return os.path.join(drive, 'steam\\skins')

        log.error('Steamapps path given does not exist.')
        return ''



    def InstallSkin(self):
        zf = zipfile.ZipFile('data.zip')

        for f in zf.namelist():
            if f.startswith('Metro for Steam'):
                if f.endswith('/'):
                    os.makedirs(f)
                else:
                    zf.extract(f)


        distutils.dir_util.copy_tree('Metro for Steam', os.path.join(self.skin_folder, 'Metro for Steam'), update=1)


    def CleanUp(self):
        shutil.rmtree('Metro for Steam')
        os.remove("data.zip")
