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


# TODO: for future use, these values should be go into a JSON file,
#       so we have not to modify code if things are added or changed.
#
#       Or better, move into preferences!

class SocketColor:
    """Utility Class // Data Class."""

    _colors = {
        "bxdf": (0.25, 1.00, 0.25, 1.00),
        "float": (0.50, 0.50, 0.50, 1.00),
        "vector": (0.00, 0.00, 0.50, 1.00),
        "rgb": (1.00, 0.50, 0.00, 1.00),
        "euler": (0.00, 0.50, 0.50, 1.00),
        "struct": (1.00, 1.00, 0.00, 1.00),
        "string": (0.00, 0.00, 1.00, 1.00),
        "int": (1.00, 1.00, 1.00, 1.00)}

    @classmethod
    def get(cls, ident):
        try:
            return cls._colors[ident]

        except KeyError:
            # return magenta
            return (1.00, 0.00, 1.00, 1.00)
