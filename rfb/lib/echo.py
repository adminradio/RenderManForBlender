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
from .. registry import Registry as rr


def stdmsg(msg):
    _echo(msg, extend=False)


def stdadd(msg=""):
    _echo(msg, extend=True)


def _echo(msg, extend=False):
    pre = (
        "                      ...   "
        if extend
        else "[{}] RfB - ".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    print('{}{}'.format(pre, msg))


def slugify(s, length=79, offset=0):
    """Shorten a string by removing the mid part of it."""
    #
    # TODO:   be sure that offset doesn't go to a negative
    #         value of len(string).
    # DATE:   2018-01-17
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    m = str(s)
    slen = len(m)
    if slen <= length:
        return s
    else:

        pos_e = int(length / 2 + offset)
        pos_s = int(slen - (length / 2) + offset)
        slg_l = m[:pos_e]
        slg_r = m[pos_s:]

        return "{}...{}".format(slg_l, slg_r)


def debug(lvl, *argv):
    lvl = lvl.lower()

    if (lvl == 'warning' or
            lvl == 'error' or
            lvl == 'osl'):

        if(lvl == 'warning'):
            stdmsg("WRN: {}".format(argv))
        elif(lvl == "error"):
            stdmsg("ERR: ", argv)
        elif(lvl == "osl"):
            for item in argv:
                stdmsg("OSL: {}".format(argv))
    else:
        if rr.get('RFB_DEBUG'):
            if(lvl == 'info'):
                stdmsg("INF: {}".format(argv))
            else:
                stdmsg("DBG: {}".format(argv))
        else:
            pass
