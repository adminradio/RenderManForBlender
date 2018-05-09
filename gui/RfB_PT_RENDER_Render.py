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
from bpy.types import Panel

#
# RenderManForBlender Imports
#
from .. import engine

from . icons import iconid
from . icons import toggle
from . utils import split11
from . utils import split12
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Render(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Render"

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return

        lay = self.layout
        scn = context.scene
        rnd = context.scene.render
        rmn = context.scene.renderman

        _sro_ = []  # selected renderable objects
        if context.selected_objects:
            for obj in bpy.context.selected_objects:
                if obj.type not in ['CAMERA', 'LAMP', 'SPEAKER']:
                    _sro_.append(obj)

        #
        # Render Control
        #
        lco, rco = split12(lay)

        row = lco.row(align=True)
        sub = row.row(align=True)
        # sub.scale_x = 2.0
        sub.active = True if _sro_ else False
        prp = "render_selected_objects_only"
        sub.prop(rmn, prp, icon_only=True, icon='CURSOR')

        sub = row.row(align=True)
        # sub.scale_x = 2.0
        iid = toggle("dnoise", rmn.do_denoise)
        sub.prop(rmn, "do_denoise", text="", icon_value=iid)

        row = rco.row(align=True)

        # disable if no camera in scene
        row.enabled = True if context.scene.camera else False

        #
        # Render
        #
        opr = "render.render"
        txt = "Frame"
        iid = iconid("render")
        row.operator(opr, text=txt, icon_value=iid)

        #
        # Batch Render
        #
        opr = "render.render"
        txt = "Ani"
        iid = iconid("batch_render")
        row.operator(opr, text=txt, icon_value=iid).animation = True

        #
        # IPR
        #
        opr = "rfb.tool_ipr"
        txt = "IPR"
        iid = iconid("stop_ipr" if engine.ipr else "start_ipr")
        row.operator(opr, text=txt, icon_value=iid)

        lco, rco = split12(lay)

        lco.label(text="Display:")
        row = rco.row(align=True)
        row.prop(rnd, "display_mode", text="")
        row.prop(rnd, "use_lock_interface", icon_only=True)

        lco.label("Render To:")
        rco.prop(rmn, "render_into", text="")

        col = lay.column(align=True)
        icn = 'CHECKBOX_HLT' if rmn.enable_external_rendering else 'CHECKBOX_DEHLT'
        prp = "enable_external_rendering"
        col.prop(rmn, prp, icon=icn)
        if rmn.enable_external_rendering:
            box = col.box()
            lco, rco = split12(box)

            row = lco.row(align=True)
            # row.scale_x = 2.0

            prp = "external_animation"
            iid = toggle("animation", rmn.external_animation)
            row.prop(rmn, prp, text="", icon_value=iid)

            prp = "external_denoise"
            iid = toggle("dnoise", rmn.external_denoise)
            row.prop(rmn, prp, text="", icon_value=iid)

            sub = row.row(align=True)
            # sub.scale_x = 2.0
            sub.enabled = rmn.external_animation and rmn.external_denoise

            prp = "crossframe_denoise"
            iid = toggle("crossdn", rmn.crossframe_denoise)
            sub.prop(rmn, prp, text="", icon_value=iid)

            opr = "rfb.file_spool_render"
            txt = "Spool Animation" if rmn.external_animation else "Spool Frame"
            iid = iconid("render_spool")
            rco.operator(opr, text=txt, icon_value=iid)
            rco.prop(rmn, "display_driver", text="")

            sub_row = rco.row(align=True)
            sub_row.enabled = rmn.external_animation
            sub_row.prop(scn, "frame_start", text="Start")
            sub_row.prop(scn, "frame_end", text="End")

            cll = box.column(align=True)

            icn = 'TRIA_DOWN' if rmn.export_options else 'TRIA_RIGHT'
            prp = "export_options"
            txt = "Export Options"
            cll.prop(rmn, prp, text=txt, icon=icn)
            if rmn.export_options:
                cll = cll.box()

                lco, rco = split11(cll)

                lco.prop(rmn, "generate_rib")

                row = rco.row()
                row.enabled = rmn.generate_rib
                row.prop(rmn, "generate_object_rib")

                lco.prop(rmn, "generate_alf")

                split = cll.split()
                split.enabled = rmn.generate_alf and rmn.generate_render
                split.prop(rmn, "do_render")

                sub_row = split.row()
                sub_row.enabled = rmn.do_render and rmn.generate_alf and rmn.generate_render
                sub_row.prop(rmn, "queuing_system")

            if rmn.generate_alf:
                cll = box.column(align=True)

                icn = 'TRIA_DOWN' if rmn.export_options else 'TRIA_RIGHT'
                prp = "alf_options"
                txt = "ALF Options"
                cll.prop(rmn, prp, text=txt, icon=icn)
                if rmn.alf_options:
                    cll = cll.box()
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

        row = lay.row()
        row.scale_y = 1.25
        row.operator("rfb.bake_pattern_nodes", icon='TEXTURE')
