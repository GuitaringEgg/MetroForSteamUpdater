pyinstaller gui.py updater.py -n MetroForSteamUpdater -i MetroForSteamUpdater.ico
xcopy data\* dist\MetroForSteamUpdater\data /s /i
