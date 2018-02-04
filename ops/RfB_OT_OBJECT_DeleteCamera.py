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


class RfB_OT_OBJECT_DeleteCamera(bpy.types.Operator):
    bl_idname = "rfb.object_delete_camera"
    bl_label = "Delete Camera"
    bl_description = "Delete this camera (disabled if camera is hidden)."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scn = context.scene

        cam_type = bpy.context.object.data.type
        #
        # if we  are going to delete an active camera, we should know!
        #
        bpy.ops.object.delete()
        cams = [
            obj for obj in bpy.context.scene.objects
            if obj.type == "CAMERA" and obj.data.type == cam_type
        ]

        if cams:
            #
            # if we deleted an active, we should mark a new one
            # as active to make sure that there is an active one
            #
            try:
                _tmp = bpy.data.scenes[scn.name].camera.name
            except AttributeError:
                bpy.data.scenes[scn.name].camera = cams[0]
            cams[0].select = True
            bpy.context.scene.objects.active = cams[0]
            return {"FINISHED"}

        else:
            return {"FINISHED"}
