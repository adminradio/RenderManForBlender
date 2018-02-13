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


class RfB_OT_OBJECT_DeleteLight(bpy.types.Operator):
    bl_idname = "rfb.object_delete_light"
    bl_label = "Delete Light"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    types = {
        'AREA': 'ui_ts_arealight',
        'HEMI': 'ui_ts_envlight',
        'SUN': 'ui_ts_daylight'
    }

    def execute(self, context):

        _t_ = context.object.data.type
        bpy.ops.object.delete()

        lamps = [obj for obj in context.scene.objects
                 if obj.type == 'LAMP'
                 and obj.data.type == _t_]

        if lamps:
            lamps[0].select = True
            context.scene.objects.active = lamps[0]
        else:
            #
            # No light of type _t_, close sublayout 'ui_ts_*'
            #
            setattr(context.scene, self.types[_t_], False)

        return {"FINISHED"}
