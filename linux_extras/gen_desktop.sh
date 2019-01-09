#/bin/sh

# This script generates eduactiv8.desktop file using eduactiv8.desktop.in template and po files

rm -f eduactiv8.desktop
echo `ls ../i18n/po|grep .po|cut -d "." --fields=1` > ../i18n/po/LINGUAS
msgfmt --desktop -d ../i18n/po --template eduactiv8.desktop.in -o eduactiv8.desktop
rm -f ../i18n/po/LINGUAS
