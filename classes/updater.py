# -*- coding: utf-8 -*-

import urllib
import socket
import threading
import classes.cversion


class Updater(threading.Thread):
    def __init__(self, config, android):
        self.config = config
        self.android = android
        if android is None:
            threading.Thread.__init__(self)

    @staticmethod
    def internet(host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as ex:
            #print ex.message
            return False

    def check4updates(self):
        if self.android is None:
            from lxml import etree
            url = "https://www.updates.eduactiv8.org/update.xml"
            update = urllib.urlopen(url).read()
            root = etree.XML(update)
            version = root.find(".//v")
            version_value = version.text
            self.config.avail_version = version_value
            if version_value != classes.cversion.ver:
                self.config.update_available = True
            else:
                self.config.update_available = False

    def run(self):
        try:
            if self.internet():
                self.check4updates()
        except:
            pass


"""
update.xml
<vi>
    <v>3.80.411</v>
</vi>
"""