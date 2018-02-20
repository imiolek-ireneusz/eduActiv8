# -*- coding: utf-8 -*-

# standard lib modules
import datetime
import hashlib
import os
import sqlite3
import sys


class DBConnection():
    def __init__(self, dbname, mainloop):
        self.dbname = dbname
        self.mainloop = mainloop
        self.userid = 0
        self.username = ""
        db_version = 1
        self.connect()
        if self.db_connected:
            #self.db_fix()
            self.c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name = 'admin'")
            self.conn.commit()
            count = self.c.fetchone()
            if count[0] == 0:
                print("Thank you for downloading eduActiv8.\nCreating database for storage of game data.")
                default_lang = "en_GB"
                os_lang = os.environ.get('LANG', '').split('.')
                if os_lang[0] in self.mainloop.config.all_lng:
                    default_lang = os_lang[0][:]
                else:
                    lcount = len(self.mainloop.config.all_lng)
                    for i in range(lcount):
                        if os_lang[0][0:2] == self.mainloop.config.all_lng[i][0:2]:
                            default_lang = self.mainloop.config.all_lng[i]
                            continue

                self.c.execute(
                    "CREATE TABLE users (username TEXT, password TEXT, date_added TEXT, last_login TEXT, lang TEXT, sounds INTEGER, espeak INTEGER, screenw INTEGER, screenh INTEGER, score INTEGER, scheme INTEGER, age_group INTEGER)")
                self.c.execute("CREATE TABLE levelcursors (userid INTEGER KEY, gameid INTEGER KEY,lastlvl INTEGER)")
                # self.c.execute("CREATE TABLE completions (userid integer, constructor text, variant integer, lvl_completed integer)")
                self.c.execute(
                    "CREATE TABLE completions (userid INTEGER KEY, gameid INTEGER KEY, lvl_completed INTEGER, lang_id INTEGER, num_completed INTEGER, age INTEGER)")
                # admin data - 1, admin, admin_pass, "en_gb", "00000"
                self.c.execute(
                    "CREATE TABLE admin (admin_id INTEGER KEY, admin_name TEXT, admin_pass TEXT, default_lang TEXT, login_screen_defaults TEXT, autologin_userid INTEGER, autologin INTEGER, db_version INTEGER)")
                # self.c.execute("INSERT INTO admin VALUES (?, ?, ?, ?, ?)", (admin_id, admin_name, admin_pass, default_lang, login_screen_defaults, db_version,autologin_userid TEXT,autologin INTEGER))
                self.c.execute("INSERT INTO admin VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (0, "", "", default_lang, "01101", 0, 0, db_version))
                self.conn.commit()

                self.lang = self.mainloop.lang
                self.lang.load_language(lang_code=default_lang)
                guest_name = self.lang.b["Guest"]
                if sys.version_info < (3, 0):
                    try:
                        if not isinstance(guest_name, unicode):
                            guest_name = unicode(guest_name, "utf-8")
                    except:
                        pass

                self.add_user(guest_name, "", default_lang, 0, 0, 800, 480)
                print("Database successfully created.")
            else:
                # check the db_version for future updates if database needs to be changed this will be used
                # to upgrade the db instead of recreating the db from scratch

                self.c.execute("SELECT db_version FROM admin WHERE (admin_id = 0)")
                self.conn.commit()
                """
                row = self.c.fetchone()
                current_db_ver = row[0]
                if 0 < current_db_ver < 4:
                    print("Database structure changed in this version of the game. Updating the database to version 4.")

                if current_db_ver == 1:
                    self.c.execute("ALTER TABLE admin ADD COLUMN autologin_userid INTEGER DEFAULT 0")
                    self.c.execute("ALTER TABLE admin ADD COLUMN autologin INTEGER DEFAULT 0")
                    self.c.execute("ALTER TABLE completions ADD COLUMN lang_id INTEGER DEFAULT 1")
                    self.c.execute("UPDATE admin SET db_version = ? WHERE (admin_id = 0)", (db_version,))

                    self.c.execute("ALTER TABLE users ADD COLUMN scheme INTEGER DEFAULT 0")
                    self.c.execute("UPDATE users SET scheme = 0")
                    self.conn.commit()
                    # update db_version
                elif current_db_ver == 2:
                    self.c.execute("ALTER TABLE users ADD COLUMN scheme INTEGER DEFAULT 0")
                    self.c.execute("UPDATE users SET scheme = 0")
                    self.c.execute("UPDATE admin SET db_version = ? WHERE (admin_id = 0)", (db_version,))
                    self.conn.commit()
                elif current_db_ver == 3:
                    self.c.execute("ALTER TABLE completions ADD COLUMN lang_id INTEGER DEFAULT 1")
                    self.c.execute("UPDATE admin SET db_version = ? WHERE (admin_id = 0)", (db_version,))
                    self.conn.commit()
                """

                """
                    #this was already commented out
                    self.c.execute("UPDATE users SET username = ? WHERE (ROWID=?)", ("Guest", 1))
                    self.c.execute("SELECT username FROM users WHERE (ROWID=?)", (1,))
                    self.conn.commit()
                    row = self.c.fetchone()
                    name = row[0]
                    print("Guest username set to: %s" % name)
                """
                """
                if 0 < current_db_ver < 4:
                    print("Database version updated from %d to %d." % (current_db_ver, db_version))
                """

    def unset_autologin(self):
        if self.db_connected:
            self.c.execute("UPDATE admin SET autologin_userid = 0, autologin = 0 WHERE (admin_id = 0)")
            self.conn.commit()

    def set_autologin(self, userid):
        if self.db_connected:
            self.c.execute("UPDATE admin SET autologin_userid = ?, autologin = 1 WHERE (admin_id = 0)", (userid,))
            self.conn.commit()

    def get_autologin(self):
        if self.db_connected:
            self.c.execute("SELECT autologin_userid, autologin FROM admin WHERE (admin_id = 0)")
            self.conn.commit()
            row = self.c.fetchone()
            if row[1] == 1:
                return row
            else:
                return None

    def admin_exists(self):
        if self.db_connected:
            self.c.execute("SELECT admin_name, admin_pass FROM admin WHERE (admin_id = 0)")
            self.conn.commit()
            row = self.c.fetchone()
            if row[0] == "" and row[1] == "":
                return False
            else:
                return True

    def get_login_defs(self):
        if self.db_connected:
            self.c.execute("SELECT default_lang, login_screen_defaults FROM admin WHERE (admin_id = 0)")
            self.conn.commit()
            row = self.c.fetchone()
            return row

    def get_lang(self):
        if self.db_connected:
            self.c.execute("SELECT default_lang FROM admin WHERE (admin_id = 0)")
            self.conn.commit()
            row = self.c.fetchone()
            return row[0]

    def set_lang(self, lang):
        # default_lang
        if self.db_connected:
            self.c.execute("UPDATE admin SET default_lang = ? WHERE (admin_id = 0)", (lang,))
            self.conn.commit()

    def add_admin_name(self, admin_name, password):
        if self.db_connected:
            self.c.execute("SELECT admin_name, admin_pass FROM admin WHERE (admin_id = 0)")
            self.conn.commit()
            row = self.c.fetchone()
            if row[0] == "" and row[1] == "":
                m = hashlib.md5()
                m.update(password.encode("utf-8"))
                md5_password = m.hexdigest()
                self.c.execute("UPDATE admin SET admin_name = ?, admin_pass = ? WHERE (admin_id = 0)",
                               (admin_name, md5_password))
                self.conn.commit()
                return 0  # "Admin's password has been updated"
            else:
                return -1  # "ERROR: This operation is not allowed at this point"
        return ""

    def update_admin_password(self, prev_pass, new_pass):
        if self.db_connected:
            m = hashlib.md5()
            m.update(prev_pass.encode("utf-8"))
            md5prev_password = m.hexdigest()
            self.c.execute("SELECT admin_name FROM admin WHERE (admin_pass = ?)", (md5prev_password,))
            self.conn.commit()
            count = self.c.fetchone()
            if count is None:
                return -1  # "Previous password doesn't seem to be in the database"
            else:
                m2 = hashlib.md5()
                m2.update(new_pass.encode("utf-8"))
                md5new_password = m2.hexdigest()
                self.c.execute("UPDATE admin SET admin_pass = ? WHERE (admin_pass = ?)",
                               (md5new_password, md5prev_password))
                self.conn.commit()
                return 0  # "Admin's password has been updated"
        return ""

    """
    self.c.execute("CREATE TABLE admin (admin_id INTEGER KEY, admin_name TEXT, admin_pass TEXT, default_lang TEXT, login_screen_defaults TEXT)")
    #self.c.execute("INSERT INTO admin VALUES (?, ?, ?, ?, ?)", (admin_id, admin_name, admin_pass, default_lang, login_screen_defaults))
    self.c.execute("INSERT INTO admin VALUES (?, ?, ?, ?, ?)", (0, "", "", "en_gb", "01011"))
    """

    def update_defaults(self, defs):
        if self.db_connected:
            self.c.execute("UPDATE admin SET login_screen_defaults = ? WHERE (admin_id = 0)", (defs,))
            self.conn.commit()

    def get_now(self):
        return str(datetime.datetime.now())[:19]

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbname)
            self.c = self.conn.cursor()
            self.db_connected = True
        except:
            self.db_connected = False

    def update_cursor(self, userid, gameid, lastlvl):
        if self.db_connected:
            self.c.execute("SELECT count(*) FROM levelcursors WHERE (userid = ? AND gameid = ?)", (userid, gameid))
            self.conn.commit()
            count = self.c.fetchone()
            if count[0] == 0:
                self.c.execute("INSERT INTO levelcursors VALUES (?, ?, ?)", (userid, gameid, lastlvl))
            else:
                self.c.execute("UPDATE levelcursors SET lastlvl = ?  WHERE (userid=? AND gameid = ?)",
                               (lastlvl, userid, gameid))
            self.conn.commit()

    def get_age(self):
        if self.mainloop.config.user_age_group < 7:
            return self.mainloop.config.user_age_group
        else:
            return self.mainloop.config.max_age

    def get_lang_id(self):
        if self.mainloop.m is not None:
            if self.mainloop.m.lang_activity:
                return self.mainloop.lang.lang_id
            else:
                return 0
        else:
            return self.mainloop.lang.lang_id

    def db_fix(self):
        #self.c.execute("SELECT num_completed FROM completions WHERE (gameid = ?)", (26,))
        #self.conn.commit()
        #count = self.c.fetchone()
        self.c.execute("DELETE FROM completions WHERE (gameid = ?)", (26,))
        self.conn.commit()

    def update_completion(self, userid, gameid, lvl):
        if self.db_connected:
            age = self.get_age()
            lng = self.get_lang_id()
            self.c.execute(
                "SELECT num_completed FROM completions WHERE (userid = ? AND gameid = ? AND lvl_completed = ? AND lang_id = ? AND age = ?)",
                (userid, gameid, lvl, lng, age))
            self.conn.commit()
            count = self.c.fetchone()

            if count is None:
                self.c.execute("INSERT INTO completions VALUES (?, ?, ?, ?, ?, ?)",
                               (userid, gameid, lvl, lng, 1, age))
            else:
                self.c.execute(
                    "UPDATE completions SET num_completed = ?  WHERE (userid = ? AND gameid = ? AND lang_id = ? AND lvl_completed = ? AND age = ?)",
                    (count[0] + 1, userid, gameid, lng, lvl, age))
            self.conn.commit()

    def query_completion(self, userid, gameid, lvl):
        if self.db_connected:
            age = self.get_age()
            lng = self.get_lang_id()
            self.c.execute(
                "SELECT num_completed FROM completions WHERE (userid = ? AND gameid = ? AND lang_id = ? AND lvl_completed = ? AND age = ?)",
                (userid, gameid, lng, lvl, age))
            self.conn.commit()
            count = self.c.fetchone()
            if count is None:
                return 0
            else:
                return count[0]

    def get_completion_count(self, userid):
        if self.db_connected:
            self.c.execute("SELECT count(*) FROM completions WHERE userid=?", (userid,))
            self.conn.commit()
            count = self.c.fetchone()
            if count is None:
                return 0
            else:
                return count[0]

    def completion_book(self, userid, offset=0):
        if self.db_connected:
            self.c.execute(
                "SELECT gameid, lvl_completed, lang_id, num_completed, age FROM completions WHERE (userid = ?) LIMIT 10 OFFSET ?",
                (userid, offset))
            self.conn.commit()
            temp = []
            for each in self.c:
                temp.append(each)
            return temp

    def load_all_cursors(self, userid):
        if self.db_connected:
            self.c.execute("SELECT * FROM levelcursors WHERE (userid = ?)", (userid,))
            self.conn.commit()
            temp = dict()
            for each in self.c:
                temp[each[1]] = each[2]
            return temp

    def load_usernames(self):
        if self.db_connected:
            self.c.execute("SELECT username FROM users")
            self.conn.commit()
            temp = []
            for each in self.c:
                temp.append(each[0])
            return temp

    def get_user_id(self, username):
        if self.db_connected:
            self.c.execute("SELECT ROWID FROM users WHERE username = ?", (username,))
            self.conn.commit()
            row = self.c.fetchone()
            if row is not None:
                return row[0]
        return None

    def get_user_score(self, userid):
        if self.db_connected:
            self.c.execute("SELECT score FROM users WHERE ROWID = ?", (userid,))
            self.conn.commit()
            row = self.c.fetchone()
            if row is not None:
                return row[0]
        return None

    def increase_score(self, userid, points):
        if self.db_connected:
            prev_score = self.get_user_score(userid)
            if prev_score is not None:
                if points > 0:
                    new_score = prev_score + points
                    self.c.execute("UPDATE users SET score = ? WHERE (ROWID=?)", (new_score, userid))
                    self.conn.commit()
                    return new_score
                else:
                    return prev_score
        return None

    def change_username(self, prev_name, new_name):
        if self.db_connected:
            uid = self.get_user_id(prev_name)
            # check if new username is not taken
            uid_new = self.get_user_id(new_name)
            if uid_new is None and uid is not None:
                self.c.execute("UPDATE users SET username = ? WHERE (ROWID=?)", (new_name, uid))
                self.conn.commit()

    def load_user_details(self, username):
        if self.db_connected:
            self.c.execute("SELECT username, date_added, last_login, score FROM users WHERE username = ?", (username,))
            self.conn.commit()
            count = self.c.fetchone()
            return count

    def add_user(self, username, password, lang, sounds, espeak, screenw, screenh):
        if self.db_connected:
            self.c.execute("SELECT count(*) FROM users WHERE username=?", (username,))
            self.conn.commit()
            count = self.c.fetchone()
            m = hashlib.md5()
            m.update(password.encode("utf-8"))
            md5password = m.hexdigest()
            if count[0] == 0:
                self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                username, md5password, self.get_now(), "", lang, sounds, espeak, screenw, screenh, 0, 0, 0))
                self.conn.commit()
                return 0  # "%s added" % username
            else:
                return -1  # "This user name already exists, please choose a different one"
        return ""

    def del_user(self, username):
        # check if user exists + get user id
        if self.db_connected:
            self.c.execute("SELECT count(*) FROM users")
            self.conn.commit()
            count = self.c.fetchall()
            if count is not None and count[0][0] > 1:
                self.c.execute("SELECT ROWID FROM users WHERE username=?", (username,))
                self.conn.commit()
                row = self.c.fetchone()
                if row is not None:
                    userid = row[0]
                    self.c.execute("DELETE FROM levelcursors WHERE userid = ?", (userid,))
                    self.c.execute("DELETE FROM completions WHERE userid = ?", (userid,))
                    self.c.execute("DELETE FROM users WHERE username = ?", (username,))
                    self.conn.commit()
                    return 0  # "%s deleted from database." % username
        return -1

    def save_user_settings(self, lang, sounds, espeak, screenw, screenh, scheme):
        if self.db_connected:
            self.c.execute(
                "UPDATE users SET lang = ?, sounds = ?, espeak = ?, screenw = ?, screenh = ?, scheme = ? WHERE (ROWID=?)",
                (lang, sounds, espeak, screenw, screenh, scheme, self.userid))
            self.conn.commit()

    def save_user_lang(self, lang):
        if self.db_connected:
            self.c.execute("UPDATE users SET lang = ? WHERE (ROWID=?)", (lang, self.userid))
            self.conn.commit()

    def load_user_settings(self, userid):
        if self.db_connected:
            self.c.execute("SELECT lang, sounds, espeak, screenw, screenh, scheme FROM users WHERE (ROWID=?)",
                           (self.userid,))
            self.conn.commit()
            row = self.c.fetchone()
            return row

    def update_age_group(self, username, age_group):
        if self.db_connected:
            # print("updating age_group for user %s to %d" % (username, age_group))
            self.c.execute("UPDATE users SET age_group = ? WHERE (username=?)", (age_group, username))
            self.conn.commit()

    def get_age_group(self, username="", userid=-1):
        if self.db_connected:
            if username != "":
                self.c.execute("SELECT age_group FROM users WHERE (username=?)", (username,))
            else:
                self.c.execute("SELECT age_group FROM users WHERE (ROWID=?)", (userid,))
            self.conn.commit()

            row = self.c.fetchone()
            if row is None:
                return None
            else:
                return row[0]

    def update_user(self, prev_username, prev_password, new_username, new_password):
        if self.db_connected:
            m = hashlib.md5()
            m.update(prev_password.encode("utf-8"))
            md5prev_password = m.hexdigest()
            self.c.execute("SELECT count(*) FROM users WHERE (username=? AND password=?)",
                           (prev_username, md5prev_password))
            self.conn.commit()
            count = self.c.fetchone()
            if count[0] == 0:
                return -2  # "Nothing to update..."
            else:
                self.c.execute("SELECT count(*) FROM users WHERE username=?", (new_username,))
                self.conn.commit()
                count = self.c.fetchone()
                if count[0] == 0:
                    m = hashlib.md5()
                    m.update(new_password.encode("utf-8"))
                    md5new_password = m.hexdigest()
                    self.c.execute("UPDATE users SET username = ? , password = ? WHERE (username=? AND password=?)",
                                   (new_username, md5new_password, prev_username, md5prev_password))
                    self.conn.commit()
                    if prev_username != new_username:
                        return 0  # "%s, your name was updated to %s" % (prev_username, new_username)
                    if prev_password != new_password:
                        return 1  # "%s, Your password has been updated" % new_username
                else:
                    return -1  # "This username already exists, please choose a different one"

        return ""

    def login_user(self, username, password):
        if self.db_connected:
            m = hashlib.md5()
            m.update(password.encode("utf-8"))
            md5password = m.hexdigest()
            self.c.execute("SELECT ROWID, username FROM users WHERE username=? AND password=?", (username, md5password))
            self.conn.commit()
            a = self.c.fetchone()
            if a is not None:
                self.userid = a[0]
                self.username = a[1]
                self.c.execute("UPDATE users SET last_login = ? WHERE (ROWID=?)", (self.get_now(), self.userid))
                self.conn.commit()
                return 0  # "Hello %s! You are logged in." % a[1] #(a[1],a[0])
            else:
                self.userid = -1
                return -1  # "This username and password combination doesn't exist."
        return ""

    def login_auto(self, userid):
        if self.db_connected:
            self.c.execute("SELECT ROWID, username FROM users WHERE ROWID=?", (userid,))
            self.conn.commit()
            a = self.c.fetchone()
            if a is not None:
                self.userid = a[0]
                self.username = a[1]
                self.c.execute("UPDATE users SET last_login = ? WHERE (ROWID=?)", (self.get_now(), self.userid))
                self.conn.commit()
                return 0  # "Hello %s! You are logged in." % a[1] #(a[1],a[0])
            else:
                self.userid = -1
                return -1  # "This username doesn't exist."
        return ""

    def login_user_no_pass(self, username):
        if self.db_connected:
            self.c.execute("SELECT ROWID, username FROM users WHERE username=?", (username,))
            self.conn.commit()
            a = self.c.fetchone()
            if a is not None:
                self.userid = a[0]
                self.username = a[1]
                self.c.execute("UPDATE users SET last_login = ? WHERE (ROWID=?)", (self.get_now(), self.userid))
                self.conn.commit()
                return 0  # "Hello %s! You are logged in." % a[1] #(a[1],a[0])
            else:
                self.userid = -1
                return -1  # "This username doesn't exist."
        return ""

    def login_admin(self, username, password):
        if self.db_connected:
            m = hashlib.md5()
            m.update(password.encode("utf-8"))
            md5password = m.hexdigest()
            self.c.execute("SELECT ROWID, admin_name FROM admin WHERE admin_name=? AND admin_pass=?",
                           (username, md5password))
            self.conn.commit()
            a = self.c.fetchone()
            if a is not None:
                self.userid = -2
                return 0  # "You are logged in."
            else:
                self.userid = -1
                return -1  # "This username and password combination doesn't exist."
        return -2

    def printlvls(self):
        if self.db_connected:
            self.c.execute("SELECT * FROM levelcursors")
            self.conn.commit()
            a = self.c.fetchall()
            for each in a:
                print(each)

    def printcompl(self):
        if self.db_connected:
            self.c.execute("SELECT * FROM completions")
            self.conn.commit()
            a = self.c.fetchall()
            for each in a:
                print(each)

    def print_db(self):
        if self.db_connected:
            self.c.execute("SELECT ROWID, username, password FROM users")
            self.conn.commit()
            a = self.c.fetchall()
            for each in a:
                print(each)

    def close(self):
        if self.db_connected:
            self.conn.close()
            self.db_connected = False
