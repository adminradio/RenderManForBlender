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

################################################################################
################################################################################
##                                                                            ##
##                         -= S T U B  -  W I P =-                            ##
##                                                                            ##
##                   N O T  I M P L E M E N T E D  Y E T                      ##
##                                                                            ä#
################################################################################
################################################################################

#
# Blender Imports
#
import bpy
from functools import wraps
from bpy.app.handlers import persistent


def validCallback(function):
    @wraps(function)
    def wrapper(self, context):
        function(self, context)
    return wrapper


rfb_post = []
load_pre = []
load_post = []
save_pre = []
save_post = []
scene_pre = []
scene_post = []
frame_pre = []
frame_post = []
render_pre = []
render_init = []
render_cancel = []
render_complete = []


def event_handler(evt):
    def decorator(function):
        if evt == "RFB_POST":
            rfb_post.append(function)
        if evt == "LOAD_PRE":
            load_post.append(function)
        if evt == "LOAD_POST":
            load_post.append(function)
        if evt == "SAVE_PRE":
            save_pre.append(function)
        if evt == "SAVE_POST":
            save_post.append(function)
        if evt == "SCENE_PRE":
            scene_pre.append(function)
        if evt == "SCENE_POST":
            scene_post.append(function)
        if evt == "FRAME_PRE":
            frame_pre.append(function)
        if evt == "FRAME_POST":
            frame_post.append(function)
        if evt == "RENDER_PRE":
            render_pre.append(function)
        if evt == "RENDER_INIT":
            render_init.append(function)
        if evt == "RENDER_CANCEL":
            render_cancel.append(function)
        if evt == "RENDER_COMPLETE":
            render_complete.append(function)
        return function
    return decorator


rfb_modified = False


@persistent
def h_rfp_post():
    for h in rfb_post:
        h()


@persistent
def h_load_pre(scene):
    for h in load_pre:
        h(scene)


@persistent
def h_load_post(scene):
    for h in load_post:
        h()


@persistent
def h_save_pre(scene):
    for h in save_pre:
        h(scene)


@persistent
def h_save_post(scene):
    for h in save_post:
        h(scene)


@persistent
def h_scene_pre(scene):
    for h in scene_pre:
        h(scene)


@persistent
def h_scene_post(scene):
    for h in scene_post:
        h(scene)

    #
    # 'rfb_modified' is true when register() was called and thus
    # this happened only if the addon was loaded during startup
    # or a restart of the addon
    #
    global rfb_modified
    if rfb_modified:
        rfb_modified = False
        for h in rfb_post:
            h()


@persistent
def h_frame_pre(scene):
    for h in frame_pre:
        h(scene)


@persistent
def h_frame_post(scene):
    for h in frame_post:
        h(scene)


@persistent
def h_render_pre(scene):
    for h in render_pre:
        h()


@persistent
def h_render_init(scene):
    for h in render_init:
        h()


@persistent
def h_render_cancel(scene):
    for h in render_cancel:
        h()


@persistent
def h_render_complete(scene):
    for h in render_complete:
        h()


def register():
    bpy.app.handlers.load_pre.append(h_load_pre)
    bpy.app.handlers.load_post.append(h_load_post)

    bpy.app.handlers.save_pre.append(h_save_pre)
    bpy.app.handlers.save_post.append(h_save_post)

    bpy.app.handlers.scene_update_pre.append(h_scene_pre)
    bpy.app.handlers.scene_update_post.append(h_scene_post)

    bpy.app.handlers.frame_change_pre.append(h_frame_pre)
    bpy.app.handlers.frame_change_post.append(h_frame_post)

    bpy.app.handlers.render_pre.append(h_render_pre)
    bpy.app.handlers.render_init.append(h_render_init)
    bpy.app.handlers.render_cancel.append(h_render_cancel)
    bpy.app.handlers.render_complete.append(h_render_complete)

    global rfb_modified
    rfb_modified = True


def unregister():
    bpy.app.handlers.load_pre.remove(h_load_pre)
    bpy.app.handlers.load_post.remove(h_load_post)

    bpy.app.handlers.save_pre.remove(h_save_pre)
    bpy.app.handlers.save_post.remove(h_save_post)

    bpy.app.handlers.scene_update_pre.remove(h_scene_pre)
    bpy.app.handlers.scene_update_post.remove(h_scene_post)

    bpy.app.handlers.frame_change_pre.remove(h_frame_pre)
    bpy.app.handlers.frame_change_post.remove(h_frame_post)

    bpy.app.handlers.render_pre.remove(h_render_pre)
    bpy.app.handlers.render_init.remove(h_render_init)
    bpy.app.handlers.render_cancel.remove(h_render_cancel)
    bpy.app.handlers.render_complete.remove(h_render_complete)
