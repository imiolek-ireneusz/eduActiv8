# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d

d["local_kbrd"] = "Ελληνικά γράμματα"
numbers = ['ένα', 'δύο', 'τρία', 'τέσσερα', 'πέντε', 'έξι', 'επτά', 'οκτώ', 'εννέα', 'δέκα', 'έντεκα', 'δώδεκα',
           'δεκατρία', 'δεκατέσσερα', 'δεκαπέντε', 'δεκαέξι', 'δεκαεπτά', 'δεκαοκτώ', 'δεκαεννέα', 'είκοσι',
           'είκοσι ένα', 'είκοσι δύο', 'είκοσι τρία', 'είκοσι τέσσερα', 'είκοσι πέντε', 'είκοσι έξι', 'είκοσι επτά',
           'είκοσι οκτώ', 'είκοσι εννέα']
numbers2090 = ['είκοσι', 'τριάντα', 'σαράντα', 'πενήντα', 'εξήντα', 'εβδομήντα', 'ογδόντα', 'ενενήντα']

dp['abc_flashcards_word_sequence'] = ['Άλογο', 'Βάρκα', 'Γάτα', 'Δέντρο', 'Ελέφαντας', 'Ζέβρα', 'Ήλιος', 'Θάμνος',
                                      'Ιπποπόταμος', 'Καμηλοπάρδαλη', 'Λουλούδια', 'Μήλο', 'Ντομάτα', 'Ξυλόφωνο',
                                      'Ομπρέλα', 'Πάπια', 'Ρούχα', 'Σπίτι', 'Τσαγιέρα', 'Ύπνος', 'Φορτηγό', 'Χιμπατζής',
                                      'Ψάρι', 'Ώρα']
d['abc_flashcards_word_sequence'] = ['<1>Ά<2>λογο', '<1>Β<2>άρκα', '<1>Γ<2>άτα', '<1>Δ<2>έντρο',
                                     '<1>Ε<2>λ<1>έ<2>φαντας', '<1>Ζ<2>έβρα', '<1>Ή<2>λιος', '<1>Θ<2>άμνος',
                                     '<1>Ι<2>πποπόταμος', '<1>Κ<2>αμηλοπάρδαλη', '<1>Λ<2>ου<1>λ<2>ούδια', '<1>Μ<2>ήλο',
                                     '<1>Ν<2>τομάτα', '<1>Ξ<2>υλόφωνο', '<1>Ο<2>μπρέλα', '<1>Π<2>ά<1>π<2>ια',
                                     '<1>Ρ<2>ούχα', '<1>Σ<2>πίτι', '<1>Τ<2>σαγιέρα', '<1>Ύ<2>πνος', '<1>Φ<2>ορτηγό',
                                     '<1>Χ<2>ιμπατζής', '<1>Ψ<2>άρι', '<1>Ώ<2>ρα']

d['abc_flashcards_frame_sequence'] = [45, 1, 2, 31, 4, 25, 18, 46, 47, 30, 36, 42, 33, 23, 20, 3, 48, 7, 19, 49, 50, 37,
                                      5, 51]

# alphabet gr
alphabet_lc = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ',
               'χ', 'ψ', 'ω']
alphabet_uc = ['Α', 'Β', 'Γ', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ξ', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ',
               'Χ', 'Ψ', 'Ω']
# correction of eSpeak pronounciation of single letters if needed
letter_names = []

accents_lc = ['-', 'ς', 'ά', 'έ', 'ή', 'ί', 'ϊ', 'ό', 'ύ', 'ώ']
accents_uc = ['Ά', 'Έ', 'Ή', 'Ί', 'Ϊ', 'Ό', 'Ύ', 'Ώ']


def n2txt(n, twoliner=False):
    "takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."
    if 0 < n < 30:
        return numbers[n - 1]
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m == 0:
            return tens
        elif m > 0:
            ones = numbers[m - 1]
            if twoliner:
                return [tens, ones]
            else:
                return tens + " " + ones

    elif n == 0:
        return "μηδέν"
    elif n == 100:
        return "εκατό"
    return ""


hrs = ['μία', 'δύο', 'τρεις', 'τέσσερις', 'πέντε', 'έξι', 'επτά', 'οκτώ', 'εννέα', 'δέκα', 'έντεκα', 'δώδεκα']


def time2str(h, m):
    'takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55'
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return "%s ακριβώς" % hrs[h - 1]
    elif m == 1:
        return "%s και ένα λεπτό" % hrs[h - 1]
    elif m == 15:
        return "%s και τέταρτο" % hrs[h - 1]
    elif m == 30:
        return "%s και μισή" % hrs[h - 1]
    elif m == 45:
        return "%s παρά τέταρτο" % hrs[h - 1]
    elif m == 59:
        return "%s παρά ένα λεπτό" % hrs[h - 1]
    elif m < 30:
        return "%s και %s" % (hrs[h - 1], n2txt(m))
    elif m > 30:
        return "%s παρά %s" % (hrs[h - 1], n2txt(60 - m))
    return ""


# write a fraction in words
numerators = ['ένα', 'δύο', 'τρία', 'τέσσερα', 'πέντε', 'έξι', 'επτά', 'οκτώ', 'εννέα', 'δέκα', 'έντεκα', 'δώδεκα']
d_singular = ['', 'δεύτερο', 'τρίτο', 'τέταρτο', 'πέμπτο', 'έκτο', 'έβδομο', 'όγδοο', 'ένατο', 'δέκατο', 'ενδέκατο', 'δωδέκατο']
d_plural = ['', 'δεύτερα', 'τρίτα', 'τέταρτα', 'πέμπτα', 'έκτα', 'έβδομα', 'όγδοα', 'ένατα', 'δέκατα', 'ενδέκατα', 'δωδέκατα']

def fract2str(n, d):
    if n == 1:
        return numerators[0] + " " + d_singular[d-1]
    else:
        return numerators[n-1] + " " + d_plural[d-1]
