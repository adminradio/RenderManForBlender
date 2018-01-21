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
# RenderMan for Blender Imports
#
from . import icons
from . utils import draw_props
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Sampling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Sampling → Integrator"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        sub = layout.row(align=True)

        mnu = "rfb_mt_render_presets"
        txt = bpy.types.rfb_mt_render_presets.bl_label
        sub.menu(mnu, text=txt)

        opr = "rfb.render_add_preset"
        sub.operator(opr, text="", icon='ZOOMIN')

        opr = "rfb.render_add_preset"
        sub.operator(opr, text="", icon='ZOOMOUT').remove_active = True

        sub = layout.row()
        sub.prop(rm, "pixel_variance")

        row = layout.row(align=True)
        row.prop(rm, "min_samples", text="Min. Samples")
        row.prop(rm, "max_samples", text="Max. Samples")

        row = layout.row(align=True)
        row.prop(rm, "max_specular_depth", text="Spec. Depth")
        row.prop(rm, "max_diffuse_depth", text="Diff. Depth")

        layout.separator()

        row = layout.row()
        row.prop(rm, 'incremental')

        layout.separator()

        # find args for integrators here!
        integrator_settings = getattr(rm, "%s_settings" % rm.integrator)
        sub = layout.box()
        layout.separator()

        iid = icons.toggle("panel", rm.show_integrator_settings)

        sub.prop(rm, "show_integrator_settings",
                 icon_value=iid,
                 text="Integrator Settings",
                 emboss=False)
        sub.prop(rm, "integrator", text="")

        # draw properties in scope of
        # current layout (sub)
        if rm.show_integrator_settings:
            draw_props(integrator_settings,
                       integrator_settings.prop_names, sub)
