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
from . import draw_props
from . RfB_PT_RootPanel import RfB_PT_RootPanel


class RfB_PT_PropsRenderSampling(RfB_PT_RootPanel, Panel):
    # class RENDER_PT_renderman_sampling(RfB_PT_RootPanel, Panel):
    bl_label = "Sampling → Integrator"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        # layout.prop(rm, "display_driver")

        # cl: currentlayout
        cl = layout.row(align=True)

        cl.menu("RfB_MT_render_presets", text=bpy.types.RfB_MT_render_presets.bl_label)
        cl.operator("rfb.render_add_preset",
                    text="",
                    icon='ZOOMIN')
        cl.operator("rfb.render_add_preset",
                    text="",
                    icon='ZOOMOUT'
                    ).remove_active = True

        cl = layout.row()
        cl.prop(rm, "pixel_variance")

        cl = layout.row(align=True)
        cl.prop(rm, "min_samples", text="Samples Min.")
        cl.prop(rm, "max_samples", text="Samples Max.")

        cl = layout.row(align=True)
        cl.prop(rm, "max_specular_depth", text="Specular Depth")
        cl.prop(rm, "max_diffuse_depth", text="Diffuse Depth")

        layout.separator()

        cl = layout.row(align=True)
        cl.prop(rm, 'incremental')

        layout.separator()

        # find args for integrators here!
        integrator_settings = getattr(rm, "%s_settings" % rm.integrator)
        cl = layout.box()
        layout.separator()

        iid = (
            icons.iconid("panel_open")
            if rm.show_integrator_settings
            else icons.iconid("panel_closed"))

        cl.prop(rm, "show_integrator_settings",
                icon_value=iid,
                text="Integrator Settings",
                emboss=False)
        cl.prop(rm, "integrator", text="")

        # draw properties in scope of
        # current layout (cl)
        if rm.show_integrator_settings:
            draw_props(integrator_settings,
                       integrator_settings.prop_names, cl)
