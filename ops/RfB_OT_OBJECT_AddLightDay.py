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


class RfB_OT_OBJECT_AddLightDay(bpy.types.Operator):
    bl_idname = "rfb.object_add_light_day"
    bl_label = "Add DayLight"
    bl_description = "Adds a PxrEnvDayLight to the current scene."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        #
        # FIXME:  Adding the lamp as type 'SUN' here from operator, will add
        #         the lamp as 'HEMI' due to the 'renderman.renderman_type'
        #         update method in properties.py
        # QUICK:  Change explicitly to 'SUN' type before returning.
        #         Have to investigate further.
        # DATE:   2018-01-21
        # AUTHOR: Timm Wimmers
        # STATUS: -unassigned-
        #
        bpy.ops.object.lamp_add(type='SUN')
        _tmp = {'material': None, 'lamp': bpy.context.active_object.data}
        bpy.ops.rfb.node_add_nodetree(_tmp, idtype='lamp')
        bpy.context.object.data.renderman.renderman_type = 'SKY'
        # QUICK: change late explicitly
        bpy.context.object.data.type = 'SUN'
        return {"FINISHED"}
