:: %1 is full path of exe
:: %2 is full path of lnk
:: %3 is full path of ico
:: %4 is shortcut text

@echo off
cd %~dp2
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = %2 >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = %1 >> CreateShortcut.vbs
echo oLink.WorkingDirectory = %~dp2 >> CreateShortcut.vbs
echo oLink.Description = %4 >> CreateShortcut.vbs
echo oLink.IconLocation = %3 >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs