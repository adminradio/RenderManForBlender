# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2017 Pixar
#                    - 2018 Timm Wimmers
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

__all__ = ["iconid", "toggle"]

# Python Imports
import os

# Blender Imports
import bpy
import bpy.utils.previews

# RenderMan for Blender Imports
from ... rfb.lib.echo import stdmsg


def iconid(ident):
    """Return an 'icon_id' which can be used as 'icon_value'"""
    icon = _collections["main"].get(ident.lower())
    iid = None

    if icon:
        iid = icon.icon_id
    else:
        stdmsg("ICONS: Requested ID {} not found."
               "Using 'dev_error' instead!").format(ident.lower())
        iid = _collections["main"].get("dev_error").icon_id

    return iid


def toggle(prefix, b):
    """Return an 'icon_id' with on or off suffix (depending on boolean)."""
    suffix = "_on" if b else '_off'
    ident = "{}{}".format(prefix, suffix)
    return iconid(ident)


#
# 'theme' is a preperation for theming support. (TW, 2018-02-05)
#
def __load(theme='default'):
    prvcoll = bpy.utils.previews.new()
    basedir = os.path.join(os.path.dirname(__file__), "themes", theme)

    for f in os.listdir(basedir):
        if f.endswith(".png"):
            ident = os.path.splitext(f)[0].lower()
            prvcoll.load(ident, os.path.join(basedir, f), 'IMAGE')

    return prvcoll


_collections = {}
_collections["main"] = __load()
