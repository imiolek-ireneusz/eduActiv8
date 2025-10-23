# -*- coding: utf-8 -*-
"""
# Initial Code by Oleg A. Paraschenko <olpa uucode com>
# Adapted from http://uucode.com/blog/2014/12/08/using-freebidi-from-python-using-ctypes/
# LICENCE: Public Domain

Updated FriBidi wrapper compatible with FriBidi >= 1.0
Keeps backward support for old libfribidi versions.
"""

import ctypes
import ctypes.util
import sys
import array

fb_name = ctypes.util.find_library('fribidi')
fb = None
if fb_name is not None:
    fb = ctypes.CDLL(fb_name)

# Detect availability of old API symbols
has_old_api = hasattr(fb, "fribidi_utf8_to_unicode")

# FriBidi types
FriBidiChar = ctypes.c_uint32
FriBidiCharType = ctypes.c_int


def _string_to_unicode_buffer(s):
    """Convert Python string to FriBidiChar buffer."""
    codepoints = array.array('I', (ord(ch) for ch in s))
    n = len(codepoints)
    buf = (FriBidiChar * (n + 1))()
    for i, cp in enumerate(codepoints):
        buf[i] = cp
    return buf, n


def _unicode_buffer_to_string(buf, n):
    """Convert FriBidiChar buffer back to Python string."""
    return ''.join(chr(buf[i]) for i in range(n))


def _preamble(s):
    """Prepare input/output buffers depending on available API."""
    if has_old_api:
        # Old FriBidi API (pre-1.0)
        if sys.version_info < (3, 0):
            if isinstance(s, unicode):
                utf8_bytes = s.encode('utf-8')
                n = len(s)
            else:
                utf8_bytes = s
                n = len(unicode(s, 'utf8'))
        else:
            utf8_bytes = s.encode('utf-8')
            n = len(s)
        c_buf1 = ctypes.create_string_buffer(4 * n)
        c_buf2 = ctypes.create_string_buffer(4 * n)
        n2 = fb.fribidi_utf8_to_unicode(utf8_bytes, len(utf8_bytes), c_buf1)
        assert n == n2
        return c_buf1, c_buf2, n
    else:
        # New FriBidi API (1.0+)
        c_buf1, n = _string_to_unicode_buffer(s)
        c_buf2 = (FriBidiChar * (n + 1))()
        return c_buf1, c_buf2, n


def log2vis(s, pbase_dir=1):
    (c_buf1, c_buf2, n) = _preamble(s)
    c_dir = ctypes.c_int(pbase_dir)
    fb.fribidi_log2vis(c_buf1, n, ctypes.byref(c_dir), c_buf2, None, None, None)

    if has_old_api:
        # Convert back using old helper
        fb.fribidi_unicode_to_utf8(c_buf2, n, c_buf1)
        if sys.version_info < (3, 0):
            return unicode(c_buf1.value, 'utf8')
        else:
            return c_buf1.value.decode('utf8')
    else:
        # Convert back manually
        return _unicode_buffer_to_string(c_buf2, n)


def log2levels(s, pbase_dir=1):
    (c_buf1, c_buf2, n) = _preamble(s)
    c_dir = ctypes.c_byte(pbase_dir)
    c_levels = (ctypes.c_byte * n)()
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
