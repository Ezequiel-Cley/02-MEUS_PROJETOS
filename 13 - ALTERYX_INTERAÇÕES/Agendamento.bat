set file=%1
set log=%file:yxwz=log.txt%
set log=%log:yxmd=log.txt%
"C:\Users\robo_mis_mfd\AppData\Local\Alteryx\bin\AlteryxEngineCmd.exe" %1 > %log%