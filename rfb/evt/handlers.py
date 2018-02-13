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
# Blender Imports
#
import bpy
from bpy.app.handlers import persistent

#
# RenderManForBlender Imports
#
from .. prf import pref
from .. lib.echo import stdmsg


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

load_enabled = False
save_enabled = False
scene_enabled = False
frame_enabled = False
render_enabled = False


#
# Define the decorator
#
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


#
# 'rfb_modified' is true only when register() was called and thus this
# happened if the addon was reloaded
#
rfb_modified = False


@persistent
def h_rfp_post(scene):
    for h in rfb_post:
        h(scene)


@persistent
def h_load_pre(scene):
    for h in load_pre:
        h(scene)


@persistent
def h_load_post(scene):
    for h in load_post:
        h(scene)


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

    global rfb_modified
    if rfb_modified:
        rfb_modified = False
        for h in rfb_post:
            h(scene)


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
        h(scene)


@persistent
def h_render_init(scene):
    for h in render_init:
        h(scene)


@persistent
def h_render_cancel(scene):
    for h in render_cancel:
        h(scene)


@persistent
def h_render_complete(scene):
    for h in render_complete:
        h(scene)


def disable(h):
    global load_enabled
    global save_enabled
    global scene_enabled
    global frame_enabled
    global render_enabled

    if h == 'LOAD':
        if not load_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'LOAD' already unregistered.")
            return
        else:
            if h_load_pre in bpy.app.handlers.load_pre:
                bpy.app.handlers.load_pre.remove(h_load_pre)
            if h_load_post in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.remove(h_load_post)
            load_enabled = False
        if pref('rfb_info'):
            stdmsg("EventHandler 'LOAD' unregistered.")
        return

    if h == 'SAVE':
        if not save_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'SAVE' already unregistered.")
            return
        else:
            if h_save_pre in bpy.app.handlers.save_pre:
                bpy.app.handlers.save_pre.remove(h_save_pre)
            if h_save_post in bpy.app.handlers.save_post:
                bpy.app.handlers.save_post.remove(h_save_post)
            save_enabled = False
        if pref('rfb_info'):
            stdmsg("EventHandler 'SAVE' unregistered.")
        return

    if h == 'SCENE':
        if not scene_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'SCENE' already unregistered.")
            return
        else:
            if h_scene_pre in bpy.app.handlers.scene_update_pre:
                bpy.app.handlers.scene_update_pre.remove(h_scene_pre)
            if h_scene_post in bpy.app.handlers.scene_update_post:
                bpy.app.handlers.scene_update_post.remove(h_scene_post)
            scene_enabled = False
        if pref('rfb_info'):
            stdmsg("EventHandler 'SCENE' unregistered.")
        return

    if h == 'FRAME':
        if not frame_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'FRAME' already unregistered.")
            return
        else:
            if h_frame_pre in bpy.app.handlers.frame_change_pre:
                bpy.app.handlers.frame_change_pre.remove(h_frame_pre)
            if h_frame_post in bpy.app.handlers.frame_change_post:
                bpy.app.handlers.frame_change_post.remove(h_frame_post)
        frame_enabled = False
        if pref('rfb_info'):
            stdmsg("EventHandler 'FRAME' unregistered.")
        return

    if h == 'RENDER':
        if not render_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'RENDER' already unregistered.")
            return
        else:
            if h_render_pre in bpy.app.handlers.render_pre:
                bpy.app.handlers.render_pre.remove(h_render_pre)
            if h_render_init in bpy.app.handlers.render_init:
                bpy.app.handlers.render_init.remove(h_render_init)
            if h_render_cancel in bpy.app.handlers.render_cancel:
                bpy.app.handlers.render_cancel.remove(h_render_cancel)
            if h_render_complete in bpy.app.handlers.render_complete:
                bpy.app.handlers.render_complete.remove(h_render_complete)
        if pref('rfb_info'):
            stdmsg("EventHandler 'RENDER' unregistered.")
        render_enabled = False
        return


def enable(h):
    global load_enabled
    global save_enabled
    global scene_enabled
    global frame_enabled
    global render_enabled

    if h == 'LOAD':
        if load_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'FILE (LOAD)' already registered.")
            return
        else:
            if h_load_pre not in bpy.app.handlers.load_pre:
                bpy.app.handlers.load_pre.append(h_load_pre)
            if h_load_post not in bpy.app.handlers.load_post:
                bpy.app.handlers.load_post.append(h_load_post)
        load_enabled = True
        if pref('rfb_info'):
            stdmsg("EventHandler 'FILE (LOAD)' registered.")
        return

    if h == 'SAVE':
        if save_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'FILE (SAVE)' already registered.")
            return
        else:
            if h_save_pre not in bpy.app.handlers.save_pre:
                bpy.app.handlers.save_pre.append(h_save_pre)
            if h_save_post not in bpy.app.handlers.save_post:
                bpy.app.handlers.save_post.append(h_save_post)
        save_enabled = True
        if pref('rfb_info'):
            stdmsg("EventHandler 'FILE (SAVE)' registered.")
        return

    if h == 'FRAME':
        if frame_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'FRAME' already registered.")
            return
        else:
            if h_frame_pre not in bpy.app.handlers.frame_change_pre:
                bpy.app.handlers.frame_change_pre.append(h_frame_pre)
            if h_frame_post not in bpy.app.handlers.frame_change_post:
                bpy.app.handlers.frame_change_post.append(h_frame_post)
        frame_enabled = True
        if pref('rfb_info'):
            stdmsg("EventHandler 'FRAME' registered.")
        return

    if h == 'SCENE':
        if scene_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'SCENE' already registered.")
            return
        else:
            if h_scene_pre not in bpy.app.handlers.scene_update_pre:
                bpy.app.handlers.scene_update_pre.append(h_scene_pre)
            if h_scene_post not in bpy.app.handlers.scene_update_post:
                bpy.app.handlers.scene_update_post.append(h_scene_post)
        scene_enabled = True
        if pref('rfb_info'):
            stdmsg("EventHandler 'SCENE' registered.")
        return

    if h == 'RENDER':
        if render_enabled:
            if pref('rfb_info'):
                stdmsg("EventHandler 'RENDER' already registered.")
            return
        else:
            if h_render_pre not in bpy.app.handlers.render_pre:
                bpy.app.handlers.render_pre.append(h_render_pre)
            if h_render_init not in bpy.app.handlers.render_init:
                bpy.app.handlers.render_init.append(h_render_init)
            if h_render_cancel not in bpy.app.handlers.render_cancel:
                bpy.app.handlers.render_cancel.append(h_render_cancel)
            if h_render_complete not in bpy.app.handlers.render_complete:
                bpy.app.handlers.render_complete.append(h_render_complete)
        render_enabled = True
        if pref('rfb_info'):
            stdmsg("EventHandler 'RENDER' registered.")
        return


def register():
    #
    # not yet sure if LOAD or SAVE are useful for anything (?)
    #
    # enable('LOAD')
    # enable('SAVE')
    enable('FRAME')
    enable('SCENE')
    enable('RENDER')

    global rfb_modified
    rfb_modified = True


def unregister():
    disable('RENDER')
    disable('SCENE')
    disable('FRAME')
    # disable('SAVE')
    # disable('LOAD')
