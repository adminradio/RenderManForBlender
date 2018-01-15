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
# blender imports
#
import bpy

#
# RfB imports
#
from . import icons
from .. import engine


class RfB_HT_RenderUiView3D(bpy.types.Header):
    bl_idname = 'RfB_HT_render_ui_view3d'
    bl_space_type = 'VIEW_3D'

    iid_render = icons.iconid("render")
    iid_sunlight = icons.iconid("animation_on")
    iid_ipr_stop = icons.iconid("stop_ipr")
    iid_ipr_start = icons.iconid("start_ipr")

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return
        layout = self.layout
        row = layout.row(align=True)
        row.scale_x = 1.25
        row.separator()
        row.prop(
            context.scene.renderman,
            "external_animation",
            text="",
            icon_value=self.iid_sunlight
        )
        row.operator(
            "render.render",
            text='',
            icon_value=self.iid_render
        )
        if engine.ipr:
            row.operator(
                'rfb.tool_ipr',
                text='',
                icon_value=self.iid_ipr_stop
            )
        else:
            row.operator(
                'rfb.tool_ipr',
                text='',
                icon_value=self.iid_ipr_start
            )
