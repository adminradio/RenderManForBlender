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
from bgl import *


def vp_border(self, vp):
    w = vp.width
    h = vp.height
    l = 6  # noqa
    a = l // 2  # noqa

    glEnable(GL_BLEND)
    # glEnable(GL_LINE_SMOOTH)
    #
    # TODO:   Color and linewidth should go into Userprefs.
    # DATE:   2018-01-23
    # AUTHOR: Timm Wimmers
    # STATUS: -unassigned-
    #
    glColor4f(0.870, 0.325, 0.375, 0.750)
    glLineWidth(l)

    # bottom left, bottom right, top right, top left
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
    # glDisable(GL_LINE_SMOOTH)
