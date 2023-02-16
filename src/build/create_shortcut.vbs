' "C:\Users\WDAGUtilityAccount\Downloads\create_shortcut.vbs" "C:\Program Files\ROSA\ROSA.exe" "C:\Users\WDAGUtilityAccount\Desktop\ROSA.lnk" "C:\Users\WDAGUtilityAccount\AppData\Local\Temp\_MEI50202\ico\hotpot-ai.ico" "ROBOTICALLY OBNOXIOUS SERVING ASSISTANT - An emotional smart assistant that doesnt listen to you"

'https://github.com/Cornelius-Figgle/ROSA/
'ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX
'HARRISON, AS OF 2023
'
'It may work separately and independently of the main repo, it may not
'
' - Code (c) Max Harrison 2023
' - Ideas (c) Callum Blumfield 2023
' - Ideas (c) Max Harrison 2023
' - Vocals (c) Evie Peacock 2023

'Thanks also to everyone else for support throughout (sorry for 
'the spam). Also thanks to all the internet peoples that helped with 
'this as well 


exe = WScript.Arguments.Item(0) 'exe path
work = WScript.Arguments.Item(0) 'working dir of exe
lnk = WScript.Arguments.Item(1) 'full path of lnk
ico = WScript.Arguments.Item(2) 'full path of ico file
text = WScript.Arguments.Item(3) 'tooltip text


Set oWS = WScript.CreateObject("WScript.Shell") 
Set fso = CreateObject("Scripting.FileSystemObject")
Set oLink = oWS.CreateShortcut(lnk) 
oLink.TargetPath = exe
oLink.WorkingDirectory = fso.GetParentFolderName(exe)
oLink.Description = text
oLink.IconLocation = ico
oLink.Save 
