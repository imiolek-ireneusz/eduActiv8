# -*- coding: utf-8 -*-

# Code by Oleg A. Paraschenko <olpa uucode com>
# Adapted from http://uucode.com/blog/2014/12/08/using-freebidi-from-python-using-ctypes/
# LICENCE: Public Domain

import ctypes
import ctypes.util
import sys

fb_name = ctypes.util.find_library('fribidi')
fb = None

if fb_name is not None:
    fb = ctypes.CDLL(fb_name)


def _preamble(s):
    if sys.version_info < (3, 0):
        if isinstance(s, unicode):
            utf8_bytes = s.encode('utf-8')
            n = len(s)
        else:
            utf8_bytes = s  # assume that the strings are utf8
            n = len(unicode(s, 'utf8'))
    else:
        utf8_bytes = s.encode('utf-8')
        n = len(s)
    c_buf1 = ctypes.create_string_buffer(4*n)  # fribidi: 4 bytes per char,
    c_buf2 = ctypes.create_string_buffer(4*n)  # utf8: max 4 bytes per char
    n2 = fb.fribidi_utf8_to_unicode(utf8_bytes, len(utf8_bytes), c_buf1)
    assert n == n2
    return (c_buf1, c_buf2, n)


def log2vis(s, pbase_dir=1):
    (c_buf1, c_buf2, n) = _preamble(s)
    c_dir = ctypes.c_int(pbase_dir)
    fb.fribidi_log2vis(c_buf1, n, ctypes.byref(c_dir), c_buf2, None, None, None)
    fb.fribidi_unicode_to_utf8(c_buf2, n, c_buf1)
    if sys.version_info < (3, 0):
        s = unicode(c_buf1.value, 'utf8')
    else:
        s = c_buf1.value.decode('utf8')
    return s


def log2levels(s, pbase_dir=1):
    (c_buf1, c_buf2, n) = _preamble(s)
    c_dir = ctypes.c_byte(pbase_dir)
    c_levels = (ctypes.c_byte * n)()
    ctypes.cast(c_levels, ctypes.POINTER(ctypes.c_byte))
    fb.fribidi_log2vis(c_buf1, n, ctypes.byref(c_dir), None, None, None, c_levels)
    return c_levels


def insert_markers(s, levels, pbase_dir=1):
    if not s:
        return
    start_markers = (u'\u202a', u'\u202b')  # LRE, RLE = l-r and r-l embedding
    end_marker = u'\u202c'  # PDF = pop directional formatting
    dir_i = pbase_dir
    assert (0 == dir_i) or (1 == dir_i)
    while pbase_dir > levels[0]:
        pbase_dir = pbase_dir - 2
    last_level = pbase_dir
    a = []
    lvl = None
    for (ch, lvl) in zip(s, levels):
        while lvl > last_level:
            dir_i = 1 - dir_i
            a.append(start_markers[dir_i])
            last_level = last_level + 1
        while lvl < last_level:
            dir_i = 1 - dir_i
            a.append(end_marker)
            last_level = last_level - 1
        a.append(ch)
    if lvl is not None:
        while lvl > pbase_dir:
            a.append(end_marker)
            lvl = lvl - 1
    return u''.join(a)
