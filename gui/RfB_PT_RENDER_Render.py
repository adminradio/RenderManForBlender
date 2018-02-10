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
from bpy.types import Panel

#
# RenderManForBlender Imports
#
from . import icons
from .. import engine

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Render(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Render"

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return

        layout = self.layout
        rd = context.scene.render
        rm = context.scene.renderman

        #
        # Render Control (row)
        #
        row = layout.row(align=True)
        # disable if no camera in scene
        row.enabled = True if context.scene.camera else False

        #
        # Render
        #
        opr = "render.render"
        txt = "Frame"
        iid = icons.iconid("render")
        row.operator(opr, text=txt, icon_value=iid)

        #
        # Batch Render
        #
        opr = "render.render"
        txt = "Animation"
        iid = icons.iconid("batch_render")
        row.operator(opr, text=txt, icon_value=iid).animation = True

        #
        # IPR
        #
        if engine.ipr:
            # Stop IPR
            opr = "rfb.tool_ipr"
            txt = "Stop IPR"
            iid = icons.iconid("stop_ipr")
            row.operator(opr, text=txt, icon_value=iid)
        else:
            # Start IPR
            opr = "rfb.tool_ipr"
            txt = "Start IPR"
            iid = icons.iconid("start_ipr")
            row.operator(opr, text=txt, icon_value=iid)

        layout.separator()

        split = layout.split(percentage=0.33)

        split.label(text="Display:")
        row = split.row(align=True)
        row.prop(rd, "display_mode", text="")
        row.prop(rd, "use_lock_interface", icon_only=True)
        col = layout.column()
        row = col.row()
        row.prop(rm, "render_into", text="Render To")

        layout.separator()
        col = layout.column()
        col.prop(context.scene.renderman, "render_selected_objects_only")
        col.prop(rm, "do_denoise")
