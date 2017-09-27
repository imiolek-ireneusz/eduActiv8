#!/usr/bin/env python

# This is a helper program used to automatise some tasks related to distribution of this package.
# Removes all files with certain extensions in this directory and all subdirectories (5 levels deep)
# this is used to clear all temporary files and compiled code before packaging for distribution.
# The following extensions are being affected: ".py~", ".pyc", ".po~", ".pot~", ".txt~"
# and all __pycache__ directories including it's contents.
# rmcopy argument passed (ie. cleanup.py rmcopy) will also remove all copies of files (made on English locales)
# - removes all *copy).py files on top of earlier mentioned extensions.
# It also checks for any .mo files floating in .po directory and moves them to appropriate location in locale dir.

import datetime
import os
import shutil
import sys


def findNremove(path, file_patterns, dir_patterns, maxdepth=1):
    cpath = path.count(os.sep)

    # removing all matching files
    count = 0
    if len(file_patterns) > 0:
        for r, d, f in os.walk(path):
            if r.count(os.sep) - cpath < maxdepth:
                for files in f:
                    for pattern in file_patterns:
                        if files.endswith(pattern):
                            try:
                                # print "Removing %s" % (os.path.join(r,files))
                                count += 1
                                os.remove(os.path.join(r, files))
                            except Exception as e:
                                print(e)
    print("%d file(s) removed." % count)

    # removing all matching directories
    count = 0
    if len(dir_patterns) > 0:
        for r, d, f in os.walk(path):
            if r.count(os.sep) - cpath < maxdepth:
                for dirs in d:
                    for pattern in dir_patterns:
                        if dirs.endswith(pattern):
                            try:
                                # print "Removing %s" % (os.path.join(r,dirs))
                                count += 1
                                shutil.rmtree(os.path.join(r, dirs))
                            except Exception as e:
                                print(e)
    print("%d directories removed." % count)


def distribute_mo(hpath, path, pattern):
    cpath = path.count(os.sep)
    maxdepth = 1
    count = 0
    for r, d, f in os.walk(path):
        if r.count(os.sep) - cpath < maxdepth:
            for files in f:
                if files.endswith(pattern):
                    try:
                        src = os.path.join(r, files)
                        code = files[:-3]
                        dst = os.path.join(hpath, "locale", code, "LC_MESSAGES", "eduactiv8.mo")
                        shutil.copyfile(src, dst)  # copy
                        os.remove(os.path.join(r, files))  # remove
                    except Exception as e:
                        print(e)
                    else:
                        count += 1
    print("%d %s file(s) distributed." % (count, pattern))


def main():
    # path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    # determine extensions and directories to be removed
    file_patterns = [".py~", ".pyc", ".po~", ".pot~", ".txt~"]
    if len(sys.argv) == 2:
        if sys.argv[1] == "rmcopy":
            file_patterns.append("copy).py")

    # path to the directory where poedit saves compiled mo files (usually in the same dir as the source py files)
    popath = os.path.join(path, "i18n", "po")

    s = path.split("/")
    if len(s[-1]) > 9:
        dir_patterns = ["__pycache__", ".idea"]
        v = s[-1][10:]
        if v[0] in ["0", "1", "2", "3"]:
            with open(os.path.join(path, "classes", "cversion.py"), "w") as s_file:
                s_file.write('ver = "%s"' % v)
                print("\nVersion number updated.\n")
    else:
        dir_patterns = ["__pycache__"]
        t = datetime.date.today()
        c = t.strftime('%Y%m%d')
        v = "3.%s.%s" % (c[3:5], c[5:])

        with open(os.path.join(path, "classes", "cversion.py"), "w") as s_file:
            s_file.write('ver = "%s"' % v)
            print(
            "\nVersion updated - based on todays date - no version number in parent folder name. Please remember to change version number in eduactiv8.6 file before release.\n")

    # move the files to the locale directory based on its locale code
    distribute_mo(path, popath, ".mo")

    # remove all mentioned above
    findNremove(path, file_patterns, dir_patterns, 5)

    print("Done!\n")

if __name__ == "__main__":
    main()
