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

# RfB imports
from . import icons
from .. import engine


class RfB_HT_RenderUiInfo(bpy.types.Header):
    bl_idname = 'RfB_HT_render_ui_info'
    bl_space_type = "INFO"

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return
        layout = self.layout

        row = layout.row(align=True)
        iid = icons.iconid("render")
        row.operator("render.render", text="Render", icon_value=iid)

        iid = icons.iconid("render_spool")
        if context.scene.renderman.enable_external_rendering:
            row.operator("rfb.file_spool_render",
                         text="External Render",
                         icon_value=iid)
        if engine.ipr:
            iid = icons.iconid("stop_ipr")
            row.operator('rfb.tool_ipr',
                         text="Stop IPR",
                         icon_value=iid)
        else:
            iid = icons.iconid("start_ipr")
            row.operator('rfb.tool_ipr',
                         text="Start IPR",
                         icon_value=iid)
