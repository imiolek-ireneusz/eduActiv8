# -*- coding: utf-8 -*-

from __future__ import with_statement

import gettext
import locale
import os
import sys

from classes.extras import reverse
from classes.extras import unival


# game003.py holds the GUI for language switching for game screen and loginscreen for the login/admin screen

class Language:
    def __init__(self, configo, path):
        #lib_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.locale_dir = unival(os.path.join(path, 'locale/'))
        if 'LC_MESSAGES' in vars(locale):
            # linux
            locale.setlocale(locale.LC_MESSAGES, '')
        else:
            # windows
            locale.setlocale(locale.LC_ALL, '')
        # locale.setlocale(locale.LC_MESSAGES, '') # use user's preferred locale

        self.config = configo
        self.alphabet_26 = ["en_GB", "en_US", "pt_PT"]
        self.def_imported = False
        self.trans = dict()
        self.lang_titles = self.config.lang_titles
        self.all_lng = self.config.all_lng
        self.ok_lng = self.config.ok_lng

    def load_language(self, lang_code=None):
        if lang_code is None:
            if self.config.settings["lang"] not in self.all_lng:
                self.config.reset_settings()

            self.lang = self.config.settings["lang"]
        else:
            if lang_code not in self.all_lng:
                self.lang = 'en_GB'
            else:
                self.lang = lang_code

        self.get_lang_attr()

    def _n(self, word, count):
        return self.trans[self.lang].ngettext(word, word, count)

    def get_lang_attr(self):
        filename = os.path.join(self.locale_dir, self.lang, "LC_MESSAGES", "eduactiv8.mo")
        # filename = "locale/%s/LC_MESSAGES/eduactiv8.mo" % self.lang
        self.trans[self.lang] = gettext.GNUTranslations(open(filename, "rb"))
        try:
            # print("Opening message file %s for locale %s" % (filename, self.lang) )
            self.trans[self.lang] = gettext.GNUTranslations(open(filename, "rb"))
        except IOError:
            print("Locale not found. Using default messages")
            self.trans[self.lang] = gettext.NullTranslations()

        self.trans[self.lang].install()

        import i18n.custom.default
        self.oi18n = i18n.custom.default.I18n()
        self.kbrd = None
        self.ltr_text = True
        self.ltr_numbers = True
        self.ltr_math = True
        self.has_uc = True
        self.has_cursive = True
        font_variant = 0
        self.ico_suffix = ""
        self.lang_id = 0  # used to identify the language in database - do not reorganize numbers when adding new language
        if self.lang == 'en_US':
            import i18n.custom.en_us
            import i18n.custom.word_lists.en_us_di
            import i18n.custom.kbrd.en_us
            import i18n.custom.kbrd.en_course
            # self.voice = ["-s 170","-a 100","-p 80","-ven-us+m1"]
            self.voice = ["-ven-us+m1"]
            self.di = i18n.custom.word_lists.en_us_di.di
            self.lang_file = i18n.custom.en_us
            self.kbrd = i18n.custom.kbrd.en_us
            self.kbrd_course_mod = i18n.custom.kbrd.en_course
            self.lang_id = 1
        elif self.lang == 'pl':
            import i18n.custom.pl
            import i18n.custom.word_lists.pl_di
            import i18n.custom.kbrd.pl
            import i18n.custom.kbrd.pl_course
            # self.voice = ["-s 160","-a 100","-p 80","-vpl+m1"] #"-g 5",
            self.voice = ["-vpl+m1"]
            self.di = i18n.custom.word_lists.pl_di.di
            self.lang_file = i18n.custom.pl
            self.kbrd = i18n.custom.kbrd.pl
            self.kbrd_course_mod = i18n.custom.kbrd.pl_course
            self.lang_id = 3
        elif self.lang == 'sr':
            import i18n.custom.sr
            import i18n.custom.word_lists.sr_di
            # self.voice = ["-s 160","-a 100","-p 80","-vpl+m1"] #"-g 5",
            self.voice = ["-vsr+m1"]
            self.di = i18n.custom.word_lists.sr_di.di
            self.lang_file = i18n.custom.sr
            self.lang_id = 19
            self.ico_suffix = "ru"
            self.has_cursive = False
            self.time2str_short = self.lang_file.time2str_short
        elif self.lang == 'ca':
            import i18n.custom.ca
            import i18n.custom.word_lists.ca_di
            self.voice = ["-vca+m1"]
            self.di = i18n.custom.word_lists.ca_di.di
            self.lang_file = i18n.custom.ca
            self.lang_id = 5
        elif self.lang == 'es_ES':
            import i18n.custom.es
            import i18n.custom.word_lists.es_di
            self.voice = ["-ves+m1"]
            self.di = i18n.custom.word_lists.es_di.di
            self.lang_file = i18n.custom.es
            self.lang_id = 8
        elif self.lang == 'pt_PT':
            import i18n.custom.pt
            import i18n.custom.word_lists.pt_di
            self.voice = ["-vpt-pt+m1"]
            self.di = i18n.custom.word_lists.pt_di.di
            self.lang_file = i18n.custom.pt
            self.lang_id = 9
        elif self.lang == 'fr':
            import i18n.custom.fr
            import i18n.custom.word_lists.fr_di
            import i18n.custom.kbrd.fr
            import i18n.custom.kbrd.fr_course
            self.voice = ["-vfr+m1"]
            self.di = i18n.custom.word_lists.fr_di.di
            self.lang_file = i18n.custom.fr
            self.kbrd = i18n.custom.kbrd.fr
            self.kbrd_course_mod = i18n.custom.kbrd.fr_course
            self.lang_id = 10
        elif self.lang == 'it':
            import i18n.custom.it
            import i18n.custom.word_lists.it_di
            self.voice = ["-vit+m1"]
            self.di = i18n.custom.word_lists.it_di.di
            self.lang_file = i18n.custom.it
            self.lang_id = 11
        elif self.lang == 'de':
            import i18n.custom.de
            import i18n.custom.word_lists.de_di
            import i18n.custom.kbrd.de
            import i18n.custom.kbrd.de_course
            self.voice = ["-vde+m1"]
            self.di = i18n.custom.word_lists.de_di.di
            self.lang_file = i18n.custom.de
            self.kbrd = i18n.custom.kbrd.de
            self.kbrd_course_mod = i18n.custom.kbrd.de_course
            self.lang_id = 12
        elif self.lang == 'ru':
            import i18n.custom.ru
            import i18n.custom.word_lists.ru_di
            import i18n.custom.kbrd.ru
            import i18n.custom.kbrd.ru_course
            # self.voice = ["-s 130","-a 100","-p 80","-vru+m1"]
            # self.voice = ["-vru+m1"] s 150 -vru
            self.voice = ["-s 150", "-vru"]
            self.di = i18n.custom.word_lists.ru_di.di
            self.lang_file = i18n.custom.ru
            self.kbrd = i18n.custom.kbrd.ru
            self.kbrd_course_mod = i18n.custom.kbrd.ru_course
            self.time2spk = self.lang_file.time2spk
            self.time2officialstr = self.lang_file.time2officialstr
            self.time2officialspk = self.lang_file.time2officialspk
            self.ico_suffix = "ru"
            self.lang_id = 13
        elif self.lang == 'uk':
            import i18n.custom.uk
            import i18n.custom.word_lists.uk_di
            import i18n.custom.kbrd.uk
            import i18n.custom.kbrd.uk_course
            self.voice = None
            self.di = i18n.custom.word_lists.uk_di.di
            self.lang_file = i18n.custom.uk
            self.kbrd = i18n.custom.kbrd.uk
            self.kbrd_course_mod = i18n.custom.kbrd.uk_course
            self.ico_suffix = "ru"
            self.lang_id = 14
        elif self.lang == 'fi':
            import i18n.custom.fi
            import i18n.custom.word_lists.fi_di
            self.voice = ["-vfi+m1"]
            self.di = i18n.custom.word_lists.fi_di.di
            self.lang_file = i18n.custom.fi
            self.lang_id = 15
        elif self.lang == 'el':  # Greek
            import i18n.custom.el
            import i18n.custom.word_lists.el_di
            import i18n.custom.kbrd.el
            import i18n.custom.kbrd.el_course
            self.voice = ["-vel+m1"]
            self.di = i18n.custom.word_lists.el_di.di
            self.lang_file = i18n.custom.el
            self.kbrd = i18n.custom.kbrd.el
            self.kbrd_course_mod = i18n.custom.kbrd.el_course
            self.ico_suffix = "el"
            self.lang_id = 16
        elif self.lang == 'he':  # Hebrew
            import i18n.custom.he
            import i18n.custom.word_lists.he_di
            self.voice = ["-ven+m1"]  # None
            self.di = i18n.custom.word_lists.he_di.di
            self.lang_file = i18n.custom.he
            self.time2spk = self.lang_file.time2spk
            self.ltr_text = False
            self.has_uc = False
            self.has_cursive = False
            self.alpha = i18n.custom.he.alpha
            self.n2spk = self.lang_file.n2spk
            # font_variant = 1
            self.ico_suffix = "he"
            self.lang_id = 17
        elif self.lang == 'lkt':
            import i18n.custom.lkt
            import i18n.custom.word_lists.lkt_di
            self.voice = None
            self.has_cursive = False
            self.di = i18n.custom.word_lists.lkt_di.di
            self.lang_file = i18n.custom.lkt
            # self.alpha = i18n.custom.cn.alpha
            # self.n2spk = self.lang_file.n2spk
            self.ico_suffix = ""
            self.lang_id = 20
        elif self.lang == 'te_ST':
            import i18n.custom.te_st
            import i18n.custom.word_lists.te_st_di
            self.voice = ["-ven+m1"]
            self.di = i18n.custom.word_lists.te_st_di.di
            self.lang_file = i18n.custom.te_st
            self.lang_id = 1
        else:  # self.lang == 'en_GB':
            import i18n.custom.en_gb
            import i18n.custom.word_lists.en_gb_di
            import i18n.custom.kbrd.en_gb
            import i18n.custom.kbrd.en_course
            self.voice = ["-ven+m1"]
            self.di = i18n.custom.word_lists.en_gb_di.di
            self.lang_file = i18n.custom.en_gb
            self.kbrd = i18n.custom.kbrd.en_gb
            self.kbrd_course_mod = i18n.custom.kbrd.en_course
            self.lang_id = 1

        #  languages that have not been translated are temporarily switched off
        """
        elif self.lang == 'sk':
            import i18n.custom.sk
            import i18n.custom.word_lists.sk_di
            # self.voice = ["-s 160","-a 100","-p 80","-vpl+m1"] #"-g 5",
            self.voice = ["-vsk+m1"]
            self.di = i18n.custom.word_lists.sk_di.di
            self.lang_file = i18n.custom.sk
            self.lang_id = 4
        elif self.lang == 'da':
            import i18n.custom.da
            import i18n.custom.word_lists.da_di
            self.voice = ["-vda+m1"]
            self.di = i18n.custom.word_lists.da_di.di
            self.lang_file = i18n.custom.da
            self.lang_id = 6
        elif self.lang == 'nl':
            import i18n.custom.nl
            import i18n.custom.word_lists.nl_di
            self.voice = ["-vnl+m1"]
            self.di = i18n.custom.word_lists.nl_di.di
            self.lang_file = i18n.custom.nl
            self.lang_id = 7
            
        elif self.lang == 'ar':  # Arabic
            import i18n.custom.ar
            import i18n.custom.word_lists.ar_di
            self.voice = None
            self.di = i18n.custom.word_lists.ar_di.di
            self.lang_file = i18n.custom.ar
            self.ltr_text = False
            self.has_uc = False
            self.has_cursive = False
            self.alpha = i18n.custom.ar.alpha
            self.n2spk = self.lang_file.n2spk
            self.ico_suffix = "ar"
            self.lang_id = 2
        elif self.lang == 'cn':
            import i18n.custom.cn
            import i18n.custom.word_lists.cn_di
            self.voice = None
            self.di = i18n.custom.word_lists.cn_di.di
            self.lang_file = i18n.custom.cn
            # self.alpha = i18n.custom.cn.alpha
            # self.n2spk = self.lang_file.n2spk
            self.ico_suffix = ""
            self.lang_id = 18
        """

        if self.lang in ["ar", "he"]:
            self.config.font_multiplier = 1.1
            self.config.font_line_height_adjustment = 1.5
            self.config.font_start_at_adjustment = 5
        else:
            self.config.font_multiplier = 1
            self.config.font_line_height_adjustment = 1
            self.config.font_start_at_adjustment = 0

        if self.kbrd is None:  # self.lang not in ["en_gb","en_us","pl","ru","el","uk","fr"]:
            import i18n.custom.kbrd.en_gb
            import i18n.custom.kbrd.en_course
            self.kbrd = i18n.custom.kbrd.en_gb
            self.kbrd_course_mod = i18n.custom.kbrd.en_course
        self.d = dict()
        self.b = dict()
        self.dp = dict()
        self.kbrd_course = self.kbrd_course_mod.course

        self.d.update(self.oi18n.d)
        self.d.update(self.lang_file.d)
        self.b.update(self.oi18n.b)
        self.numbers = self.lang_file.numbers
        self.numbers2090 = self.lang_file.numbers2090
        self.n2txt = self.lang_file.n2txt
        self.time2str = self.lang_file.time2str
        if self.lang in ["en_GB", "en_US", "pl"]:
            self.fract2str = self.lang_file.fract2str

        self.solid_names = self.oi18n.solid_names
        self.shape_names = self.oi18n.shape_names
        self.letter_names = self.lang_file.letter_names
        self.config.set_font_family(font_variant)
        if not self.ltr_text:
            for each_d in [self.d, self.b]:
                for key in each_d.keys():
                    if isinstance(each_d[key], list):
                        for index in range(len(each_d[key])):
                            if sys.version_info < (3, 0):
                                if isinstance(each_d[key][index], basestring):
                                    each_d[key][index] = reverse(each_d[key][index], self.alpha, self.lang)
                            else:
                                if isinstance(each_d[key][index], str):
                                    each_d[key][index] = reverse(each_d[key][index], self.alpha, self.lang)
                    else:
                        each_d[key] = reverse(each_d[key], self.alpha, self.lang)
            for each in [self.solid_names, self.shape_names]:
                for index in range(len(each)):
                    if sys.version_info < (3, 0):
                        if isinstance(each[index], basestring):
                            each[index] = reverse(each[index], self.alpha, self.lang)
                    else:
                        if isinstance(each[index], str):
                            each[index] = reverse(each[index], self.alpha, self.lang)

        self.dp.update(self.d)
        # if self.lang == 'ru' or self.lang == 'he':
        self.dp.update(self.lang_file.dp)
        if self.lang == "he":
            s = unival(self.d['abc_flashcards_word_sequence'][0])
            if len(s) > 0:
                if s[0] == unival("א"):
                    self.d['abc_flashcards_word_sequence'] = self.d['abc_flashcards_word_sequencer']

        self.alphabet_lc = self.lang_file.alphabet_lc
        self.alphabet_uc = self.lang_file.alphabet_uc
        self.accents_lc = self.lang_file.accents_lc
        self.accents_uc = self.lang_file.accents_uc
