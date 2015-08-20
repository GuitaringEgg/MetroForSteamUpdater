from Updater import Updater
import os
import urllib2
import urllib
import zipfile
import distutils
import glob

from bs4 import BeautifulSoup


class UpdaterDev(Updater):

    def __init__(self):
        Updater.__init__(self)


    def RunDev(self):
        self.CheckForUpdateDev()
        self.DownloadUpdateOld()
        self.InstallSkinDev()


    def CheckForUpdateDev(self):
        data = urllib2.urlopen('http://www.metroforsteam.com/')

        soup = BeautifulSoup(data.read())
        div = soup.find_all(attrs={'id':'date'})
        text = div[0].get_text()
        self.version = text
        print "Latest Version: {}".format(self.version)

        download = soup.find_all(attrs={'class':'button'})
        print download
        self.link = download[0].get('href')


    def DownloadUpdateOld(self):
        data = urllib2.urlopen(self.link)

        data = urllib.urlretrieve(self.link, 'data.zip')

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


    def InstallSkinDev(self):
        fn = glob.glob('./*.zip')
        zf = zipfile.ZipFile(fn[0])

        for f in zf.namelist():
            if f.startswith('Metro for Steam'):
                if f.endswith('/'):
                    if not os.path.exists(f):
                        os.makedirs(f)
                else:
                    zf.extract(f)

        distutils.dir_util.copy_tree('Metro for Steam', os.path.join(self.skin_folder, 'Metro for Steam'), update=1)
