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
from bpy.props import StringProperty

#
# RenderMan for Blender Imports
#
from .. import engine


class RfB_OT_ITEM_ToggleLightlink(bpy.types.Operator):
    bl_idname = 'rfb.item_toggle_lightlink'
    bl_label = 'Add/Remove Selected from Object Group'

    add_remove = StringProperty(default='add')
    ll_name = StringProperty(default='')

    def execute(self, context):
        scene = context.scene

        add_remove = self.properties.add_remove
        ll_name = self.properties.ll_name

        if add_remove == 'add':
            ll = scene.renderman.ll.add()
            ll.name = ll_name
        else:
            ll_index = scene.renderman.ll.keys().index(ll_name)
            if engine.is_ipr_running():
                engine.ipr.remove_light_link(
                    context, scene.renderman.ll[ll_index])
            scene.renderman.ll.remove(ll_index)

        return {'FINISHED'}
