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
from . utils import draw_props
from . RfB_PT_MIXIN_ShaderTypePolling import RfB_PT_MIXIN_ShaderTypePolling


class RfB_PT_DATA_Camera(RfB_PT_MIXIN_ShaderTypePolling, Panel):
    bl_context = "data"
    bl_label = "Camera Settings"

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        if not context.camera:
            return False
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        cam = context.camera
        scene = context.scene
        dof_options = cam.gpu_dof  # FIXME: never used?

        row = layout.row()
        row.prop(scene.renderman, "depth_of_field")
        sub = row.row()
        sub.enabled = scene.renderman.depth_of_field
        sub.prop(cam.renderman, "fstop")

        split = layout.split()

        col = split.column()

        col.label(text="Focus:")
        col.prop(cam, "dof_object", text="")
        sub = col.column()
        sub.active = (cam.dof_object is None)
        sub.prop(cam, "dof_distance", text="Distance")

        col = split.column()
        sub = col.column(align=True)
        sub.label("Aperture Controls:")
        sub.prop(cam.renderman, "dof_aspect", text="Aspect")
        sub.prop(cam.renderman, "aperture_sides", text="Sides")
        sub.prop(cam.renderman, "aperture_angle", text="Angle")
        sub.prop(cam.renderman, "aperture_roundness", text="Roundness")
        sub.prop(cam.renderman, "aperture_density", text="Density")

        layout.prop(cam.renderman, "projection_type")
        if cam.renderman.projection_type != 'none':
            projection_node = cam.renderman.get_projection_node()
            draw_props(projection_node, projection_node.prop_names, layout)
