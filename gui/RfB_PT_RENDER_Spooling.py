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
from . utils import split12

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Spooling(RfB_PT_MIXIN_Panel, Panel):
    # class RENDER_PT_renderman_spooling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "External Rendering"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout.column(align=True)
        scn = context.scene
        rmn = context.scene.renderman

        icn = 'CHECKBOX_HLT' if rmn.enable_external_rendering else 'CHECKBOX_DEHLT'
        prp = "enable_external_rendering"
        lay.prop(rmn, prp, icon=icn)
        if not rmn.enable_external_rendering:
            return

        box = lay.box()
        cll = box.row()

        lco, rco = split12(box)

        row = lco.row(align=True)
        row.prop(rmn, "external_animation")

        opr = "rfb.file_spool_render"
        txt = "Spool Animation" if rmn.external_animation else "Spool Frame"
        iid = icons.iconid("render_spool")
        rco.operator(opr, text=txt, icon_value=iid)
        rco.prop(rmn, "display_driver", text="")

        sub_row = rco.row(align=True)
        sub_row.enabled = rmn.external_animation
        sub_row.prop(scn, "frame_start", text="Start")
        sub_row.prop(scn, "frame_end", text="End")

        split = box.split(percentage=0.5)
        split.enabled = rmn.generate_alf
        split.prop(rmn, 'external_denoise')

        sub_row = split.row()
        sub_row.enabled = rmn.external_denoise and rmn.external_animation
        sub_row.prop(rmn, 'crossframe_denoise')

        cll = box.box()
        cll = cll.column()

        icn = 'panel_open' if rmn.export_options else 'panel_closed'
        iid = icons.iconid(icn)
        prp = "export_options"
        txt = "Export Options"
        cll.prop(rmn, prp, text=txt, icon_value=iid, emboss=False
                 )
        if rmn.export_options:
            cll.prop(rmn, "generate_rib")

            row = cll.row()
            row.enabled = rmn.generate_rib
            row.prop(rmn, "generate_object_rib")

            cll.prop(rmn, "generate_alf")

            split = cll.split(percentage=0.33)
            split.enabled = rmn.generate_alf and rmn.generate_render
            split.prop(rmn, "do_render")

            sub_row = split.row()
            sub_row.enabled = rmn.do_render and rmn.generate_alf and rmn.generate_render
            sub_row.prop(rmn, "queuing_system")

        if rmn.generate_alf:
            icn = 'panel_open' if rmn.alf_options else 'panel_closed'
            iid = icons.iconid(icn)
            cll = box.box()
            cll = cll.column()
            cll.prop(rmn,
                     "alf_options",
                     text="ALF Options",
                     icon_value=iid,
                     emboss=False
                     )
            if rmn.alf_options:
                cll.prop(rmn, 'custom_alfname')
                cll.prop(rmn, "convert_textures")
                cll.prop(rmn, "generate_render")

                row = cll.row()
                row.enabled = rmn.generate_render
                row.prop(rmn, 'custom_cmd')

                split = cll.split(percentage=0.33)
                split.enabled = rmn.generate_render
                split.prop(rmn, "override_threads")

                sub_row = split.row()
                sub_row.enabled = rmn.override_threads
                sub_row.prop(rmn, "external_threads")

                row = cll.row()
                row.enabled = rmn.external_denoise
                row.prop(rmn, 'denoise_cmd')
                row = cll.row()
                row.enabled = rmn.external_denoise
                row.prop(rmn, 'spool_denoise_aov')
                row = cll.row()
                row.enabled = rmn.external_denoise and not rmn.spool_denoise_aov
                row.prop(rmn, "denoise_gpu")

                # checkpointing
                cll = cll.column()
                cll.enabled = rmn.generate_render

                row = cll.row()
                row.prop(rmn, 'recover')

                row = cll.row()
                row.prop(rmn, 'enable_checkpoint')

                row = cll.row()
                row.enabled = rmn.enable_checkpoint
                row.prop(rmn, 'asfinal')

                row = cll.row()
                row.enabled = rmn.enable_checkpoint
                row.prop(rmn, 'checkpoint_type')

                row = cll.row(align=True)
                row.enabled = rmn.enable_checkpoint
                row.prop(rmn, 'checkpoint_interval')
                row.prop(rmn, 'render_limit')
