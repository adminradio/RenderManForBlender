# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2017 Pixar
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
# borrowed from Animation Nodes, by Jacques Lucke
#
def split_ll(layout, alignment=True):
    """Split a layout into two colums. Both are left aligned."""
    row = layout.row()

    # left column, left aligned
    lc = row.row(align=alignment)
    lc.alignment = "LEFT"

    # right column, left aligned
    rc = row.row(align=alignment)
    rc.alignment = "LEFT"
    return lc, rc


#
# borrowed from Animation Nodes, by Jacques Lucke
#
def split_lr(layout, alignment=True):
    """Split a layout into two colums. First is left, second is right aligned."""
    row = layout.row()

    # left column, left aligned
    lc = row.row(align=alignment)
    lc.alignment = "LEFT"

    # right column, right aligned
    rc = row.row(align=alignment)
    rc.alignment = "RIGHT"
    return lc, rc


def bbox_h(layout):
    """Draw a bordered box with horizontal arrangement."""
    box = layout.box()
    return box.row()


def bbox_v(layout):
    """Draw a bordered box with vertical arrangement."""
    box = layout.box()
    return box.column()
