
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

#
# Blender Imports
#
import bpy


#
# #### A T T E N T I O N  #####
#
# This operator should not be exposed to the UI as
# this can cause the loss of data since Blender does not
# preserve any information during script restart.
#
# As of 2018-01-19 this tool isn't available via UI, also it
# doesn't work well. (TW)
#
class RfB_OT_VIEW3D_CameraApertureType(bpy.types.Operator):
    bl_idname = "rfb.camera_aperture_type"
    bl_label = "Toggle Camera Aperture Type"
    bl_description = "Toggle camera aperture type (Shutter | Radius)."

    def execute(self, context):
        scn = context.scene
        cam = bpy.data.scenes[scn.name].camera
        cur = cam.data.cycles.aperture_type
        cam.data.cycles.aperture_type = 'RADIUS' if cur == 'FSTOP' else 'FSTOP'
        return {"FINISHED"}
