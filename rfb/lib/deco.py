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

#
# Python Imports
#

#
# Blender Imports
#

#
# RenderManForBlender Imports
#

import time
import functools

from . time import pretty
from . echo import stdmsg

from .. registry import Registry as rr


_ids_ = set()


def nonrecursive(f):
    @functools.wraps(f)
    def _w_(*args, **kwargs):
        _id_ = id(f)
        if _id_ not in _ids_:
            _ids_.add(_id_)
            r = f(*args, **kwargs)
            _ids_.remove(_id_)
            return r
    return _w_


def laptime(f):
    if not rr.get('RFB_TIME_IT'):
        return f

    @functools.wraps(f)
    def _w_(*args, **kwargs):
        s = time.clock()
        r = f(*args, **kwargs)
        e = time.clock()
        t = e - s
        stdmsg("Lap time: {} | f() = '{}'".format(pretty(t), f.__name__))
        return r
    return _w_
