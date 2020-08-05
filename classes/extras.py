# -*- coding: utf-8 -*-

import pygame
import colorsys
import random
import sys
import math

fribidi_loaded = False
ar_reshaper_loaded = False
he_reverse = False

try:
    # import pyfribidi as fribidi
    import classes.rtl.ctfribidi as fribidi
    if fribidi.fb is not None:
        fribidi_loaded = True
        print("Using fribidi library.")
    else:
        fribidi_loaded = False
except:
    fribidi = None

if not fribidi_loaded:
    try:
        from classes.rtl.arabic_reshaper import ArabicReshaper
        # providing ligature support slows the loading time dramatically
        """
        configuration_init = {
            'delete_harakat': False,
            'support_ligatures': True,
            'RIAL SIGN': True,  # Replace ر ي ا ل with ﷼
        }

        configuration = {
            'delete_harakat': False,
            'support_ligatures': False,
            'RIAL SIGN': False,  # Replace ر ي ا ل with ﷼
        }
        """
        reshaper = ArabicReshaper()

        from classes.rtl.bidi.algorithm import get_display
        ar_reshaper_loaded = True
        he_reverse = True
        print("Using arabic_reshaper library.")
    except:
        ar_reshaper_loaded = False
        print("Unable to load arabic_reshaper.")

if not he_reverse:
    from classes.rtl.bidi.algorithm import get_display


def hsv_to_rgb(h, s, v):
    hsv = [h, s, v]
    hsv_clean = hsv
    for i in range(3):
        if hsv[i] <= 0:
            hsv_clean[i] = 0
        elif hsv[i] >= 255:
            hsv_clean[i] = 1
        else:
            hsv_clean[i] = float(hsv[i]) / 255.0
    rgb = colorsys.hsv_to_rgb(*hsv_clean)
    return [int(each * 255) for each in rgb]


def hsva_to_rgba(h, s, v, a):
    rgb = hsv_to_rgb(h, s, v)
    rgb.append(a)
    return rgb


def rgb_to_hsv(r, g, b, a=255):
    hsv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    hsv255 = [int(each * 255) for each in hsv]
    return hsv255


def hsl_to_rgb(h, s, l):
    hsl = [h, l, s]
    hsl_clean = hsl
    for i in range(3):
        if hsl[i] <= 0:
            hsl_clean[i] = 0
        elif hsl[i] >= 255:
            hsl_clean[i] = 1
        else:
            hsl_clean[i] = float(hsl[i]) / 255.0

    rgb = colorsys.hls_to_rgb(*hsl_clean)
    return [int(each * 255) for each in rgb]


def rgb_to_hsl(r, g, b, a=255):
    hsl = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    hsl255 = [int(each * 255) for each in hsl]
    hsl255 = [hsl255[0], hsl255[2], hsl255[1]]
    return hsl255


def unival(value):
    val = value
    if sys.version_info < (3, 0):
        try:
            if not isinstance(value, unicode):
                val = unicode(value, "utf-8")
        except UnicodeDecodeError:
            val = value
        except TypeError:
            val = value
    else:
        val = value
    return val


def is_rtl(s, alpha):
    if sys.version_info < (3, 0):
        alpha = unival(alpha)
    if s[0] in alpha and s[-1] in alpha:
        return True
    return False


def he_rtl_man(s):
    st = unival(s)
    return get_display(st)


def ar_rtl(s):
    st = unival(s)
    if fribidi_loaded:
        return fribidi.log2vis(st)
    elif ar_reshaper_loaded:
        reshaped_text = reshaper.reshape(st)
        return get_display(reshaped_text)
    else:
        return st


def reverse(s, lng):
    if sys.version_info < (3, 0):
        if not isinstance(s, unicode):
            s = s.decode('utf-8')
    if lng == "ar":
        return ar_rtl(s)
    elif lng == "he":
        if fribidi_loaded:
            st = unival(s)
            return fribidi.log2vis(st)
        else:
            return he_rtl_man(s)


def rr2(from1, to1, from2, to2, step=1):
    x = random.choice([-1, 1])
    if x == -1:
        a = random.randrange(from1, to1, step)
    else:
        a = random.randrange(from2, to2, step)
    return a


def rr3(from1, to2, center, exclusion_zone, step=1):
    to1 = center - exclusion_zone
    from2 = center + exclusion_zone
    if from1 < to1 < from2 < to2:
        return rr2(from1, to1, from2, to2, step)


