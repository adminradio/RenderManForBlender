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
# RenderMan for Blender Imports
#
from . import icons

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Spooling(RfB_PT_MIXIN_Panel, Panel):
    # class RENDER_PT_renderman_spooling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "External Rendering"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        icon = 'CHECKBOX_HLT' if rm.enable_external_rendering else 'CHECKBOX_DEHLT'

        cl = layout.box()
        cll = cl.row()
        cll.prop(rm,
                 "enable_external_rendering",
                 icon=icon, emboss=False
                 )
        if not rm.enable_external_rendering:
            return

        cll = cl.row()
        iid = icons.iconid("render_spool")
        cll.operator("rfb.file_spool_render",
                     text="Export",
                     icon_value=iid
                     )
        cll = cl.column()
        cll.prop(rm, "display_driver", text='Render To')

        split = cl.split(percentage=0.5)
        split.prop(rm, "external_animation")

        sub_row = split.row(align=True)
        sub_row.enabled = rm.external_animation
        sub_row.prop(scene, "frame_start", text="Start")
        sub_row.prop(scene, "frame_end", text="End")

        split = cl.split(percentage=0.5)
        split.enabled = rm.generate_alf
        split.prop(rm, 'external_denoise')

        sub_row = split.row()
        sub_row.enabled = rm.external_denoise and rm.external_animation
        sub_row.prop(rm, 'crossframe_denoise')

        cll = cl.box()
        cll = cll.column()

        icn = 'panel_open' if rm.export_options else 'panel_closed'
        iid = icons.iconid(icn)
        cll.prop(rm,
                 "export_options",
                 text="Export Options",
                 icon_value=iid,
                 emboss=False
                 )
        if rm.export_options:
            cll.prop(rm, "generate_rib")

            row = cll.row()
            row.enabled = rm.generate_rib
            row.prop(rm, "generate_object_rib")

            cll.prop(rm, "generate_alf")

            split = cll.split(percentage=0.33)
            split.enabled = rm.generate_alf and rm.generate_render
            split.prop(rm, "do_render")

            sub_row = split.row()
            sub_row.enabled = rm.do_render and rm.generate_alf and rm.generate_render
            sub_row.prop(rm, "queuing_system")

        if rm.generate_alf:
            icn = 'panel_open' if rm.alf_options else 'panel_closed'
            iid = icons.iconid(icn)
            cll = cl.box()
            cll = cll.column()
            cll.prop(rm,
                     "alf_options",
                     text="ALF Options",
                     icon_value=iid,
                     emboss=False
                     )
            if rm.alf_options:
                cll.prop(rm, 'custom_alfname')
                cll.prop(rm, "convert_textures")
                cll.prop(rm, "generate_render")

                row = cll.row()
                row.enabled = rm.generate_render
                row.prop(rm, 'custom_cmd')

                split = cll.split(percentage=0.33)
                split.enabled = rm.generate_render
                split.prop(rm, "override_threads")

                sub_row = split.row()
                sub_row.enabled = rm.override_threads
                sub_row.prop(rm, "external_threads")

                row = cll.row()
                row.enabled = rm.external_denoise
                row.prop(rm, 'denoise_cmd')
                row = cll.row()
                row.enabled = rm.external_denoise
                row.prop(rm, 'spool_denoise_aov')
                row = cll.row()
                row.enabled = rm.external_denoise and not rm.spool_denoise_aov
                row.prop(rm, "denoise_gpu")

                # checkpointing
                cll = cll.column()
                cll.enabled = rm.generate_render

                row = cll.row()
                row.prop(rm, 'recover')

                row = cll.row()
                row.prop(rm, 'enable_checkpoint')

                row = cll.row()
                row.enabled = rm.enable_checkpoint
                row.prop(rm, 'asfinal')

                row = cll.row()
                row.enabled = rm.enable_checkpoint
                row.prop(rm, 'checkpoint_type')

                row = cll.row(align=True)
                row.enabled = rm.enable_checkpoint
                row.prop(rm, 'checkpoint_interval')
                row.prop(rm, 'render_limit')
