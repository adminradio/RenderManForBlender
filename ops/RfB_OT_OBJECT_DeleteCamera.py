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
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        type_camera = bpy.context.object.data.type
        bpy.ops.object.delete()

        camera = [obj for obj in bpy.context.scene.objects if obj.type ==
                  "CAMERA" and obj.data.type == type_camera]

        if len(camera):
            camera[0].select = True
            bpy.context.scene.objects.active = camera[0]
            return {"FINISHED"}

        else:
            return {"FINISHED"}
