@echo off
set /P f1="Etner number of FONTS needed to be deleted: "
python.exe %~dp0font_fingerprint.py %f1%
@pause