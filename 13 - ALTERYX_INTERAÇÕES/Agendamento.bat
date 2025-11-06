set file=%1
set log=%file:yxwz=log.txt%
set log=%log:yxmd=log.txt%
"C:\Users\arquivos_programas\Alteryx\bin\AlteryxEngineCmd.exe" %1 > %log%