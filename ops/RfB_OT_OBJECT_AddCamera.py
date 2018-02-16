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
# Python Imports
#

#
# Blender Imports
#
import bpy

#
# RenderMan ForBlender Imports
#
from .. rfb.prf import pref


class RfB_OT_OBJECT_AddCamera(bpy.types.Operator):
    bl_idname = "rfb.object_add_camera"
    bl_label = "Add Camera"
    bl_description = "Add a Camera into the current Scene (Lens=65mm)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.context.space_data.lock_camera = False

        bpy.ops.object.camera_add()
        bpy.ops.view3d.object_as_camera()
        bpy.ops.view3d.viewnumpad(type="CAMERA")
        bpy.ops.view3d.camera_to_view()

        cam = bpy.context.object
        cam.data.clip_end = 10000
        cam.data.lens = 65

        if pref('add_cams_rigged'):
            _n_ = pref('add_cams_rigname')
            rig = None
            aex = True  # already existing rig

            try:
                rig = bpy.data.objects[_n_]
            except KeyError:
                # no rig object found. we have to create one
                aex = False

            if not aex:
                rig = bpy.data.objects.new(_n_, None)
                bpy.context.scene.objects.link(rig)
                #
                # TODO:   Add pref for size of empty/rig
                # DATE:   2018-02-09
                # AUTHOR: Timm Wimmers
                # STATUS: -unassigned-
                #
                rig.empty_draw_size = 3.0
                rig.empty_draw_type = 'PLAIN_AXES'
                rig.name = _n_
            cam.parent = rig
        bpy.context.scene.objects.active = cam
        cam.select = True
        return {"FINISHED"}
