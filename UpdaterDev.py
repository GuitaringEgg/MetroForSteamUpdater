from Updater import Updater
import os
import urllib2

from bs4 import BeautifulSoup


class UpdaterDev(Updater):

    def __init__(self):
        Updater.__init__(self)


    def RunDev(self):
        self.CheckForUpdateDev()
        self.DownloadUpdateDev()
        self.InstallSkinDev()


    def CheckForUpdateDev(self):
        data = urllib2.urlopen('http://www.metroforsteam.com/')

        soup = BeautifulSoup(data.read())
        div = soup.find_all(attrs={'class':'left info'})
        text = div[0].get_text()
        self.version = text[text.find('Latest Version: ') + len('Latest Version: '):text.find('Download') - 1]
        print "Latest Version: {}".format(self.version)

        download = div[0].find_all('a')
        self.link = download[0].get('href')


    def DownloadUpdateOld(self):
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


ud = UpdaterDev()
ud.RunDev()
