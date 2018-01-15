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
# from . import icons

from . RfB_PT_RootPanel import RfB_PT_RootPanel


class RfB_PT_PropsLayerOptions(RfB_PT_RootPanel, Panel):
    bl_label = "Layer"
    bl_context = "render_layer"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rl = rd.layers.active

        split = layout.split()

        col = split.column()
        col.prop(scene, "layers", text="Scene")

        rm = scene.renderman
        rm_rl = None
        active_layer = scene.render.layers.active
        for l in rm.render_layers:
            if l.render_layer == active_layer.name:
                rm_rl = l
                break
        if rm_rl is None:
            return
            # layout.operator('renderman.add_pass_list')
        else:
            split = layout.split()
            col = split.column()
            # cutting this for now until we can export multiple cameras
            # col.prop_search(rm_rl, 'camera', bpy.data, 'cameras')
            col.prop_search(rm_rl, 'light_group',
                            scene.renderman, 'light_groups', icon='DOT')
            col.prop_search(rm_rl, 'object_group',
                            scene.renderman, 'object_groups', icon='DOT')

            col.prop(rm_rl, "denoise_aov")
            col.prop(rm_rl, 'export_multilayer')
            if rm_rl.export_multilayer:
                col.prop(rm_rl, 'use_deep')
                col.prop(rm_rl, "exr_format_options")
                col.prop(rm_rl, "exr_compression")
                col.prop(rm_rl, "exr_storage")
