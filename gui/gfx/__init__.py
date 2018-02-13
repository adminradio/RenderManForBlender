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
# Blender imports
#
import blf
from bgl import *

#
# RenderManForBlender Imports
#
from ... rfb.prf import pref

dpi = 72


def text_dpi(val):
    global dpi
    dpi = val


def border(self, vp):
    w = vp.width
    h = vp.height
    l = 6  # noqa
    a = l // 2  # noqa
    c = pref('rfb_ipr_border')

    glEnable(GL_BLEND)
    glColor4f(*c)
    glLineWidth(l)

    #
    # to avoid nasty corners we draw four indiividual lines
    # instead of a single quad vertex group:
    #
    glBegin(GL_LINE_STRIP)
    glVertex2i(0, a)
    glVertex2i(w, a)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2i(0, h - a)
    glVertex2i(w, h - a)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2i(a, l)
    glVertex2i(a, h - l)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex2i(w - a, l)
    glVertex2i(w - a, h - l)
    glEnd()
    glDisable(GL_BLEND)


def hline(x, y, l, c=None, lw=None):
    line(x, y, x + l, y, c, lw)


def vline(x, y, l, c=None, lw=None):
    line(x, y, x, y + l, c, lw)


def line(x1, y1, x2, y2, c=None, lw=None):
    # horizontal or vertical lines don't need smooth drawing
    if not x1 == x2 or y1 == y2:
        glEnable(GL_LINE_SMOOTH)
    else:
        glDisable(GL_LINE_SMOOTH)

    if lw:
        glLineWidth(lw)

    if c:
        glColor4f(*c)

    glEnable(GL_BLEND)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()
    if lw:
        glLineWidth(1)


def text(txt, x, y, f=0, h="LEFT", v="BASELINE", s=12, c=(1, 1, 1, 1)):
    _txt = str(txt)
    blf.size(font, s, int(dpi))
    glColor4f(*c)

    if h == "LEFT" and v == "BASELINE":
        blf.position(font, x, y, 0)
    else:
        _w, _h = blf.dimensions(font, _txt)
        _x, _y = x, y
        if h == "RIGHT":
            _x -= _w
        elif h == "CENTER":
            _x -= _w * 0.5
        if v == "CENTER":
            _y -= blf.dimensions(font, "x")[1] * 0.75

        blf.position(font, _x, _y, 0)

    blf.draw(font, _txt)


def ngon(verts, c=None):
    if c:
        glColor4f(*c)
    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glBegin(GL_POLYGON)
    for x, y in verts:
        glVertex2f(x, y)
    glEnd()
    glDisable(GL_BLEND)
