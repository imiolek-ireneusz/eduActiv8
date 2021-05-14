# -*- coding: utf-8 -*-

# FAO Translators:
# First of all thank you for your interest in translating this game,
# I will be grateful if you could share it with the community -
# if possible please send it back to my email, and I'll add it to the next version.

# The translation does not have to be exact as long as it makes sense and fits in its location
# (if it doesn't I'll try to either make the font smaller or make the area wider - where possible).
# The colour names in other languages than English are already in smaller font.

from classes.extras import reverse
from classes.extras import unival

d = dict()
dp = dict()  # messages with pronunciation exceptions - this dictionary will override entries in a copy of d


def r(s):
    return reverse(s, "ar")

numbers = ['واحد', 'اثنان', 'ثلاثة', 'أربعة', 'خمسة', 'ستة', 'سبعة', 'ثمانية', 'تسعة', 'عشرة',
           'أحد عشر', 'اثنا عشر', 'ثلاثة عشر', 'أربعة عشر', 'خمسة عشر',
           'ستة عشر', 'سبعة عشر', 'ثمانية عشر', 'تسعة عشر', 'عشرون',
           'وَاحِد و عِشْرُونَ', 'اِثْنَان و عِشْرُونَ', 'ثَلَاثَة و عِشْرُونَ', 'أَرْبَعَة و عِشْرُونَ', 'خَمْسَة و عِشْرُونَ',
           'سِتَّة و عِشْرُونَ', 'سَبْعَة و عِشْرُونَ', 'ثَمَانِيَة و عِشْرُونَ', 'تِسْعَة و عِشْرُونَ']
numbers2090 = ['عِشْرُونَ', 'ثَلَاثُونَ', 'أَرْبَعُونَ', 'خَمْسُونَ', 'سِتُّونَ', 'سَبْعُونَ', 'ثَمَانُونَ', 'تِسْعُونَ']
numbers_m = numbers
numbers2090_m = numbers2090
numbers_f = ['وَاحِدَة', 'اِثْنَتَيْن', 'ثَلَاث', 'أَرْبَع', 'خَمْس', 'سِت', 'سَبْع', 'ثَمَان', 'تِسْع', 'عَشْر', 'إِحْدَى عَشْرَةَ', 'اِثْنَتَا عَشْرَةَ', 'اِثْنَتِي عَشْرَةَ', 'ثَلَاثَ عَشْرَةَ', 'أَرْبَعَ عَشْرَةَ', 'خَمْسَ عَشْرَةَ', 'سِتَّ عَشْرَةَ', 'سَبْعَ عَشْرَةَ', 'ثَمَانِيَ عَشْرَةَ', 'تِسْعَ عَشْرَةَ', 'عِشْرِيْن', 'إِحْدَى وَعِشْرُونَ', 'اِثْنَتَيْن وعِشْرِيْنَ', 'ثَلاَث وَعِشْرُونَ', 'أَرْبَع وَعِشْرُونَ', 'خَمْس وَعِشْرُونَ', 'سِتّ وَعِشْرُونَ', 'سَبْع وَعِشْرُونَ', 'ثَمَانٍ وَعِشْرُونَ', 'تِسْع وَعِشْرُونَ']
numbers2090_f = ['عِشْرُونَ', 'ثَلَاثُون', 'أَرْبَعُون', 'خَمْسُون', 'سِتُّون', 'سَبْعُون', 'ثَمَانُون', 'تِسْعُوْن']

# The following 2 lines are not to be translated but replaced with a sequence of words starting in each of the letters of your alphabet in order, best if these words have a corresponding picture in images/flashcard_images.jpg. The second line has the number of the image that the word describes.
# The images are numbered from left to bottom such that the top left is numbered 0, the last image is 73, if none of the available things have names that start with any of the letters we can add new pictures.
d['abc_flashcards_word_sequence'] = ['الفيل', 'بطة', 'تفاحة', 'ثعلب', 'جبنه', 'حصان', 'خبز', 'دولفين', 'ذهب', 'ريشة', 'زهور', 'سمك', 'شمس', 'صخرة', 'ضفدعة', 'طماطم', 'ظرف', 'عين', 'غزل',  'فراشة', 'قارب', 'كمان', 'ليل', 'منزل', 'نملة', 'هاتف', 'وحيد القرن', 'يتسلق']
d['abc_flashcards_frame_sequence'] = [4, 3, 42, 110, 57, 45, 35, 59, 108, 66, 36, 5, 18, 97, 105, 33, 109, 75, 24, 27, 1, 21, 54, 7, 0, 79, 106, 107]

dp['abc_flashcards_word_sequence'] = d['abc_flashcards_word_sequence']

d['abc_flashcards_word_sequencer'] = ["None"]

