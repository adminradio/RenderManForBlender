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
from . utils import split12

from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection


class RfB_PT_LAYER_RenderPasses(RfB_PT_MIXIN_Collection, Panel):
    bl_label = "Passes"
    bl_context = "render_layer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine in {'PRMAN_RENDER'}

    def draw_item(self, layout, context, item):
        #
        # AOV Type
        #
        box = layout.box()
        box.prop(item, "aov_name")
        if item.aov_name == "color custom_lpe":
            box.prop(item, "name")
            box.prop(item, "custom_lpe_string")

        #
        # Advanced sub panel
        #
        lay = layout.column(align=True)

        icon = 'TRIA_DOWN' if item.show_advanced else 'TRIA_RIGHT'
        lay.prop(item, "show_advanced",
                 text="Advanced", icon=icon, emboss=True)

        if item.show_advanced:
            box = lay.box()
            col = box.column(align=True)

            lco, rco = split12(col, align=True)

            lco.label("Exposure Settings:")
            lco.label("")
            rco.prop(item, "exposure_gain")
            rco.prop(item, "exposure_gamma")

            lco.separator()
            rco.separator()

            lco.label("Remap Settings:")
            row = rco.row(align=True)
            row.prop(item, "remap_a", text="A")
            row.prop(item, "remap_b", text="B")
            row.prop(item, "remap_c", text="C")

            lco.separator()
            rco.separator()

            lco.label(text="Quantize Settings:")
            lco.label("")
            row = rco.row(align=True)
            row.prop(item, "quantize_zero")
            row.prop(item, "quantize_one")
            row = rco.row(align=True)
            row.prop(item, "quantize_min")
            row.prop(item, "quantize_max")

            lco.separator()
            rco.separator()

            lco.label("Pixel Filter:")
            rco.prop(item, "aov_pixelfilter", text="")

            if item.aov_pixelfilter != 'default':
                lco.label("")
                row = rco.row(align=True)
                row.prop(item, "aov_pixelfilter_x", text="Size X")
                row.prop(item, "aov_pixelfilter_y", text="Size Y")

            lco.separator()
            rco.separator()
            lco.label("Statistics:")
            rco.prop(item, "stats_type", text="")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman
        rm_rl = None
        active_layer = scene.render.layers.active
        for l in rm.render_layers:
            if l.render_layer == active_layer.name:
                rm_rl = l
                break
        if rm_rl is None:
            layout.operator('rfb.rpass_add_renderman')
            split = layout.split()
            col = split.column()
            rl = active_layer
            col.prop(rl, "use_pass_combined")
            col.prop(rl, "use_pass_z")
            col.prop(rl, "use_pass_normal")
            col.prop(rl, "use_pass_vector")
            col.prop(rl, "use_pass_uv")
            col.prop(rl, "use_pass_object_index")
            # col.prop(rl, "use_pass_shadow")
            # col.prop(rl, "use_pass_reflection")

            col = split.column()
            col.label(text="Diffuse:")
            row = col.row(align=True)
            row.prop(rl, "use_pass_diffuse_direct", text="Direct", toggle=True)
            row.prop(rl, "use_pass_diffuse_indirect",
                     text="Indirect", toggle=True)
            row.prop(rl, "use_pass_diffuse_color", text="Albedo", toggle=True)
            col.label(text="Specular:")
            row = col.row(align=True)
            row.prop(rl, "use_pass_glossy_direct", text="Direct", toggle=True)
            row.prop(rl, "use_pass_glossy_indirect",
                     text="Indirect", toggle=True)

            col.prop(rl, "use_pass_subsurface_indirect", text="Subsurface")
            col.prop(rl, "use_pass_refraction", text="Refraction")
            col.prop(rl, "use_pass_emit", text="Emission")

            # layout.separator()
            # row = layout.row()
            # row.label('Holdouts')
            # rm = scene.renderman.holdout_settings
            # layout.prop(rm, 'do_collector_shadow')
            # layout.prop(rm, 'do_collector_reflection')
            # layout.prop(rm, 'do_collector_refraction')
            # layout.prop(rm, 'do_collector_indirectdiffuse')
            # layout.prop(rm, 'do_collector_subsurface')

            col.prop(rl, "use_pass_ambient_occlusion")
        else:
            layout.context_pointer_set("pass_list", rm_rl)
            self._draw_collection(context, layout, rm_rl, "",
                                  "rfb.collection_toggle_path", "pass_list",
                                  "custom_aovs", "custom_aov_index")