def rand_safe_curve(point, width, height):
    x_space = width - point[0]
    y_space = height - point[1]

    if x_space > point[0]:
        max_x = point[0]
    else:
        max_x = x_space

    if y_space > point[1]:
        max_y = point[1]
    else:
        max_y = y_space

    x = rr3(point[0] - max_x, point[0] + max_x, point[0], max_x // 2)
    y = rr3(point[1] - max_y, point[1] + max_y, point[1], max_y // 2)
    return [x, y]


def sqr(num):
    return num * num


def cube(num):
    return num * num * num


# points = [[200, 400], [300, 250], [450, 500], [500, 475]]
# points = [[beginning], [beginning_midifier], [end],[end_midifier]]
# points as Vector2
def DrawBezier(points):
    bezier_points = []
    t = 0.0
    while t < 1.02:  # Increment through values of t (between 0 and 1)
        # Append the point on the curve for the current value of t to the list of Bezier points
        bezier_points.append(GetBezierPoint(points, t))
        t += 0.02
    return bezier_points


def GetBezierPoint(points, t):
    p1 = points[0] * cube(1.0 - t)
    p2 = points[1] * (3 * sqr(1.0 - t) * t)
    p3 = points[2] * cube(t)
    p4 = points[3] * (3 * (1.0 - t) * sqr(t))
    return p1 + p2 + p3 + p4


def inversions(p):
    lp = len(p)
    total_inversions = 0
    for i in range(lp):  # pick each number from left to right
        for j in range(i, lp):  # and check it against any numbers to the right
            if p[i] > p[j]:  # if any of them are greater than the number itself
                total_inversions += 1
    return total_inversions


def get_word_list(di):
    'used in touch typing program'
    wl = []
    for i in range(8):
        tmp = set()
        while len(tmp) < 10:
            word = di[i][random.randrange(1, di[i][0])]
            tmp.add(word)
        wl.append(list(tmp))
    return wl


def first_upper(text):
    # word_list[i][k][0]) + word_list[i][k][1:]
    if sys.version_info < (3, 0):
        utf = unicode(text, "utf-8")
        # utf = text
        text = utf[0].upper() + utf[1:]
        text = text.encode("utf-8")
    else:
        text = text[0].upper() + text[1:]

    return text


def word_typing_course(word_list):
    'used in touch typing program to build a list of words to retype'
    # repeats =[3,4,5,6,7,8,9,10]
    repeats = [4, 4, 3, 3, 2, 2, 2, 2]
    # repeats = [1,1,1,1,1,1,1,1]
    levels = []
    for i in range(8):
        # tmp = []
        words_line_1 = ""
        words_line_2 = ""
        for k in range(10):
            for j in range(repeats[i]):
                if k < 5:
                    words_line_1 += " " + word_list[i][k]
                else:
                    if j == 0:
                        words_line_2 += " " + first_upper(word_list[i][k])
                    else:
                        words_line_2 += " " + word_list[i][k]
            if 0 <= k < 4:
                words_line_1 += ","
            elif k == 4:
                words_line_1 += "."
            elif 5 <= k < 10:
                words_line_2 += "."
        levels.append([[1, 1], [words_line_1, words_line_2]])
    return levels


def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse

    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """

    if rect is None:
        rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom

    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h,
        float(b[3] - a[3]) / h
    )

    if vertical:
        for line in range(y1, y2):
            color = (
                int(min(max(a[0] + (rate[0] * (line - y1)), 0), 255)),
                int(min(max(a[1] + (rate[1] * (line - y1)), 0), 255)),
                int(min(max(a[2] + (rate[2] * (line - y1)), 0), 255)),
                int(min(max(a[3] + (rate[3] * (line - y1)), 0), 255))
            )
            pygame.draw.line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                int(min(max(a[0] + (rate[0] * (col - x1)), 0), 255)),
                int(min(max(a[1] + (rate[1] * (col - x1)), 0), 255)),
                int(min(max(a[2] + (rate[2] * (col - x1)), 0), 255)),
                int(min(max(a[3] + (rate[3] * (col - x1)), 0), 255))
            )
            pygame.draw.line(surface, color, (col, y1), (col, y2))


def _rotate_point(point, centre, angle):
    """ Rotates a point around another point by a number of degrees (anticlockwise)
    :param point: point coordinates - 2 element list
    :param centre: centre of rotation coordinates - 2 element list
    :param angle: rotate by the given angle
    :return: a rotated point - 2 element list
    """
    # convert angle to radians
    angle = math.radians(angle)

    pt = [0, 0]

    # translate the rotation point to the origin
    pt[0] = point[0] - centre[0]
    pt[1] = point[1] - centre[1]

    # calculate the new coordinates after rotation
    res = [int(round(pt[0] * math.cos(angle) - pt[1] * math.sin(angle))),
           int(round(pt[1] * math.cos(angle) + pt[0] * math.sin(angle)))]

    # cancel translation
    res[0] += centre[0]
    res[1] += centre[1]

    return res


def rotate_points(points, centre, angle):
    """ Rotates a list of points around another point by a number of degrees (anticlockwise)
    :param points: a list of 2 element lists containing initial coordinates of individual points
    :param centre: a list of 2 elements containing a coordinates of the centre of rotation
    :param angle: the angle by which the points are to be rotated in degrees
    :return: a list of rotated points about a centre point
    """
    rotated_points = []
    for point in points:
        rotated_points.append(_rotate_point(point, centre, angle))

    return rotated_points
