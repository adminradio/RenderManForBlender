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

#
# Python Imports
#

#
# Blender Imports
#

#
# RenderManForBlender Imports
#

from . import state
from . handlers import event_handler as eh

from .. lib.echo import stdmsg
from .. lib.deco import nonrecursive


@eh("RFB_POST")
def rfb_loaded(scene):
    state.addon = True
    update()
    state.addon = False
    return


@eh("LOAD_PRE")
def load(scene):
    if not state.file:
        state.file = True
        update()
    return


@eh("LOAD_POST")
def loaded(scene):
    if state.file:
        state.file = False
        update()
    return


@eh("SAVE_PRE")
def save(scene):
    if not state.file:
        state.file = True
        update()
    return


@eh("SAVE_POST")
def saved(scene):
    if state.file:
        state.file = False
        update()
    return


@eh("SCENE_PRE")
def scene_in(scene):
    if not state.scene:
        state.scene = True
        update()
    return


@eh("SCENE_POST")
def scene_out(scene):
    if state.scene:
        state.scene = False
        update()
    return


@eh("FRAME_PRE")
def frame_in(scene):
    if not state.frame:
        state.frame = True
        update()
    return


@eh("FRAME_POST")
def frame_out(scene):
    if state.frame:
        state.frame = False
        update()
    return


@eh("RENDER_PRE")
def render_pre():
    if not state.rendering:
        state.rendering = True
        update()
    return


@eh("RENDER_INIT")
def render_init():
    if not state.rendering:
        state.rendering = True
        update()
    return


@eh("RENDER_CANCEL")
def render_cancel():
    if state.rendering:
        state.rendering = False
        update()
    return


@eh("RENDER_COMPLETE")
def render_complete():
    if state.rendering:
        state.rendering = False
        update()
    return


@nonrecursive
def update():
    items = state.get()
    if items:
        for item in items:
            if item == 'Scene':
                continue
            stdmsg("EventHandler '{}' triggered.".format(str(item.upper())))
