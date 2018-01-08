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

# python imports
import os

# blender imports
import bpy
import bpy.utils.previews

# RfB imports
from ..utils import (
    stdout,
    stdadd
)

__all__ = ["iconid"]


def iconid(ident):
    """Return an 'icon_id' which can be used as 'icon_value'"""
    icon = __collections["main"].get(ident)
    icon_id = None

    if icon:
        icon_id = icon.icon_id
    else:
        stdadd("Ressource Icons >> ERROR - loading ID '" + ident + "' >> using 'dev_error'!")
        icon_id = __collections.get("dev_error").icon_id

    return icon_id

#
# 'theme' is a preperation for theme support.
#
def __load(theme='default'):
    stdadd("Ressource icons >> Loading collection ...")

    prvcoll = bpy.utils.previews.new()
    basedir = os.path.join(os.path.dirname(__file__), "themes", theme)

    for file in os.listdir(basedir):
        if file.endswith(".png"):
            ident = os.path.splitext(file)[0].lower()
            prvcoll.load(ident, os.path.join(basedir, file), 'IMAGE')

    stdadd("Ressource icons >> DONE!")
    return prvcoll


stdout("Ressource Icons >> Init loading ...")
__collections = {}
__collections["main"] = __load()
