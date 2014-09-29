import urllib
import urllib2
from bs4 import BeautifulSoup

import win32api
import os
import zipfile
import distutils.core
import shutil

import json

class Updater:

    def __init__(self):
        self.link = ''
        self.current_version = ''
        self.latest_version = ''
        self.skin_folder = ''
        self.dev = False

        os.chdir("data")


    def Run(self):
        if not self.LoadConfig():
            self.GetSteamFolder()
        self.CheckForUpdate()

        if self.current_version != self.latest_version:
            if self.dev:
                self.DownloadUpdateDriver()
        self.InstallSkin()
        #self.CleanUp()


    def LoadConfig(self):
        with open('config.json', 'r') as config:
            data = json.load(config)
            self.version = data['version']
            self.skin_folder = data['skin_folder']
            self.dev = data['dev']
            self.debug = data['debug']
            return True

        return False

    def CheckForUpdateDev(self):
        data = urllib2.urlopen('http://www.metroforsteam.com/')

        soup = BeautifulSoup(data.read())
        div = soup.find_all(attrs={'class':'left info'})
        text = div[0].get_text()
        self.version = text[text.find('Latest Version: ') + len('Latest Version: '):text.find('Download') - 1]
        print "Latest Version: {}".format(self.version)

        download = div[0].find_all('a')
        self.link = download[0].get('href')

    def CheckForUpdate(self):
        latest = urllib2.urlopen('https://raw.githubusercontent.com/GuitaringEgg/MetroForSteamUpdater/master/data/link.json')
        data = json.loads(latest.read())
        self.link = data["link"]
        self.latest_version = data["version"]

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
        data = urllib2.urlopen(self.link)
        soup = BeautifulSoup(data.read())

        download = soup.find_all(attrs={'class':'dev-page-button dev-page-button-with-text dev-page-download'})
        link = download[0].get('href')
        print link
        link = 'http://fc09.deviantart.net/fs71/f/2014/267/4/e/metro_for_steam___3_8_by_boneyardbrew-d4u3kjv.zip'

        data = urllib.urlretrieve(link, 'data.zip')

        print zipfile.is_zipfile('data.zip')

    def DownloadUpdateDev(self):
        from selenium import webdriver
        import time

        fp = webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", os.getcwd())
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip")
        fp.set_preference("browser.helperApps.neverAsk.openFile","application/zip")
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)

        driver = webdriver.Firefox(firefox_profile=fp)
        driver.get(self.link)
        html = driver.page_source
        soup = BeautifulSoup(html)

        driver.find_elements_by_class_name("dev-page-download")[0].click()
        os.listdir(".")
        time.sleep(1)
        while True in [x.endswith('.part') for x in os.listdir(".")]:
            print True in [x.endswith('.part') for x in os.listdir(".")]
        driver.close()


    # Check that the passed steamapps is valid
    def GetSteamFolder(self):

        # Check default location
        if os.path.exists(os.path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')):
            self.skin_folder = os.path.join(r'%PROGRAMFILES(x86)%', 'steam\\skins')

        # True to find the folder elsewhere
        else:
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            for drive in drives:
                if os.path.exists(os.path.join(drive, 'Program Files\\steam\\skins')):
                    self.skin_folder = os.path.join(drive, 'Program Files\\steam\\skins')

                elif os.path.exists(os.path.join(drive, 'Program Files (x86)\\steam\\skins')):
                    self.skin_folder = os.path.join(drive, 'Program Files (x86)\\steam\\skins')
                elif os.path.exists(os.path.join(drive, 'steam\\skins')):
                    self.skin_folder = os.path.join(drive, 'steam\\skins')

        log.error('Steamapps path given does not exist.')
        self.skin_folder = ''



    def InstallSkin(self):
        zf = zipfile.ZipFile('data.zip')

        for f in zf.namelist():
            if f.startswith('Metro for Steam'):
                if f.endswith('/'):
                    os.makedirs(f)
                else:
                    zf.extract(f)


        distutils.dir_util.copy_tree('Metro for Steam', os.path.join(self.skin_folder, 'Metro for Steam'), update=1)

    def InstallSkinDev(self):
        fn = [f.endswith('.zip') for f in os.listdir('.')]
        zf = zipfile.ZipFile(fn[0])

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
