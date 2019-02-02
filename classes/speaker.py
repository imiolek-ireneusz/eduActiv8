# -*- coding: utf-8 -*-

# import os
import platform
# import signal
import subprocess
import sys
import threading

import classes.extras as ex


class Speaker(threading.Thread):
    def __init__(self, lang, configo, android):
        self.android = android
        if self.android is None:
            threading.Thread.__init__(self)
            self.lang = lang
            self.enabled = True
            self.started = False
            self.process = None
            self.talkative = False
            self.debug = False
            if sys.version_info < (3, 0):
                self.needs_encode = False
            else:
                self.needs_encode = True
        else:
            self.enabled = False
            self.started = False

            self.process = None
            self.talkative = False

    def start_server(self):
        if self.android is None:
            if self.enabled and self.lang.voice is not None:
                cmd = ['espeak']
                cmd.extend(self.lang.voice)
                try:
                    # IS_WIN32 = 'win32' in str(sys.platform).lower() #maybe sys.platform is more secure
                    is_win = platform.system() == "Windows"
                    if is_win:
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
                        startupinfo.wShowWindow = subprocess.SW_HIDE
                        kwargs = {}
                        kwargs['startupinfo'] = startupinfo
                        self.process = subprocess.Popen(cmd, shell=False, bufsize=0, stdin=subprocess.PIPE,
                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                        startupinfo=startupinfo)
                    else:
                        if self.debug:
                            self.process = subprocess.Popen(cmd, shell=False, bufsize=0, stdin=subprocess.PIPE)
                        else:
                            self.process = subprocess.Popen(cmd, shell=False, bufsize=0, stdin=subprocess.PIPE,
                                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.started = True
                except:
                    self.enabled = False
                    self.started = False
                    print("eduActiv8: You may like to install eSpeak to get some extra functionality, " +
                          "however this is not required to successfully use the game.")
            else:
                self.process = None

    def restart_server(self):
        if self.started:
            self.stop_server()
        self.start_server()

    def run(self):
        pass

    def stop_server(self):
        if self.android is None:
            if self.enabled and self.started and self.process is not None:
                try:
                    self.process.stdin.close()
                    if not self.debug:
                        self.process.stdout.close()
                        self.process.stderr.close()
                    self.process.terminate()
                    #os.kill(self.process.pid, signal.SIGTERM)
                except OSError:
                    print("Error killing the espeak process")

    def say(self, text, voice=1):
        if self.android is None:
            if self.enabled and self.talkative and self.lang.voice is not None:
                text = self.check_letter_name(text)
                text = text + "\n"
                try:
                    text = text.encode("utf-8")
                except:
                    pass
                try:
                    self.process.stdin.write(text)
                    self.process.stdin.flush()
                except:
                    pass

    def check_letter_name(self, text):
        if sys.version_info < (3, 0):
            try:
                val = ex.unival(text)
            except:
                val = text
            if len(val) == 1 and len(self.lang.letter_names) > 0:
                t = ex.unival(val.lower())
                for i in range(len(self.lang.alphabet_lc)):
                    if t == ex.unival(self.lang.alphabet_lc[i]):
                        text = self.lang.letter_names[i]
                        break
        else:
            if len(text) == 1 and len(self.lang.letter_names) > 0:
                t = text.lower()
                for i in range(len(self.lang.alphabet_lc)):
                    if t == self.lang.alphabet_lc[i]:
                        text = self.lang.letter_names[i]
                        break
        return text
