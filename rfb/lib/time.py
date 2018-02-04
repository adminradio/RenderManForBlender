# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####

# <pep8-80 compliant>

#
# Python Imports
#
from datetime import datetime

#
# Blender Imports
#

#
# RenderManForBlender Imports
#


def dtnow():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def pretty(_s_, sfill=True):
    """Make time values human readable."""
    #
    # Example output with @laptime decorator
    #
    # RfB - Lap time: 9999.9999 ms | f() = function_name
    # RfB - Lap time:   59.9999 s  | f() = function_name
    # RfB - Lap time:  00:01:59 h  | f() = function_name
    #
    if _s_ < 10.0:
        txt = "{: >9.4f}ms" if sfill else "{:.4f}ms"
        return txt.format(_s_ * 1000)
    elif _s_ < 60.0:
        #
        # trailing space is needed if sfill is True (i.e. @laptime decorator)
        #
        txt = "{: >9.4f}s " if sfill else "{:.4f}s"
        return txt.format(_s_)
    else:
        txt = "{: >9}h " if sfill else "{: >9}h"
        return txt.format(hhmmss(_s_))


def hhmmss(_s_):
    """Return number of seconds as day time. Turns over at 86400 sec."""
    _s_ = int(_s_)
    hh = _s_ // (60 * 60) % 24
    ss = _s_ % (60 * 60)
    mm = ss // 60
    ss %= 60
    return "{:0>2d}:{:0>2d}:{:0>2d}".format(hh, mm, ss)
