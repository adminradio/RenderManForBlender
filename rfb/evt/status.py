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

# ########################################################################### #
# ########################################################################### #
# #                                                                         # #
# #                         -= S T U B  -  W I P =-                         # #
# #                                                                         # #
# #                   N O T  I M P L E M E N T E D  Y E T                   # #
# #                                                                         ä #
# ########################################################################### #
# ########################################################################### #


class Status:
    def __init__(self):
        self.reset()
        self.rendering = False

    def reset(self):
        self.ls = False
        self.nt = False
        self.tex = False
        self.cam = False
        self.shd = False
        self.file = False
        self.scene = False
        self.frame = False
        self.addon = False

    def get(self):
        s = set()
        if self.ls:
            s.add("LightShader")
        if self.nt:
            s.add("NodeTree")
        if self.tex:
            s.add("Texture")
        if self.cam:
            s.add("Camera")
        if self.shd:
            s.add("Shader")
        if self.file:
            s.add("File")
        if self.addon:
            s.add("Addon")
        if self.scene:
            s.add("Scene")
        if self.frame:
            s.add("Frame")
        return s


def rendering(self):
    return self.rendering
