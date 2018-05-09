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
from . icons import toggle
from . utils import split12
from . utils import draw_props
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Sampling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Sampling → Integrator"

    def draw(self, context):

        lay = self.layout
        scn = context.scene
        rmn = scn.renderman

        lco, rco = split12(lay)

        lco.prop(rmn, 'incremental', text="Incremental")
        row = rco.row(align=True)
        row.menu("rfb_mt_render_presets", text=bpy.types.rfb_mt_render_presets.bl_label)
        opr = "rfb.render_add_preset"
        row.operator(opr, text="", icon='ZOOMIN')
        row.operator(opr, text="", icon='ZOOMOUT').remove_active = True

        lco.label("Pixel Vatiance:")
        rco.prop(rmn, "pixel_variance", text="")

        lco.label("Samples:")
        row = rco.row(align=True)
        row.prop(rmn, "min_samples", text="Min.")
        row.prop(rmn, "max_samples", text="Max.")

        lco.label("Depth:")
        row = rco.row(align=True)
        row.prop(rmn, "max_specular_depth", text="Specular")
        row.prop(rmn, "max_diffuse_depth", text="Diffuse")

        col = lay.column(align=True)

        icn = "TRIA_DOWN" if rmn.show_integrator_settings else "TRIA_RIGHT"
        prp = "show_integrator_settings"
        txt = "Integrator Settings"
        col.prop(rmn, prp, icon=icn, text=txt, emboss=True)

        if rmn.show_integrator_settings:
            # find args for integrators here!
            props = getattr(rmn, "%s_settings" % rmn.integrator)

            sub = col.box()
            sub.prop(rmn, "integrator", text="")
            draw_props(props, props.prop_names, sub)
