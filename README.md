# AntiFontFingerprint
Simple script that protects you from the Font Fingerprint technique

### How it works?
Script moves several of your installed fonts into the hidden key - after that, the font fingerprint will be changed. Next time these fonts will be placed back, so that to be replaced with other fonts. This way you can change your font fingerprint without deleting your actual fonts. If you placed to Hidden any fonts you need for work, just run the script with `--recover-only` command-line key, it will place all hidden fonts back.

### How to use?
Run `python.exe font_fingerprint.py N`, where N is number of fonts you want to move to Hidden key.

If you are not comfortable with the command-line, simply start the file START.dat with the administrator privileges and enter number from 1 to 64



### Test - https://browserleaks.com/fonts