alphabet_ar_iso = [r('ا'), r('ب'), r('ت'), r('ث'), r('ج'), r('ح'), r('خ'), r('د'), r('ذ'), r('ر'), r('ز'), r('س'), r('ش'), r('ص'), r('ض'), r('ط'), r('ظ'), r('ع'), r('غ'), r('ف'), r('ق'), r('ك'), r('ل'), r('م'), r('ن'), r('ه'), r('و'), r('ي')]
alphabet_ar_ini = [r('ا'), r('بـ'), r('تـ'), r('ثـ'), r('جـ'), r('حـ'), r('خـ'), r('د'), r('ذ'), r('ر'), r('ز'), r('سـ'), r('شـ'), r('صـ'), r('ضـ'), r('طـ'), r('ظـ'), r('عـ'), r('غـ'), r('فـ'), r('قـ'), r('كـ'), r('لـ'), r('مـ'), r('نـ'), r('ھـ'), r('و'), r('يـ')]
alphabet_ar_mid = [r('ـا'), r('ـبـ'), r('ـتـ'), r('ـثـ'), r('ـجـ'), r('ـحـ'), r('ـخـ'), r('ـد'), r('ـذ'), r('ـر'), r('ـز'), r('ـسـ'), r('ـشـ'), r('ـصـ'), r('ـضـ'), r('ـطـ'), r('ـظـ'), r('ـعـ'), r('ـغـ'), r('ـفـ'), r('ـقـ'), r('ـكـ'), r('ـلـ'), r('ـمـ'), r('ـنـ'), r('ـھـ'), r('ـو'), r('ـيـ')]
alphabet_ar_end = [r('ـا'), r('ـب'), r('ـت'), r('ـث'), r('ـج'), r('ـح'), r('ـخ'), r('ـد'), r('ـذ'), r('ـر'), r('ـز'), r('ـس'), r('ـش'), r('ـص'), r('ـض'), r('ـط'), r('ـظ'), r('ـع'), r('ـغ'), r('ـف'), r('ـق'), r('ـك'), r('ـل'), r('ـم'), r('ـن'), r('ـه'), r('ـو'), r('ـي')]

alphabet_lc = alphabet_ar_iso

alphabet_uc = alphabet_lc
alpha = None

# correction of eSpeak pronunciation of single letters if needed
letter_names = []

accents_lc = ['-']
accents_uc = []

def n2txt(n, twoliner=False):
    """takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."""
    if 0 < n < 30:
        return r(numbers[n - 1])
    elif 30 <= n < 100:
        m = n % 10
        tens = r(numbers2090[(n // 10) - 2])
        if m == 0:
            return tens
        elif m > 0:
            ones = r(numbers[m - 1])
            return tens + unival(" و ") + ones

    elif n == 0:
        return r("صفر")
    elif n == 100:
        return r("مائة")
    else:
        return ""


def n2spk(n, twoliner=False):
    """takes a number from 1 - 99 and returns it back in a word form, ie: 63 returns 'sixty three'."""
    if 0 < n < 30:
        return unival(numbers[n - 1])
    elif 30 <= n < 100:
        m = n % 10
        tens = numbers2090[(n // 10) - 2]
        if m == 0:
            return unival(tens)
        elif m > 0:
            ones = numbers[m - 1]
            return unival(tens) + unival(" و ") + unival(ones)

    elif n == 0:
        return unival("صفر")
    elif n == 100:
        return unival("مائة")
    else:
        return ""


h_numbers = ['الواحدة', 'الثانية', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة', 'الثامنة', 'التاسعة', 'العاشرة', 'الحادية عشرة', 'الثانية عشرة']
m_numbers_3_10 = ['ثلاث', 'أربع', 'خمس', 'ست', 'سبع', 'ثمان', 'تسع', 'عشر']


def time2str(h, m):
    """takes 2 variables: h - hour, m - minute, returns time as a string, ie. five to seven - for 6:55"""
    if m > 30:
        if h == 12:
            h = 1
        else:
            h += 1
    if m == 0:
        return r("الساعة " + h_numbers[h-1])
    elif m == 1:
        return r("الساعة " + h_numbers[h-1] + " و دقيقة")
    elif m == 2:
        return r("الساعة " + h_numbers[h-1] + " و دقيقتان")
    elif 2 < m < 11:
        return r("الساعة " + h_numbers[h-1] + " و " + m_numbers_3_10[m - 1 - 2] + " دقائق")
    elif m == 15:
        return r("الساعة " + h_numbers[h-1] + " والربع")
    elif m == 20:
        return r("الساعة " + h_numbers[h - 1] + " والثلث")
    elif m == 30:
        return r("الساعة " + h_numbers[h-1] + " والنصف")
    elif m == 40:
        return r("الساعة " + h_numbers[h - 1] + " إلا الثلث")
    elif m == 45:
        return r("الساعة " + h_numbers[h-1] + " إلا الربع")
    elif m == 58:
        return r("الساعة " + h_numbers[h-1] + " إلا دقيقتان")
    elif m == 59:
        return r("الساعة " + h_numbers[h-1] + " إلا دقيقة")
    elif 49 < m < 58:
        return r("الساعة " + h_numbers[h-1] + " إلا " + m_numbers_3_10[60 - m - 1 - 2] + " دقائق")
    elif m < 30:
        return r("الساعة " + h_numbers[h-1] + " و " + numbers[m - 1] + " دقيقة")
    elif m > 30:
        return r("الساعة " + h_numbers[h-1] + " إلا " + numbers[60 - m - 1] + " دقيقة")
    return ""


# write a fraction in words
# numerators_en = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
# d_singular_en = ['', 'half', 'third', 'quarter', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
# d_plural_en = ['', 'halves', 'thirds', 'quarters', 'fifths', 'sixths', 'sevenths', 'eighths', 'ninths', 'tenths', 'elevenths', 'twelfths']

numerators = ['', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
d_singular = ['', 'نِصْف', 'ثُلْثْ', 'رُبْع', 'خُمْس', 'سُدْس', 'سُبْع', 'ثْمْن', 'تُسْع', 'عُشْر', 'eleventh', 'twelfth']
d_plural = ['', 'أَنْصَاف', 'أَثْلَاث', 'أَرْبَاع', 'أَخْمَاس', 'أَسْدَاس', 'أَسْبَاع', 'أَثْمَان', 'أَتْسَاع', 'أَعْشَار', 'elevenths', 'twelfths']


def fract2str(n, d):
    if n == 1:
        return r(numerators[0] + " " + d_singular[d-1])
    else:
        return r(numerators[n-1] + " " + d_plural[d-1])
