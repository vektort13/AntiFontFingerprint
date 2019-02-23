@echo off
set /P f1="Etner number of FONTS needed to be deleted: "
%~dp0delete_random_font.py %f1%
@pause