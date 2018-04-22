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
from . utils import draw_props
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Sampling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Sampling → Integrator"

    def draw(self, context):

        lay = self.layout
        scn = context.scene
        rmn = scn.renderman

        row = lay.row(align=True)

        icn = toggle("selected", rmn.incremental)
        row.prop(rmn, 'incremental', text="", icon_value=icn)

        row.separator()

        row.menu("rfb_mt_render_presets", text=bpy.types.rfb_mt_render_presets.bl_label)

        opr = "rfb.render_add_preset"
        row.operator(opr, text="", icon='ZOOMIN')
        row.operator(opr, text="", icon='ZOOMOUT').remove_active = True

        col = lay.column()
        col.prop(rmn, "pixel_variance")

        row = col.row(align=True)
        row.prop(rmn, "min_samples", text="Samples Min.")
        row.prop(rmn, "max_samples", text="Samples Max.")

        row = col.row(align=True)
        row.prop(rmn, "max_specular_depth", text="Specular Depth")
        row.prop(rmn, "max_diffuse_depth", text="Diffuse Depth")

        # row = lay.row(align=True)
        # row.prop(rmn, 'incremental')

        col = lay.column(align=True)

        icn = "TRIA_DOWN" if rmn.show_integrator_settings else "TRIA_RIGHT"
        prp = "show_integrator_settings"
        txt = "Integrator Settings"
        col.prop(rmn, prp, icon=icn, text=txt, emboss=True)

        # draw properties in scope of
        # current lay (cl)
        if rmn.show_integrator_settings:
            # find args for integrators here!
            props = getattr(rmn, "%s_settings" % rmn.integrator)
            lay = col.box().column(align=False)
            lay.prop(rmn, "integrator", text="")
            draw_props(props, props.prop_names, lay)
