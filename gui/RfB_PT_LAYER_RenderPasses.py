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
from . utils import split33

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
        lay = self.layout
        rmn = context.scene.renderman
        rml = None
        for l in rmn.render_layers:
            if l.render_layer == context.scene.render.layers.active.name:
                rml = l
                break
        if rml is None:
            lay.operator('rfb.rpass_add_renderman')
            lco, mco, rco = split33(lay)

            _l_ = context.scene.render.layers.active
            lco.prop(_l_, "use_pass_diffuse_direct")
            lco.prop(_l_, "use_pass_diffuse_indirect")
            lco.prop(_l_, "use_pass_diffuse_color")
            lco.prop(_l_, "use_pass_glossy_direct")
            lco.prop(_l_, "use_pass_glossy_indirect")

            mco.prop(_l_, "use_pass_combined")
            mco.prop(_l_, "use_pass_z", text="Depth (Z)")
            mco.prop(_l_, "use_pass_normal")
            mco.prop(_l_, "use_pass_vector")
            mco.prop(_l_, "use_pass_uv")

            rco.prop(_l_, "use_pass_object_index")
            rco.prop(_l_, "use_pass_subsurface_indirect")
            rco.prop(_l_, "use_pass_refraction")
            rco.prop(_l_, "use_pass_emit", text="Emission")
            rco.prop(_l_, "use_pass_ambient_occlusion")
        else:
            lay.context_pointer_set("pass_list", rml)
            self._draw_collection(context, lay, rml, "",
                                  "rfb.collection_toggle_path", "pass_list",
                                  "custom_aovs", "custom_aov_index")
